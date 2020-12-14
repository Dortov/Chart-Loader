# Chart-Loader
Utility for visualization financial data (retail credit portfolio in charts) in organization

Chart Loader представляет собой утилиту для оперативной визуализации финансовых данных организации – в данном примере розничного кредитного портфеля банка или МФО. Обычно подобные утилиты являются элементом CRM системы или иного внутреннего ПО.

Для старта Chart Loader необходим запуск файла main.py

Что делает Chart Loader:
1. принимает на вход выгрузку из базы данных (предполагает стандартизированную выгрузку по заранее согласованному между подразделениями шаблону) или подключается к БД (в данной версии подключение не реализовано). Примеры выгрузки представлены в корне репозитория (txt - файлы). Другие выгрузки можно получить, воспользовавшись утилитой Loan Portfolio Generator, представленной в другом репозитории.
2. демонстрирует набор графиков и диаграмм, необходимых для оперативного контроля портфеля, 
3. выгружает выбранный график или все графики в PDF для демонстрации на кредитном комитете или в ходе сессий иных совещательных органов.

Как пользоваться Chart Loader:
1.	Загрузка файла: Menu – Import data file
Загрузка данных из файла может занимать от нескольких секунд до нескольких минут в зависимости от размера файла и производительности компьютера
2.	После загрузки для демонстрации необходимо выбрать интересующий график в списке в правой части основного окна
3.	Выгрузка текущего представленного графика в файл PDF: Menu – Export – Current Chart to PDF
4.	Выгрузка всех графиков в один файл PDF: Menu – Export – All Charts to PDF