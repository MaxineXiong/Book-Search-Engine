# Book Search Engine

[![GitHub](https://badgen.net/badge/icon/GitHub?icon=github&color=black&label)](https://github.com/MaxineXiong)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Made with Python](https://img.shields.io/badge/Python->=3.6-blue?logo=python&logoColor=white)](https://www.python.org)

<br>

## Project Description

The **Book Search Engine** is a desktop application developed in Python using the *Tkinter* and *CustomTkinter* library. It enables users to interact with a local SQLite database to manage and query book information effectively. This application is particularly useful for librarians, bookstore owners, or any book enthusiast who needs to manage a collection of books.

You can check out the application demo video below:

https://github.com/MaxineXiong/Book-Search-Engine/assets/55864839/d8395ef0-4bd2-47c7-8f14-59cb7f76fd9e

<br>

## Features

- **Search Functionality**: Users can search for books based on attributes like ISBN, title, author, and rating.
- **Database Management**: Provides capabilities to **add**, **update**, and **delete** book records in the database.
- **User-friendly Interface**: A simple and intuitive interface built with *Tkinter* and *CustomTkinter* ensures that users can navigate the application easily.

<br>

## Repository Structure

The repository is structured as follows:

```
BookSearchEngine/
├── main.py                     
├── sql_queries.py              
├── assets/                    
│   ├── books.csv              
│   ├── books.db                
│   └── books.ico              
├── requirements.txt           
├── .gitignore                  
├── README.md                   
└── LICENSE                   
```

- **main.py**: This is the core script that initializes the application, sets up the GUI, and handles user interactions and database operations.
- **sql_queries.py**: This file stores all SQL commands used by `main.py`, ensuring a clean separation of database logic from the application logic.
- **assets/**: This directory contains necessary files for the application's operation, including:
    - **books.csv**: Used to initially populate the `books.db` with data, enabling the application to start with a predefined set of book records. This dataset was downloaded from [Kaggle Goodreads-books](https://www.kaggle.com/jealousleopard/goodreadsbooks).
    - **books.db**: The SQLite database file where all book data is stored and managed.
    - **books.ico**: The application icon, enhancing the GUI aesthetic.
- **requirements.txt**: Lists all necessary Python libraries and dependencies required to run the application. These can be installed via the command `pip install -r requirements.txt`.
- **.gitignore**: Specifies which files and directories Git should ignore, helping to keep the repository clean from unnecessary or sensitive files.
- **README.md**: Provides a detailed overview of the repository, including descriptions of its features, usage instructions, and information on how to contribute.
- **LICENSE**: The license file for the project.

<br>

## **Usage**

To run the Book Search Engine program on your local computer, please follow these steps:

1. Clone this repository to your local machine using the following command:
    
    ```
    git clone https://github.com/MaxineXiong/Book-Search-Engine.git
    ```
    
2. Download and install the latest version of [Python](https://www.python.org/downloads/) for your system. Make sure to select the "Add Python to PATH" option during the installation process.
3. Navigate to the project folder using File Explorer, type `cmd` in the address bar at the top of the window, and press Enter. This will open Command Prompt in the project folder.
4. Install the required packages by executing the following command in the Command Prompt:
    
    ```
    pip install -r requirements.txt
    ```
    
5. Now launch the Book Search Engine program by entering the following command in the Command Prompt:
    
    ```
    python main.py
    ```

<br>

## **Contribution**

Contributions to the Book Search Engine are welcome! If you have suggestions to improve the application or add new features, please fork the repository and submit a pull request, or open an issue detailing the changes or additional features you have in mind.

<br>

## License

This project is licensed under the MIT License. See the [LICENSE](https://choosealicense.com/licenses/mit/) file for more details.

<br>

## **Acknowledgements**

Special thanks to the following tools and libraries that have made this project possible:

- [**Tkinter**](https://docs.python.org/3/library/tkinter.html): The standard GUI library for Python, which has been instrumental in building the application's interface.
- [**CustomTkinter**](https://github.com/TomSchimansky/CustomTkinter): An enhanced version of Tkinter that provides additional widgets and themes, which enhanced the aesthetics and functionality of the user interface.
- [**SQLite3**](https://docs.python.org/3/library/sqlite3.html): Integrated within Python, SQLite3 has provided a robust and lightweight database solution for storing and managing book data efficiently.
- [**Pandas**](https://pandas.pydata.org/): This powerful data analysis library has been crucial for handling CSV data manipulation and database initialization.
- [**Python**](https://www.python.org/): The core programming language used to develop this application, celebrated for its readability and rich ecosystem of libraries.
