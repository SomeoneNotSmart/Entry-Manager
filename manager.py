import os
from datetime import datetime
from cryptography.fernet import Fernet

SQL_FILE_PATH = "path-to-your-sql"
KEY_FILE_PATH = "path/key.key"

def generate_key():
    """Generate a new encryption key and save it to a file."""
    key = Fernet.generate_key()
    with open(KEY_FILE_PATH, 'wb') as key_file:
        key_file.write(key)
    print(f"New encryption key generated and saved to '{KEY_FILE_PATH}'.")

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
            # Prepare and encrypt entry
            entry_data = f"INSERT INTO entries (data, timestamp) VALUES ('{entry}', '{timestamp}');"
            encrypted_entry = encrypt_data(entry_data, key)
            f.write(encrypted_entry + b'\n')

def read_encrypted_sql_file(key):
    """Read the encrypted SQL file and display entries in a readable format."""
    if not os.path.exists(SQL_FILE_PATH):
        print(f"File '{SQL_FILE_PATH}' not found.")
        return

    with open(SQL_FILE_PATH, 'rb') as f:
        encrypted_lines = f.readlines()

    print("\nReadable Entries:")
    for encrypted_line in encrypted_lines:
        # Decrypt and display each line
        try:
            decrypted_line = decrypt_data(encrypted_line.strip(), key)
            if decrypted_line.startswith("INSERT INTO"):
                values = decrypted_line.split("VALUES")[1].strip().replace("(", "").replace(");", "").replace("'", "").split(",")
                entry = values[0].strip()
                timestamp = values[1].strip()
                print(f" - {entry} (Recorded at: {timestamp})")
        except Exception as e:
            print(f"Error decrypting line: {e}")

def main():
    # Load or generate the encryption key
    key = load_key()

    print("Choose an option:")
    print("1. Add new entries")
    print("2. Read and display SQL entries")

    choice = input("> ")
    if choice == '1':
        entries = []
        print("Enter your entries below (type 'quit' to finish):")

        while True:
            user_input = input("> ")
            if user_input.lower() in ['quit', 'exit']:
                break

            # Record the current date and time for each entry
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            entries.append((user_input, timestamp))

        save_to_encrypted_sql_file(entries, key)
        print(f"Entries saved and encrypted to '{SQL_FILE_PATH}'.")

    elif choice == '2':
        read_encrypted_sql_file(key)
    else:
        print("Invalid option. Please choose either '1' or '2'.")
      
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
