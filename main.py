from tkinter import Tk, Frame, Label, Entry, Button, Listbox,Scrollbar, messagebox, Toplevel,ttk
from PIL import Image, ImageTk
import mysql.connector
import csv
from tkinter import scrolledtext
from tkinter import END,VERTICAL
from tkinter import Label
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
class Login:
    def __init__(self, root,cursor):
        self.root = root
        self.cursor=cursor
        self.login_frame = Frame(self.root, bg='Light yellow')
        self.login_frame.pack(fill='both', expand=True)

        # Logo
        logo_image = logo_image = Image.open(r"C:\\Users\\lenovo\\Desktop\\HostelVacancy\\download.png")

        logo_image = logo_image.resize((100, 100), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = Label(self.login_frame, image=self.logo_photo, bg='Light yellow')
        logo_label.pack(side="left", padx=5, pady=5)
        logo_label.pack(anchor="nw", padx=5, pady=5)

        college_label = Label(self.login_frame, text='SHRI VISHNU ENGINEERING COLLEGE FOR WOMEN \n BHIMAVARAM',
                              font=('Calibri', 30, 'bold'), bg='Light Yellow', fg='Dark orange')
        college_label.pack(padx=5, pady=5)

        student_login_frame = Frame(self.login_frame, width=600, height=500, bg='Light Yellow')
        student_login_frame.pack(side='left', fill='both', expand=True)

        title_label = Label(student_login_frame, text='Student Login', font=font1, bg='Dark Orange', fg='White')
        title_label.place(x=(student_login_frame.winfo_reqwidth() - title_label.winfo_reqwidth()) / 1.5, y=70)

        self.user_name = Label(student_login_frame, text='USER NAME  : ', font=fonts, bg='white', fg='Orange', width=12)
        self.user_name.place(x=50, y=150)
        self.user_name_entry = Entry(student_login_frame, width=13, font=font1, bg='white')
        self.user_name_entry.place(x=280, y=150)

        self.user_pass = Label(student_login_frame, text='PASSWORD  : ', font=fonts, bg='white', fg='Orange', width=12)
        self.user_pass.place(x=50, y=200)
        self.user_pass_entry = Entry(student_login_frame, width=13, font=font1, bg='white', show=".")
        self.user_pass_entry.place(x=280, y=200)

        self.submit_btn = Button(student_login_frame, text='Student Login', fg='White', bg='Dark Orange', font=font1,
                                 command=self.check_student_login, cursor='hand2', activebackground='Light Yellow')
        self.submit_btn.place(x=220, y=300)

        # Inserting photo on left side of the button
        self.student_photo_label = Label(student_login_frame)
        self.student_photo_label.place(x=90, y=300)

        self.user_name_entry.bind("<Return>", lambda event: self.user_pass_entry.focus())
        self.user_pass_entry.bind("<Return>", lambda event: self.check_student_login())

        admin_login_frame = Frame(self.login_frame, width=600, height=500, bg='Light Yellow')
        admin_login_frame.pack(side='right', fill='both', expand=True)

        title_label = Label(admin_login_frame, text='Admin Login', font=font1, bg='Dark Orange', fg='White')
        title_label.place(x=(admin_login_frame.winfo_reqwidth() - title_label.winfo_reqwidth()) / 1.5, y=60)

        self.admin_user_name = Label(admin_login_frame, text='USER NAME  : ', font=fonts, bg='white', fg='Orange',
                                      width=12)
        self.admin_user_name.place(x=100, y=150)
        self.admin_user_name_entry = Entry(admin_login_frame, width=13, font=font1, bg='white')
        self.admin_user_name_entry.place(x=350, y=150)

        self.admin_user_pass = Label(admin_login_frame, text='PASSWORD  : ', font=fonts, bg='white', fg='Orange',
                                      width=12)
        self.admin_user_pass.place(x=100, y=200)
        self.admin_user_pass_entry = Entry(admin_login_frame, width=13, font=font1, bg='white', show=".")
        self.admin_user_pass_entry.place(x=350, y=200)

        self.admin_submit_btn = Button(admin_login_frame, text='Admin Login', fg='White', bg='Dark Orange', font=font1,
                                       command=self.check_admin_login, cursor='hand2', activebackground='Light Yellow')
        self.admin_submit_btn.place(x=250, y=300)

        # Inserting photo on left side of the button
        self.admin_photo_label = Label(admin_login_frame)
        self.admin_photo_label.place(x=110, y=300)

        self.admin_user_name_entry.bind("<Return>", lambda event: self.admin_user_pass_entry.focus())
        self.admin_user_pass_entry.bind("<Return>", lambda event: self.check_admin_login())

        # Load and display the initial images
        self.resize_images()

    def resize_images(self):
        # Resize and update student photo
        student_photo = Image.open("C:\\Users\\lenovo\\Desktop\\HostelVacancy\\student1.jpg")
        student_photo = student_photo.resize((105, 95), Image.LANCZOS)
        self.student_photo = ImageTk.PhotoImage(student_photo)
        self.student_photo_label.config(image=self.student_photo)

        # Resize and update admin photo
        admin_photo = Image.open("C:\\Users\\lenovo\\Desktop\\HostelVacancy\\admin.jpg")
        admin_photo = admin_photo.resize((95, 87), Image.LANCZOS)
        self.admin_photo = ImageTk.PhotoImage(admin_photo)
        self.admin_photo_label.config(image=self.admin_photo)

    def check_student_login(self):
        name = self.user_name_entry.get()
        password = self.user_pass_entry.get()

        if password != "svecw":
            messagebox.showerror('WRONG PASSWORD', 'Incorrect password. Please try again.')
            return

        # Check if user already exists in the database
        cursor.execute("SELECT * FROM student WHERE name = %s", (name,))
        user = cursor.fetchone()

        if user:  # User already exists
            messagebox.showinfo('WELCOME', 'WELCOME USER')
            self.login_frame.destroy()
            self.student_dashboard()
        else:  # New user, insert into database
            cursor.execute("INSERT INTO student (name, password) VALUES (%s, %s)", (name, password))
            conn.commit()
            messagebox.showinfo('WELCOME', 'WELCOME USER')
            self.login_frame.destroy()
            dashboard = Dashboard(self.root, admin=False)

    def check_admin_login(self):
        name = self.admin_user_name_entry.get()
        password = self.admin_user_pass_entry.get()

        # Check if admin already exists in the database
        cursor.execute("SELECT * FROM admin1 WHERE name = %s", (name,))
        admin = cursor.fetchone()

        if admin:  # Admin already exists
            if password == admin[1]:  # Verify password
                messagebox.showinfo('WELCOME', 'WELCOME ADMIN')
                self.login_frame.destroy()
                dashboard = Dashboard(self.root, admin=True)
            else:
                messagebox.showerror('WRONG PASSWORD', 'CHECK YOUR PASSWORD')
        else:  # New admin, insert into database
            cursor.execute("INSERT INTO admin1 (name, password) VALUES (%s, %s)", (name, password))
            conn.commit()
            messagebox.showinfo('WELCOME', 'WELCOME ADMIN')
            self.login_frame.destroy()
            dashboard = Dashboard(self.root, admin=True)

    def student_dashboard(self):
        student_dashboard_frame = Frame(self.root, bg='Light Green')
        student_dashboard_frame.pack(fill='both', expand=True)

        search_label = Label(student_dashboard_frame, text="Search:", font=('Calibri', 14, 'bold'), bg='Light Green')
        search_label.grid(row=0, column=3, padx=10, pady=10)

        self.search_entry = Entry(student_dashboard_frame, font=('Calibri', 14), bg='white')
        self.search_entry.grid(row=0, column=4, padx=10, pady=10)

        search_button = Button(student_dashboard_frame, text="Search", command=self.perform_search,
                               bg='Dark Orange', fg='white', font=('Calibri', 14, 'bold'),
                               width=10, height=1, activebackground='Dark Orange', bd=0, cursor='hand2')
        search_button.grid(row=0, column=5, padx=10, pady=10)

        # Create a Treeview widget to display search results
        self.search_results_tree = ttk.Treeview(student_dashboard_frame, columns=("Hostel Name", "Room No", "Beds"),
                                                show="headings")
        self.search_results_tree.grid(row=1, column=3, columnspan=3, padx=10, pady=10)

        # Define column headings
        self.search_results_tree.heading("Hostel Name", text="Hostel Name")
        self.search_results_tree.heading("Room No", text="Room No")
        self.search_results_tree.heading("Beds", text="Beds")

        # Create a scrollbar for the search results treeview
        scrollbar = Scrollbar(student_dashboard_frame, orient='vertical')
        scrollbar.grid(row=1, column=6, sticky="ns")

        # Attach the scrollbar to the search results treeview
        self.search_results_tree.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.search_results_tree.yview)

        # Create a Listbox widget to display hostel names
        self.hostel_listbox = Listbox(student_dashboard_frame, font=('Calibri', 14), bg='white')
        self.hostel_listbox.grid(row=1, column=5, padx=10, pady=10, sticky="nsew")

        # Create a scrollbar for the hostel listbox
        hostel_scrollbar = Scrollbar(student_dashboard_frame, orient='vertical')
        hostel_scrollbar.grid(row=1, column=6, sticky="ns")

        # Attach the scrollbar to the hostel listbox
        self.hostel_listbox.config(yscrollcommand=hostel_scrollbar.set)
        hostel_scrollbar.config(command=self.hostel_listbox.yview)

        # Retrieve unique hostel names from the database
        cursor.execute("SELECT DISTINCT hostel_name FROM hostel")
        hostels = cursor.fetchall()

        # Insert unique hostel names into the scrollbar
        for hostel in hostels:
            self.hostel_listbox.insert(END, hostel[0])

        # Bind a function to handle hostel selection
        self.hostel_listbox.bind("<<ListboxSelect>>", self.display_hostel_details)

        # Create a frame for displaying hostel details
        self.hostel_details_frame = Frame(student_dashboard_frame, bg='Light Green')
        self.hostel_details_frame.grid(row=2, column=0, columnspan=6, padx=10, pady=10, sticky='nsew')

        self.hostel_details_label = Label(self.hostel_details_frame, text="", font=('Calibri', 14), bg='Light Green')
        self.hostel_details_label.pack(padx=10, pady=10)

    def perform_search(self):
        query = self.search_entry.get()

        if not query:
            messagebox.showwarning("Empty Query", "Please enter a search query.")
            return

        cursor.execute("SELECT hostel_name, room_no, beds FROM hostel WHERE hostel_name LIKE %s", ('%' + query + '%',))
        search_results = cursor.fetchall()

        if not search_results:
            messagebox.showinfo("No Results", "No matching results found.")
            return

        # Clear existing treeview items
        self.search_results_tree.delete(*self.search_results_tree.get_children())

        # Insert search results into the treeview
        for result in search_results:
            self.search_results_tree.insert("", "end", values=result)

    def display_hostel_details(self, event):
        selected_index = self.hostel_listbox.curselection()
        if selected_index:
            selected_hostel = self.hostel_listbox.get(selected_index)
            cursor.execute("SELECT room_no, beds FROM hostel WHERE hostel_name = %s", (selected_hostel,))
            hostel_details = cursor.fetchall()
            details_text = "Hostel Details:\n"
            for detail in hostel_details:
                details_text += f"Room No: {detail[0]}, Beds: {detail[1]}\n"
            self.hostel_details_label.config(text=details_text)
        else:
            self.hostel_details_label.config(text="")
class Dashboard:
    def __init__(self, root, admin=False):
        self.root = root
        self.admin = admin
        if admin:
            self.root.title('ADMIN DASHBOARD')
            bg_color = 'Light Blue'

            self.admin_dashboard()
        else:
            self.root.title('STUDENT DASHBOARD')
            bg_color = 'Light Green'
            self.student_dashboard()

    def admin_dashboard(self):
        admin_dashboard_frame = Frame(self.root, bg='Light Yellow')  # Change background color here
        admin_dashboard_frame.pack(fill='both', expand=True)

        
        buttons_data = [
            ("ADD", self.add_data),
            ("UPDATE", self.update_data),
            ("DELETE", self.delete_data),
            ("LOGOUT", self.logout)
        ]
        

        for button_text, command_func in buttons_data:
            if button_text == "LOGOUT":
                button = Button(admin_dashboard_frame, text=button_text, command=command_func,
                                bg='red', fg='white', font=('Calibri', 14, 'bold'), width=10, height=2,
                                bd=0, cursor='hand2')
            else:
                button = Button(admin_dashboard_frame, text=button_text, command=command_func,
                                bg='Dark Orange', fg='white', font=('Calibri', 14, 'bold'), width=10, height=2,
                                activebackground='Dark Orange', bd=0, cursor='hand2')
            button.pack(pady=10)
    


    def add_data(self):
        add_window = Toplevel(self.root)
        add_window.title("Add Data")
        add_window.geometry("400x240")

        # Centering the window on the screen
        self.center_window(add_window)

        hostel_label = Label(add_window, text="Hostel Name:", font=('Calibri', 14, 'bold'), bg='Light Yellow')
        hostel_label.grid(row=0, column=0, padx=10, pady=10)
        hostel_entry = Entry(add_window, font=('Calibri', 14), bg='white')
        hostel_entry.grid(row=0, column=1, padx=10, pady=10)

        room_label = Label(add_window, text="Room No:", font=('Calibri', 14, 'bold'), bg='Light Yellow')
        room_label.grid(row=1, column=0, padx=10, pady=10)
        room_entry = Entry(add_window, font=('Calibri', 14), bg='white')
        room_entry.grid(row=1, column=1, padx=10, pady=10)
        beds_label = Label(add_window, text="Number of Beds:", font=('Calibri', 14, 'bold'), bg='Light Yellow')
        beds_label.grid(row=2, column=0, padx=10, pady=10)
        beds_entry = Entry(add_window, font=('Calibri', 14), bg='white')
        beds_entry.grid(row=2, column=1, pady=10)

        store_btn = Button(add_window, text="ADD", command=lambda: self.store_data(hostel_entry.get(), room_entry.get(), beds_entry.get()),
                           bg='Dark Orange', fg='white', font=('Calibri', 14, 'bold'), width=10, height=1,
                           activebackground='Dark Orange', bd=0, cursor='hand2')
        store_btn.grid(row=3, column=0, columnspan=2, pady=10)

        

    def update_data(self):
        update_window = Toplevel(self.root)
        update_window.title("Update Data")
        update_window.geometry("400x200")

        # Centering the window on the screen
        self.center_window(update_window)

        hostel_label = Label(update_window, text="Hostel Name:", font=('Calibri', 14, 'bold'), bg='Light Yellow')
        hostel_label.grid(row=0, column=0, padx=10, pady=10)
        hostel_entry = Entry(update_window, font=('Calibri', 14), bg='white')
        hostel_entry.grid(row=0, column=1, padx=10, pady=10)

        room_label = Label(update_window, text="Room No:", font=('Calibri', 14, 'bold'), bg='Light Yellow')
        room_label.grid(row=1, column=0, padx=10, pady=10)
        room_entry = Entry(update_window, font=('Calibri', 14), bg='white')
        room_entry.grid(row=1, column=1, padx=10, pady=10)

        beds_label = Label(update_window, text="Number of Beds:", font=('Calibri', 14, 'bold'), bg='Light Yellow')
        beds_label.grid(row=2, column=0, padx=10, pady=10)
        beds_entry = Entry(update_window, font=('Calibri', 14), bg='white')
        beds_entry.grid(row=2, column=1, pady=10)

        store_btn = Button(update_window, text="UPDATE", command=lambda: self.update_data_in_db(hostel_entry.get(), room_entry.get(), beds_entry.get()),
                        bg='Dark Orange', fg='white', font=('Calibri', 14, 'bold'), width=10, height=1,
                        activebackground='Dark Orange', bd=0, cursor='hand2')
        store_btn.grid(row=3, column=0, columnspan=2, pady=10)
    def delete_data(self):
        delete_window = Toplevel(self.root)
        delete_window.title("Delete Data")
        delete_window.geometry("400x200")

        # Centering the window on the screen
        self.center_window(delete_window)

        hostel_label = Label(delete_window, text="Hostel Name:", font=('Calibri', 14, 'bold'), bg='Light Yellow')
        hostel_label.grid(row=0, column=0, padx=10, pady=10)
        hostel_entry = Entry(delete_window, font=('Calibri', 14), bg='white')
        hostel_entry.grid(row=0, column=1, padx=10, pady=10)

        room_label = Label(delete_window, text="Room No:", font=('Calibri', 14, 'bold'), bg='Light Yellow')
        room_label.grid(row=1, column=0, padx=10, pady=10)
        room_entry = Entry(delete_window, font=('Calibri', 14), bg='white')
        room_entry.grid(row=1, column=1, padx=10, pady=10)

        beds_label = Label(delete_window, text="Number of Beds:", font=('Calibri', 14, 'bold'), bg='Light Yellow')
        beds_label.grid(row=2, column=0, padx=10, pady=10)
        beds_entry = Entry(delete_window, font=('Calibri', 14), bg='white')
        beds_entry.grid(row=2, column=1, pady=10)

        store_btn = Button(delete_window, text="DELETE", command=lambda: self.delete_data_from_db(hostel_entry.get(), room_entry.get(), beds_entry.get()),
                        bg='Dark Orange', fg='white', font=('Calibri', 14, 'bold'), width=10, height=1,
                        activebackground='Dark Orange', bd=0, cursor='hand2')
        store_btn.grid(row=3, column=0, columnspan=2, pady=10)

    def display_history(self):
        history_window = Toplevel(self.root)
        history_window.title("History")
        history_window.geometry("600x400")

        # Centering the window on the screen
        self.center_window(history_window)

        history_text = scrolledtext.ScrolledText(history_window, width=60, height=20)
        history_text.pack(expand=True, fill='both')

        # Read history from CSV file and display it in the text area
        with open("hostel_history.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                history_text.insert('end', ', '.join(row) + '\n')

    def store_data(self, hostel_name, room_no, beds):
        # Here you can add your code to store the data in the database
        with open("hostel_history.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([hostel_name, room_no, beds])
        print("Data stored successfully.")

    def center_window(self, window):
        # Centering the window on the screen
        window_width = window.winfo_reqwidth()
        window_height = window.winfo_reqheight()
        position_right = int(window.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(window.winfo_screenheight() / 2 - window_height / 2)
        window.geometry("+{}+{}".format(position_right, position_down))

  
    def store_data(self, hostel_name, room_no, beds):
        try:
        # Insert data into the database table
            cursor.execute("INSERT INTO hostel (hostel_name, room_no, beds) VALUES (%s, %s, %s)", (hostel_name, room_no, beds))
            conn.commit()  # Commit the transaction
            messagebox.showinfo("Success", "Data added successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error occurred: {err}")
    def update_data_in_db(self, hostel_name, room_no, beds):
        try:
            # Update data in the database table
            cursor.execute("UPDATE hostel SET beds = %s WHERE hostel_name = %s AND room_no = %s", (beds, hostel_name, room_no))
            conn.commit()  # Commit the transaction
            messagebox.showinfo("Success", "Data updated successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error occurred: {err}")
    def delete_data_from_db(self, hostel_name, room_no, beds):
        try:
        # Delete data from the database table
            cursor.execute("DELETE FROM hostel WHERE hostel_name = %s AND room_no = %s AND beds = %s", (hostel_name, room_no, beds))
            conn.commit()  # Commit the transaction
            messagebox.showinfo("Success", "Data deleted successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error occurred: {err}")
    
    def logout(self):
        self.root.destroy()  # Close the current window, i.e., the admin dashboard
        root = Tk()
        root.title('LOGIN')
        root.geometry('1300x500+200+140')
        root.resizable(False, False)
        login = Login(root)
        root.mainloop()

if __name__ == "__main__":
    root = Tk()
    root.title('LOGIN')
    root.geometry('1300x500+200+140')
    root.resizable(False, False)
    login = Login(root,cursor)
    root.mainloop()
