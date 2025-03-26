from sqlalchemy import inspect
from database.db import engine

inspector = inspect(engine)
for table_name in inspector.get_table_names():
    print(f"\nTabla: {table_name}")
    for column in inspector.get_columns(table_name):
        print(f" - {column['name']} ({column['type']})")
