import psycopg2
import configparser
import pprint


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
    email VARCHAR(60)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Phonebook(
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES Customer(id),
    phone_number VARCHAR(40)
    );
    """)
    conn.commit()


def add_customer(cur, first_name, last_name, email=None):
    cur.execute("""
    INSERT INTO Customer(first_name, last_name, email) VALUES (%s, %s, %s);
    """, (first_name, last_name, email))
    conn.commit()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')
    conn = psycopg2.connect(database=config['DB']['name'], user=config['DB']['user'], password=config['DB']['password'])
    with conn.cursor() as cursor:
        drop_tables(cursor)
        create_tables(cursor)
        add_customer(cursor, 'John', 'Doe', 'strange@gmail.com')
    conn.close()
