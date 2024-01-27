import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

hostname = os.getenv("DB_HOSTNAME")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USERNAME")
pw = os.getenv("DB_PASSWORD")
port_id = os.getenv("DB_PORT")

conn = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = username,
    password = pw,
    port = port_id
)

cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS panels_data")

create_table = '''CREATE TABLE IF NOT EXISTS panels_data (
                    id          serial4 NOT NULL,
                    name        text NOT NULL,
                    stack       int4 NOT NULL,
                    efficiency  float4,
                    num_panels  int4 NOT NULL,
                    tilt        float4 NOT NULL
                )'''
cur.execute(create_table)

insert_table = "INSERT INTO panels_data(name, stack, efficiency, num_panels, tilt) VALUES (%s, %s, %s, %s, %s)"
insert_values = [("Back Left 1", 7, 0.25, 28, -8.28),
                 ("Back Right 1", 8, 0.25, 28, -8.28),
                 ("Back Middle 1", 3, 0.25, 12, -8.06),
                 ("Back Left 2", 9, 0.25, 28, -5.21),
                 ("Back Right 2", 10, 0.25, 28, -5.21),
                 ("Middle Left 1", 15, 0.25, 18, -2.14),
                 ("Middle Right 1", 16, 0.25, 18, -2.14),
                 ("Middle Left 2", 4, 0.25, 10, 0.77),
                 ("Middle Right 2", 4, 0.25, 10, 0.77),
                 ("Front Left", 13, 0.25, 21, 5.13),
                 ("Front Right", 2, 0.25, 21, 5.13), 
                 ("Front Middle", 11, 0.25, 16, 8.75), 
                ]

for values in insert_values:
    cur.execute(insert_table, values)

cur.close()
conn.commit()
conn.close()

