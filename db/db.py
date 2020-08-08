import sqlite3
from model.const import Const


class DB:
    def __init__(self):
        self.__db = None
        self.__cursor = None

    def connect(self):
        self.__db = sqlite3.connect('db/my.db')
        self.__cursor = self.__db.cursor()


    def close(self):
        self.__cursor.close()
        self.__db.close()

    def read_db(self):
        with open('db/my.db', 'rb') as file:
            return file.read()

    def write_db(self, data):
        with open('db/my.db', mode='wb') as file:
            file.write(data)

    def create_tables(self):
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS cat1(
            id             TEXT,
            prev_id        TEXT,
            name           TEXT,
            next           TEXT DEFAULT 0,
            type           TEXT DEFAULT cat,
            level          INTEGER DEFAULT 1   
        )""")
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS cat2(
            id             TEXT,
            prev_id        TEXT,
            name           TEXT,
            next           TEXT DEFAULT 0,
            type           TEXT DEFAULT cat,
            level          INTEGER DEFAULT 2 
        )""")
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS cat3(
            id             TEXT,
            prev_id        TEXT,
            name           TEXT,
            next           TEXT DEFAULT 0,
            type           TEXT DEFAULT cat,
            level          INTEGER DEFAULT 3 
        )""")
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS cat4(
            id             TEXT,
            prev_id        TEXT,
            name           TEXT,
            next           TEXT DEFAULT 0,
            type           TEXT DEFAULT cat,
            level          INTEGER DEFAULT 4 
        )""")
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS cat5(
            id             TEXT, 
            prev_id        TEXT,
            name           TEXT,
            next           TEXT DEFAULT 0,
            type           TEXT DEFAULT cat,
            level          INTEGER DEFAULT 5
        )""")
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS note(
            id             TEXT,
            cat_id         TEXT,
            cat_prev_id    TEXT,
            title          TEXT,
            prev_cat       INTEGER DEFAULT 0,
            type           TEXT DEFAULT note,
            level          INTEGER DEFAULT 6,
            text1          TEXT,
            text2          TEXT,
            text3          TEXT,
            text4          TEXT,
            text5          TEXT,
            image1         BLOB,
            image2         BLOB,
            image3         BLOB,
            image4         BLOB,
            image5         BLOB,
            result1        TEXT,
            result2        TEXT,
            result3        TEXT,
            result4        TEXT,
            result5        TEXT
            
        )""")
        self.__db.commit()

    def create(self, number, id, prev_id, cat_name, opt, cat_prev_id=None, texts=None, images=None, results=None, prev_cat=None):
        if opt == Const.CREATE_CATEGORY:
            sql = f"INSERT INTO cat{number} (id, prev_id, name, level) VALUES (?, ?, ?, ?)"
            self.__cursor.execute(sql, (id, prev_id, cat_name, number))

        if opt == Const.CREATE_NOTE:
            sql = f"""INSERT INTO note 
                     (id, cat_id, cat_prev_id, title, prev_cat, text1, text2, text3, text4, text5,
                      image1, image2, image3, image4, image5,
                      result1, result2, result3, result4, result5) 
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            self.__cursor.execute(sql, (id, prev_id, cat_prev_id, cat_name, prev_cat, texts[0].text, texts[1].text, texts[2].text,
                                        texts[3].text, texts[4].text, images[0].im, images[1].im, images[2].im,
                                        images[3].im, images[4].im, results[0].text, results[1].text, results[2].text,
                                        results[3].text, results[4].text))
        self.__db.commit()


    def read(self, type, id, opt=None, search=''):
        if opt == Const.GET_SUBMENU:
            sql = f"SELECT id, prev_id, name, next, type, level  FROM {type} WHERE prev_id = ? AND (next = 'cat' OR next ='0')"
            self.__cursor.execute(sql, (id,))

        if opt == Const.GET_SUBMENU_FOR_NOTES:
            sql = f"SELECT id, prev_id, name, next, type, level  FROM {type} WHERE prev_id = ?"
            self.__cursor.execute(sql, (id,))

        if opt == Const.GET_UPMENU:
            sql = f"SELECT id, prev_id, name, next, type, level  FROM {type} WHERE id = ?"
            self.__cursor.execute(sql, (id,))

        if opt == Const.GET_NOTE_UPMENU:
            sql = f"SELECT id, prev_id, name, next, type, level  FROM {type} WHERE id = ? AND (next = 'note' OR next ='0')"
            self.__cursor.execute(sql, (id,))

        if opt == Const.GET_MENU:
            sql = f"SELECT id, prev_id, name, next, type, level  FROM {type}"
            self.__cursor.execute(sql)

        if opt == Const.GET_MENU_NAMES:
            sql = f"SELECT name FROM {type}"
            self.__cursor.execute(sql)
            return [name[0] for name in self.__cursor.fetchall()]

        if opt == Const.GET_NOTES_IN_SUBMENU:
            sql = f"SELECT * FROM {type} WHERE cat_id = ?"
            self.__cursor.execute(sql, (id,))

        if opt == Const.GET_NOTES_TITLES_IN_SUBMENU:
            sql = f"SELECT title FROM {type} WHERE cat_id = ?"
            self.__cursor.execute(sql, (id,))

        if opt == Const.SEARCH:
            sql = f"SELECT * FROM {type} WHERE (title LIKE ? OR text1 LIKE ? OR text2 LIKE ? OR text3 LIKE ? OR text4 LIKE ? OR text5 LIKE ? OR result1 LIKE ? OR result2 LIKE ? OR result3 LIKE ? OR result4 LIKE ? OR result5 LIKE ?)"
            search = f"%{search[1:]}%"
            self.__cursor.execute(sql, (search, search, search, search, search, search, search, search, search, search, search))

        if opt == Const.GET_NOTE:
            sql = f"SELECT * FROM {type} WHERE id = ?"
            self.__cursor.execute(sql, (id,))
            return self.__cursor.fetchone()

        if opt == Const.GET_CAT:
            sql = f"SELECT name FROM {type} WHERE id = ?"
            self.__cursor.execute(sql, (id,))
            return self.__cursor.fetchone()

        return self.__cursor.fetchall()


    def update(self, type, id, opt, *args):
        if opt == Const.UPDATE_BY_CAT:
            sql = f"UPDATE {type} SET next = 'cat' WHERE id = ?"
            self.__cursor.execute(sql, (id,))
        if opt == Const.UPDATE_BY_DEFAULT:
            sql = f"UPDATE {type} SET next = '0' WHERE id = ?"
            self.__cursor.execute(sql, (id,))
        if opt == Const.UPDATE_BY_NOTE:
            sql = f"UPDATE {type} SET next = 'note' WHERE id = ?"
            self.__cursor.execute(sql, (id,))
        if opt == Const.UPDATE_CAT_NAME:
            sql = f"UPDATE {type} SET name = ? WHERE id = ?"
            self.__cursor.execute(sql, (args[0], id,))
        if opt == Const.UPDATE_NOTE:
            sql = f"""UPDATE {type} SET cat_id = ?, cat_prev_id = ?, prev_cat = ?, title = ?,  
                                  text1 = ?, text2 = ?, text3 = ?, text4 = ?, text5 = ?,
                                  image1 = ?, image2 = ?, image3 = ?, image4 = ?, image5 = ?,
                                  result1 = ?, result2 = ?, result3 = ?, result4 = ?, result5 = ? 
                                  WHERE id = ?"""
            self.__cursor.execute(sql, (args[0], args[1], args[2], args[3],
                                        args[4][0].text, args[4][1].text, args[4][2].text, args[4][3].text, args[4][4].text,
                                        args[5][0].im, args[5][1].im, args[5][2].im, args[5][3].im, args[5][4].im,
                                        args[6][0].text, args[6][1].text, args[6][2].text, args[6][3].text, args[6][4].text,
                                        id))

        self.__db.commit()


    def delete(self, type, id, opt):
        if opt == Const.REMOVE_CATEGORY:
            sql = f"DELETE FROM {type} WHERE id = ?"
            self.__cursor.execute(sql, (id,))

        if opt == Const.DELETE_NOTE:
            sql = f"DELETE FROM {type} WHERE id = ?"
            self.__cursor.execute(sql, (id,))

        self.__db.commit()
