import psycopg2

'''
никода, никогда не используйте этот проект для реферанса
ОН ПРОСТО УЖАСЕН
ПРОШУ НЕ ДЕЛАЙТЕ ЭТИХ ОШИБОК
Я ЕГО ДЕЛАЛ НА ОТВАЛИ
ХААХХААХАХАХ
Я НЕ ШУЧУ
ВОТ КАК ТО ТАК И ЖИВЕМ
'''

#TODO сделать класс
# креды postgres
DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "12345"
DB_USER_MANAGER = "manager"

# подключение к бд админом
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

# подключение к бд менеджером
def get_db_connection_manager():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER_MANAGER,
        password=DB_PASS
    )
    return conn
