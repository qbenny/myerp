# create the company db
# use the python 3.5 and SQLite3 DB

import sqlite3

def query(db_name, sql, data):
    "access the sqlite3 data base"
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(sql, data)
        db.commit()

def create_orders_table(db_name):
    sql = """
            CREATE TABLE Orders(
                OrderNumber     integer,
                OrderDate       text,                
                PartNumber      text,
                Quantity        integer,
                UnitPrice       real,                
                ETADate         text,
                Amount          real,
                Primary Key(PartNumber)                
            )
    """
    query(db_name, sql, ())

def create_products_table(db_name):
    sql = """
            CREATE TABLE Products(
                Product_name        text,
                Product_name_cn     text,
                PartNumber          text,
                Description         text,
                Description_cn      text,
                UnitPrice           real
            )
    """
    query(db_name, sql, ())

def create_tables(db_name):
    "create the table"
    create_orders_table(db_name)
    create_products_table(db_name)


def drop_table(db_name, tables):
    "drop the table"
    for table in tables:
        sql = "DROP TABLE IF EXISTS {0}".format(table)
        query(db_name, sql, ())

def main():
    "all table need to be recreated if exists, because table get a foreign key"
    db_name = "shanglin.db"

    recreate = False
    response = input("are you sure to erase all the table and create again(y/n)?: ")
    if response.lower() == 'y':
        tables = ("Orders", "Products")
        drop_table(db_name, tables)
        print("all existing data is erased!")
        recreate = True

    if recreate:
        create_tables(db_name)

if __name__ == '__main__':
    main()
