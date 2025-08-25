from tkinter import Tk, Frame, Label, Entry, Button, Listbox, Scrollbar, messagebox, Toplevel, ttk,Canvas,PhotoImage
from PIL import Image, ImageTk
import mysql.connector
import csv
from tkinter import scrolledtext
from tkinter import END, VERTICAL
import datetime
# Establishing connection to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Lavanya@23',
    database='mydatabase'
)
cursor = conn.cursor()

fonts = ('Calibri', 25, 'bold')
font1 = ('Calibri', 20, 'bold')

class Home:
    def __init__(self, root):
        self.root = root
        self.root.title("Hostel Management")
        self.root.geometry("1250x500+200+140")
        self.root.resizable(True,True)

        
        self.home_frame = Frame(self.root, bg='Alice Blue')
        self.home_frame.pack(fill='both', expand=True)

        # College Logo and Info Frame
        # College Logo and Info Frame (Placed Lower & Centered)
        logo_info_frame = Frame(self.home_frame, bg='Alice Blue')
        logo_info_frame.place(relx=0.5, rely=0.3, anchor="center")  # Center it lower on the frame

        # Vishnu Logo (Left Side)
        logo_image = Image.open("C:\\Users\\lenovo\\Desktop\\HostelVacancy\\vishnu_logo.png")
        logo_image = logo_image.resize((120, 120), Image.LANCZOS)  # Resize to maintain proportions
        self.logo_photo = ImageTk.PhotoImage(logo_image)

        logo_label = Label(logo_info_frame, image=self.logo_photo, bg='Alice Blue')
        logo_label.grid(row=0, column=0, rowspan=2, padx=15, pady=10)  # Add spacing around the image

        # College Name and Additional Info (Right Side)
        college_label = Label(logo_info_frame, text='SHRI VISHNU ENGINEERING COLLEGE FOR WOMEN',
                            font=('Calibri', 22, 'bold'), bg='Alice Blue', fg='Steel Blue')
        college_label.grid(row=0, column=1, sticky='w', padx=10)

        additional_info = Label(logo_info_frame, text='Autonomous | Bhimavaram\nContact: info@svecw.edu.in',
                                font=('Calibri', 14), bg='Alice Blue', fg='Steel Blue')
        additional_info.grid(row=1, column=1, sticky='w', padx=10)


        
        # Login Buttons
        # Button Frame (Centered Below Logo & Text)
        button_frame = Frame(self.home_frame, bg='Alice Blue')
        button_frame.place(relx=0.55, rely=0.6, anchor="center")  # Centered below text

        # Student Login Button
        self.student_login_btn = Button(button_frame, text="Student Login", font=('Calibri', 18, 'bold'),
                                        bg='Steel Blue', fg='White', width=15, command=self.show_student_login)
        self.student_login_btn.pack(pady=10)

        # Admin Login Button
        self.admin_login_btn = Button(button_frame, text="Admin Login", font=('Calibri', 18, 'bold'),
                                    bg='Steel Blue', fg='White', width=15, command=self.show_admin_login)
        self.admin_login_btn.pack(pady=10)


    def show_student_login(self):
        self.home_frame.pack_forget()
        StudentLogin(self.root, cursor, self.home_frame)  # Pass self.home_frame


    def show_admin_login(self):
        self.home_frame.pack_forget()
        AdminLogin(self.root, cursor,self.home_frame)  # Now passing home_frame


from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

class StudentLogin:
    def __init__(self, root, cursor, home_frame):
        self.root = root
        self.cursor = cursor
        self.home_frame = home_frame
        self.saved_username = ""  # To store username when going back

        # Student Login Frame
        self.login_frame = Frame(self.root, bg='Steel Blue')
        self.login_frame.pack(fill='both', expand=True)

        # Centered Content Frame
        login_content_frame = Frame(self.login_frame, bg='Steel Blue')
        login_content_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Load and Display Student Image (Left Side)
        img = Image.open("C:\\Users\\lenovo\\Desktop\\HostelVacancy\\student1.jpg")  # Change image path if needed
        img = img.resize((150, 150), Image.LANCZOS)
        self.student_photo = ImageTk.PhotoImage(img)

        img_label = Label(login_content_frame, image=self.student_photo, bg='Steel Blue')
        img_label.grid(row=0, column=0, rowspan=3, padx=20, pady=10)  # Left side image

        # Login Title (Right Side)
        title_label = Label(login_content_frame, text='Student Login', font=('Calibri', 22, 'bold'),
                            bg='Steel Blue', fg='White')
        title_label.grid(row=0, column=1, sticky='w', padx=10)

        # Username Entry
        self.user_name_entry = Entry(login_content_frame, width=22, font=('Calibri', 16),
                                     bg='white', fg='Steel Blue', relief='solid', bd=2)
        self.user_name_entry.grid(row=1, column=1, pady=5)
        self.user_name_entry.insert(0, "Enter Student Username")
        self.user_name_entry.bind("<FocusIn>", self.clear_placeholder)
        self.user_name_entry.bind("<Return>", lambda event: self.user_pass_entry.focus())  # Move to Password on Enter

        # Password Entry
        self.user_pass_entry = Entry(login_content_frame, width=22, font=('Calibri', 16),
                                     bg='white', fg='Steel Blue', show="*", relief='solid', bd=2)
        self.user_pass_entry.grid(row=2, column=1, pady=5)
        self.user_pass_entry.insert(0, "Enter Password")
        self.user_pass_entry.bind("<FocusIn>", self.clear_placeholder)
        self.user_pass_entry.bind("<Return>", lambda event: self.check_student_login())  # Press Enter to Login

        # Buttons Frame (Below Inputs)
        button_frame = Frame(login_content_frame, bg='Steel Blue')
        button_frame.grid(row=3, column=1, pady=10)

        # Login Button
        self.login_btn = Button(button_frame, text='Login', fg='White', bg='Dark Blue',
                                font=('Calibri', 16, 'bold'), relief='raised', width=10,
                                command=self.check_student_login, cursor='hand2')
        self.login_btn.pack(side="left", padx=5)

        # Back Button
        self.back_btn = Button(button_frame, text='Back', fg='White', bg='Gray',
                               font=('Calibri', 16, 'bold'), relief='raised', width=10,
                               command=self.go_back, cursor='hand2')
        self.back_btn.pack(side="left", padx=5)

    def clear_placeholder(self, event):
        """ Clears placeholder text when the user clicks on an entry field """
        event.widget.delete(0, "end")

    def check_student_login(self):
        """ Checks login credentials """
        name = self.user_name_entry.get().strip()
        password = self.user_pass_entry.get().strip()

        self.cursor.execute("SELECT * FROM student WHERE name = %s AND password = %s", (name, password))
        user = self.cursor.fetchone()

        if user:
            self.saved_username = name  # Save username
            messagebox.showinfo('WELCOME', 'WELCOME STUDENT')
            self.login_frame.pack_forget()
            Dashboard(self.root, admin=False, student_login=self)
        else:
            messagebox.showerror('ERROR', 'Invalid Credentials')

    def go_back(self):
        """ Returns to Home Page (Keeps username) """
        self.login_frame.pack_forget()
        self.home_frame.pack(fill='both', expand=True)

    def clear_credentials(self):
        """ Clears the stored user credentials (For logout) """
        self.saved_username = ""
        self.user_name_entry.delete(0, END)
        self.user_pass_entry.delete(0, END)
        self.user_name_entry.insert(0, "Enter Student Username")
        self.user_pass_entry.insert(0, "Enter Password")




class AdminLogin:
    def __init__(self, root, cursor, home_frame):
        self.root = root
        self.cursor = cursor
        self.home_frame = home_frame

        # Admin Login Frame
        self.login_frame = Frame(self.root, bg='Steel Blue')
        self.login_frame.pack(fill='both', expand=True)

        # Centered Content Frame
        login_content_frame = Frame(self.login_frame, bg='Steel Blue')
        login_content_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Load and Display Admin Image (Left Side)
        img = Image.open("C:\\Users\\lenovo\\Desktop\\HostelVacancy\\admin.jpg")  # Change image path if needed
        img = img.resize((150, 150), Image.LANCZOS)
        self.admin_photo = ImageTk.PhotoImage(img)

        img_label = Label(login_content_frame, image=self.admin_photo, bg='Steel Blue')
        img_label.grid(row=0, column=0, rowspan=3, padx=20, pady=10)  # Left side image

        # Login Title (Right Side)
        title_label = Label(login_content_frame, text='Admin Login', font=('Calibri', 22, 'bold'),
                            bg='Steel Blue', fg='White')
        title_label.grid(row=0, column=1, sticky='w', padx=10)

        # Username Entry
        self.admin_user_name_entry = Entry(login_content_frame, width=22, font=('Calibri', 16),
                                           bg='white', fg='Steel Blue', relief='solid', bd=2)
        self.admin_user_name_entry.grid(row=1, column=1, pady=5)
        self.admin_user_name_entry.insert(0, "Enter Admin Username")
        self.admin_user_name_entry.bind("<FocusIn>", self.clear_placeholder)
        self.admin_user_name_entry.bind("<Return>", lambda event: self.admin_user_pass_entry.focus())  # Move to Password

        # Password Entry
        self.admin_user_pass_entry = Entry(login_content_frame, width=22, font=('Calibri', 16),
                                           bg='white', fg='Steel Blue', show="*", relief='solid', bd=2)
        self.admin_user_pass_entry.grid(row=2, column=1, pady=5)
        self.admin_user_pass_entry.insert(0, "Enter Password")
        self.admin_user_pass_entry.bind("<FocusIn>", self.clear_placeholder)
        self.admin_user_pass_entry.bind("<Return>", lambda event: self.check_admin_login())  # Press Enter to Login

        # Buttons Frame (Below Inputs)
        button_frame = Frame(login_content_frame, bg='Steel Blue')
        button_frame.grid(row=3, column=1, pady=10)

        # Login Button
        self.login_btn = Button(button_frame, text='Login', fg='White', bg='Dark Blue',
                                font=('Calibri', 16, 'bold'), relief='raised', width=10,
                                command=self.check_admin_login, cursor='hand2')
        self.login_btn.pack(side="left", padx=5)

        # Back Button
        self.back_btn = Button(button_frame, text='Back', fg='White', bg='Gray',
                               font=('Calibri', 16, 'bold'), relief='raised', width=10,
                               command=self.go_back, cursor='hand2')
        self.back_btn.pack(side="left", padx=5)

    def clear_placeholder(self, event):
        """ Clears placeholder text when the user clicks on an entry field """
        event.widget.delete(0, "end")

    def check_admin_login(self):
        """ Validates the Admin Login """
        name = self.admin_user_name_entry.get().strip()
        password = self.admin_user_pass_entry.get().strip()

        self.cursor.execute("SELECT password FROM admin1 WHERE name = %s", (name,))
        result = self.cursor.fetchone()

        if result:
            db_password = result[0]
            if password == db_password:
                messagebox.showinfo('WELCOME', 'WELCOME ADMIN')
                self.login_frame.pack_forget()
                Dashboard(self.root, admin=True)  # Load Admin Dashboard
            else:
                messagebox.showerror('WRONG PASSWORD', 'Incorrect Password. Please try again.')
        else:
            messagebox.showerror('ERROR', 'Admin not found.')

    def go_back(self):
        """ Navigates back to the Home Page """
        self.login_frame.pack_forget()
        self.home_frame.pack(fill='both', expand=True) 

class Dashboard:
    def __init__(self, root, admin=False,student_login=None):
        self.root = root
        self.admin = admin
        self.student_login=student_login
        self.clear_frame()  # Now it will work!

        if admin:
            self.root.title('ADMIN DASHBOARD')
            self.admin_dashboard()
        else:
            self.root.title('STUDENT DASHBOARD')
            self.student_dashboard()

    def clear_frame(self):
        """Clears all widgets from the root window before displaying a new frame."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def student_dashboard(self):

        self.clear_frame()  # Clear previous UI elements

        student_dashboard_frame = Frame(self.root, bg='Alice Blue', padx=20, pady=20)
        student_dashboard_frame.pack(fill='both', expand=True)

        # Top Frame for Back and Logout buttons
        top_frame = Frame(student_dashboard_frame, bg='Alice Blue')
        top_frame.pack(fill='x', padx=10, pady=5)

        Button(top_frame, text="Back", command=self.go_back, bg='Gray', fg='white',
            font=('Calibri', 14, 'bold'), width=10, height=1, cursor='hand2').pack(side='left', padx=10)

        Button(top_frame, text="Logout", command=self.logout, bg='Red', fg='white',
            font=('Calibri', 14, 'bold'), width=10, height=1, cursor='hand2').pack(side='right', padx=10)

        # Dashboard Title
        Label(student_dashboard_frame, text="Student Dashboard", font=('Calibri', 24, 'bold'),
            bg='Steel Blue', fg='White', pady=10).pack(pady=10)

        # Search Section
        search_frame = Frame(student_dashboard_frame, bg='Alice Blue')
        search_frame.pack(pady=10)

        Label(search_frame, text="Search Hostel:", font=('Calibri', 14, 'bold'), bg='Alice Blue').pack(side='left', padx=10)

        # Search Entry
        self.search_entry = Entry(search_frame, font=('Calibri', 14), bd=3, relief='solid')
        self.search_entry.pack(side='left', padx=10)
        self.search_entry.bind("<Return>", lambda event: self.perform_search())  # Bind Enter key

        # Search Button (for mouse users)
        Button(search_frame, text="Search", font=('Calibri', 14, 'bold'), bg='Steel Blue', fg='white',
            width=10, cursor='hand2', command=self.perform_search).pack(side='left', padx=10)

        # Search Results Table
        results_frame = Frame(student_dashboard_frame, bg='Alice Blue')
        results_frame.pack(fill='both', expand=True, pady=10)

        self.search_results_tree = ttk.Treeview(results_frame, columns=("Hostel Name", "Room No", "Beds"),
                                                show="headings", height=10)
        self.search_results_tree.pack(side="left", fill="both", expand=True)

        # Define column headings
        self.search_results_tree.heading("Hostel Name", text="Hostel Name")
        self.search_results_tree.heading("Room No", text="Room No")
        self.search_results_tree.heading("Beds", text="Beds")

        # Scrollbar for search results
        scrollbar = Scrollbar(results_frame, orient='vertical', command=self.search_results_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.search_results_tree.configure(yscroll=scrollbar.set)

        # Load all hostel details initially
        self.load_all_hostels()
        def load_all_hostels(self):
            cursor.execute("SELECT hostel_name, room_no, beds FROM hostel")
            all_hostels = cursor.fetchall()

            # Clear previous entries
            self.search_results_tree.delete(*self.search_results_tree.get_children())

            # Insert all hostel data into the table
            for hostel in all_hostels:
                self.search_results_tree.insert("", "end", values=hostel)


    def perform_search(self):
        query = self.search_entry.get().strip()

        # SQL Query: If empty, show all hostels again
        if not query:
            self.load_all_hostels()  # Reload all hostels when search is empty
            return

        cursor.execute("SELECT hostel_name, room_no, beds FROM hostel WHERE hostel_name LIKE %s", ('%' + query + '%',))
        search_results = cursor.fetchall()

        # Clear existing search results
        self.search_results_tree.delete(*self.search_results_tree.get_children())

        # Insert only the matched results
        for result in search_results:
            self.search_results_tree.insert("", "end", values=result)

        # Show a message if no results found
        if not search_results:
            messagebox.showinfo("No Results", "No matching hostel found.")



    def go_back(self):
        """Navigates back to the home page."""
        self.clear_frame()
        Home(self.root)

    def logout(self):
        """Logs out and returns to the login page."""
        self.root.destroy()
        root = Tk()
        root.title('LOGIN')
        root.geometry('1300x500+200+140')
        root.resizable(False, False)
        Home(root)
        root.mainloop()



    def admin_dashboard(self):
        """Creates a unified admin dashboard with all functionalities in a single frame"""
        self.clear_frame()

        self.admin_dashboard_frame = Frame(self.root, bg='Alice Blue', padx=20, pady=20)
        self.admin_dashboard_frame.pack(fill='both', expand=True)

        # Top Row: Logout (Top-Right) & Back (Top-Left)
        top_frame = Frame(self.admin_dashboard_frame, bg='Alice Blue')
        top_frame.pack(fill='x', padx=10, pady=5)

        Button(top_frame, text="Back", command=self.go_back, bg='Gray', fg='white',
               font=('Calibri', 14, 'bold'), width=10, height=1, cursor='hand2').pack(side='left', padx=10)

        Button(top_frame, text="Logout", command=self.logout, bg='Red', fg='white',
               font=('Calibri', 14, 'bold'), width=10, height=1, cursor='hand2').pack(side='right', padx=10)

        # Dashboard Title
        Label(self.admin_dashboard_frame, text="Admin Dashboard", font=('Calibri', 24, 'bold'),
              bg='Steel Blue', fg='White', pady=10).pack(pady=10)

        # Buttons for Admin Actions
        button_frame = Frame(self.admin_dashboard_frame, bg='Alice Blue')
        button_frame.pack(pady=10)

        buttons_data = [
            ("ADD", lambda: self.show_action_frame("Add Hostel Data")),
            ("UPDATE", lambda: self.show_action_frame("Update Hostel Data")),
            ("DELETE", lambda: self.show_action_frame("Delete Hostel Data")),
            ("HISTORY", self.display_history)
        ]

        for button_text, command_func in buttons_data:
            btn = Button(button_frame, text=button_text, command=command_func,
                         bg='Steel Blue', fg='white', font=('Calibri', 14, 'bold'), width=12, height=2,
                         bd=3, relief='raised', cursor='hand2', activebackground='Dark Blue')
            btn.pack(side='left', padx=10, pady=10)

        # Frame for displaying Add, Update, Delete content
        self.action_frame = Frame(self.admin_dashboard_frame, bg='Alice Blue', pady=10)
        self.action_frame.pack(fill='both', expand=True)

    def show_action_frame(self, action_title):
    # Prevent history from triggering this form
        if action_title == "Admin Action History":
            self.display_history()
            return

        # Clear previous content
        for widget in self.action_frame.winfo_children():
            widget.destroy()

        # Action Title
        Label(self.action_frame, text=action_title, font=('Calibri', 18, 'bold'), 
            bg='Steel Blue', fg='White', pady=5).pack(pady=5)

        # Create a frame to align input fields horizontally
        input_frame = Frame(self.action_frame, bg='Alice Blue')
        input_frame.pack(pady=10)

        # Hostel Name
        Label(input_frame, text="Hostel Name:", font=('Calibri', 14, 'bold'), bg='Alice Blue').grid(row=0, column=0, padx=10)
        hostel_entry = Entry(input_frame, font=('Calibri', 14), bd=3, relief='solid')
        hostel_entry.grid(row=1, column=0, padx=10, pady=5)

        # Room No
        Label(input_frame, text="Room No:", font=('Calibri', 14, 'bold'), bg='Alice Blue').grid(row=0, column=1, padx=10)
        room_entry = Entry(input_frame, font=('Calibri', 14), bd=3, relief='solid')
        room_entry.grid(row=1, column=1, padx=10, pady=5)

        # Number of Beds
        Label(input_frame, text="Number of Beds:", font=('Calibri', 14, 'bold'), bg='Alice Blue').grid(row=0, column=2, padx=10)
        beds_entry = Entry(input_frame, font=('Calibri', 14), bd=3, relief='solid')
        beds_entry.grid(row=1, column=2, padx=10, pady=5)

        def execute_action():
            """Executes the correct function and clears fields after submission"""
            if action_title == "Add Hostel Data":
                self.store_data(hostel_entry.get(), room_entry.get(), beds_entry.get())
            elif action_title == "Update Hostel Data":
                self.update_data_in_db(hostel_entry.get(), room_entry.get(), beds_entry.get())
            elif action_title == "Delete Hostel Data":
                self.delete_data_from_db(hostel_entry.get(), room_entry.get(), beds_entry.get())

            # Clear fields after action
            hostel_entry.delete(0, END)
            room_entry.delete(0, END)
            beds_entry.delete(0, END)

        # Confirm Button (placed below)
        Button(self.action_frame, text="Confirm", font=('Calibri', 14, 'bold'), 
            bg='Steel Blue', fg='White', width=12, command=execute_action).pack(pady=15)

    
    def display_history(self):
    

    # Clear previous content
        for widget in self.action_frame.winfo_children():
            widget.destroy()

        Label(self.action_frame, text="Admin Action History", font=('Calibri', 18, 'bold'), 
            bg='Steel Blue', fg='White', pady=5).pack(pady=5)

        # Create a treeview widget (table)
        columns = ("Timestamp", "Action", "Hostel Name", "Room No", "Beds")
        history_tree = ttk.Treeview(self.action_frame, columns=columns, show="headings")
        history_tree.pack(expand=True, fill='both')

        # Define column headings
        for col in columns:
            history_tree.heading(col, text=col)
            history_tree.column(col, anchor='center')

        # Fetch history data from file
        try:
            with open("history_log.txt", "r") as file:
                for line in file.readlines():
                    parts = line.strip().split("|")
                    if len(parts) == 5:
                        history_tree.insert("", "end", values=[p.strip() for p in parts])
        except FileNotFoundError:
            history_tree.insert("", "end", values=["No history records found"] * 5)


    def clear_frame(self):
        """Clears the root window before displaying a new frame"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def go_back(self):
        """Navigates back to the Home Page"""
        self.clear_frame()
        Home(self.root)

    def logout(self):
        """Logs out and returns to the login page"""
        self.root.destroy()
        root = Tk()
        root.title('LOGIN')
        root.geometry('1300x500+200+140')
        root.resizable(False, False)
        Home(root)
        root.mainloop()

    def store_data(self, hostel_name, room_no, beds):
        try:
            cursor.execute("INSERT INTO hostel (hostel_name, room_no, beds) VALUES (%s, %s, %s)",
                           (hostel_name, room_no, beds))
            conn.commit()
            self.log_history("ADD", hostel_name, room_no, beds)
            messagebox.showinfo("Success", "Data added successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error occurred: {err}")

    def update_data_in_db(self, hostel_name, room_no, beds):
        try:
            cursor.execute("UPDATE hostel SET beds = %s WHERE hostel_name = %s AND room_no = %s",
                           (beds, hostel_name, room_no))
            conn.commit()
            self.log_history("UPDATE", hostel_name, room_no, beds)
            messagebox.showinfo("Success", "Data updated successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error occurred: {err}")

    def delete_data_from_db(self, hostel_name, room_no, beds):
        try:
            cursor.execute("DELETE FROM hostel WHERE hostel_name = %s AND room_no = %s AND beds = %s",
                           (hostel_name, room_no, beds))
            conn.commit()
            self.log_history("DELETE", hostel_name, room_no, beds)
            messagebox.showinfo("Success", "Data deleted successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error occurred: {err}")

    def log_history(self, action, hostel_name, room_no, beds):
        """Logs every action performed by the admin into history"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history_entry = f"{timestamp} | {action} | Hostel: {hostel_name} | Room: {room_no} | Beds: {beds}\n"

        with open("history_log.txt", "a") as file:
            file.write(history_entry)

if __name__ == "__main__":
    root = Tk()
    Home(root)
    root.mainloop()
