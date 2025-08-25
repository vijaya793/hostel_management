import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Colors
BG_COLOR = "#f0f8ff"  # Alice Blue
BTN_COLOR = "#4682b4"  # Steel Blue
BTN_TEXT = "white"
FONT = ("Arial", 16, "bold")

# Dummy credentials for authentication
STUDENT_CREDENTIALS = {"student": "password123"}
ADMIN_CREDENTIALS = {"admin": "admin123"}

def student_dashboard():
    student_win = tk.Toplevel()
    student_win.title("Student Dashboard")
    student_win.geometry("1300x500+200+140")
    student_win.configure(bg=BG_COLOR)
    
    tk.Label(student_win, text="Welcome to Student Dashboard", font=FONT, bg=BG_COLOR).pack(pady=20)
    tk.Button(student_win, text="Logout", font=("Arial", 14), bg=BTN_COLOR, fg=BTN_TEXT, command=lambda: logout(student_win)).pack(pady=20)

def admin_dashboard():
    admin_win = tk.Toplevel()
    admin_win.title("Admin Dashboard")
    admin_win.geometry("1300x500+200+140")
    admin_win.configure(bg=BG_COLOR)
    
    tk.Label(admin_win, text="Welcome to Admin Dashboard", font=FONT, bg=BG_COLOR).pack(pady=20)
    tk.Button(admin_win, text="Logout", font=("Arial", 14), bg=BTN_COLOR, fg=BTN_TEXT, command=lambda: logout(admin_win)).pack(pady=20)

def logout(window):
    window.destroy()
    root.deiconify()

def authenticate(user_type, username, password, login_win):
    if user_type == "student" and STUDENT_CREDENTIALS.get(username) == password:
        login_win.destroy()
        student_dashboard()
    elif user_type == "admin" and ADMIN_CREDENTIALS.get(username) == password:
        login_win.destroy()
        admin_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

def login_page(user_type):
    login_win = tk.Toplevel()
    login_win.title(f"{user_type.capitalize()} Login")
    login_win.geometry("400x300+600+250")
    login_win.configure(bg=BG_COLOR)
    
    tk.Label(login_win, text=f"{user_type.capitalize()} Login", font=FONT, bg=BG_COLOR).pack(pady=20)
    tk.Label(login_win, text="Username:", font=("Arial", 14), bg=BG_COLOR).pack()
    username_entry = tk.Entry(login_win, font=("Arial", 14))
    username_entry.pack(pady=5)
    
    tk.Label(login_win, text="Password:", font=("Arial", 14), bg=BG_COLOR).pack()
    password_entry = tk.Entry(login_win, font=("Arial", 14), show="*")
    password_entry.pack(pady=5)
    
    tk.Button(login_win, text="Login", font=("Arial", 14), bg=BTN_COLOR, fg=BTN_TEXT,
              command=lambda: authenticate(user_type, username_entry.get(), password_entry.get(), login_win)).pack(pady=20)

def student_login():
    login_page("student")

def admin_login():
    login_page("admin")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("College Management System")
    root.geometry('1300x500+200+140')
    root.configure(bg=BG_COLOR)
    
    try:
        img = Image.open("download.png")
        img = img.resize((100, 100), Image.LANCZOS)
        logo = ImageTk.PhotoImage(img)
        logo_label = tk.Label(root, image=logo, bg=BG_COLOR)
        logo_label.pack(pady=10)
    except Exception:
        tk.Label(root, text="[Logo Not Found]", font=("Arial", 12), bg=BG_COLOR, fg="red").pack(pady=10)
    
    tk.Label(root, text="Shri Vishnu Engineering College for Women, Bhimavaram", font=("Arial", 20, "bold"), bg=BG_COLOR, fg="darkblue").pack(pady=10)
    
    tk.Button(root, text="Student Login", command=student_login, font=FONT, bg=BTN_COLOR, fg=BTN_TEXT, width=20, height=2).pack(pady=15)
    tk.Button(root, text="Admin Login", command=admin_login, font=FONT, bg=BTN_COLOR, fg=BTN_TEXT, width=20, height=2).pack(pady=15)
    
    root.mainloop()
