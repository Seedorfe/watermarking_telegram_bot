
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
            row INTEGER,
            options_name VARCHAR (100),
            var INTEGER
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
            INSERT INTO options VALUES (1, "opacity", 0.75);
            INSERT INTO options VALUES (2, "duration", 10);
            INSERT INTO options VALUES (3, "position", 1);
        """
        cursor.executescript(_sql_command)


    db.commit()
    db.close()

    try:
        _file = open(config.ROOT_PATH + "/data/" + "watermark.txt", mode="x")
    except FileExistsError:
        pass # do nothing
    else:
        _file.write("None") 
        _file.close()




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




def get_watermark_text():
    _file = open(config.ROOT_PATH + "/data/" + "watermark.txt")

    _temp_bot_1 = _file.read()

    _file.close()

    return _temp_bot_1


def set_watermark_text(text):
    _file = open(config.ROOT_PATH + "/data/" + "watermark.txt", mode="w")
    _file.write(
        f"""{text}"""
    )

    _file.close()




def update_options(name, var):

    _options_names = ["opacity", "duration", "position"]
    
    db = sqlite3.connect(config.ROOT_PATH + "/data/databace.db")
    cursor = db.cursor()

    _row = _options_names.index(name) + 1

    _sql_command = f"""
        UPDATE options SET var = {var} WHERE row LIKE {_row}
    """

    cursor.execute(_sql_command)

    db.commit()
    db.close()



def get_options(name):

    _options_names = ["opacity", "duration", "position"]


    db = sqlite3.connect(config.ROOT_PATH + "/data/databace.db")
    cursor = db.cursor()

    _sql_command = f"""
        SELECT * FROM options 
    """

    cursor.execute(_sql_command)

    _temp_databace_1 = list(cursor)

    db.close()

    return _temp_databace_1[_options_names.index(name)][2]


