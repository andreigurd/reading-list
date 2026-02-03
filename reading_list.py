import json
from tabulate import tabulate
from datetime import datetime,date,timedelta
import os


#-----------------------------------------------------------------------
#   opening tasks json file
#-----------------------------------------------------------------------
try:
    with open('books.json', 'r') as file:
        books = json.load(file)
except FileNotFoundError:
    print("Books file not found. Blank list created.")
    books = [] # makes an empty list
except json.JSONDecodeError:
    print("Issue loading Books file. File empty or invalid JSON file. Blank Books list created.")
    books = []
except ValueError:
    print("Invalid Books item. Blank list created.")
    books = []
except PermissionError:
    print("Need permission to access Books file. Blank Books list created.")
    books = []


#-----------------------------------------------------------------------
#   function to write to expenses json
#-----------------------------------------------------------------------
def write_json():
    with open('books.json', 'w') as file:
        json.dump(books, file, indent=4)