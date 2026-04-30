from sqlalchemy import text, create_engine


# def testing1(option):
#     print(f"Hello, what is your name?")
#     print(f'{option}')

def new_engine(database_name: str):
    """
    database_name: the name of the database
    """
    return create_engine(
        f"mssql+pyodbc://LAPTOP-DU4JGOHJ/{database_name}"
        "?driver=ODBC+Driver+17+for+SQL+Server"
        "&trusted_connection=yes"
        "&TrustServerCertificate=yes"
    )

def wipe_tables_clean(engine):
    """Clears all data from tables in child-to-parent order to respect FK constraints."""
    tables = [
        'blushes'
              ]
    with engine.connect() as connection:
        trans = connection.begin()
        try:
            for table in tables:
                print(f"Clearing: {table}...")
                connection.execute(text(f"DELETE FROM {table}"))
            trans.commit()
            print("--- All tables cleared. ---")
        except Exception as e:
            trans.rollback()
            print(f"Error: {e}")