
"""
Written by Seedorfe
"""

import sqlite3


import config


def creat_databace():
    '''creat databace'''

    db = sqlite3.connect(config.ROOT_PATH + "/data/databace.db")
    cursor = db.cursor()

    _sql_command = """

        CREATE TABLE IF NOT EXISTS admin (
            row INTEGER,
            chat_id INTEGER
        );


        CREATE TABLE IF NOT EXISTS options (
            name VARCHAR (100),
            int_var INTEGER,
            str_var VARCHAR (100)
        );

    """

    cursor.executescript(_sql_command)


    _sql_command = """
        SELECT * FROM admin
    """
    cursor.execute(_sql_command)

    if list(cursor) == []:
        _sql_command = """
            INSERT INTO admin VALUES (1, 0)
        """
        cursor.execute(_sql_command)


    _sql_command = """
        SELECT * FROM options
    """
    cursor.execute(_sql_command)

    if list(cursor) == []:
        _sql_command = """
            INSERT INTO options VALUES ("unknow", 0, "unknow");
            INSERT INTO options VALUES ("unknow", 0, "unknow")
        """
        cursor.executescript(_sql_command)


    db.commit()
    db.close()




def get_admin_CHAT_ID():

    db = sqlite3.connect(config.ROOT_PATH + "/data/databace.db")
    cursor = db.cursor()

    _sql_command = """
        SELECT * FROM admin WHERE row LIKE 1
    """

    cursor.execute(_sql_command)

    _temp_databace_1 = list(cursor)

    return _temp_databace_1[0][-1]



def set_admin_CHAT_ID(chat_id):

    db = sqlite3.connect(config.ROOT_PATH + "/data/databace.db")
    cursor = db.cursor()

    _sql_command = f"""
        UPDATE admin SET chat_id = {chat_id} WHERE row LIKE 1
    """

    cursor.execute(_sql_command)

    db.commit()
    db.close()

