import psycopg2


def drop_tables(db_user, db_password, db_host, db_name, table_names):
    host, port = db_host.split(":")
    conn = psycopg2.connect(
        host=host, port=port, user=db_user, password=db_password, dbname=db_name
    )
    cursor = conn.cursor()
    for table_name in table_names:
        cursor.execute(f"DROP TABLE IF EXISTS public.{table_name} CASCADE;")
    conn.commit()
    conn.close()
    print(f"Successfully dropped tables: {', '.join(table_names)}")


def main(db_user, db_password, db_host, db_name, table_names):
    drop_tables(db_user, db_password, db_host, db_name, table_names)


if __name__ == "__main__":
    db_user = ""
    db_password = ""
    db_host = ""
    db_name = ""
    table_names = [""]
    main(db_user, db_password, db_host, db_name, table_names)
