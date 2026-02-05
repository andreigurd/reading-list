markdown

# Reading List Data Structure

## Features

- Add a book
- View all books (using tabulate)
- View by status (Want to Read / Reading / Finished)
- Move book to different status
- Add rating and review (only for finished books)
- Search by title or author
- Delete a book
- Save/load from JSON
- auto Track and display reading pace (pages per day) at top
- Track reading goal (e.g., "read 12 books this year")
- Export reading stats report
- Recommend random book from "Want to Read" list
- Statistics Feature:
    - Total books tracked
    - Average rating of finished books
    - Books finished this month
    - Most read author
    - Current reading streak


## Book Object
- title (string)
- author (string)
- genre/category  
- status (Want to Read / Reading / Finished)
- rating (int 1-5, only if Finished)
- review (string, optional and only if Finished)
- date_added (string)
- date_finished (string, only if Finished)
- current_page (int, only if Reading)
- total_pages (int)

## Menu options
- [0] Exit
- [1] Add Book
- [2] View All Books
- [3] View By Status
- [4] Update Status
- [5] Rate and Review Finished Book
- [6] Show Reading Statistics
- [7] Search By Title or Author
- [8] Delete a Book
- [9] Reading Goal
- [10] Export Reading Statistics Report
- [11] Recommend Book