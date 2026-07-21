import importlib.util
import database
from database.database import Database

print("database =", database)
print("Database =", Database)
print(importlib.util.find_spec("database"))