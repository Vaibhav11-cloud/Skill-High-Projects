import tkinter as tk
from tkinter import filedialog, messagebox
import os, hashlib, time
from crypto_utils import encrypt_file, decrypt_file
from key_manager import generate_key

# Simple in-memory user database (for demo)
users_db = {}

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🔐 Secure File Tool - Login")
        self.geometry("400x250")
        self.configure(bg="#2c3e50")

        tk.Label(self, text="Login / Create Account",
                 font=("Arial", 16, "bold"), fg="white", bg="#2c3e50").pack(pady=15)

        tk.Label(self, text="Username:", fg="white", bg="#2c3e50").pack()
        self.username_entry = tk.Entry(self, width=30)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Password:", fg="white", bg="#2c3e50").pack()
        self.password_entry = tk.Entry(self, show="*", width=30)
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Login", width=12, bg="#2980b9", fg="white",
                  command=self.login).pack(pady=5)
        tk.Button(self, text="Create Account", width=12, bg="#27ae60", fg="white",
                  command=self.create_account).pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in users_db and users_db[username] == password:
            messagebox.showinfo("Success", "Login successful!")
            self.destroy()
            app = SecureFileApp(username)
            app.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    def create_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in users_db:
            messagebox.showerror("Error", "Username already exists!")
        elif not username or not password:
            messagebox.showerror("Error", "Username and password required!")
        else:
            users_db[username] = password
            messagebox.showinfo("Success", "Account created! You can now log in.")

class SecureFileApp(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.title(f"🔐 Secure File Encryption Tool - Welcome {username}")
        self.geometry("700x500")
        self.configure(bg="#2c3e50")

        # Title
        tk.Label(self, text="Secure File Encryption & Decryption",
                 font=("Arial", 16, "bold"), fg="white", bg="#2c3e50").pack(pady=15)

        # Password Frame
        pass_frame = tk.Frame(self, bg="#34495e")
        pass_frame.pack(pady=10, fill="x", padx=20)
        tk.Label(pass_frame, text="Enter Encryption Password:", font=("Arial", 12),
                 fg="white", bg="#34495e").pack(side="left", padx=10)
        self.password_entry = tk.Entry(pass_frame, show="*", width=30)
        self.password_entry.pack(side="left", padx=10)

        # Buttons
        btn_frame = tk.Frame(self, bg="#2c3e50")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Encrypt File", width=15,
                  bg="#27ae60", fg="white", font=("Arial", 12, "bold"),
                  command=self.encrypt_action).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Decrypt File", width=15,
                  bg="#2980b9", fg="white", font=("Arial", 12, "bold"),
                  command=self.decrypt_action).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="Exit", width=15,
                  bg="#c0392b", fg="white", font=("Arial", 12, "bold"),
                  command=self.quit).grid(row=0, column=2, padx=10)

        # File Details Panel
        details_frame = tk.LabelFrame(self, text="File Details",
                                      font=("Arial", 12, "bold"),
                                      fg="white", bg="#34495e", labelanchor="n")
        details_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.details_text = tk.Text(details_frame, height=12, wrap="word",
                                    bg="#1c2833", fg="white", font=("Consolas", 11))
        self.details_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Status
        self.status_label = tk.Label(self, text="Ready", font=("Arial", 12),
                                     fg="white", bg="#2c3e50")
        self.status_label.pack(pady=10)

    def show_file_details(self, file_path, status="Unknown"):
        size_bytes = os.path.getsize(file_path)
        size_kb = round(size_bytes / 1024, 2)
        size_mb = round(size_bytes / (1024*1024), 2)

        created = time.ctime(os.path.getctime(file_path))
        modified = time.ctime(os.path.getmtime(file_path))
        accessed = time.ctime(os.path.getatime(file_path))

        sha256_hash = hashlib.sha256()
        md5_hash = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
                md5_hash.update(chunk)

        details = f"""
File: {os.path.basename(file_path)}
Path: {file_path}
Type: {os.path.splitext(file_path)[1]}
Size: {size_bytes} bytes ({size_kb} KB / {size_mb} MB)

Created: {created}
Modified: {modified}
Accessed: {accessed}

SHA-256 Hash: {sha256_hash.hexdigest()}
MD5 Hash: {md5_hash.hexdigest()}

Status: {status}
"""
        self.details_text.delete("1.0", tk.END)
        self.details_text.insert(tk.END, details)

    def encrypt_action(self):
        file_path = filedialog.askopenfilename()
        if not file_path: return
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Password required!")
            return
        key = generate_key(password)
        encrypt_file(file_path, key)
        enc_file = file_path + ".enc"
        self.show_file_details(enc_file, status="Encrypted")
        self.status_label.config(text="✅ File encrypted successfully!")

    def decrypt_action(self):
        file_path = filedialog.askopenfilename()
        if not file_path: return
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Password required!")
            return
        key = generate_key(password)
        decrypt_file(file_path, key)
        original_file = file_path.replace(".enc", "")
        self.show_file_details(original_file, status="Decrypted")
        self.status_label.config(text="✅ File decrypted successfully!")

if __name__ == "__main__":
    login = LoginWindow()
    login.mainloop()
