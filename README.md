# Entry Manager

A simple Python application that allows users to create, view, and delete encrypted entries using a GUI built with `Tkinter`. The entries are stored in an encrypted SQL file, ensuring that only the app can access and manipulate the data. Without an app, SQL file cannot(probably) be read by a human

## Features
- **Add New Entries**: Easily add new entries that also contain a date of addition.
- **View Entries**: View all the encrypted entries in a readable format.
- **Delete Entries**: Select and delete entries from the database.
- **Encrypted Storage**: Entries are stored in an encrypted SQL file, which make data unreadable(maybe).

## Getting Started

### Prerequisites
- Python 3.6 or higher.
- `pip` installed.

### Installation
1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/username/entry-manager.git
    cd encrypted-sql-entry-manager
    ```

2. Install the required dependencies using `pip`:

    ```bash
    pip install -r requirements.txt
    ```


    
### How to Run the Application
1. Open your terminal or command prompt.
2. Navigate to the project directory.
3. Run the following command to start the GUI:

    ```bash
    python entry_manager.py
    ```

### File Paths
- Make the SQL and KEY paths like:

    Windows:
    ```plaintext
    C:/path/to/repo/entries.sql
    C:/path/to/repo/key/key.key
    ```
    Linux/Mac:
    ```plaintext
    /home/path/to/repo/entries.sql
    /home/path/to/repo/key/key.key
    ```


- **Make sure to update the `SQL_FILE_PATH` variable in the script to reflect the actual path of your SQL file.**

### Application Overview
- **Add Entry**: Opens a text box where you can add a new entry.
- **View Entries**: Displays all entries in a read-only format with their timestamps.
- **Delete Entry**: Opens a menu to view and delete specific entries.
- **Exit**: Closes the application

