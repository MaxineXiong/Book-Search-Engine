from tkinter import *
import customtkinter
import sqlite3
import sql_queries
import pandas as pd



class BookSearchEngine:
    """A class to encapsulate the functionality of a desktop application
    designed for searching, viewing, adding, updating, and deleting book
    records using a GUI. It interfaces with an SQLite database to perform
    data operations, providing users with a visually appealing and
    functional platform for managing their book collection.
    """

    def __init__(self):
        """Initializes an instance of the BookSearchEngine class"""
        # Establish a connection to the SQLite database located ...
        # ...at './assets/books.db'
        self.conn = sqlite3.connect(database="./assets/books.db")
        # Create a cursor object from the database connection to ...
        # ...execute SQL commands
        self.cur = self.conn.cursor()
        # Execute the SQL command to create the 'books' table if it ...
        # ...does not already exist
        self.cur.execute(sql_queries.CREATE_TABLE)
        # Assign None to selected_row as its default value
        self.selected_row = None


    def reset(self):
        """Method to reset the book database to a predefined state. It clears
        all existing records in the 'books' table and then populates it with
        the data from the CSV file.
        """
        # Execute the SQL command to delete all records in ...
        # ...the 'books' table
        self.cur.execute(sql_queries.TRUNCATE_TABLE)
        # Read book data from the CSV file into a pandas DataFrame
        books_df = pd.read_csv("./assets/books.csv")
        # Iterate over each row in the DataFrame and insert it into ...
        # ...the 'books' table
        for row_id in range(len(books_df)):
            row = books_df.loc[row_id]
            self.cur.execute(sql_queries.INSERT_RECORD,(row["title"],
                                                        row["author"],
                                                        row["rating"],
                                                        row["isbn"]))


    def view_all_records(self):
        """Method to retrieve and display all book records from the database
        in the GUI list box.
        """
        # Clear the list box
        self.clear_list_box()
        # Execute the SQL command to query all book records available ...
        # ...in the database
        self.cur.execute(sql_queries.VIEW_RECORDS)
        # Retrieve the records from the query result
        records = self.cur.fetchall()
        # Iterate over each record to insert them into the list box
        for record in records:
            self.list_box.insert(END, record)


    def search_records(self):
        """Method to search the book records in the database based on the
        user input in the GUI entry fields.
        The search is dynamic, allowing for partial and case-insensitive
        matches.
        """
        # Clear the list box to prepare for search results
        self.clear_list_box()

        # Retrieve user input values from GUI entry fields
        title = self.title.get()
        author = self.author.get()
        rating = self.rating.get()
        isbn = self.isbn.get()

        # Initiate empty lists for SQL query conditions and ...
        # ...corresponding values
        list_entry_values = []
        list_conditions = []

        # Append the SQL query condition and value for Title to ...
        # ...corresponding lists if the title entry field is not empty
        if title.strip():
            list_conditions.append("LOWER(title) LIKE ?")
            list_entry_values.append(f"%{title}%")

        # Append the SQL query condition and value for Author to ...
        # ...corresponding lists if the author entry field is not empty
        if author.strip():
            list_conditions.append("LOWER(author) LIKE ?")
            list_entry_values.append(f"%{author}%")

        # Append the SQL query condition and value for Rating to ...
        # ...corresponding lists if the rating entry field is not empty
        if rating.strip():
            list_conditions.append("rating = ?")
            list_entry_values.append(rating)

        # Append the SQL query condition and value for ISBN to ...
        # ...corresponding lists if the isbn entry field is not empty
        if isbn.strip():
            list_conditions.append("isbn LIKE ?")
            list_entry_values.append(f"%{isbn}%")

        # Check if there are any conditions set
        if list_entry_values:
            # If so, form the full SQL query using the conditions
            query = "SELECT * FROM books WHERE " \
                    + " AND ".join(list_conditions)
            # Convert the list of entry values to tuple
            tuple_entry_values = tuple(list_entry_values)
            # Execute the SQL command to search the book records ...
            # ...in the database that match the user input
            self.cur.execute(query, tuple_entry_values)
            # Retrieve the records from the query result
            records = self.cur.fetchall()
            # Iterate over each record to insert them into the list box
            for record in records:
                self.list_box.insert(END, record)


    def add_record(self):
        """Method to add a new book record to the database using the
        data entered by the user in the GUI input fields.
        """
        # Collect the data from entry fields
        new_record = (
            self.title.get(),
            self.author.get(),
            self.rating.get(),
            self.isbn.get(),
        )
        # Execute the SQL command to add a new record to the database
        self.cur.execute(sql_queries.INSERT_RECORD,new_record)
        # Clear the list box
        self.clear_list_box()
        # Display confirmation message and details of the added record in ...
        # ...the list box
        self.list_box.insert(
            END,
            "The following record has successfully been added:",
        )
        self.list_box.insert(END, new_record)
        # Disable the list box to prevent further interactions
        self.list_box.config(state=DISABLED)


    def update_record(self):
        """Method to update the currently selected book record in the
        database with the new data entered by the user in the GUI input
        fields.
        """
        # Check if any item in the list box has been selected
        if self.selected_row is not None:
            # Collect updated data from input fields
            updated_record = [
                self.title.get(),
                self.author.get(),
                self.rating.get(),
                self.isbn.get(),
            ]
            # Execute the SQL command to update the selected record ...
            # ...in the database with the new data
            self.cur.execute(
                sql_queries.UPDATE_RECORD,
                tuple(updated_record + [self.selected_row[0]]),
            )
            # Clear the list box
            self.list_box.delete(0, END)
            # Display confirmation message and details of the updated ...
            # ...record in the list box
            self.list_box.insert(
                END,
                "The following record has been updated:",
            )
            self.list_box.insert(
                END,
                tuple([self.selected_row[0]] + updated_record),
            )
            # Reset the selected_row variable to the default None
            self.selected_row = None
            # Disable the list box to prevent further interactions
            self.list_box.config(state=DISABLED)


    def delete_record(self):
        """Method to delete the currently selected book record from
        the database and updates the GUI to reflect the change.
        """
        # Check if any item in the list box has been selected
        if self.selected_row:
            # Execute the SQL command to delete the selected record ...
            # ...from the database
            self.cur.execute(
                sql_queries.DELETE_RECORD,(self.selected_row[0],))
            # Clear the list box to remove any existing data
            self.list_box.delete(0, END)
            # Inform the user which record was deleted by displaying ...
            # ...the record details in the list box
            self.list_box.insert(
                END,
                "The following record has been deleted:",
            )
            self.list_box.insert(END, self.selected_row)
            # Reset the selected_row variable to the default None
            self.selected_row = None
            # Disable the list box to prevent further interactions
            self.list_box.config(state=DISABLED)


    def clear(self):
        """Method to clear both the list box and all entry fields
        in the GUI.
        """
        # Clear all entry fields in the GUI
        self.clear_all_entries()
        # Clear all items in the list box and reset its state ...
        # ...back to NORMAL
        self.clear_list_box()


    def get_selected_row(self, event):
        """Event method to handle the selection of a row in the list
        box component. When a row is selected, this method is triggered
        to update the entry fields with the data from the selected row
        to allow viewing or updating.
        """
        # Check if any item in the list box has been selected
        if self.list_box.curselection():
            # Retrieve the index of the currently selected item ...
            # ...in the list box
            selected_index = self.list_box.curselection()[0]
            # Retrieve the data tuple for the selected item through ...
            # ...its index
            self.selected_row = self.list_box.get(selected_index)
            # Clear all entry values
            self.clear_all_entries()
            # Input data from the selected row into each corresponding ...
            # ...entry field
            self.title_entry.insert(END, self.selected_row[1])
            self.author_entry.insert(END, self.selected_row[2])
            self.rating_entry.insert(END, self.selected_row[3])
            self.ISBN_entry.insert(END, self.selected_row[4])


    def clear_list_box(self):
        """Method to clear all the contents of the list box and reset its state
        to NORMAL.
        """
        # Reset the state of list box to NORMAL to ensure the items ...
        # ...can be selected
        self.list_box.config(state=NORMAL)
        # Clear all items from the list box
        self.list_box.delete(0, END)
        # Reset the selected_row to the default None
        self.selected_row = None


    def clear_all_entries(self):
        """Method to clear all the entry fields."""
        # Clear the title, author, rating and isbn entry fields
        self.title_entry.delete(0, END)
        self.author_entry.delete(0, END)
        self.rating_entry.delete(0, END)
        self.ISBN_entry.delete(0, END)


    def run(self):
        """Method to run the main GUI for the Book Search Engine application.
        It sets up the interface window, labels, entry fields, list box,
        scrollbars, and buttons for user interaction, and configures all
        visual elements using the customtkinter library and binds functions
        to buttons and other interactive components.
        """
        # Create a new window using the CTk class from the customtkinter ...
        # ...module
        window = customtkinter.CTk(fg_color="#2B2D31")
        # Set the title of the window
        window.title("Book Search Engine")
        # Set the size of the window
        window.geometry("700x610")
        # Set the window icon
        window.iconbitmap("./assets/books.ico")
        # Set dark mode
        customtkinter.set_appearance_mode("dark")
        # Set default color theme
        customtkinter.set_default_color_theme("blue")

        # Create a frame to hold entry fields within the main window
        frame_entries = customtkinter.CTkFrame(master=window,
                                               fg_color="#2B2D31")
        # Position the frame on the window
        frame_entries.pack(pady=30)

        # Create a label for the title entry field
        title_label = customtkinter.CTkLabel(
            master=frame_entries,
            text="Title",
            font=("sans-serif", 14),
            text_color="#CCCCCC",
        )
        # Position the label inside the frame and align it to the right
        title_label.grid(row=0, column=0, padx=10, sticky=E)

        # Create a StringVar object to store the Title input text
        self.title = StringVar()
        # Create an entry field for title with custom styling
        self.title_entry = customtkinter.CTkEntry(
            master=frame_entries,
            textvariable=self.title,
            fg_color="#313338",
            text_color="#BABCBE",
            width=250,
            height=40,
            border_width=1,
        )
        # Position the entry appropriately inside the frame
        self.title_entry.grid(row=0, column=1, padx=10, pady=10)

        # Create a label for the author entry field
        author_label = customtkinter.CTkLabel(
            master=frame_entries,
            text="Author",
            font=("sans-serif", 14),
            text_color="#CCCCCC",
        )
        # Position the label inside the frame and align it to the right
        author_label.grid(row=0, column=2, padx=10, sticky=E)

        # Create a StringVar object to store the Author input text
        self.author = StringVar()
        # Create an entry field for author with custom styling
        self.author_entry = customtkinter.CTkEntry(
            master=frame_entries,
            textvariable=self.author,
            fg_color="#313338",
            text_color="#BABCBE",
            width=250,
            height=40,
            border_width=1,
        )
        # Position the entry appropriately inside the frame
        self.author_entry.grid(row=0, column=3, padx=10, pady=10)

        # Create a label for the rating entry field
        rating_label = customtkinter.CTkLabel(
            master=frame_entries,
            text="Rating",
            font=("sans-serif", 14),
            text_color="#CCCCCC",
        )
        # Position the label inside the frame and align it to the right
        rating_label.grid(row=1, column=0, padx=10, sticky=E)

        # Create a StringVar object to store the Rating input text
        self.rating = StringVar()
        # Create an entry field for rating with custom styling
        self.rating_entry = customtkinter.CTkEntry(
            master=frame_entries,
            textvariable=self.rating,
            fg_color="#313338",
            text_color="#BABCBE",
            width=250,
            height=50,
            border_width=1,
        )
        # Position the entry appropriately inside the frame
        self.rating_entry.grid(row=1, column=1, padx=10, pady=10)

        # Create a label for the isbn entry field
        ISBN_label = customtkinter.CTkLabel(
            master=frame_entries,
            text="ISBN",
            font=("sans-serif", 14),
            text_color="#CCCCCC",
        )
        # Position the label inside the frame and align it to the right
        ISBN_label.grid(row=1, column=2, padx=10, sticky=E)

        # Create a StringVar object to store the ISBN input text
        self.isbn = StringVar()
        # Create an entry field for ISBN with custom styling
        self.ISBN_entry = customtkinter.CTkEntry(
            master=frame_entries,
            textvariable=self.isbn,
            fg_color="#313338",
            text_color="#BABCBE",
            width=250,
            height=50,
            border_width=1,
        )
        # Position the entry appropriately inside the frame
        self.ISBN_entry.grid(row=1, column=3, padx=10, pady=10)

        # Create a second frame for managing the data display and buttons
        frame_data_mgmt = customtkinter.CTkFrame(master=window,
                                                 fg_color="#2B2D31")
        # Position the frame below the frame_entries
        frame_data_mgmt.pack()

        # Create a list box for displaying book records, with custom styling
        self.list_box = Listbox(
            master=frame_data_mgmt,
            bg="#313338",
            width=64,
            height=23,
            bd=1,
            font=("sans-serif", 12),
            fg="#BABCBE",
            relief="flat",
            selectbackground="#5865f2",
        )
        # Position the list box inside the second frame
        self.list_box.grid(row=0, column=0, rowspan=6)

        # Create a horizontal scrollbar for the list box
        x_scrollbar = customtkinter.CTkScrollbar(
            master=frame_data_mgmt,
            orientation="horizontal",
            command=self.list_box.xview,
        )
        # Position the horizontal scrollbar to the bottom of the list box
        x_scrollbar.grid(row=7, column=0, sticky=W + E + N)
        # Create a vertical scrollbar for the list box
        y_scrollbar = customtkinter.CTkScrollbar(
            master=frame_data_mgmt,
            orientation="vertical",
            command=self.list_box.yview,
        )
        # Position the vertical scrollbar to the right of the list box
        y_scrollbar.grid(row=0, column=1, rowspan=6, sticky=N + S + W)
        # Configure the list box to link to the horizontal and vertical ...
        # ...scrollbars
        self.list_box.configure(
            xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set
        )

        # Bind the list box selection change event to the ...
        # ...get_selected_row method
        self.list_box.bind("<<ListboxSelect>>", self.get_selected_row)

        # Set up a button that displays all records in the list box
        view_all_button = customtkinter.CTkButton(
            master=frame_data_mgmt,
            text="View All",
            fg_color="#5865f2",
            hover_color="#2133ee",
            height=40,
            command=self.view_all_records,
        )
        # Position the button appropriately inside the second frame
        view_all_button.grid(row=0, column=2, padx=10)

        # Set up a button that searches for the records meeting attribute ...
        # ...conditions
        search_button = customtkinter.CTkButton(
            master=frame_data_mgmt,
            text="Search",
            fg_color="#5865f2",
            hover_color="#2133ee",
            height=40,
            command=self.search_records,
        )
        # Position the button appropriately inside the second frame
        search_button.grid(row=1, column=2, padx=10)

        # Set up a button that adds a new record to the database
        add_button = customtkinter.CTkButton(
            master=frame_data_mgmt,
            text="Add",
            fg_color="#5865f2",
            hover_color="#2133ee",
            height=40,
            command=self.add_record,
        )
        # Position the button appropriately inside the second frame
        add_button.grid(row=2, column=2, padx=10)

        # Set up a button that updates an existing record
        update_button = customtkinter.CTkButton(
            master=frame_data_mgmt,
            text="Update",
            fg_color="#5865f2",
            hover_color="#2133ee",
            height=40,
            command=self.update_record,
        )
        # Position the button appropriately inside the second frame
        update_button.grid(row=3, column=2, padx=10)

        # Set up a button that deletes a record from the database
        delete_button = customtkinter.CTkButton(
            master=frame_data_mgmt,
            text="Delete",
            fg_color="#5865f2",
            hover_color="#2133ee",
            height=40,
            command=self.delete_record,
        )
        # Position the button appropriately inside the second frame
        delete_button.grid(row=4, column=2, padx=10)

        # Set up a button that clears all the entry values and displayed ...
        # ...data on GUI
        clear_button = customtkinter.CTkButton(
            master=frame_data_mgmt,
            text="Clear",
            fg_color="#5865f2",
            hover_color="#2133ee",
            height=40,
            command=self.clear,
        )
        # Position the button appropriately inside the second frame
        clear_button.grid(row=5, column=2, padx=10)

        # Start the tkinter event loop, which keeps the application ...
        # ...running and handles user interactions
        window.mainloop()

        # Close the database connection when the application is closed
        self.conn.close()



# Check if this script is being run directly (and not imported as a module)
if __name__ == "__main__":
    # Instantiate the book search engine application
    engine = BookSearchEngine()
    # Reset the database to a default state with initial data
    engine.reset()
    # Start the GUI and the application's event loop
    engine.run()
