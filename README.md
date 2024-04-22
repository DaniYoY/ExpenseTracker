EXPENSE TRACKER
This is an app that keeps track of expenses based on input categories
and provides historical and category spend reviews: 

    A. Required libraries:
        Babel 2.12.1
        Matplotlib 3.7.2
        Pandas 2.1.0
        Tkcalendar 1.6.1



B. CRUD operations are supported for categories and expenses

B. Instructions:

1. In order to start the app, user name is required. This is used to save the data.

2. If this is unused name and no file is generated for saved data, then the user has to add categories
3. Once at least one category is added, the user can add expenses:
4. On the left side there 3 requirements: Category, Amount (must be positive number) 
 and a date (selected from the calendar, the default is today's date). Then User has to click "Add Expense"
5. For editing or deleting the user has to select the expense from the top table and then: -change the 3 fields 
and click "Edit Expense" OR simply click "Del Expense" respectively
6. By clicking "Exit" user exits the program without saving the data
7. By clicking "Save updates" user saves the data. If the user is new, it creates a new file OR overwrites existing one
8. By clicking "Report" a new pop up window appears. User can select the report criteria. Which categories to be
included, what time period is to be takes and whether the report is for historical spend review or category 
redistribution overview

Others:

9. By clicking "Edit Category" and pop up window appears. The user has to select the category and provide a new name, 
it can be updated by clicking "Edit". The user can close the window by clicking "Back"
10. By clicking "Del Category" and pop up window appears. The user has to select the category (one or more) and delete 
it (them) by clicking "Remove selected". The user can close the window by clicking "Back".
Please note that by clicking "Remove selected" and if categories is removed, it is substituted by "N/A" for any expenses 
related to it
11. By "Set today" the user is changing the date to today.

