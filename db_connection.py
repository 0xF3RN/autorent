import psycopg2

# креды postgres
DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "12345"
DB_USER_MANAGER = "manager"
# подключение к бд
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

def get_db_connection_manager():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER_MANAGER,
        password=DB_PASS
    )
    return conn
