import psycopg2


class DBManager:

    def __init__(self, dbname: str, user: str, password: str):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.is_connected = False

    def create_connection(self):
        self.connection = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password)
        self.cur = self.connection.cursor()
        self.is_connected = True

    def close_connection(self):
        if self.connection:
            self.cur.close()
            self.connection.close()

    def insert_data(self, plate: str, photo: bytes, user_id: int, first_name: str, last_name: str, message_date: str):
        self.cur.execute(
            'INSERT INTO bot_data (licence_plate, photo, user_id, user_first_name, user_last_name, message_date)'
            'VALUES (%s, %s, %s, %s, %s, %s)',
            (plate, bytearray(photo), user_id, first_name, last_name, message_date))
        self.connection.commit()

    def get_data(self, plate: str):
        self.cur.execute('SELECT photo '
                         'FROM bot_data '
                         'WHERE licence_plate = %s '
                         'ORDER BY data_id DESC ', (plate,))

        return bytes(self.cur.fetchone()[0])