import sqlite3

## User
class User:
    def __init__(self, user_id: int, balance: int, count_buy: int, referal_id: int, is_admin: bool):
        self.user_id = int(user_id)
        self.balance = int(balance)
        self.count_buy = int(count_buy)
        self.referal_id = int(referal_id)
        self.is_admin = bool(is_admin)

    def __str__(self) -> str:
        return f'<User id={self.user_id}, balance={self.balance}, admin status={self.is_admin}>'

## Category
class Category:
    def __init__(self, id: int, name: str):
        self.id = int(id)
        self.name = str(name)

## Good
class Good:
    def __init__(self, id: int, category_id: int, name: str, cost: int, count: int):
        self.id = int(id)
        self.category = str(category_id)
        self.name = str(name)
        self.cost = int(cost)
        self.count = int(count)

## Db
class DataBase:
    def __init__(self, db_filename: str = 'main.db'):
        self.db = sqlite3.connect(db_filename, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cur = self.db.cursor()
        cur.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            balance INTEGER,
            count_buy INTEGER,
            referal_id INEGER,            
            is_admin BOOLEAN
        );
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT                
        );
        CREATE TABLE IF NOT EXISTS goods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            name TEXT,
            cost INTEGER,
            count INTEGER      
        )''')
        cur.close()

    ## Methods 

    def create_user(self, user_id, balance, count_buy, referal_id, is_admin):
        cur = self.db.cursor()
        res = cur.execute('SELECT * FROM users WHERE user_id=?', (user_id, )).fetchone()
        if res is None:
            cur.execute("INSERT INTO users (user_id, balance, count_buy, referal_id, is_admin) VALUES(?, ?, ?, ?, ?)", (user_id, balance, count_buy, referal_id, is_admin))
        else:
            pass
        self.db.commit()
        cur.close()

    def get_user(self, user_id) -> User:
        cur = self.db.cursor()
        res = cur.execute('SELECT * FROM users WHERE user_id=?', (user_id, )).fetchone()
        cur.close()
        return User(*res)
    
    def get_categories(self) -> list[Category]:
        cur = self.db.cursor()
        res = cur.execute('SELECT * FROM categories').fetchall()
        cur.close()
        return [Category(*x) for x in res]
    
    def get_category(self, id):
        cur = self.db.cursor()
        res = cur.execute('SELECT * FROM categories WHERE id=?', (id, )).fetchone()
        cur.close()
        return Category(*res)

    def add_good(self, category: str, name: str, cost: int, count: int):
        cur = self.db.cursor()
        cur.execute('INSERT INTO goods (category, name, cost, count) VALUES (?, ?, ?, ?)', (category, name, cost, count))
        self.db.commit()
        cur.close()

    def add_category(self, name: str):
        cur = self.db.cursor()
        cur.execute('INSERT INTO categories (name) VALUES (?)', (name,))
        self.db.commit()
        cur.close()
    