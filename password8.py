import tkinter as tk
from tkinter import messagebox
import re
import math
import random, string

# ---------------- Password Strength Functions ----------------
def calculate_entropy(password):
    charset = 0
    if re.search(r'[a-z]', password): charset += 26
    if re.search(r'[A-Z]', password): charset += 26
    if re.search(r'[0-9]', password): charset += 10
    if re.search(r'[^A-Za-z0-9]', password): charset += 32
    entropy = math.log2(charset ** len(password)) if charset else 0
    return entropy

def check_strength():
    pwd = entry.get()
    if not pwd:
        messagebox.showwarning("Input Error", "Please enter a password!")
        return
    
    entropy = calculate_entropy(pwd)
    has_upper = bool(re.search(r'[A-Z]', pwd))
    has_lower = bool(re.search(r'[a-z]', pwd))
    has_digit = bool(re.search(r'[0-9]', pwd))
    has_special = bool(re.search(r'[^A-Za-z0-9]', pwd))
    length_ok = len(pwd) >= 8
    
    strength = "Weak"
    color = "red"
    if entropy > 40 and length_ok and has_upper and has_lower and has_digit:
        strength = "Moderate"
        color = "orange"
    if entropy > 60 and length_ok and has_upper and has_lower and has_digit and has_special:
        strength = "Strong"
        color = "green"
    
    result_label.config(
        text=f"Entropy: {entropy:.2f} bits\nStrength: {strength}",
        fg=color
    )

def suggest_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    strong_pwd = ''.join(random.choice(chars) for _ in range(14))
    messagebox.showinfo("Suggested Strong Password", f"Try this:\n{strong_pwd}")

# ---------------- Login Page ----------------
def login():
    username = user_entry.get()
    password = pass_entry.get()
    if username == "admin" and password == "admin123":
        messagebox.showinfo("Login Success", "Welcome to the Password Tool!")
        show_main_page()
    else:
        messagebox.showerror("Login Failed", "Invalid credentials!")

def toggle_password():
    if pass_entry.cget("show") == "*":
        pass_entry.config(show="")
        toggle_btn.config(text="🙈 Hide")
    else:
        pass_entry.config(show="*")
        toggle_btn.config(text="👁 Show")

def create_account():
    messagebox.showinfo("Create Account", "Account creation page (demo).\nHere you could add fields to register new users.")

# ---------------- Page Switching ----------------
def show_login_page():
    clear_frame()
    tk.Label(root, text="🔐 Login Page", font=("Arial", 22, "bold"), fg="white", bg="#2C3E50").pack(pady=20)
    
    tk.Label(root, text="Username:", font=("Arial", 16), fg="white", bg="#2C3E50").pack(pady=5)
    global user_entry
    user_entry = tk.Entry(root, width=30, font=("Arial", 16))
    user_entry.pack(pady=5)
    
    tk.Label(root, text="Password:", font=("Arial", 16), fg="white", bg="#2C3E50").pack(pady=5)
    global pass_entry, toggle_btn
    pass_entry = tk.Entry(root, show="*", width=30, font=("Arial", 16))
    pass_entry.pack(pady=5)
    
    toggle_btn = tk.Button(root, text="👁 Show", command=toggle_password, font=("Arial", 12), bg="#95A5A6", fg="black")
    toggle_btn.pack(pady=5)
    
    tk.Button(root, text="Login", command=login, font=("Arial", 16, "bold"), bg="#1ABC9C", fg="white").pack(pady=10)
    tk.Button(root, text="Create Account", command=create_account, font=("Arial", 16), bg="#9B59B6", fg="white").pack(pady=10)
    tk.Button(root, text="Exit", command=root.quit, font=("Arial", 16), bg="#E74C3C", fg="white").pack(pady=10)

def show_main_page():
    clear_frame()
    tk.Label(root, text="🔧 Password Tools", font=("Arial", 22, "bold"), fg="white", bg="#2C3E50").pack(pady=20)
    
    tk.Button(root, text="Check Password Strength", command=show_strength_checker,
              font=("Arial", 16), bg="#3498DB", fg="white", width=25).pack(pady=10)
    tk.Button(root, text="Suggest Strong Password", command=suggest_password,
              font=("Arial", 16), bg="#9B59B6", fg="white", width=25).pack(pady=10)
    tk.Button(root, text="Password Policy", command=show_policy_page,
              font=("Arial", 16), bg="#F1C40F", fg="black", width=25).pack(pady=10)
    tk.Button(root, text="Logout", command=show_login_page,
              font=("Arial", 16), bg="#E67E22", fg="white", width=25).pack(pady=10)
    tk.Button(root, text="Exit", command=root.quit,
              font=("Arial", 16), bg="#E74C3C", fg="white", width=25).pack(pady=10)

def show_strength_checker():
    clear_frame()
    tk.Label(root, text="🔑 Password Strength Checker", font=("Arial", 22, "bold"), fg="white", bg="#2C3E50").pack(pady=20)
    
    tk.Label(root, text="Enter Password:", font=("Arial", 16), fg="white", bg="#2C3E50").pack(pady=5)
    global entry
    entry = tk.Entry(root, show="*", width=30, font=("Arial", 16))
    entry.pack(pady=5)
    
    tk.Button(root, text="Check Strength", command=check_strength,
              font=("Arial", 16, "bold"), bg="#1ABC9C", fg="white", width=20).pack(pady=15)
    
    global result_label
    result_label = tk.Label(root, text="", font=("Arial", 16, "bold"), bg="#2C3E50")
    result_label.pack(pady=20)
    
    tk.Button(root, text="Back", command=show_main_page,
              font=("Arial", 16), bg="#E67E22", fg="white", width=20).pack(pady=10)

def show_policy_page():
    clear_frame()
    tk.Label(root, text="📜 Password Policy", font=("Arial", 22, "bold"), fg="white", bg="#2C3E50").pack(pady=20)
    
    policy_text = (
        "Strong Password Rules:\n\n"
        "- Minimum length: 8 characters\n"
        "- At least one uppercase letter\n"
        "- At least one lowercase letter\n"
        "- At least one digit\n"
        "- At least one special character (!@#$%^&*)\n"
        "- Avoid common words or sequences\n"
    )
    
    tk.Label(root, text=policy_text, font=("Arial", 16), fg="white", bg="#2C3E50", justify="left").pack(pady=20)
    
    tk.Button(root, text="Back", command=show_main_page,
              font=("Arial", 16), bg="#E67E22", fg="white", width=20).pack(pady=10)

# ---------------- Utility ----------------
def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

# ---------------- Tkinter Setup ----------------
root = tk.Tk()
root.title("Password Security Application")
root.geometry("600x600")
root.configure(bg="#2C3E50")  # Dark stylish background

show_login_page()
root.mainloop()
