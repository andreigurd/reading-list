import json
from tabulate import tabulate
from datetime import datetime,date,timedelta
import os
import random

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
#   opening reading_log json file
#-----------------------------------------------------------------------
try:
    with open('reading_log.json', 'r') as file:
        reading_log = json.load(file)
except FileNotFoundError:
    print("Log file not found. Blank list created.")
    reading_log = []
except json.JSONDecodeError:
    print("Issue loading Log file. File empty or invalid JSON file. Blank Log list created.")
    reading_log = []
except ValueError:
    print("Invalid budget item. Blank list created.")
    reading_log = []
except PermissionError:
    print("Need permission to access Log file. Blank Log list created.")
    reading_log = []

#-----------------------------------------------------------------------
#   opening reading goals json file
#-----------------------------------------------------------------------
# reading goal is a simple int but better to store as a dictionary. easier to update with user input later. note for now reading_goals = {year_goal:0}
try:
    with open('reading_goals.json', 'r') as file:
        reading_goals = json.load(file)
except FileNotFoundError:
    print("Goals file not found. Goal set to default zero.")
    reading_goals = {"year_goal": 0}
except json.JSONDecodeError:
    print("Issue loading Goals file. File empty or invalid JSON file. Goal set to default zero.")
    reading_goals = {"year_goal": 0}
except ValueError:
    print("Invalid Goals item. Goal set to default zero.")
    reading_goals = {"year_goal": 0}
except PermissionError:
    print("Need permission to access Goals file. Goal set to default zero.")
    reading_goals = {"year_goal": 0}

#-----------------------------------------------------------------------
#   timestamp
#-----------------------------------------------------------------------

def datetime_now_stamp():    
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d")
    return date_string

#-----------------------------------------------------------------------
#   showing reading pace today
#-----------------------------------------------------------------------

date_string = datetime_now_stamp()   
pages_sum = sum(log['pages read'] for log in reading_log if log['date of reading'] == date_string)
if pages_sum == 0:
    print(f'No pages read today.{pages_sum}')
elif pages_sum == 1:
    print(f'1 page read today.')
else:
    print(f'Current reading pace: {pages_sum} pages read today.')

#-----------------------------------------------------------------------
#   showing menu
#-----------------------------------------------------------------------

def show_menu():
    print("")
    print("Welcome to Reading Tracker")     
    print("[0] Exit")
    print("[1] Add Book")
    print("[2] View All Books")
    print("[3] View By Status")
    print("[4] Update Status")
    print("[5] Log Pages Read")
    print("[6] Rate and Review Finished Book")
    print("[7] Show Reading Statistics")
    print("[8] Search By Title or Author")
    print("[9] Delete a Book")
    print("[10] Book Reading Goals")
    print("[11] Export Reading Statistics Report")
    print("[12] Get Book Recommendation")

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

#-------- genre    
    while True:        
        category = input("Enter book genre (Sci Fi, Fantasy, Mystery, Thriller, Romance, Horror, Graphic Novel): ").lower()
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
            break

        if status == "reading":
            reading_flag = "reading_flag_active"
            break            
        
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
    
    date_finished = "not finished"
    if finish_flag == "finish_flag_active":
        date_finished = datetime_now_stamp()

#-------- started reading    
    
    started_reading = "not reading"
    if reading_flag == "reading_flag_active":
        started_reading = datetime_now_stamp()

#-------- current page (if reading)
    current_page = 0
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
        "genre" : category,
        "status" : status,
        "rating" : rating,
        "review" : review,
        "date added" : date_string,
        "started reading " : started_reading,
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
            "genre" : book_item["genre"],
            "status" : book_item["status"],
            "rating" : book_item["rating"],
            "review" : book_item["review"],
            "date added" : book_item["date added"],
            "started reading " : book_item["started reading "],
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
    # filter list and then enumerate after to avoid number gaps
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
            "genre" : book["genre"],
            "status" : book["status"],
            "rating" : book["rating"],
            "review" : book["review"],
            "date added" : book["date added"],
            "started reading " : book["started reading "],
            "date finished" : book["date finished"],
            "current page" : book["current page"],
            "total pages" : book["total pages"],
            "global number": book["number"]
            } 

            numbered_fin_list.append(fin_numbered_books)

    return numbered_fin_list

#-----------------------------------------------------------------------
#    (only reading now books) display numbered list to choose from
#-----------------------------------------------------------------------
# note finished books list will have a different number but will also keep global list number for refrencing global books list.

def create_reading_numbered_list():
    numbered_list = create_numbered_list()

    reading_books = []
    for book in numbered_list:
        if book["status"] == "reading":
            reading_books.append(book)

    numbered_reading_list = []
    for number, book in enumerate(reading_books, start=1):
        if book["status"] == "reading":
            reading_numbered_books = {
            "number": number,
            "title" : book["title"],
            "author" : book["author"],
            "genre" : book["genre"],
            "status" : book["status"],
            "rating" : book["rating"],
            "review" : book["review"],
            "date added" : book["date added"],
            "started reading " : book["started reading "],
            "date finished" : book["date finished"],
            "current page" : book["current page"],
            "total pages" : book["total pages"],
            "global number": book["number"]
            } 

            numbered_reading_list.append(reading_numbered_books)

    return numbered_reading_list

#-----------------------------------------------------------------------
#   option [2] View All Books
#-----------------------------------------------------------------------
def view_books():
    print("Displaying All Books")
    print(tabulate(books, headers="keys", tablefmt="grid"))

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
        
    print(tabulate(searched_list,headers = "keys", tablefmt="grid"))

#-----------------------------------------------------------------------
#   option [4] Update Status
#-----------------------------------------------------------------------

def update_status():
    # create numbered list of all to choose from.
    print('Displaying All Books')
    numbered_list = create_numbered_list()

    print(tabulate(numbered_list,headers = "keys", tablefmt="grid"))  

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
        
    selected_book = books[choice-1]   
    while True:        
        status = input("Enter status update (Want to Read / Reading / Finished): ").lower()

        if status == "want to read":
            started_reading = "not reading"
            date_finished = "not finished"
            break
        elif status == "reading":
            started_reading = datetime_now_stamp()
            date_finished = "not finished"
            selected_book['started reading '] = started_reading
            break
        elif status == "finished":
                date_finished = datetime_now_stamp()
                selected_book['date finished'] = date_finished
                current_page = 0
                selected_book['current page'] = current_page
                break
        else:
            print("Invalid Status. Please try again.")
            
    
    selected_book['status'] = status
    
    print(f'({selected_book["title"]}) book marked {status}.')        

#-----------------------------------------------------------------------
#   option [5] Log Pages Read
#-----------------------------------------------------------------------
    
def log_pages_read():
    # note user cant log pages on book that are in status not started or finished.
    # create reading numbered list to choose from.
    print('Displaying Books Being Read')
    numbered_list = create_reading_numbered_list()
    print(tabulate(numbered_list,headers = "keys", tablefmt="grid"))    

    # user chooses book # to update status.
    while True:
        try:
            choice = int(input("Select book number to log read pages for: "))
            if 1 <= choice and choice <= len(numbered_list):
                break
            else:
                print("Number out of range. Please try again.")

        except ValueError:
            print("Invalid entry. Please try again.")
                
    selected_book = books[choice-1]
    previous_page = selected_book['current page']    

    while True:
        try:
            current_page = int(input(f"Enter current page number of ({selected_book['title']}): "))
            if current_page > previous_page:
                break
            elif current_page == previous_page:
                print(f'Invalid entry. Enter page number greater than previous {previous_page} page.')
            else:
                print("Invalid entry. Please try again.")
        except ValueError:
            print("Invalid entry. Please try again.")

    # note there is a gloabal reading_log = []
    
    pages_read = current_page - previous_page
    selected_book['current page'] = current_page
    reading_date = datetime_now_stamp()
    date_read = {
        "date of reading" : reading_date,
        "pages read" : pages_read
    }
    reading_log.append(date_read)
    print(f'{pages_read} pages of {selected_book["title"]} book logged.')

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
        print(tabulate(numbered_fin_list,headers = "keys", tablefmt="grid"))            

    while True:
        try:
            choice = int(input("Select book number to rate and review: "))
            if 1 <= choice and choice <= len(numbered_fin_list):                
                break
            else:
                print("Number out of range. Please try again.")

        except ValueError:
            print("Invalid entry. Please try again.")
    
    # choice should match number from numbered_fin_list or match global number from books    
    selected_book = numbered_fin_list[choice-1]  
    global_number = selected_book['global number'] 
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
    now = datetime.now()    
    month_fin_books = []
    for book in fin_books:
        
        date_string = now.strftime("%Y-%m-%d %H:%M:%S")       

        book_date = book['date finished'][:7]
        month_now = date_string[:7]

        if book_date == month_now:
            month_fin_books.append(book)
        
#-------- Most read author (of books being read or finished)     
    
    author_list = []
    for author in books:
        if author["status"] != "want to read":
            author_list.append(author['author'])
    #print(author_list)
    most_author = max(author_list, key=author_list.count)
    #print(most_author)
        
#-------- Current reading streak (most days in a row at least one book is in reading status)
    # note there is a gloabal reading_log = [] of date objects        
    
    page_dates = []
    for entry in reading_log:        
        converted_date = datetime.strptime(entry["date of reading"], "%Y-%m-%d").date()
        page_dates.append(converted_date)        
        
    today = date.today()
    
    page_dates = set(page_dates)
    
    sorted_page_dates = sorted(page_dates, reverse=True)

    days_streak = []
    for number, date_item in enumerate(sorted_page_dates):
        if timedelta(days=number) == today - date_item:
            days_streak.append(date_item)
        else:            
            break

    stats_table = [
        ["Total Books Tracked", total_books],
        ["Average Rating of Finished Books", f"{average_rating:.0f}"],
        ["Books Fininished This Month", len(month_fin_books)],
        ["Most Read Author", most_author],
        ["Current Reading Streak Days", len(days_streak)]
    ]
    
    return stats_table

#-----------------------------------------------------------------------
#   option [8] Search By Title or Author
#-----------------------------------------------------------------------
def search():

    search_term = input("Enter search term for Title or Author search: ").strip().lower()
    searched_list = []
    for book in books:
        if (
        search_term == book['title'] or
        search_term == book['author']            
        ):
            searched_list.append(book)
    
    if searched_list:
        print("---Displaying Matching Books---")
        print(tabulate(searched_list,headers = "keys", tablefmt="grid"))
    else:
        print("No matching books.")

#-----------------------------------------------------------------------
#   option [9] Delete a Book
#-----------------------------------------------------------------------
def delete_book():
    # create numbered list of all to choose from.
    print('Displaying All Books')
    numbered_list = create_numbered_list()

    print(tabulate(numbered_list,headers = "keys", tablefmt="grid")) 

    # user chooses task # to delete.
    removed_book_list = []
    while True:
        try:
            choice = int(input("Select book to delete: "))
            if 1 <= choice and choice <= len(books):
                print(f"Book number {choice} deleted.")                
                removed_book = books.pop(choice-1) 
                removed_book_list.append(removed_book)                               
                print(tabulate(removed_book_list,headers = "keys", tablefmt="grid"))                
                break
            else:
                print("Number out of range. Please try again.")

        except ValueError:
            print("Invalid entry. Please try again.")

#-----------------------------------------------------------------------
#   option [10] Reading Goal
#-----------------------------------------------------------------------
def set_goal():
    
    #-------- Books finished this year
    now = datetime.now()    
    this_year_fin_books = []
    # loop through books and append all with date finished this year
    date_string = now.strftime("%Y-%m-%d %H:%M:%S") 
    for book in books:        

        book_date = book['date finished'][:4]
        year_now = date_string[:4]

        if book_date == year_now:
            this_year_fin_books.append(book)

    #-------- determin goal status

    number_fin_books = len(this_year_fin_books)
    current_goal = reading_goals["year_goal"] 
    if 0 < current_goal:
        if current_goal <= number_fin_books:
            print(f'Reading goal met! {len(this_year_fin_books)} books read this year.')
        else:               
            print(f'Reading goal not met yet. {len(this_year_fin_books)} books read this year.')
    
    #-------- overide or user existing goal
    if current_goal > 0:
        print(f"Current yearly reading goal is {current_goal} books.")
        while True:            
            answer = input("Override or Continue with goal?: ").lower()

            if answer == "override":
                reading_goals.clear()                
                break
            elif answer == "continue":
                return
            else:
                print("Invalid option. Please try again.")

    #-------- input reading goal amount 
    while True:        
        try:
            reading_goals["year_goal"] = int(input("Enter yearly book goal: "))
            print(f"goal of {reading_goals['year_goal']} books entered.")
            break         
        except ValueError:
            print("Invalid number. Please try again.")

#-----------------------------------------------------------------------
#   option [11] Export Reading Statistics Report (CSV)
#-----------------------------------------------------------------------
def export_report():
    stats_table = show_statistics()
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d %H:%M:%S")     
    date_now = date_string[:10]

    with open(f'{date_now} Reading_Stats.csv', 'w') as file:
        
        for stat in stats_table:
            file.write(f"{stat[0]},{stat[1]}\n")
    
    file_path = os.path.abspath(f'{date_now} Reading_Stats.csv')
    print(f"CSV file exported to:\n{file_path}")

#-----------------------------------------------------------------------
#   option [12] Get Book Recommendation from want to read list
#-----------------------------------------------------------------------
def book_recommendation():
    # make list of want to read book titles
    want_to_books = []
    for book in books:
        if book["status"] == "want to read":
            want_to_books.append(book['title'])
    
    #make list of all books want to read

    
    if want_to_books:
        recommended_book = random.choice(want_to_books)
        print(f"Recommending to read {recommended_book}.")
    else:
        print(f'No books with "Want to Read" status.')
    
#-----------------------------------------------------------------------
#   function to write to books json
#-----------------------------------------------------------------------
def write_json():
    with open('books.json', 'w') as file:
        json.dump(books, file, indent=4)

#-----------------------------------------------------------------------
#   function to write to reading_log json
#-----------------------------------------------------------------------
def write_pages_log_json():
    with open('reading_log.json', 'w') as file:
        json.dump(reading_log, file, indent=4)

#-----------------------------------------------------------------------
#   function to write to reading_goal json
#-----------------------------------------------------------------------
def write_reading_goals_json():
    with open('reading_goals.json', 'w') as file:
        json.dump(reading_goals, file, indent=4)


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
        write_pages_log_json()
    elif option == '6':
        update_rating()
        write_json()
    elif option == '7':
        stats_table = show_statistics()
        print("---Book Statistics---")
        print(tabulate(stats_table, tablefmt="grid"))
    elif option == '8':
        search()
    elif option == '9':
        delete_book()
        write_json()
    elif option == '10':
        set_goal()
        write_reading_goals_json()
    elif option == '11':
        export_report()
    elif option == '12':
        book_recommendation()
    else:
        print("Invalid action. Please try again.")