import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from cryptography.fernet import Fernet

# Constants for file paths
SQL_FILE_PATH = "####"  # Set your full path to the encrypted SQL file
KEY_FILE_PATH = "####"  # Key file path(Make it like: ~/entry-folder/key/key.key; it will generate key for you)

# Global Variables
entries = []

def generate_key():
    """Generate a new encryption key and save it to a file."""
    key = Fernet.generate_key()
    with open(KEY_FILE_PATH, 'wb') as key_file:
        key_file.write(key)

def load_key():
    """Load the encryption key from the key file."""
    if not os.path.exists(KEY_FILE_PATH):
        generate_key()
    with open(KEY_FILE_PATH, 'rb') as key_file:
        return key_file.read()

def encrypt_data(data, key):
    """Encrypt data using the given key."""
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())

def decrypt_data(encrypted_data, key):
    """Decrypt data using the given key."""
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data).decode()

def save_to_encrypted_sql_file(entries, key):
    """Save encrypted entries along with their timestamps to an SQL file."""
    with open(SQL_FILE_PATH, 'wb') as f:
        for entry, timestamp in entries:
            entry_data = f"INSERT INTO entries (data, timestamp) VALUES ('{entry}', '{timestamp}');"
            encrypted_entry = encrypt_data(entry_data, key)
            f.write(encrypted_entry + b'\n')

def read_encrypted_sql_file(key):
    """Read the encrypted SQL file and return the decrypted entries."""
    if not os.path.exists(SQL_FILE_PATH):
        return []

    with open(SQL_FILE_PATH, 'rb') as f:
        encrypted_lines = f.readlines()

    readable_entries = []
    for encrypted_line in encrypted_lines:
        try:
            decrypted_line = decrypt_data(encrypted_line.strip(), key)
            if decrypted_line.startswith("INSERT INTO"):
                values = decrypted_line.split("VALUES")[1].strip().replace("(", "").replace(");", "").replace("'", "").split(",")
                entry = values[0].strip()
                timestamp = values[1].strip()
                readable_entries.append((entry, timestamp))
        except Exception as e:
            print(f"Error decrypting line: {e}")
    return readable_entries

def load_existing_entries():
    """Load existing entries from the encrypted SQL file into the entries list."""
    global entries
    entries = read_encrypted_sql_file(key)

def add_entry_window():
    """Open a new window to add an entry."""
    def save_entry():
        entry_text = entry_input.get("1.0", "end-1c").strip()
        if entry_text:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            entries.append((entry_text, timestamp))
            save_to_encrypted_sql_file(entries, key)
            messagebox.showinfo("Success", "Entry added successfully!")
            add_window.destroy()
        else:
            messagebox.showwarning("Warning", "Entry cannot be empty!")

    add_window = tk.Toplevel()
    add_window.title("Add New Entry")
    add_window.geometry("400x200")

    tk.Label(add_window, text="Enter your entry:").pack(pady=5)
    entry_input = tk.Text(add_window, height=5, width=40)
    entry_input.pack(pady=5)

    tk.Button(add_window, text="Save Entry", command=save_entry).pack(pady=5)

def view_entries_window():
    """Open a new window to view all entries."""
    readable_entries = read_encrypted_sql_file(key)

    view_window = tk.Toplevel()
    view_window.title("View Entries")
    view_window.geometry("500x400")

    text_area = tk.Text(view_window, wrap="word")
    text_area.pack(expand=True, fill="both")

    for entry, timestamp in readable_entries:
        text_area.insert("end", f" - {entry} (Recorded at: {timestamp})\n")

    text_area.config(state="disabled")

def delete_entries_window():
    """Open a new window to delete specific entries."""
    global entries
    readable_entries = read_encrypted_sql_file(key)
    
    delete_window = tk.Toplevel()
    delete_window.title("Delete Entries")
    delete_window.geometry("500x400")

    frame = tk.Frame(delete_window)
    frame.pack(expand=True, fill="both")

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, selectmode=tk.SINGLE)
    listbox.pack(expand=True, fill="both")
    
    scrollbar.config(command=listbox.yview)

    # Display each entry with delete button
    for idx, (entry, timestamp) in enumerate(readable_entries):
        listbox.insert("end", f" {idx + 1}. {entry} (Recorded at: {timestamp})")

    def delete_selected_entry():
        selected_index = listbox.curselection()
        if selected_index:
            index = selected_index[0]
            # Remove from entries list
            del entries[index]
            save_to_encrypted_sql_file(entries, key)  # Save the updated list
            messagebox.showinfo("Success", "Entry deleted successfully!")
            delete_window.destroy()
        else:
            messagebox.showwarning("Warning", "Please select an entry to delete.")

    tk.Button(delete_window, text="Delete Selected Entry", command=delete_selected_entry).pack(pady=10)

def main():
    global key
    key = load_key()
    load_existing_entries()

    root = tk.Tk()
    root.title("Entry Manager")
    root.geometry("300x250")

    tk.Label(root, text="SQL Entry Manager", font=("Helvetica", 16)).pack(pady=10)

    tk.Button(root, text="Add Entry", width=20, command=add_entry_window).pack(pady=5)
    tk.Button(root, text="View Entries", width=20, command=view_entries_window).pack(pady=5)
    tk.Button(root, text="Delete Entry", width=20, command=delete_entries_window).pack(pady=5)
    tk.Button(root, text="Exit", width=20, command=root.quit).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
