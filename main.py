import psycopg2

conn = psycopg2.connect(database='lesson', user='postgres', password='120290Vova')

with conn.cursor() as cur:

    cur.execute("""
    DROP TABLE homework;
    DROP TABLE course;
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS course(
    id SERIAL PRIMARY KEY,
    name VARCHAR(60) UNIQUE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS homework(
    id SERIAL PRIMARY KEY,
    number INTEGER NOT NULL,
    description TEXT NOT NULL,
    course_id INTEGER NOT NULL REFERENCES course(id)
    );
    """)

    cur.execute("""
    INSERT INTO course(name) VALUES ('Python');
    """)

    cur.execute("""
    INSERT INTO course(name) VALUES ('Java') RETURNING id, name;
    """)

    cur.execute("""
    INSERT INTO homework(number, description, course_id) VALUES(1, 'Домашка по питону', 1);
    """)

    cur.execute("""
    SELECT * FROM course;
    """)
    conn.commit()

    def get_course_name(cursor, course_id: int) -> str:
        cursor.execute("""
        SELECT name FROM course WHERE id=%s;
        """, (course_id,))
        return cur.fetchone()[0]

    course_name = get_course_name(cur, 1)

    cur.execute("""
    INSERT INTO homework(number, description, course_id) VALUES(%s, %s, %s);
    """, (2, 'Задание на джаву', 2))

    cur.execute("""
    SELECT * FROM homework;
    """)

    cur.execute("""
    UPDATE course SET name=%s WHERE id=%s;
    """, ('Advanced Python', 1))

    cur.execute("""
    SELECT * FROM course;
    """)
    print(cur.fetchall())

conn.close()
