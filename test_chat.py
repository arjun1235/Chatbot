import sys
import importlib.util

print("cwd:", __import__("os").getcwd())
print("sys.path:", sys.path)

spec = importlib.util.find_spec("database")
print("spec:", spec)

import database
print("database imported:", database)

from database.database import Database
print(Database)