import psycopg2
from psycopg2 import Error
import configparser


def drop_tables(cur):
    cur.execute("""
    DROP TABLE IF EXISTS Customer CASCADE;
    DROP TABLE IF EXISTS Phonebook CASCADE;
    """)
    conn.commit()


def create_tables(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Customer(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(40) NOT NULL,
    last_name VARCHAR(40) NOT NULL,
    email VARCHAR(60) UNIQUE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Phonebook(
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES Customer(id),
    phone_number VARCHAR(40) UNIQUE
    );
    """)
    conn.commit()


def add_customer(cur, first_name, last_name, email=None):
    cur.execute("""
    INSERT INTO Customer(first_name, last_name, email) VALUES (%s, %s, %s);
    """, (first_name, last_name, email))
    conn.commit()


def add_phone(cur, customer_id, phone_number):
    try:
        cur.execute("""
        INSERT INTO Phonebook (customer_id, phone_number) VALUES (%s, %s);
        """, (customer_id, phone_number))
    except(Exception, Error):
        print('There is no customer with id =', customer_id)
    conn.commit()


def update_info(cur, customer_id, first_name=None, last_name=None, email=None, old_number=None, new_number=None):
    cur.execute("""
    SELECT * FROM Customer
    WHERE id = %s;
    """, (customer_id,))
    if not cur.fetchall():
        print('There is no customer with id =', customer_id)
    else:
        if first_name:
            cur.execute("""
            UPDATE Customer SET first_name = %s
            WHERE id = %s
            """, (first_name, customer_id))

        if last_name:
            cur.execute("""
            UPDATE Customer SET last_name = %s
            WHERE id = %s
            """, (last_name, customer_id))

        if email:
            cur.execute("""
            UPDATE Customer SET email = %s
            WHERE id = %s
            """, (email, customer_id))

        if old_number:
            cur.execute("""
            SELECT * FROM Phonebook
            WHERE phone_number = %s;
            """, (old_number,))
            if not cur.fetchall():
                print('There is no number to change like', old_number)
            else:
                cur.execute("""
                UPDATE Phonebook SET phone_number = %s
                WHERE id = %s AND phone_number = %s
                """, (new_number, customer_id, old_number))
    conn.commit()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')
    conn = psycopg2.connect(database=config['DB']['name'], user=config['DB']['user'], password=config['DB']['password'])
    with conn.cursor() as cursor:
        drop_tables(cursor)
        create_tables(cursor)
        add_customer(cursor, 'John', 'Doe', 'strange@gmail.com')
        add_customer(cursor, 'Some', 'Buddy', 'somebody@buddy.com')
        add_phone(cursor, 1, '123-45-67')
        add_phone(cursor, 1, '777-9-777')
        add_phone(cursor, 2, '987412365')
        update_info(cursor, 1, 'Changed', 'All', 'info@all', '123-45-67', '555-OK')
    conn.close()
