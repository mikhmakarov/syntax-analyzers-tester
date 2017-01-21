# Генератор тестов для синтаксических анализаторов

Получая на вход КС грамматику входного языка, генерирует набор позитивных
и негативных тестов.  
Язык реализации - Python 2.7.11.  
Версия antlr - 4.

Команда для генерации лексера и парсера по грамматике:  
`antlr4 -Dlanguage=Python2 InputGrammar.g4`

Команда для запуска парсера (по умолчанию грамматика считывается из
файла "input.txt"):  
`python parser.py`

Для того, чтобы указать путь до входной грамматики нужно использовать
ключ -i (по умолчанию grammars/input.txt):  
`python parser.py -i grammars/pascal.txt`

После завершения работы программы в текущей директории создается папка
tests с тестами. Чтобы записать тесты в другую папку, нужно использовать
ключ -t:  
`python parser.py -t ./output`

Ключ --grammar-check позволяет протестировать лексер/парсер 
(т.е. порождение тестов не производится).