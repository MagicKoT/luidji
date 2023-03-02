import mysql.connector
from globals import host, user, password, database


class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        self.connection = None

    def init(self):
        # Подключение к базе данных MySQL
        self.connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)    

    def query(self, query: str):
        if self.connection is None:
            self.init()

        # Запускаем полученный запрос на выборку
        cursor = self.connection.cursor()
        cursor.execute(query)

        # Забираем данные и обрубаем соединение
        result = cursor.fetchall() if query.startswith("SELECT") else self.connection.commit()

        return result

    def disconnect(self):
        self.connection.close()
        self.connection = None

    def __del__(self):
        self.connection.close()

global db

db = Database(host, user, password, database)
