import json
from tabulate import tabulate
from datetime import datetime,date,timedelta
import os

valid_status = ['want to read', 'reading', 'finished']
valid_category = ["sci fi", "fantasy", "mystery", "thriller", "romance", "horror", "graphic novel"]

#-----------------------------------------------------------------------
#   opening books json file
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
    print("[4] Update Status")
    print("[5] Log Pages Read")
    print("[6] Rate and Review Finished Book")
    print("[7] Show Reading Statistics")


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
        
        if status == "want to read":
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
# this should be timestamped not user input
    
    
    date_finished = "not finished"
    if finish_flag == "finish_flag_active":
        date_finished = datetime_now_stamp()

    #     while True:
    #         try:
    #             date_finished = str(input("Enter date book was finished on (yyyy-mm-dd) format): "))
    #             if date_finished == '':
    #                 print("Blank is invalid entry. Please try again.")
    #             else:
    #                 break
                
    #         except ValueError:
    #             print("Invalid entry. Please try again.")

#-------- date started reading    
    
    started_reading = "not reading"
    if reading_flag == "reading_flag_active":
        started_reading = datetime_now_stamp()

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
        "status" : status,
        "rating" : rating,
        "review" : review,
        "date added" : date_string,
        "date started reading" : started_reading,
        "date finished" : date_finished,        
        "current page" : current_page,
        "total pages" : total_pages
    }

    books.append(book_item)
    print(f'{title} added.')


#-----------------------------------------------------------------------
#    create numbered list to choose from (note this does not print)
#-----------------------------------------------------------------------
def create_numbered_list():
    
    numbered_list = []    
    for number, book_item in enumerate(books, start=1):
            numbered_books = {
            "number": number,
            "title" : book_item["title"],
            "author" : book_item["author"],
            "genre/category" : book_item["genre/category"],
            "status" : book_item["status"],
            "rating" : book_item["rating"],
            "review" : book_item["review"],
            "date added" : book_item["date added"],
            "date started reading" : book_item["started_reading"],
            "date finished" : book_item["date finished"],
            "current page" : book_item["current page"],
            "total pages" : book_item["total pages"]
            }                
            numbered_list.append(numbered_books)
    
    return numbered_list


#-----------------------------------------------------------------------
#    (only finished books) display numbered list to choose from
#-----------------------------------------------------------------------
# note finished books list will have a different number but will also keep global list number for refrencing global books list.

def create_fin_numbered_list():
    numbered_list = create_numbered_list()

    finished_books = []
    for book in numbered_list:
        if book["status"] == "finished":
            finished_books.append(book)      
        
    numbered_fin_list = []
    for number, book in enumerate(finished_books, start=1):
        if book["status"] == "finished":
            fin_numbered_books = {
            "number": number,
            "title" : book["title"],
            "author" : book["author"],
            "genre/category" : book["genre/category"],
            "status" : book["status"],
            "rating" : book["rating"],
            "review" : book["review"],
            "date added" : book["date added"],
            "date started reading" : book["started_reading"],
            "date finished" : book["date finished"],
            "current page" : book["current page"],
            "total pages" : book["total pages"],
            "global number": book["number"]
            } 

            numbered_fin_list.append(fin_numbered_books)

    return numbered_fin_list

#-----------------------------------------------------------------------
#   option [2] View All Books
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
#   option [4] Update Status
#-----------------------------------------------------------------------

def update_status():
    # create numbered list to choose from.
    print('Displaying All Books')
    numbered_list = create_numbered_list()
    print(tabulate(numbered_list,headers = "keys", tablefmt="fancy_grid"))    

    # user chooses book # to update status.
    while True:
        try:
            choice = int(input("Select book number to update status: "))
            if 1 <= choice and choice <= len(books):
                break
            else:
                print("Number out of range. Please try again.")

        except ValueError:
            print("Invalid entry. Please try again.")

        # user chooses new status.   
    while True:        
        status = input("Enter status update (Want to Read / Reading / Finished): ").lower()

        if status == "want to read":
            started_reading = "not reading"
            date_finished = "not finished"
            break
        elif status == "reading":
            started_reading = datetime_now_stamp()
            date_finished = "not finished"
            break
        elif status == "finished":
                date_finished = datetime_now_stamp()
                current_page = "N/A"
                break
        else:
            print("Invalid Status. Please try again.")

            
    # choice-1 is index for global books list that we want to mark complete.
    selected_book = books[choice-1]

    selected_book['status'] = status
    selected_book['date started reading'] = started_reading
    selected_book['date finished'] = date_finished 
    selected_book['current page'] = current_page 
    print(f'({selected_book["title"]}) book marked {status}.')
        
    print(tabulate(books,headers = "keys", tablefmt="fancy_grid"))
    
#-----------------------------------------------------------------------
#   option [6] Log Pages Read
#-----------------------------------------------------------------------
    
def log_pages_read():

    # create numbered list to choose from.
    print('Displaying All Books')
    numbered_list = create_numbered_list()
    print(tabulate(numbered_list,headers = "keys", tablefmt="fancy_grid"))    

    # user chooses book # to update status.
    while True:
        try:
            choice = int(input("Select book number to log read pages: "))
            if 1 <= choice and choice <= len(books):
                break
            else:
                print("Number out of range. Please try again.")

        except ValueError:
            print("Invalid entry. Please try again.")    
#-----------------------------------------------------------------------
#   option [6] Update Rate and review finished books
#-----------------------------------------------------------------------
def update_rating():     
    # display numbered finished list to choose from.

    print('Displaying Finished Books')
    numbered_fin_list = create_fin_numbered_list()
    if not numbered_fin_list:
        print("No books are currently finished.")
        return
    else:          
        print(tabulate(numbered_fin_list,headers = "keys", tablefmt="fancy_grid"))            

    while True:
        try:
            choice = int(input("Select book number to rate and review: "))
            if 1 <= choice and choice <= len(numbered_fin_list):
                # selected_fin_book = numbered_fin_list[choice]
                # global_number = selected_fin_book['global_number']
                break
            else:
                print("Number out of range. Please try again.")

        except ValueError:
            print("Invalid entry. Please try again.")
    
    # choice should match number from numbered_fin_list or match global number from books    
    selected_book = numbered_fin_list[choice-1]    
    # ^ this gives us the whole book dictionary
    global_number = selected_book['global number']    
    # ^ this should give us the cooresponding global number
    global_selected_book = books[global_number-1]

    
    while True:
            try:
                rating = int(input("Select book rating (1 to 5): "))
                if 1<= rating and rating <=5:                    
                    global_selected_book['rating'] = rating
                    break
                else:
                    print("Number out of range. Please try again.")
            except ValueError:
                print("Invalid entry. Please try again.")            
    
    while True:
        optional = input("Do you want to leave a review (Yes or No)").lower()
        if optional == "yes":
            try:
                review = str(input("Enter book review: "))
                if review == "":
                    print("Blank is invalid entry. Please try again.")
                else:                    
                    global_selected_book['review'] = review
                    break                
            except ValueError:
                print("Invalid entry. Please try again.")
        elif optional == "no":
            break
        else:
            print("Invalid entry. Please try again.")

    print(f'({global_selected_book["title"]}) book rating and review updated.')

#-----------------------------------------------------------------------
#   option [7] Show reading stats
#-----------------------------------------------------------------------
def show_statistics():
#-------- Total books tracked
    total_books = len(books)    

    fin_books = []
    for book in books:
        if book['status'] == "finished":
            fin_books.append(book)        
    
    rating_sum = sum(item['rating'] for item in fin_books)

    total_rated_books = len(fin_books)
    if total_rated_books:
        average_rating = rating_sum / total_rated_books
    else:
        print("No current finished books.")

#-------- Books finished this month
        
    month_fin_books = []
    for book in fin_books:
        now = datetime.now()
        date_string = now.strftime("%Y-%m-%d %H:%M:%S")       

        book_date = book['date finished'][:7]
        month_now = date_string[:7]

        if book_date == month_now:
            month_fin_books.append(book)
        
#-------- Most read author      
    # max() finds the largest element in an iterable

    author_list = []
    for author in books:
        author_list.append(author['author'])
    #print(author_list)
    most_author = max(author_list, key=author_list.count)
    print(most_author)
        
#-------- Current reading streak (most days in a row at least one book is in reading status)

    books_reading = []
    for reading in books:
        if reading['status'] == "reading":
            books_reading.append(reading)

    # Statistics Feature:
    # - Total books tracked
    # - Average rating of finished books
    # - Books finished this month
    # - Most read author
    # - Current reading streak


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
    elif option == '4':
        update_status()
        write_json()
    elif option == '5':
        log_pages_read()
        write_json()
    elif option == '6':
        update_rating()
        write_json()
    elif option == '7':
        show_statistics()

    else:
        print("Invalid action. Please try again.")