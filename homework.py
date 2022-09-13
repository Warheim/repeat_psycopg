import psycopg2
import configparser

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')
    conn = psycopg2.connect(database=config['DB']['name'], user=config['DB']['user'], password=config['DB']['password'])
    with conn.cursor() as cur:
        pass
        conn.commit()
    conn.close()
