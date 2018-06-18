/*
 Генерация графа конфигураций

 запуск:

 node buildGraph <input_type> <input_path> <verbose>

 - input_type:
 grammar - запуск построения графа конфигураций для заданной грамматики
 table   - запуск построения графа конфигураций для уже созданной таблицы разбора

 - input_path - путь до файла грамматики/таблицы разбора (в зависимости от input_type)

 - verbose - если параметр указан (true), к выводу добавляются логи работы построителя графа
 */

const fs = require('fs');
const path = require('path');
const spawn = require('child_process').spawn;

const inputType = process.argv[2] || 'grammar';
const inputPath = process.argv[3] || '';
const verbose = process.argv[4] || false;

var grammar = {
    table: {},
    recover: {},
    terminals: [],
    axiom: null
};

var id = 0;

const nodes = [];

// Общий класс для вершин графа
class Node {
    constructor(state = null, ancestor = null) {
        this.state = state !== null ? state.slice() : null;
        this.ancestor = ancestor || null;
        this.id = id++;
        this.level = ancestor ? (ancestor.level + 1) : 0;
        this.isFinal = false;
    }
}

// Класс ребер графа (исходящих из конфигурации)
// Указывает на вершину, переход в которую осуществляется
// по некоторому терминалу
class Transition {
    constructor(term, node, toEqualState, error) {
        this.term = term;
        this.toEqualState = toEqualState || false;
        this.node = node || null;
        this.error = error || false;
    }

    toString() {
        return `by "${this.term}" to [${this.node ? this.node.id : 'null'} (${this.error ? 'error' : 'normal'})`
    }
}

// Конфигурация
// Имеет стек и потомков (по терминальным переходам)
class ConfigurationNode extends Node {
    constructor(state, ancestor) {
        super(state, ancestor);
        this.transitions = {};

        this.hasAllTransitions = true;

        grammar.terminals.filter(t => t !== '$').forEach(term => this.transitions[term] = new Transition(term));
    }

    findTransitionTerminal(child) {
        for (let t in this.transitions) {
            if (this.transitions[t].node === child) {
                return t;
            }
        }

        return null;
    }

    toString() {
        return `CONFIGURATION: [${this.state.slice().reverse().join(', ')}] ` +
            `from [${this.ancestor.state.slice().reverse().join(', ')}]\n` +
                `transitions:\n` + Object.keys(this.transitions).map(t => '-- ' + this.transitions[t].toString()).join("\n")
    }
}

// Let-вершина
// Не указывается родитель (то есть не имеет доступа к истории)
// Имеет двух потомков: верхнего и нижнего.
// Таким образом, дочерние конфигурации let-вершины независимые
class LetNode extends Node {
    constructor(state, upperNode, lowerNode) {
        super(state, null);
        this.upperNode = upperNode || null;
        this.lowerNode = lowerNode || null;
    }

    toString() {
        return `LET NODE for:\n` + this.upperNode.toString() + '\n' + this.lowerNode.toString();
    }
}


function addRecoverRules(grammar) {
    let terminalToRuleMap = {};
    let terminalRules = [];

    // Словарь с правилами восстановления
    grammar.recover = {};

    Object.keys(grammar.table).forEach(N => grammar.recover[N] = {});

    // Добавление фиктивных правил для терминалов
    // добавление переходов в таблицы разбора и восстановления
    grammar.terminals.forEach((term, i) => {
        let ruleName = '<' + term + '>';

        terminalToRuleMap[term] = ruleName;
        terminalRules.push(ruleName);

        grammar.table[ruleName] = {};
        grammar.recover[ruleName] = {};

        // Строки таблиц:
        //      a       b       x       $
        // N_x  null    null    [x]     null // table
        // N_x  [a]     [b]     null    []   // recover
        grammar.terminals.forEach(x => {
            // Для символа "$" правило N -> eps
            if (x === "$") {
                grammar.table[ruleName][x] = (x === term) ? [] : null;
                grammar.recover[ruleName][x] = (x === term) ? null : [];
            } else {
                grammar.table[ruleName][x] = (x === term) ? [term] : null;
                grammar.recover[ruleName][x] = (x === term) ? null : [x]
            }
        });
    });

    // Для обычных нетерминалов добавляем правила восстановления
    // а также заменяем терминалы на фиктивные правила
    for (let N in grammar.table) {
        if (!terminalRules.includes(N)) {
            for (let a in grammar.table[N]) {
                // Если ячейка пустая (то есть ошибочная)
                // пытаемся добавить правило восстановления
                // на основе FOLLOW(N)

                if (!grammar.table[N][a]) {
                    // Если символ не входит в FOLLOW(N)
                    // добавляем правило N -> aN
                    // (для символа "$" правило восстановления всегда N -> eps)

                    if (a === '$') {
                        grammar.recover[N][a] = [];
                    } else if (!grammar.follow[N].includes(a)) {
                        grammar.recover[N][a] = [a, N];

                        // Иначе добавляем правило N -> eps
                    } else {
                        grammar.recover[N][a] = [];
                    }

                    // Иначе, заменяет терминалы на фиктивные правила
                } else {
                    grammar.table[N][a] = grammar.table[N][a].map(
                        r => grammar.terminals.indexOf(r) == -1 ? r : terminalToRuleMap[r]
                    );

                    grammar.recover[N][a] = null;
                }
            }
        }
    }

    return grammar;
}

// Процедура построения графа конфигураций
// 1. Посещаем все переходы из текущей вершины
// 2. Для каждого перехода проверяем стек на:
//      - эквивалентность
//      - вложение
//      - обобщение
// 3. В случае отсутствия указанных отношений,
//    создаем новую конфигурацию
function buildConfigurationGraph() {
    // Указывает на корень дерева даже в случае замены
    // корневой конфигурации на let-вершину
    let root = new ConfigurationNode([], null);

    // Обнуляем список вершин
    // и счетчик идентификаторов
    nodes.length = 0;
    id = 0;

    // Создаем корневую конфигурацию,
    // содержащую аксиому (и нетерминал-маркер конца)
    let rootConfiguration = new ConfigurationNode([grammar.axiom], root);

    root.transitions[''] = new Transition('', rootConfiguration);

    // Помещаем конфигурацию в очередь для дальнейшего её разбора и добавления в список конфигураций
    let stack = [];

    nodes.push(rootConfiguration);
    stack.push(rootConfiguration);

    log('Создание графа конфигураций...');

    // Проходим по всем конфигурациям в глубину
    do {
        // Вынимаем последний элемент из стека
        // и начинаем обработку всех возможных переходов из него
        let node = stack.pop();

        log('---------------\n', 'CURRENT NODE:', node.toString());

        // Выполняем переход по таблице разбора для каждого терминала
        // c целью создания/обобщения новых конфигураций.
        // Полученные конфигурации добавляются в стек
        if (node instanceof ConfigurationNode) {
            visitAllTransitions(node, stack);
        }
    } while (stack.length !== 0);

    // TODO: В случае замены корневой вершины на let-вершину граф может оказаться пустым
    return root.transitions[''].node;
}

function getNextState(stack, term) {

    let error = false,
        hasTerminal = false;

    do {
        log(stack, term);

        let rule = stack.pop();

        // Если текущий символ - терминал,
        // тогда в случае его несовпадения с ожидаемым - ошибка
        if (grammar.terminals.indexOf(rule) !== -1) {
            error = error || rule !== term;
            hasTerminal = true;
            break;
        } else {
            // Добавляем в стек правило перехода.
            // Если ячейка таблицы переходов переходов пуста,
            // то берем переход из таблицы восстановления
            // и выходим из цикла.

            let table = grammar.table;

            if (grammar.table[rule][term] == null) {
                table = grammar.recover;
                error = true;
            }

            stack = stack.concat(table[rule][term].slice().reverse());
        }

    } while (stack.length);

    return {stack, hasTerminal, error};
}

function getStateIsEmpty(stack) {
    log('IS FINAL NODE: ', stack);

    let res = stack.every(r => (r in grammar.first) && grammar.first[r].includes("eps"));

    log('     res:', res);
    return res
}

function visitAllTransitions(parentConf, configStack) {
    // Если встречаем конфигурацию с пустым стеком,
    // то пропускаем её - все переходы из неё - пустые - были инициализированы.
    // Иначе просматриваем переходы по каждому терминальному символу

    if (parentConf.state.length) {
        let nodesToVisit = [];

        grammar.terminals.filter(t => t !== '$').every(term => {
            // Выполняем переход по таблицам разбора и восстановления,
            // пока не встретим терминальный символ.
            // Изменяем стек анализатора
            // (пропускаем транзитные переходы)
            let {stack, hasTerminal, error} = getNextState(parentConf.state.slice(), term);

            // Если не было перехода по символу -
            // не обрабатываем стек
            if (!hasTerminal) {
                parentConf.hasAllTransitions = false;
                delete parentConf.transitions[term];
                return true;
            }

            // Финальное состояние - состояние с пустым стеком

            // Финальное состояние - либо, если все нетерминалы в данном стеке раскрываются
            // по обычным правилам в eps (если есть терминалы или правила восстановления, то нет)
            // либо пустой
            let isFinalNode = false;

            if (!stack.length || getStateIsEmpty(stack)) {
                isFinalNode = true;
            }

            // Проверяем стек на соответствие существующей конфигурации
            // или отношению Турчина

            log('=> CURRENT STACK BY TERMINAL ' + term + ': ' + stack);
            log('=> ERROR: ' + error);

            // Ищем полностью совпадающую конфигурацию
            let equalConf = findEqualState(stack);

            if (equalConf) {
                log('-- CREATED CYCLE: ' + stack);
                log('-- FROM: ' + parentConf.toString());
                log('-- TO: ' + equalConf.toString());
                log('-- by terminal: ' + term);

                parentConf.transitions[term].node = equalConf;
                parentConf.transitions[term].toEqualState = true;
                parentConf.transitions[term].error = error;

                return true;
            }

            // Проверка частичного совпадения конфигураций (отношение Турчина)
            let relation = findStateRelation(stack, parentConf);

            log('TURCHIN RELATION: ' + relation !== null);

            if (relation) {

                // Создаем новую Let вершину, одна дуга из которой указывает на существующую конфигурацию,
                // а другая развивается независимо
                if (relation.partition.length == 1) {

                    log('CREATED LET-NODE FOR A => A|B: ' + relation.configuration.state + ' => ' + stack);

                    // ВНИМАНИЕ!!!
                    // Выполняется поиск эквивалентной вершины после разделения стеков!!!
                    let letNode = new LetNode(stack);

                    equalConf = findEqualState(stack.slice(0, relation.partition[0])); // B

                    let newConf = equalConf || new ConfigurationNode(stack.slice(0, relation.partition[0]), letNode);
                    newConf.isFinal = newConf.isFinal || isFinalNode;

                    letNode.upperNode = relation.configuration;
                    relation.configuration.isFinal = relation.configuration.isFinal || isFinalNode;

                    letNode.lowerNode = newConf;

                    // Если существует эквивалентная конфигурация,
                    // то, возможно, существует эквивалентная let-вершина
                    if (equalConf) {

                        log('-- equal conf found');

                        // Выполняем поиск эквивалентной let-вершины
                        // и, в случае нахождения используем её
                        let equalLetNode = findEqualLetNode(letNode);

                        if (equalLetNode) {

                            letNode = equalLetNode;
                            parentConf.transitions[term].toEqualState = true;

                            log('-- equal let-node found');

                            // Иначе - используем только что созданную let-вершину
                            // а также добавляем её в очередь и список вершин
                        } else if (!equalLetNode) {
                            nodes.push(letNode);
                            nodesToVisit.push(letNode);
                        }

                        // Иначе - используем новую let-вершину,
                        // не забывая добавить нерассмотренную конфигурацию и саму let-вершину в списки
                    } else {
                        log('-- created new let-node and config');
                        log('-- from ' + parentConf.state + ' by ' + term);
                        nodes.push(newConf, letNode);
                        nodesToVisit.push(newConf, letNode);
                    }

                    // Подключаем вершину к родительской
                    parentConf.transitions[term].node = letNode;
                    parentConf.transitions[term].error = error;
                    parentConf.transitions[term].isFinal = parentConf.transitions[term].isFinal || isFinalNode;

                    return true;

                    // Иначе отбрасываем всех потомков найденной родительской конфигурации
                    // и создаем новую дочернюю Let вершину
                    // из которой исходят две дуги к новым независимым конфигурациям
                } else {

                    log('CREATED LET-NODE FOR A|C => A|B|C: ' + relation.configuration.state + ' => ' + stack);

                    let ancestorConf = relation.configuration.ancestor;

                    // Производим замену найденной конфигурации на let-вершину,
                    // предварительно удалив все вершины подграфа из списка вершин и очереди.

                    let transitionTerm = ancestorConf.findTransitionTerminal(relation.configuration);

                    // Запуск удаления подграфа

                    log('# REMOVE CONFIGURATION: ', relation.configuration);
                    removeNodes(ancestorConf, transitionTerm, configStack);

                    // Инициализация нового let-узла
                    let letNode = new LetNode(stack),

                        firstStack = stack.slice(relation.partition[1]), // A
                        secondStack = stack.slice(0, relation.partition[0]), // C

                        firstEqualConfig = findEqualState(firstStack),
                        secondEqualConfig = findEqualState(secondStack),

                        firstConf = firstEqualConfig || new ConfigurationNode(firstStack, letNode),
                        secondConf = secondEqualConfig || new ConfigurationNode(secondStack, letNode);

                    letNode.upperNode = firstConf;
                    letNode.lowerNode = secondConf;

                    firstConf.isFinal = firstConf.isFinal || isFinalNode;
                    secondConf.isFinal = secondConf.isFinal || isFinalNode;

                    // Поскольку потомки родительской конфигурации удалены,
                    // Остается только две созданных конфигурации (в случае их уникальности) в let-вершине для добавления в очередь
                    nodesToVisit.length = 0;

                    // Если существуют две эквивалентные конфигурации, то, быть может
                    // существует эквивалентная let-вершина
                    if (firstEqualConfig && secondEqualConfig) {
                        // Выполняем поиск эквивалентной let-вершины
                        // и, в случае нахождения используем её
                        let equalLetNode = findEqualLetNode(letNode);

                        if (equalLetNode) {

                            letNode = equalLetNode;
                            ancestorConf.transitions[transitionTerm].toEqualState = true;

                            // Иначе - используем только что созданную let-вершину
                            // а также добавляем нерассмотренные вершины в очередь и список вершин
                        } else if (!equalLetNode) {
                            nodes.push(letNode);
                            nodesToVisit.push(letNode);
                        }
                    } else {
                        nodes.push(firstConf, secondConf, letNode);
                        nodesToVisit.push(firstConf, secondConf, letNode);
                    }

                    ancestorConf.transitions[transitionTerm].node = letNode;

                    // Прекращаем цикл по терминалам, поскольку родительской вершины уже не существует
                    return false;
                }
            }

            // Полученный стек не пуст, не совпадает ни с одной из конфигураций
            // и не связан с другими отношением Турчина,
            // следовательно, необходимо создать новую конфигурацию с данным стеком

            let newConf = new ConfigurationNode(stack, parentConf);

            newConf.isFinal = newConf.isFinal || isFinalNode;
            parentConf.transitions[term].node = newConf;
            parentConf.transitions[term].error = error;

            nodes.push(newConf);
            nodesToVisit.push(newConf);

            log('ADD NEW CONFIGURATION: ', newConf.toString());

            return true;
        });

        nodesToVisit.forEach(c => configStack.push(c));
    } else {
        parentConf.transitions = {};
    }
}

function findEqualState(stack) {
    // Выполняем поиск по всем созданным ранее конфигурациям
    let confs = nodes.filter(n => n instanceof ConfigurationNode);

    for (let i = 0; i < confs.length; i++) {
        if (stack.length == confs[i].state.length && confs[i].state.every((t, i) => t === stack[i])) {
            return confs[i];
        }
    }

    return null;
}

function findEqualLetNode(currentNode) {
    let letNodes = nodes.filter(n => n instanceof LetNode);

    let stack = currentNode.state;

    for (let i = 0; i < letNodes.length; i++) {

        let existStack = letNodes[i].state;

        if (stack.length == existStack.length &&
            existStack.every((t, i) => t === stack[i]) &&
            currentNode.upperNode == letNodes[i].upperNode &&
            currentNode.lowerNode == letNodes[i].lowerNode
        ) {
            return letNodes[i];
        }
    }

    return null;
}

function findStateRelation(stack, parentConfig) {
    let parent = parentConfig;

    stack = stack.slice();

    // Путешествуем по родительским конфигурациям
    // и исследуем их на предмет отношения Турчина

    log('> CHECK TURCHIN RELATION FOR: ', stack);

    while (parent !== null) {

        // Если длина стека родителя меньше длины исследуемого стека,
        // то выполняем проверку отношения между стеками.
        // Иначе переходим к следующей родительской вершине
        if ((parent instanceof ConfigurationNode) && stack.length > parent.state.length) {
            let matchIndex = 0;

            let parentStack = parent.state.slice();

            // Выполняем поиск максимального общего префикса A двух стеков (верхушка стека справа)
            while (parentStack[parentStack.length - matchIndex - 1] === stack[stack.length - matchIndex - 1]) {
                matchIndex++;
            }

            log('>   COMPARE: ', stack, parentStack, matchIndex);

            // Если такой префикс непуст,
            // то "двойственное" отношение Турчина имеет место,
            // поэтому проверяем наличие более строгого, "тройственного" отношения.
            if (matchIndex > 0) {

                // Если найденный префикс совпадает со стеком родителя,
                // то "тройственное" отношение невыполнимо,
                // а значит A => A || B
                if (matchIndex == parentStack.length) {

                    // Возвращается найденная конфигурация,
                    // а также индексы начала подмножеств A и В в искомом стеке
                    return {
                        configuration: parent,
                        partition: [stack.length - matchIndex]
                    }
                }

                // Если длина префикса меньше длины стека родителя,
                // то ищем общий суффикс двух стеков (оставшейся длины).
                let tailMatchIndex = 0,
                    parentStackTail = parentStack.slice(0, parentStack.length - matchIndex);

                while (parentStackTail[tailMatchIndex] === stack[tailMatchIndex]) {
                    tailMatchIndex++;
                }

                log('>   suffix length: ', tailMatchIndex, matchIndex);

                // Если префикс и суффикс вместе образуют стек родителя,
                // то выполняется "тройственное" отношение Турчина:
                // A || C => A || B || C
                // (B не может быть пустым по условию несовпадения длины стеков)
                if (matchIndex + tailMatchIndex == parentStack.length) {

                    // Возвращается найденная конфигурация,
                    // а также индексы начала подмножеств A, B и C в искомом стеке
                    return {
                        configuration: parent,
                        partition: [tailMatchIndex, stack.length - matchIndex]
                    }
                }
            }
        }

        parent = parent.ancestor;
    }

    return null;
}

function removeNodes(config, term, queue) {
    visitAndRemove(config.transitions[term].node, queue);
}

function visitAndRemove(node, queue) {
    // Если тип узла - let-вершина,
    // то запускаем процесс удаления по двум её потомкам,
    // учитывая при этом возможность возникновения циклов
    if (node instanceof LetNode) {
        log('remove let node: ', node.toString());
        // Если ветви не образует цикл
        if (node.upperNode.parent == node) {
            visitAndRemove(node.upperNode, queue);
        }

        if (node.lowerNode.parent == node) {
            visitAndRemove(node.lowerNode, queue);
        }

        // Иначе вершина конфигурационная,
        // а значит необходимо запустить процесс удаления для всех
        // её потомков, также учитывая возможные циклы
    } else if (node instanceof ConfigurationNode) {
        log('remove config: ', node.id);
        Object.keys(node.transitions).forEach(term => {
            // Если ветви не образует цикл
            if (node.transitions[term] && !node.transitions[term].toEqualState) {
                visitAndRemove(node.transitions[term].node, queue);
            }
        });
    }

    // Удаляем вершину из списка вершин
    let nodeIndex = nodes.indexOf(node);

    if (nodeIndex !== -1) {
        nodes.splice(nodes.indexOf(node), 1);
    }

    nodes.forEach(anotherNode => {
        if (anotherNode instanceof ConfigurationNode) {
            for (let t in anotherNode.transitions) {
                if (anotherNode.transitions[t].node == node) {
                    anotherNode.transitions[t] = new Transition(t);
                }
            }
        }
    });

    // Удаляем вершину из очереди
    let queueIndex = queue.indexOf(node);

    if (queueIndex !== -1) {
        queue.splice(queueIndex, 1);
    }
}

function transformToDOT(nodes, showError) {

    let confNodes = nodes
            .filter(n => n instanceof ConfigurationNode && !n.isFinal)
            .map(n => `${n.id} [label="${n.id} - ${'[' + n.state.slice().reverse() + ']'}"]`),
        finalNodes = nodes
            .filter(n => n instanceof ConfigurationNode && n.isFinal)
            .map(n => `${n.id} [label="${n.id} - ${'[' + n.state.slice().reverse() + ']'}"]`),
        letNodes = nodes
            .filter(n => n instanceof LetNode)
            .map(n => `${n.id} [label="let: ${'[' + n.state.slice().reverse() + ']'}"]`);

    var code = 'digraph {\nrankdir=LR;\nsize="8,5";\n';

    if (confNodes.length) {
        code += `node [shape = circle, color = black];\n` +
            confNodes.join(';\n') + ';\n';
    }

    if (letNodes.length) {
        code += 'node [shape = square];\n' +
            letNodes.join(';\n') + ';\n';
    }

    if (finalNodes.length) {
        code += 'node [shape = doublecircle];\n' +
            finalNodes.join(';\n') + ';\n';
    }

    let edges = [];

    nodes.forEach(node => {
        if (node instanceof ConfigurationNode) {
            edges.push(...Object.keys(node.transitions)
                .filter(term => (showError || node.transitions[term].error == false) && node.transitions[term].node !== null )
                .map(term => {

                    if (node.transitions[term].error) {
                        return `${node.id} -> ${node.transitions[term].node.id} [ label = "${term}", color = "red", style = dashed ];`;
                    }

                    if (node.transitions[term].visited) {
                        return `${node.id} -> ${node.transitions[term].node.id} [ label = "${term}", color = "green" ];`;
                    }

                    return `${node.id} -> ${node.transitions[term].node.id} [ label = "${term}", color = "black" ];`;
                }));
        } else if (node instanceof LetNode) {
            edges.push(
                `${node.id} -> ${node.upperNode.id} [label="up"];`,
                `${node.id} -> ${node.lowerNode.id} [style=dotted, label="down"];`
            );
        }
    });

    code += edges.join('\n') + '\n}';

    return code;


}

function log(...msg) {
    if (verbose) {
        console.log(...msg);
    }
}

function buildGrammarTable(callback) {

    // Запуск программы генерации таблицы разбора для заданной грамматики
    let tableBuilder = spawn('python', [path.join(__dirname, '../table-builder/builder.py'), '-i', inputPath]);

    let str = '';

    tableBuilder.stdout.on('data', (data) => {
        str += data.toString('utf-8');
    });

    tableBuilder.on('error', (err) => {
        console.log('spawn err: ', err);
    });

    tableBuilder.stderr.on('data', (err) => {
        console.log('err: ', err.toString('utf-8'));
    });

    // В случае успешной генерации таблицы -
    // начать построение графа конфигураций
    tableBuilder.on('close', (code) => {
        if (code == 0) {

            let table = null;

            // Попытка извлечь данные о сгенерированной таблице
            try {
                table = JSON.parse(str.trim().split('\n').slice(-1)[0]);
            } catch (e) {
                console.log('Ошибка при генерации таблицы предсказывающего разбора:', e);
            } finally {
                if (table) {
                    callback(table)
                }
            }
        } else {
            console.log('Построение таблицы разбора завершено с ошибкой!')
        }
    });

}

function loadTableFromFile(callback) {
    fs.access(inputPath, fs.constants.R_OK, (accessError) => {
        if (accessError) {
            console.log('Ошибка доступа к файлу таблицы разбора: ', accessError);
        } else {

            let table = null;

            try {
                table = JSON.parse(fs.readFileSync(inputPath, {encoding: 'utf8'}));
            } catch (loadError) {
                console.log('Ошибка при попытке загрузки таблицы разбора: ', loadError);
            } finally {
                if (table) {
                    callback(table);
                }
            }
        }
    });
}

// Генерация позитивных тестов
function generateAllPositiveTests(graph) {
    // Помечаем все ребра и вершины как непосещенные
    nodes
        .filter(n => n instanceof ConfigurationNode)
        .forEach(n => {
            if (n.isFinal) n.processed = false;

            Object.keys(n.transitions).forEach(t => n.transitions[t].visited = false);
        });

    // Обходим граф до тех пор, пока имеются непосещенные ребра или финальные вершины
    while (!(isAllPositiveEdgesVisited() && isAllFinalNodesProcessed())) {

        // Инициализируем новый тест в начальной вершине
        let currentStep = { node: graph, result: [], terminated: false };

        // Удаляем установленные в предыдущих тестах фиктивные переходы
        getFinalNodes().forEach(n => delete n.transitions[""]);

        console.log(transformToDOT(nodes, false));

        // Выполняем проход по графу до тех пор,
        // пока не остановимся в финальном состоянии,
        // из которого нельзя попасть в непомеченные вершины
        while (!currentStep.terminated) {
            currentStep = getNextPositiveStep(currentStep);
        }

        console.log('NEW TEST: ', currentStep.result.join(' '));
        //console.log(isAllPositiveEdgesVisited());
        //console.log(isAllFinalNodesProcessed());
    }
}

function getNextPositiveStep(prevStepInfo) {

    let {node, result, terminated } = prevStepInfo;

    log('current node: ', node.toString());
    log('res: ', result.join(' '));

    // Если текущая вершина - конфигурация:
    if (node instanceof ConfigurationNode) {

        // Если текущая вершина - финальная и
        // из неё нет переходов по непомеченным ребрам,
        // завершаем проход для данного теста
        if (node.isFinal && isAllPositiveChildrenVisited(node)) {
            node.processed = true;
            terminated = true;
            return { node, result: result.filter(t => t !== null), terminated}
        }

        // Иначе выполняем поиск ближайшего непомеченного ребра
        // и переходим по нему, учитывая промежуточный путь
        if (!isAllPositiveEdgesVisited()) {
            let nextNodePath = findNotVisitedPath(node, result, terminated);

            return nextNodePath ? nextNodePath : findClosestPathToFinalNode(node, result, terminated);
        }

        return findClosestPathToFinalNode(node, result, terminated);

    // Если текущая вершина - let-узел:
    } else if (node instanceof LetNode) {
        // Переходим по верхнему узлу,
        // добавляя к финальным вершинам фиктивный переход
        // по нижнему узлу

        let epsilonTransition = new Transition(null, node.lowerNode);
        epsilonTransition.visited = false;

        getFinalNodes().forEach(n => {

            if (!("" in n.transitions)) {
                n.transitions[""] = [];
            }
            n.transitions[""].push(epsilonTransition);
        });

        return { node: node.upperNode, result, terminated }
    }
}

function findNotVisitedPath(startNode, result, terminated) {
    let queue = [{
            node: startNode,
            transitions: []
        }], target = null;

    log('find path from:', startNode.toString());

    while (!target && queue.length) {
        let { node, transitions } = queue.shift();

        log('pop: ', node.toString());

        if (node instanceof ConfigurationNode) {
            Object.keys(node.transitions).filter(t => !node.transitions[t].error).forEach(t => {

                log(target ? target.node.toString() : null);

                if (!target) {

                    log('check transition by ', t);
                    // Если ребро не посещено,
                    // останавливаем поиск на нем
                    if (t !== "" && !node.transitions[t].visited) {

                        log('not visited, target found');

                        node.transitions[t].visited = true;

                        target = {
                            node: node.transitions[t].node,
                            transitions: transitions.concat(node.transitions[t])
                        };

                    // Просматриваем фиктивные ребра
                    } else if (t === "") {

                        log('(check epsilon transitions)');

                        node.transitions[""].some(epsilonTransition => {
                            if (!epsilonTransition.visited) {

                                epsilonTransition.visited = true;

                                target = {
                                    node: epsilonTransition.node,
                                    transitions: transitions.concat(epsilonTransition)
                                };
                                return true;
                            }

                            return false;
                        });

                    // В противном случае помещаем дочерний узел в очередь
                    } else {
                        log('visited, push: ', node.transitions[t].node.toString());
                        queue.push({
                            node: node.transitions[t].node,
                            transitions: transitions.concat(node.transitions[t])
                        });
                    }
                }
            });
        } else if (node instanceof LetNode) {
            //throw new Error('Not handled let node in find path');
            queue.push({
                node: node.upperNode,
                transitions: transitions
            });
        }
    }

    if (!target) {
        return null;
    }

    return {
        node: target.node,
        result: result.concat(target.transitions.map(t => t.term)),
        terminated: terminated
    }

}

function findClosestPathToFinalNode(startNode, result, terminated) {
    let queue = [{
        node: startNode,
        transitions: []
    }], final = null;

    log('find final node from:', startNode.toString());

    while (true) {
        let { node, transitions } = queue.shift();

        log('pop: ', node.toString());

        if (node instanceof ConfigurationNode) {
            Object.keys(node.transitions).filter(t => !node.transitions[t].error).forEach(t => {
                if (!final) {

                    log('check transition by ', t);
                    // Если ребро не посещено,
                    // останавливаем поиск на нем
                    if (t !== "" && node.transitions[t].node.isFinal) {

                        log('final found');

                        final = {
                            node: node.transitions[t].node,
                            transitions: transitions.concat(node.transitions[t])
                        };

                        // Просматриваем фиктивные ребра
                    } else if (t === "") {

                        log('(check epsilon transitions)');

                        node.transitions[""].some(epsilonTransition => {
                            if (epsilonTransition.node.isFinal) {

                                final = {
                                    node: epsilonTransition.node,
                                    transitions: transitions.concat(epsilonTransition)
                                };
                                return true;
                            }

                            return false;
                        });

                        // В противном случае помещаем дочерний узел в очередь
                    } else {
                        log('is not final, push: ', node.transitions[t].node.toString());
                        queue.push({
                            node: node.transitions[t].node,
                            transitions: transitions.concat(node.transitions[t])
                        });
                    }
                }
            });
        } else if (node instanceof LetNode) {

            queue.push({
                node: node.lowerNode,
                transitions: transitions
            });

            //throw new Error('Not handled let node in find final node');
        }

        if (final) break;
    }

    return {
        node: final.node,
        result: result.concat(final.transitions.map(t => t.term)),
        terminated: terminated
    }
}

function getFinalNodes() {
    return nodes.filter(n => n instanceof ConfigurationNode && n.isFinal);
}

function isAllPositiveEdgesVisited() {
    return nodes
        .filter(n => n instanceof ConfigurationNode)
        .every(n => Object.keys(n.transitions)
            .filter(t => t == "" || !n.transitions[t].error)
            .every(t => {
                if (t == "") {
                    return n.transitions[""].every(e => e.visited == true)
                }
                return n.transitions[t].visited == true
            })
        );
}

function isAllPositiveChildrenVisited(node) {
    for (let t in node.transitions) {
        if (t == "") {
            for (let i = 0; i < node.transitions[""].length; i++) {
                if (!node.transitions[""][i].visited) {
                    return false;
                }
            }
        } else {
            if (!node.transitions[t].error && !node.transitions[t].visited) {
                return false;
            }
        }
    }

    return true;
}

function isAllFinalNodesProcessed() {
    return getFinalNodes().every(n => n.processed);
}

//
// Вызов процедуры генерации/загрузки таблицы разбора
// и построение графа конфигураций на основе загруженной таблицы
//

let cb = (grammarInfo) => {

    //console.log('table: ', JSON.stringify(grammarInfo, null, ' '));

    addRecoverRules(grammarInfo);

    log('with recover rules: ', JSON.stringify(grammarInfo, null, ' '));

    grammar = grammarInfo;

    let graph = buildConfigurationGraph();

    generateAllPositiveTests(graph);

    if (getFinalNodes().some(n => !n.processed)) {
        throw new Error('Ошибка генерации позитивных тестов: финальные вершины не обработаны!');
    }

    getFinalNodes().forEach(n => delete n.transitions[""]);

    console.log(transformToDOT(nodes, false));


};

switch (inputType.trim().toLowerCase()) {
    case 'grammar':
        buildGrammarTable(cb);
        break;

    case 'table':
        loadTableFromFile(cb);
        break;

    default:
        throw new Error(`Указан неверный тип входного файла: ${inputType}.\nДопустимые типы: grammar, table`);
}



