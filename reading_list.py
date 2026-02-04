import json
from tabulate import tabulate
from datetime import datetime,date,timedelta
import os

valid_status = ['want to read', 'reading', 'finished']
valid_category = ["sci fi", "fantasy", "mystery", "thriller", "romance", "horror", "graphic novel"]

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
#   timestamp
#-----------------------------------------------------------------------

def datetime_now_stamp():    
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d")
    return date_string

#-----------------------------------------------------------------------
#   showing menu
#-----------------------------------------------------------------------

def show_menu():
    print("")    
    print("[0] Exit")
    print("[1] Add Book")
    print("[2] View All Books")
    print("[3] View By Status")
    # print("[4] x")
    # print("[5] x")
    # print("[6] x")

#-----------------------------------------------------------------------
#   option [1] Add book
#-----------------------------------------------------------------------

def add_book():
#-------- title
    while True:
        try:
            title = str(input("Enter book title: ").lower())
            if title == "":
                print("Blank is invalid entry. Please try again.")
            else:
                break                
        except ValueError:
            print("Invalid entry. Please try again.")
#-------- author
    while True:
        try:
            author = str(input("Enter book author: ").lower())
            if author == "":
                print("Blank is invalid entry. Please try again.")
            else:
                break                
        except ValueError:
            print("Invalid entry. Please try again.")
#-------- genre/category    
    while True:        
        category = input("Enter book genre/category (Sci Fi, Fantasy, Mystery, Thriller, Romance, Horror, Graphic Novel): ").lower()
        if category in valid_category:
            break
        else:
            print("Invalid Status. Please try again.")
#-------- status
    finish_flag = None
    reading_flag = None
    while True:        
        status = input("Enter status (Want to Read / Reading / Finished): ").lower()

        if status == "finished":
            finish_flag = "finish_flag_active"

        if status == "reading":
            reading_flag = "reading_flag_active"            
        
        if status in valid_status:
            break
        else:
            print("Invalid Status. Please try again.")
#-------- rating (if finished)
    rating = "N/A"
    if finish_flag == "finish_flag_active":
        while True:
            try:
                rating = int(input("Select book rating (1 to 5): "))
                if 1<= rating and rating <=5:
                    break
                else:
                    print("Number out of range. Please try again.")
            except ValueError:
                print("Invalid entry. Please try again.")        
        
#-------- optional review
    review = "N/A"
    while True:
        optional = input("Do you want to leave a review (Yes or No)").lower()
        if optional == "yes":
            try:
                review = str(input("Enter book review: "))
                if review == "":
                    print("Blank is invalid entry. Please try again.")
                else:
                    break                
            except ValueError:
                print("Invalid entry. Please try again.")
        elif optional == "no":
            break
        else:
            print("Invalid entry. Please try again.")
        
#-------- date added
    date_string = datetime_now_stamp()
    print(f'Book added date entered as {date_string}')   
        
#-------- date finished (if finished)
    date_finished = "Not Finished"
    if finish_flag == "finish_flag_active":
        while True:
            try:
                date_finished = str(input("Enter date book was finished on (yyyy-mm-dd) format): "))
                if date_finished == '':
                    print("Blank is invalid entry. Please try again.")
                else:
                    break
                
            except ValueError:
                print("Invalid entry. Please try again.")

#-------- current page (if reading)
    current_page = "N/A"
    if reading_flag == "reading_flag_active":
        while True:
            try:
                current_page = int(input("Enter current page number: "))
                if current_page > 0:
                    break
                else:
                    print("Invalid entry. Please try again.")
            except ValueError:
                print("Invalid entry. Please try again.")

#-------- total pages in book
    while True:
            try:
                total_pages = int(input("Enter total pages in book: "))
                if total_pages > 0:
                    break
            except ValueError:
                print("Invalid entry. Please try again.")

    book_item = {
        "title" : title,
        "author" : author,
        "genre/category" : category,
        "rating" : rating,
        "review" : review,
        "date added" : date_string,
        "date finished" : date_finished,
        "current page" : current_page,
        "total book pages" : total_pages
    }

    books.append(book_item)
    print(f'{title} added.')

#-----------------------------------------------------------------------
#   option [2] View All Contacts
#-----------------------------------------------------------------------
def view_books():
    print("Displaying All Books")
    print(tabulate(books, headers="keys", tablefmt="fancy_grid"))

#-----------------------------------------------------------------------
#   option [3] View By Status
#-----------------------------------------------------------------------

def view_status():    
    while True:
        search_term = input("Enter status to view (Want to Read, Reading, Finished): ").lower()
        if search_term in valid_status:
            break
        else:
            print("Invalid Status. Please try again.")
    
    searched_list = []
    for book in books:
        if search_term == book['status']:
            searched_list.append(book)
        
    print(tabulate(searched_list,headers = "keys", tablefmt="fancy_grid"))


#-----------------------------------------------------------------------
#   function to write to expenses json
#-----------------------------------------------------------------------
def write_json():
    with open('books.json', 'w') as file:
        json.dump(books, file, indent=4)

#-----------------------------------------------------------------------
#   while loop to get user input
#-----------------------------------------------------------------------

while True:
    show_menu()
    option = input("\nSelect Option: ")
    if option == '0':        
        write_json()
        print("Goodbye.")
        break    
    elif option == '1':
        add_book()
        write_json()
    elif option == '2':
        view_books()
    elif option == '3': 
        view_status()

    # elif option == '4':
    #     
    #     
    # elif option == '5':
    #     

    else:
        print("Invalid action. Please try again.")