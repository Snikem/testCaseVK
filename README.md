Запуск основного проекта ./run.sh
просмотр витрины http://localhost:5001/top

запуск тестов:
    1)docker-compose up -d --build  внутри папки tests, чтобы запустить тестовую бд
    2)установить requirements-test.txt
    3)запуск тестов pytest test_extract_transform.py -v