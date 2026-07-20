# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 22:10:17 2026

@author: naitb
"""

# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk, messagebox
import sqlite3

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from openpyxl import Workbook

import os
import sys

def resource_path(relative_path):
    """Get absolute path to resource (works for .exe and normal run)"""
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


ICON_PATH = resource_path("navenie.ico")


def set_icon(window):
    """Safe icon setter (EXE compatible)"""
    try:
        window.iconbitmap(ICON_PATH)
    except Exception as e:
        print("Icon load failed:", e)
        
from PIL import Image, ImageTk
import time
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def splash_screen():
    splash = tk.Tk()
    splash.overrideredirect(True)

    width, height = 500, 300
    x = (splash.winfo_screenwidth() // 2) - (width // 2)
    y = (splash.winfo_screenheight() // 2) - (height // 2)
    splash.geometry(f"{width}x{height}+{x}+{y}")

    img = Image.open(resource_path("amsimage.png"))
    img = img.resize((500, 300))
    photo = ImageTk.PhotoImage(img)

    label = tk.Label(splash, image=photo)
    label.image = photo
    label.pack()

    splash.update()
    time.sleep(5)
    splash.destroy()

splash_screen()

# ================= DATABASE =================

APP_NAME = "NAVENIE AMS"
APP_DIR = os.path.join(os.environ["APPDATA"], APP_NAME)
os.makedirs(APP_DIR, exist_ok=True)

DB_PATH = os.path.join(APP_DIR, "school.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    admission TEXT,
    gender TEXT,
    class_name TEXT,
    dob TEXT,
    parent TEXT,
    address TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    term TEXT,
    year TEXT,
    subject TEXT,
    ca INTEGER,
    exam INTEGER,
    total INTEGER,
    grade TEXT   
)
""")
try:
   cursor.execute("ALTER TABLE results ADD COLUMN grade TEXT")
except:
    pass

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# Default admin (only once)
cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin','admin')")
conn.commit()

# ================= LOGIN =================
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NAVENIE Academic Management System")
        self.root.state("zoomed")
        self.root.configure(bg="#E8EEF7")  # Soft blue background

        # ================= HEADER =================
        header = tk.Frame(root, bg="#003366", height=120)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="NAVENIE ACADEMIC MANAGEMENT SYSTEM",
            bg="#003366",
            fg="white",
            font=("Segoe UI", 28, "bold")
        ).pack(pady=(20, 5))

        tk.Label(
            header,
            text="Secure Login Portal",
            bg="#003366",
            fg="gold",
            font=("Segoe UI", 14)
        ).pack()

        # ================= LOGIN CARD =================
        card = tk.Frame(
            root,
            bg="white",
            bd=3,
            relief="ridge",
            padx=40,
            pady=30
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            card,
            text="LOGIN",
            bg="white",
            fg="#003366",
            font=("Segoe UI", 22, "bold")
        ).pack(pady=(0, 20))

        # Username
        tk.Label(
            card,
            text="Username",
            bg="white",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w")

        self.username = tk.Entry(card, font=("Segoe UI", 12), width=30)
        self.username.pack(ipady=6, pady=(0, 15))

        # Password
        tk.Label(
            card,
            text="Password",
            bg="white",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w")

        self.password = tk.Entry(
            card,
            show="*",
            font=("Segoe UI", 12),
            width=30
        )
        self.password.pack(ipady=6, pady=(0, 20))

        # Login Button
        tk.Button(
            card,
            text="LOGIN",
            bg="#28A745",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            width=25,
            command=self.login
        ).pack(pady=5)

        # Change Password
        tk.Button(
            card,
            text="CHANGE PASSWORD",
            bg="#007BFF",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            width=25,
            command=self.change_password
        ).pack(pady=5)

        # Forgot Password
        tk.Button(
            card,
            text="Forgot Password?",
            bg="white",
            fg="#007BFF",
            relief="flat",
            font=("Segoe UI", 10, "underline"),
            cursor="hand2",
            command=self.forgot_password
        ).pack(pady=10)

        # ================= FOOTER =================
        footer = tk.Frame(root, bg="#003366", height=35)
        footer.pack(side="bottom", fill="x")
        footer.pack_propagate(False)

        tk.Label(
            footer,
            text="© 2026 NAVENIE Technologies | Developed by ANGEL NAITBJ for St. paul's Schools®",
            bg="#003366",
            fg="white",
            font=("Segoe UI", 10)
        ).pack(pady=6)

    # ================= LOGIN =================
    def login(self):
        user = self.username.get()
        pwd = self.password.get()

        result = cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (user, pwd)
        ).fetchone()

        if result:
            self.root.destroy()
            open_dashboard()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

    # ================= CHANGE PASSWORD =================
    def change_password(self):
        win = tk.Toplevel(self.root)
        win.title("Change Password")
        win.geometry("350x220")

        tk.Label(win, text="Old Password").pack(pady=5)
        old = tk.Entry(win, show="*")
        old.pack()

        tk.Label(win, text="New Password").pack(pady=5)
        new = tk.Entry(win, show="*")
        new.pack()

        def update_pass():
            if cursor.execute(
                "SELECT * FROM users WHERE username='admin' AND password=?",
                (old.get(),)
            ).fetchone():

                cursor.execute(
                    "UPDATE users SET password=? WHERE username='admin'",
                    (new.get(),)
                )
                conn.commit()

                messagebox.showinfo(
                    "Success",
                    "Password Changed Successfully"
                )

                win.destroy()

            else:
                messagebox.showerror(
                    "Error",
                    "Old Password is Incorrect"
                )

        tk.Button(
            win,
            text="UPDATE PASSWORD",
            bg="#007BFF",
            fg="white",
            command=update_pass
        ).pack(pady=15)

    # ================= FORGOT PASSWORD =================
    def forgot_password(self):
        win = tk.Toplevel(self.root)
        win.title("Recover Password")
        win.geometry("350x220")

        tk.Label(win, text="Username").pack(pady=5)
        username_entry = tk.Entry(win)
        username_entry.pack()

        tk.Label(win, text="New Password").pack(pady=5)
        new_pass = tk.Entry(win, show="*")
        new_pass.pack()

        def reset():
            user = username_entry.get()
            pwd = new_pass.get()

            if user == "" or pwd == "":
                messagebox.showerror(
                    "Error",
                    "All fields are required."
                )
                return

            data = cursor.execute(
                "SELECT * FROM users WHERE username=?",
                (user,)
            ).fetchone()

            if data:
                cursor.execute(
                    "UPDATE users SET password=? WHERE username=?",
                    (pwd, user)
                )

                conn.commit()

                messagebox.showinfo(
                    "Success",
                    "Password Reset Successful"
                )

                win.destroy()

            else:
                messagebox.showerror(
                    "Error",
                    "Username not found."
                )

        tk.Button(
            win,
            text="RESET PASSWORD",
            bg="#28A745",
            fg="white",
            command=reset
        ).pack(pady=15)

# ================= DASHBOARD =================
def logout(dashboard):
    if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
        dashboard.destroy()

        login_root = tk.Tk()
        login_root.title("NAVENIE AMS Login")
        set_icon(login_root)
        LoginApp(login_root)
        login_root.mainloop()

def open_dashboard():
    root = tk.Tk()
    root.title("DASHBOARD")
    root.state("zoomed")
    root.configure(bg="#1f6aa5")

    tk.Label(
        root,
        text="SCHOOL DASHBOARD",
        font=("Arial", 18, "bold"),
        bg="#1f6aa5",
        fg="white"
    ).pack(pady=20)

    # ===== STUDENT SYSTEM =====
    tk.Button(
        root,
        text="OPEN STUDENT SYSTEM",
        bg="white",
        fg="black",
        width=25,
        command=lambda: open_main_app(root)
    ).pack(pady=10)

    # ===== STAFF SYSTEM =====
    tk.Button(
        root,
        text="OPEN STAFF SYSTEM",
        bg="purple",
        fg="white",
        width=25,
        command=lambda: open_teachers_app(root)
    ).pack(pady=10)

    # ===== PAYMENT SYSTEM =====
    tk.Button(
        root,
        text="OPEN PAYMENT SYSTEM",
        bg="darkgreen",
        fg="white",
        width=25,
        command=lambda: open_bursar_app(root)
    ).pack(pady=10)

    # ===== LOGOUT BUTTON =====
    tk.Button(
        root,
        text="🚪 LOG OUT",
        bg="#dc3545",
        fg="white",
        font=("Arial", 11, "bold"),
        width=25,
        command=lambda: logout(root)
    ).pack(pady=30)

    set_icon(root)
    root.mainloop()
# ================= OPEN MAIN APP =================
def open_main_app(dashboard_root):
    dashboard_root.destroy()
    root = tk.Tk()
    root.title("STUDENTS DASHBOARD")
    root.state("zoomed")
    set_icon(root)
    SchoolApp(root)
    root.mainloop()

def open_teachers_app(dashboard_root):
    dashboard_root.destroy()
    root = tk.Tk()
    root.title("TEACHERS DASHBOARD")
    root.state("zoomed")
    set_icon(root)
    TeachersApp(root)
    root.mainloop()
    
 # ================= ⭐ OPEN BURSAR APP (NEW) =================
def open_bursar_app(dashboard_root):
    dashboard_root.destroy()
    root = tk.Tk()
    root.title("BURSAR DASHBOARD")
    root.state("zoomed")
    set_icon(root)

    BursarApp(root)   # 👈 you must create this class
    root.mainloop()   

 # ================= SCHOOL APP ==============

class SchoolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("STUDENTS MANAGEMENT SYSTEM ANGEL NAITBJ®")
        self.root.geometry("1350x750")
        self.root.configure(bg="#0b1e3a")

        # VARIABLES
        self.name = tk.StringVar()
        self.admission = tk.StringVar()
        self.gender = tk.StringVar(value="Male")
        self.class_name = tk.StringVar()
        self.dob = tk.StringVar()
        self.parent = tk.StringVar()
        self.address = tk.StringVar()

        self.term = tk.StringVar(value="First Term")
        self.year = tk.StringVar()
        self.subject = tk.StringVar()
        self.ca = tk.StringVar()
        self.exam = tk.StringVar()
        
        self.filter_year = tk.StringVar()
        self.filter_term = tk.StringVar()

        # ✅ FIXED MISSING VARIABLE
        self.search_var = tk.StringVar()

        self.selected_id = None
        self.selected_result_id = None

        self.ui()
        self.load_students()
        
    # ================= UI =================
    def ui(self):
        tk.Label(self.root, text="STUDENTS MANAGEMENT SYSTEM ANGEL NAITBJ®",
                 font=("Arial", 22, "bold"),
                 bg="#1f6aa5", fg="white").pack(fill="x")

        form = tk.LabelFrame(self.root, text=" STUDENT FORM ",
                             bg="#102542", fg="white")
        form.pack(fill="x", padx=10, pady=5)

        tk.Label(form, text="Name").grid(row=0, column=0)
        tk.Entry(form, textvariable=self.name).grid(row=0, column=1)

        tk.Label(form, text="Admission").grid(row=0, column=2)
        tk.Entry(form, textvariable=self.admission).grid(row=0, column=3)

        tk.Label(form, text="Gender").grid(row=1, column=0)
        ttk.Combobox(form, textvariable=self.gender,
                     values=["Male", "Female"]).grid(row=1, column=1)

        tk.Label(form, text="Class").grid(row=1, column=2)
        tk.Entry(form, textvariable=self.class_name).grid(row=1, column=3)

        tk.Label(form, text="DOB").grid(row=2, column=0)
        tk.Entry(form, textvariable=self.dob).grid(row=2, column=1)

        tk.Label(form, text="Parent").grid(row=2, column=2)
        tk.Entry(form, textvariable=self.parent).grid(row=2, column=3)

        tk.Label(form, text="Address").grid(row=3, column=0)
        tk.Entry(form, textvariable=self.address, width=50).grid(row=3, column=1, columnspan=3)

        tk.Button(form, text="ADD", bg="green", command=self.add_student).grid(row=4, column=0)
        tk.Button(form, text="UPDATE", bg="blue", command=self.update_student).grid(row=4, column=1)
        tk.Button(form, text="DELETE", bg="red", command=self.delete_student).grid(row=4, column=2)
        tk.Button(form, text="BACK", bg="black", fg="white", command=self.back).grid(row=4, column=3)
        
        tk.Button(form, text="VIEW RESULT", bg="black", fg="white",
                  command=self.view_result).grid(row=4, column=4)

        tk.Button(form, text="EXPORT", bg="darkgreen", fg="white",
                  command=self.export_all).grid(row=4, column=5)

        # ================= SEARCH FIX =================
        tk.Label(form, text="Search").grid(row=5, column=0)

        tk.Entry(form, textvariable=self.search_var).grid(row=5, column=1)

        tk.Button(form, text="SEARCH", bg="orange",
                  command=self.search_student).grid(row=5, column=2)

        tk.Button(form, text="RESET", bg="gray",
                  command=self.load_students).grid(row=5, column=3)
        tk.Button(form, text="CLEAR", bg="gray", fg="white",
          command=self.clear_student).grid(row=5, column=4)

        # ================= STUDENT TABLE =================
        frame1 = tk.Frame(self.root)
        frame1.pack(fill="both", expand=True)

        y1 = tk.Scrollbar(frame1, orient="vertical")
        x1 = tk.Scrollbar(frame1, orient="horizontal")

        self.tree = ttk.Treeview(
            frame1,
            columns=("ID","Name","Admission","Gender","Class","DOB","Parent","Address"),
            show="headings",
            yscrollcommand=y1.set,
            xscrollcommand=x1.set
        )

        y1.config(command=self.tree.yview)
        x1.config(command=self.tree.xview)

        y1.pack(side="right", fill="y")
        x1.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        for c in ("ID","Name","Admission","Gender","Class","DOB","Parent","Address"):
            self.tree.heading(c, text=c)

        self.tree.bind("<ButtonRelease-1>", self.select_student)

        # ================= RESULT ENTRY =================
        result = tk.LabelFrame(self.root, text=" RESULT ENTRY ",
                               bg="#102542", fg="white")
        result.pack(fill="x", padx=10, pady=5)

        tk.Label(result, text="Term").grid(row=0, column=0)
        ttk.Combobox(result, textvariable=self.term,
                     values=["First Term","Second Term","Third Term"]).grid(row=1, column=0)

        tk.Label(result, text="Year").grid(row=0, column=1)
        tk.Entry(result, textvariable=self.year).grid(row=1, column=1)

        tk.Label(result, text="Subject").grid(row=0, column=2)
        tk.Entry(result, textvariable=self.subject).grid(row=1, column=2)

        tk.Label(result, text="CA").grid(row=0, column=3)
        tk.Entry(result, textvariable=self.ca).grid(row=1, column=3)

        tk.Label(result, text="Exam").grid(row=0, column=4)
        tk.Entry(result, textvariable=self.exam).grid(row=1, column=4)

        tk.Button(result, text="ADD", command=self.add_result).grid(row=1, column=5)
        tk.Button(result, text="UPDATE", command=self.update_result).grid(row=1, column=6)
        tk.Button(result, text="DELETE", command=self.delete_result).grid(row=1, column=7)
        tk.Button(result, text="CLEAR", command=self.clear_result).grid(row=1, column=8)
        
        # ===== FILTER SECTION =====
        tk.Label(result, text="Filter Year (optional)").grid(row=2, column=0)
        tk.Entry(result, textvariable=self.filter_year, width=10).grid(row=2, column=1)

        tk.Label(result, text="Filter Term (optional)").grid(row=2, column=2)
        ttk.Combobox(
        result,
        textvariable=self.filter_term,
        values=["", "First Term", "Second Term", "Third Term"],
        width=15
        ).grid(row=2, column=3)

        # ================= RESULT TABLE =================
        frame2 = tk.Frame(self.root)
        frame2.pack(fill="both", expand=True)

        y2 = tk.Scrollbar(frame2, orient="vertical")
        x2 = tk.Scrollbar(frame2, orient="horizontal")

        self.result_tree = ttk.Treeview(
            frame2,
            columns=("ID","Term","Year","Subject","CA","Exam","Total","Grade"),
            show="headings",
            yscrollcommand=y2.set,
            xscrollcommand=x2.set
        )
        
        y2.config(command=self.result_tree.yview)
        x2.config(command=self.result_tree.xview)
        
        y2.pack(side="right", fill="y")
        x2.pack(side="bottom", fill="x")
        self.result_tree.pack(fill="both", expand=True)

        for c in ("ID","Term","Year","Subject","CA","Exam","Total","Grade"):
            self.result_tree.heading(c, text=c)

        self.result_tree.bind("<ButtonRelease-1>", self.select_result)

    # ================= SEARCH FIXED =================
    def search_student(self):
        key = self.search_var.get().strip()
        self.tree.delete(*self.tree.get_children())

        if key == "":
            self.load_students()
            return

        for r in conn.execute("""
            SELECT * FROM students
            WHERE name LIKE ? OR admission LIKE ? OR class_name LIKE ?
        """, (f"%{key}%", f"%{key}%", f"%{key}%")):
            self.tree.insert("", "end", values=r)

    # ================= STUDENT FUNCTIONS =================
    def add_student(self):
        conn.execute("""
            INSERT INTO students VALUES(NULL,?,?,?,?,?,?,?)
        """, (
            self.name.get(), self.admission.get(), self.gender.get(),
            self.class_name.get(), self.dob.get(),
            self.parent.get(), self.address.get()
        ))
        conn.commit()
        self.load_students()

    def load_students(self):
        self.tree.delete(*self.tree.get_children())
        for r in conn.execute("SELECT * FROM students"):
            self.tree.insert("", "end", values=r)

    def select_student(self, e):
        data = self.tree.item(self.tree.focus(), "values")
        if data:
            self.selected_id = data[0]
            self.load_results()

    def update_student(self):
        if self.selected_id:
            conn.execute("""
                UPDATE students SET name=?, admission=?, gender=?, class_name=?, dob=?, parent=?, address=?
                WHERE id=?
            """, (
                self.name.get(), self.admission.get(), self.gender.get(),
                self.class_name.get(), self.dob.get(),
                self.parent.get(), self.address.get(), self.selected_id
            ))
            conn.commit()
            self.load_students()

    def delete_student(self):
        if self.selected_id:
            conn.execute("DELETE FROM students WHERE id=?", (self.selected_id,))
            conn.commit()
            self.load_students()
         
    def back(self):
        self.root.destroy()
        open_dashboard() 
            
    def clear_student(self):
                            self.name.set("")
                            self.admission.set("")
                            self.gender.set("Male")
                            self.class_name.set("")
                            self.dob.set("")
                            self.parent.set("")
                            self.address.set("")
                            self.selected_id = None 
                            
    # ================= GRADE FUNCTIONS =================  
                              
    def get_grade(self, total):
          if total >= 70:
              return "A"
          elif total >= 60:
              return "B"
          elif total >= 50:
              return "C"
          elif total >= 45:
              return "D"
          elif total >= 40:
              return "E"
          else:
              return "F" 
    # ================= RESULT FUNCTIONS =================
    def clear_result(self):
        self.subject.set("")
        self.ca.set("")
        self.exam.set("")

    def add_result(self):
         if not self.selected_id:
             return

         ca = int(self.ca.get() or 0)
         exam = int(self.exam.get() or 0)
         total = ca + exam
         grade = self.get_grade(total)

         conn.execute("""
             INSERT INTO results
             VALUES(NULL,?,?,?,?,?,?,?,?)
         """, (
             self.selected_id,
             self.term.get(),
             self.year.get(),
             self.subject.get(),
             ca,
             exam,
             total,
             grade
         ))

         conn.commit()
         self.load_results()

    def select_result(self, e):
        data = self.result_tree.item(self.result_tree.focus(), "values")
        if data:
            self.selected_result_id = data[0]

    def update_result(self):
         if self.selected_result_id:
             ca = int(self.ca.get() or 0)
             exam = int(self.exam.get() or 0)
             total = ca + exam
             grade = self.get_grade(total)

             conn.execute("""
                 UPDATE results
                 SET term=?,year=?,subject=?,ca=?,exam=?,total=?,grade=?
                 WHERE id=?
             """, (
                 self.term.get(),
                 self.year.get(),
                 self.subject.get(),
                 ca,
                 exam,
                 total,
                 grade,
                 self.selected_result_id
             ))

             conn.commit()
             self.load_results()

    def delete_result(self):
        if self.selected_result_id:
            conn.execute("DELETE FROM results WHERE id=?", (self.selected_result_id,))
            conn.commit()
            self.load_results()

    def load_results(self):
        self.result_tree.delete(*self.result_tree.get_children())
        if not self.selected_id:
            return

        for r in conn.execute("SELECT * FROM results WHERE student_id=?", (self.selected_id,)):
            self.result_tree.insert("", "end", values=r)

    # ================= VIEW ============================
    def view_result(self):
         if not self.selected_id:
             messagebox.showerror("Error", "Please select a student first")
             return

         win = tk.Toplevel(self.root)
         win.title("STUDENT RESULT VIEW")
         win.geometry("800x600")

         set_icon(win)

         frame = tk.Frame(win)
         frame.pack(fill="both", expand=True)

         y_scroll = tk.Scrollbar(frame, orient="vertical")
         x_scroll = tk.Scrollbar(frame, orient="horizontal")

         text = tk.Text(frame, wrap="none",
                         yscrollcommand=y_scroll.set,
                         xscrollcommand=x_scroll.set)

         y_scroll.config(command=text.yview)
         x_scroll.config(command=text.xview)

         y_scroll.pack(side="right", fill="y")
         x_scroll.pack(side="bottom", fill="x")
         text.pack(fill="both", expand=True)

         # ================= STUDENT =================
         student = conn.execute(
             "SELECT name, class_name FROM students WHERE id=?",
             (self.selected_id,)
         ).fetchone()

         if not student:
             messagebox.showerror("Error", "Student not found")
             return

         name, class_name = student

         text.insert(tk.END, f"\n{name} ({class_name})\n")
         text.insert(tk.END, "=" * 70 + "\n")

         # ================= FILTERS =================
         year = self.filter_year.get().strip()
         term = self.filter_term.get().strip()

         query = """
             SELECT term, subject, ca, exam, total, grade
             FROM results
             WHERE student_id=?
         """
         params = [self.selected_id]

         if year:
             query += " AND year=?"
             params.append(year)

         if term:
             query += " AND term=?"
             params.append(term)

         query += " ORDER BY term"

         results = conn.execute(query, params).fetchall()

         if not results:
             text.insert(tk.END, "No results found\n")
             return

         term_totals = {}
         year_total = 0

         for t, subject, ca, exam, total, grade in results:
             text.insert(tk.END, f"{t} | {subject} | CA:{ca} EX:{exam} TOTAL:{total} GRADE:{grade}\n")

             term_totals[t] = term_totals.get(t, 0) + total
             year_total += total

         text.insert(tk.END, "\n" + "-" * 70 + "\n")
         text.insert(tk.END, "TERM TOTALS:\n")

         for t, total in term_totals.items():
             text.insert(tk.END, f"{t}: {total}\n")

         text.insert(tk.END, f"\nYEAR TOTAL:\n{year_total}\n")
         text.insert(tk.END, "=" * 70 + "\n")
         
   # ================= STUDENT FUNCTIONS =================
    def export_all(self):
         if not self.selected_id:
             messagebox.showerror("Error", "Please select a student first")
             return

         student = conn.execute(
             "SELECT name, class_name FROM students WHERE id=?",
             (self.selected_id,)
         ).fetchone()

         if not student:
             messagebox.showerror("Error", "Student not found")
             return

         name, class_name = student

         # ================= FILTERS =================
         year = self.filter_year.get().strip()
         term = self.filter_term.get().strip()

         query = """
             SELECT term, subject, ca, exam, total, grade
             FROM results
             WHERE student_id=?
         """
         params = [self.selected_id]

         if year:
             query += " AND year=?"
             params.append(year)

         if term:
             query += " AND term=?"
             params.append(term)

         query += " ORDER BY term"

         results = conn.execute(query, params).fetchall()

         if not results:
             messagebox.showerror("Error", "No results found")
             return

         term_totals = {}
         year_total = 0

         # ================= PDF =================
         doc = SimpleDocTemplate("report.pdf")
         styles = getSampleStyleSheet()
         story = []

         story.append(Paragraph(f"<b>{name} ({class_name})</b>", styles["Normal"]))
         story.append(Spacer(1, 10))

         for t, subject, ca, exam, total, grade in results:
             story.append(Paragraph(
                 f"{t} | {subject} | CA:{ca} EX:{exam} TOTAL:{total}, GRADE:{grade}",
                 styles["Normal"]
             ))

             term_totals[t] = term_totals.get(t, 0) + total
             year_total += total

         story.append(Spacer(1, 10))
         story.append(Paragraph("<b>TERM TOTALS:</b>", styles["Normal"]))

         for t, total in term_totals.items():
             story.append(Paragraph(f"{t}: {total}", styles["Normal"]))

         story.append(Spacer(1, 10))
         story.append(Paragraph(f"<b>YEAR TOTAL: {year_total}</b>", styles["Normal"]))

         doc.build(story)

         # ================= EXCEL =================
         wb = Workbook()
         ws = wb.active

         ws.append([f"{name} ({class_name})"])
         ws.append([])
         ws.append(["Term", "Subject", "CA", "Exam", "Total", "Grade"])

         for t, subject, ca, exam, total, grade in results:
             ws.append([t, subject, ca, exam, total, grade])

         ws.append([])
         ws.append(["TERM TOTALS"])

         for t, total in term_totals.items():
             ws.append([t, total])

         ws.append([])
         ws.append(["YEAR TOTAL", year_total])

         wb.save("report.xlsx")

         messagebox.showinfo("Success", "Export completed successfully")   

    # ================= TEACHERS APP ==============

class TeachersApp:
    def __init__(self, root):
        self.root = root
        self.root.title("STAFF MANAGEMENT SYSTEM ANGEL NAITBJ®")
        self.root.state("zoomed")
        self.root.configure(bg="#0b1e3a")

        # ================= DATABASE =================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            subject TEXT,
            class_assigned TEXT,
            contact TEXT,
            address TEXT,
            qualification TEXT,
            salary TEXT,
            date_employed TEXT
        )
        """)
        conn.commit()

        # ================= VARIABLES =================
        self.name = tk.StringVar()
        self.subject = tk.StringVar()
        self.class_assigned = tk.StringVar()
        self.contact = tk.StringVar()
        self.address = tk.StringVar()
        self.qualification = tk.StringVar()
        self.salary = tk.StringVar()
        self.date_employed = tk.StringVar()

        self.selected_id = None

        self.ui()
        self.load_teachers()

    # ================= UI =================
    def ui(self):

        tk.Label(
            self.root,
            text="STAFF MANAGEMENT SYSTEM ANGEL NAITBJ®",
            font=("Arial", 22, "bold"),
            bg="#1f6aa5",
            fg="white"
        ).pack(fill="x")

        form = tk.LabelFrame(
            self.root,
            text=" TEACHER FORM ",
            bg="#102542",
            fg="white"
        )
        form.pack(fill="x", padx=10, pady=10)

        # Row 0
        tk.Label(form, text="Name").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(form, textvariable=self.name, width=25).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Subject").grid(row=0, column=2, padx=5, pady=5)
        tk.Entry(form, textvariable=self.subject, width=25).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form, text="Class").grid(row=0, column=4, padx=5, pady=5)
        tk.Entry(form, textvariable=self.class_assigned, width=25).grid(row=0, column=5, padx=5, pady=5)

        # Row 1
        tk.Label(form, text="Contact").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(form, textvariable=self.contact, width=25).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Address").grid(row=1, column=2, padx=5, pady=5)
        tk.Entry(form, textvariable=self.address, width=25).grid(row=1, column=3, padx=5, pady=5)

        tk.Label(form, text="Qualification").grid(row=1, column=4, padx=5, pady=5)
        tk.Entry(form, textvariable=self.qualification, width=25).grid(row=1, column=5, padx=5, pady=5)

        # Row 2
        tk.Label(form, text="Salary").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(form, textvariable=self.salary, width=25).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form, text="Date Employed").grid(row=2, column=2, padx=5, pady=5)
        tk.Entry(form, textvariable=self.date_employed, width=25).grid(row=2, column=3, padx=5, pady=5)

        # Buttons
        tk.Button(
            form,
            text="ADD",
            bg="green",
            fg="white",
            command=self.add_teacher
        ).grid(row=3, column=0, padx=5, pady=10)

        tk.Button(
            form,
            text="UPDATE",
            bg="blue",
            fg="white",
            command=self.update_teacher
        ).grid(row=3, column=1, padx=5, pady=10)

        tk.Button(
            form,
            text="DELETE",
            bg="red",
            fg="white",
            command=self.delete_teacher
        ).grid(row=3, column=2, padx=5, pady=10)

        tk.Button(
            form,
            text="CLEAR",
            command=self.clear
        ).grid(row=3, column=3, padx=5, pady=10)

        tk.Button(
            form,
            text="BACK",
            bg="black",
            fg="white",
            command=self.back
        ).grid(row=3, column=4, padx=5, pady=10)

        # ================= TABLE FRAME =================
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Vertical Scrollbar
        scroll_y = ttk.Scrollbar(frame, orient="vertical")
        scroll_y.pack(side="right", fill="y")

        # Horizontal Scrollbar
        scroll_x = ttk.Scrollbar(frame, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")

        # Treeview
        self.tree = ttk.Treeview(
            frame,
            columns=(
                "ID",
                "Name",
                "Subject",
                "Class",
                "Contact",
                "Address",
                "Qualification",
                "Salary",
                "Date Employed"
            ),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        columns = (
            "ID",
            "Name",
            "Subject",
            "Class",
            "Contact",
            "Address",
            "Qualification",
            "Salary",
            "Date Employed"
        )

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Name", width=180)
        self.tree.column("Subject", width=150)
        self.tree.column("Class", width=120)
        self.tree.column("Contact", width=150)
        self.tree.column("Address", width=250)
        self.tree.column("Qualification", width=180)
        self.tree.column("Salary", width=120)
        self.tree.column("Date Employed", width=150)

        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<ButtonRelease-1>", self.select_teacher)

    # ================= ADD =================
    def add_teacher(self):
        conn.execute("""
        INSERT INTO teachers
        (
            name,
            subject,
            class_assigned,
            contact,
            address,
            qualification,
            salary,
            date_employed
        )
        VALUES (?,?,?,?,?,?,?,?)
        """, (
            self.name.get(),
            self.subject.get(),
            self.class_assigned.get(),
            self.contact.get(),
            self.address.get(),
            self.qualification.get(),
            self.salary.get(),
            self.date_employed.get()
        ))

        conn.commit()
        self.load_teachers()
        self.clear()

    # ================= LOAD =================
    def load_teachers(self):
        self.tree.delete(*self.tree.get_children())

        for row in conn.execute("SELECT * FROM teachers"):
            self.tree.insert("", "end", values=row)

    # ================= SELECT =================
    def select_teacher(self, e):
        row = self.tree.item(self.tree.focus(), "values")

        if row:
            self.selected_id = row[0]
            self.name.set(row[1])
            self.subject.set(row[2])
            self.class_assigned.set(row[3])
            self.contact.set(row[4])
            self.address.set(row[5])
            self.qualification.set(row[6])
            self.salary.set(row[7])
            self.date_employed.set(row[8])

    # ================= UPDATE =================
    def update_teacher(self):

        if not self.selected_id:
            return

        conn.execute("""
        UPDATE teachers
        SET
            name=?,
            subject=?,
            class_assigned=?,
            contact=?,
            address=?,
            qualification=?,
            salary=?,
            date_employed=?
        WHERE id=?
        """, (
            self.name.get(),
            self.subject.get(),
            self.class_assigned.get(),
            self.contact.get(),
            self.address.get(),
            self.qualification.get(),
            self.salary.get(),
            self.date_employed.get(),
            self.selected_id
        ))

        conn.commit()
        self.load_teachers()
        self.clear()

    # ================= DELETE =================
    def delete_teacher(self):

        if self.selected_id:
            conn.execute(
                "DELETE FROM teachers WHERE id=?",
                (self.selected_id,)
            )

            conn.commit()
            self.load_teachers()
            self.clear()

    # ================= CLEAR =================
    def clear(self):

        self.name.set("")
        self.subject.set("")
        self.class_assigned.set("")
        self.contact.set("")
        self.address.set("")
        self.qualification.set("")
        self.salary.set("")
        self.date_employed.set("")

        self.selected_id = None

    # ================= BACK =================
    def back(self):
        self.root.destroy()
        open_dashboard()
                

# ================= BURSAR APP =================

class BursarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PAYMENT MANAGEMENT SYSTEM ANGEL NAITBJ®")
        self.root.state("zoomed")
        self.root.configure(bg="#0b1e3a")
        
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS bursar (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           student_id TEXT,
                           name TEXT,
                           class_name TEXT,
                           term TEXT,
                           year TEXT,
                           school_fee REAL,
                           pta_levy REAL,
                           dev_levy REAL,
                           date_paid TEXT,
                           teller_name TEXT,
                           teller_id TEXT
                       )
                       """)
        conn.commit()
        
        # VARIABLES
        self.student_id = tk.StringVar()
        self.name = tk.StringVar()
        self.class_name = tk.StringVar()
        self.term = tk.StringVar(value="First Term")
        self.year = tk.StringVar()

        self.school_fee = tk.StringVar()
        self.pta = tk.StringVar()
        self.dev = tk.StringVar()

        self.date_paid = tk.StringVar()
        self.teller_name = tk.StringVar()
        self.teller_id = tk.StringVar()
        self.search_text = tk.StringVar()

        self.selected_id = None

        self.ui()
        self.load_data()

    # ================= UI =================
    def ui(self):
        tk.Label(
            self.root,
            text="PAYMENT MANAGEMENT SYSTEM ANGEL NAITBJ®",
            font=("Arial", 20, "bold"),
            bg="#1f6aa5",
            fg="white"
        ).pack(fill="x")

        form = tk.LabelFrame(self.root, text=" PAYMENT FORM ",
                             bg="#102542", fg="white")
        form.pack(fill="x", padx=10, pady=10)

        # ROW 1
        tk.Label(form, text="Student ID").grid(row=0, column=0)
        tk.Entry(form, textvariable=self.student_id).grid(row=0, column=1)

        tk.Label(form, text="Name").grid(row=0, column=2)
        tk.Entry(form, textvariable=self.name).grid(row=0, column=3)

        tk.Label(form, text="Class").grid(row=0, column=4)
        tk.Entry(form, textvariable=self.class_name).grid(row=0, column=5)

        # ROW 2
        tk.Label(form, text="Term").grid(row=1, column=0)
        ttk.Combobox(form, textvariable=self.term,
                     values=["First Term", "Second Term", "Third Term"]).grid(row=1, column=1)

        tk.Label(form, text="Year").grid(row=1, column=2)
        tk.Entry(form, textvariable=self.year).grid(row=1, column=3)

        tk.Label(form, text="School Fee").grid(row=1, column=4)
        tk.Entry(form, textvariable=self.school_fee).grid(row=1, column=5)

        # ROW 3
        tk.Label(form, text="PTA Levy").grid(row=2, column=0)
        tk.Entry(form, textvariable=self.pta).grid(row=2, column=1)

        tk.Label(form, text="Dev Levy").grid(row=2, column=2)
        tk.Entry(form, textvariable=self.dev).grid(row=2, column=3)

        tk.Label(form, text="Date Paid").grid(row=2, column=4)
        tk.Entry(form, textvariable=self.date_paid).grid(row=2, column=5)

        # ROW 4
        tk.Label(form, text="Teller Name").grid(row=3, column=0)
        tk.Entry(form, textvariable=self.teller_name).grid(row=3, column=1)

        tk.Label(form, text="Teller ID").grid(row=3, column=2)
        tk.Entry(form, textvariable=self.teller_id).grid(row=3, column=3)

        # ================= BUTTONS =================
        tk.Button(form, text="ADD", bg="green", fg="white",
                  command=self.add_payment).grid(row=4, column=0)

        tk.Button(form, text="UPDATE", bg="blue", fg="white",
                  command=self.update_payment).grid(row=4, column=1)

        tk.Button(form, text="DELETE", bg="red", fg="white",
                  command=self.delete_payment).grid(row=4, column=2)

        tk.Button(form, text="CLEAR", bg="gray", fg="white",
                  command=self.clear).grid(row=4, column=3)

        tk.Button(form, text="BACK", bg="black", fg="white",
                  command=self.back).grid(row=4, column=4)
        # ================= SEARCH & RECEIPTS =================
        tk.Label(form, text="Search").grid(row=5, column=0)
        tk.Entry(form, textvariable=self.search_text).grid(row=5, column=1)

        tk.Button(
            form,
            text="SEARCH",
            bg="orange",
            fg="white",
            command=self.search_payment
        ).grid(row=5, column=2)

        tk.Button(
            form,
            text="VIEW RECEIPT",
            bg="purple",
            fg="white",
            command=self.view_receipt
        ).grid(row=5, column=3)

        tk.Button(
            form,
            text="EXPORT RECEIPT",
            bg="brown",
            fg="white",
            command=self.export_receipt
        ).grid(row=5, column=4)
       

        # ================= TABLE (WITH SCROLLBARS) =================
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True)

        y_scroll = tk.Scrollbar(frame, orient="vertical")
        x_scroll = tk.Scrollbar(frame, orient="horizontal")

        self.tree = ttk.Treeview(
            frame,
            columns=(
                "ID","Student ID","Name","Class","Term","Year",
                "Fee","PTA","Dev","Date","Teller","Teller ID"
            ),
            show="headings",
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )

        y_scroll.config(command=self.tree.yview)
        x_scroll.config(command=self.tree.xview)

        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")

        self.tree.pack(fill="both", expand=True)

        for c in self.tree["columns"]:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120)

        self.tree.bind("<ButtonRelease-1>", self.select_row)

    # ================= ADD =================
    def add_payment(self):
        conn.execute("""
            INSERT INTO bursar VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            self.student_id.get(),
            self.name.get(),
            self.class_name.get(),
            self.term.get(),
            self.year.get(),
            float(self.school_fee.get() or 0),
            float(self.pta.get() or 0),
            float(self.dev.get() or 0),
            self.date_paid.get(),
            self.teller_name.get(),
            self.teller_id.get()
        ))
        conn.commit()
        self.load_data()
        self.clear()
    

    # ================= UPDATE =================
    def update_payment(self):
        if not self.selected_id:
            messagebox.showerror("Error", "Select a record first")
            return

        conn.execute("""
            UPDATE bursar SET
            student_id=?,
            name=?,
            class_name=?,
            term=?,
            year=?,
            school_fee=?,
            pta_levy=?,
            dev_levy=?,
            date_paid=?,
            teller_name=?,
            teller_id=?
            WHERE id=?
        """, (
            self.student_id.get(),
            self.name.get(),
            self.class_name.get(),
            self.term.get(),
            self.year.get(),
            float(self.school_fee.get() or 0),
            float(self.pta.get() or 0),
            float(self.dev.get() or 0),
            self.date_paid.get(),
            self.teller_name.get(),
            self.teller_id.get(),
            self.selected_id
        ))

        conn.commit()
        self.load_data()
        self.clear()

    # ================= LOAD =================
    def load_data(self):
        self.tree.delete(*self.tree.get_children())

        for r in conn.execute("SELECT * FROM bursar"):
            self.tree.insert("", "end", values=r)
      
    # ================= SELECT =================
    def select_row(self, e):
        data = self.tree.item(self.tree.focus(), "values")
        if data:
            self.selected_id = data[0]

            self.student_id.set(data[1])
            self.name.set(data[2])
            self.class_name.set(data[3])
            self.term.set(data[4])
            self.year.set(data[5])
            self.school_fee.set(data[6])
            self.pta.set(data[7])
            self.dev.set(data[8])
            self.date_paid.set(data[9])
            self.teller_name.set(data[10])
            self.teller_id.set(data[11])

    # ================= DELETE =================
    def delete_payment(self):
        if self.selected_id:
            conn.execute("DELETE FROM bursar WHERE id=?", (self.selected_id,))
            conn.commit()
            self.load_data()
            self.clear()
    def search_payment(self):
          keyword = self.search_text.get().strip()

          self.tree.delete(*self.tree.get_children())

          rows = conn.execute("""
              SELECT * FROM bursar
              WHERE student_id LIKE ?
              OR name LIKE ?
              OR class_name LIKE ?
              OR year LIKE ?
          """, (
              f"%{keyword}%",
              f"%{keyword}%",
              f"%{keyword}%",
              f"%{keyword}%"
          ))

          for row in rows:
              self.tree.insert("", "end", values=row)

          if keyword == "":
              self.load_data()
    def view_receipt(self):
       if not self.selected_id:
           messagebox.showerror("Error", "Select a payment first")
           return

       total = (
           float(self.school_fee.get() or 0)
           + float(self.pta.get() or 0)
           + float(self.dev.get() or 0)
       )

       receipt = f"""
   ====================================
            PAYMENT RECEIPT
   ====================================

   Student ID : {self.student_id.get()}
   Name       : {self.name.get()}
   Class      : {self.class_name.get()}
   Term       : {self.term.get()}
   Year       : {self.year.get()}

   School Fee : ₦{self.school_fee.get()}
   PTA Levy   : ₦{self.pta.get()}
   Dev Levy   : ₦{self.dev.get()}

   TOTAL PAID : ₦{total:,.2f}

   Date Paid  : {self.date_paid.get()}

   Teller Name: {self.teller_name.get()}
   Teller ID  : {self.teller_id.get()}

   ====================================
             THANK YOU
   ====================================
   """

       win = tk.Toplevel(self.root)
       win.title("Payment Receipt")
       win.geometry("600x500")
       
       set_icon(win)

       txt = tk.Text(win, font=("Courier New", 11))
       txt.pack(fill="both", expand=True)

       txt.insert("1.0", receipt)   
    def export_receipt(self):
          if not self.selected_id:
              messagebox.showerror("Error", "Select a payment first")
              return

          total = (
              float(self.school_fee.get() or 0)
              + float(self.pta.get() or 0)
              + float(self.dev.get() or 0)
          )

          file = filedialog.asksaveasfilename(
              defaultextension=".txt",
              filetypes=[("Text Files", "*.txt")]
          )

          if not file:
              return

          receipt = f"""
      ====================================
               PAYMENT RECEIPT
      ====================================

      Student ID : {self.student_id.get()}
      Name       : {self.name.get()}
      Class      : {self.class_name.get()}
      Term       : {self.term.get()}
      Year       : {self.year.get()}

      School Fee : ₦{self.school_fee.get()}
      PTA Levy   : ₦{self.pta.get()}
      Dev Levy   : ₦{self.dev.get()}

      TOTAL PAID : ₦{total:,.2f}

      Date Paid  : {self.date_paid.get()}

      Teller Name: {self.teller_name.get()}
      Teller ID  : {self.teller_id.get()}

      ====================================
                THANK YOU
      ====================================
      """

          with open(file, "w", encoding="utf-8") as f:
              f.write(receipt)

          messagebox.showinfo(
              "Success",
              "Receipt exported successfully."
          )
    # ================= CLEAR =================
    def clear(self):
        self.student_id.set("")
        self.name.set("")
        self.class_name.set("")
        self.term.set("First Term")
        self.year.set("")
        self.school_fee.set("")
        self.pta.set("")
        self.dev.set("")
        self.date_paid.set("")
        self.teller_name.set("")
        self.teller_id.set("")
        self.selected_id = None

    # ================= BACK =================
    def back(self):
        self.root.destroy()
        open_dashboard()

# ================= RUN ==============
if __name__ == "__main__":
    root = tk.Tk()
    set_icon(root)
    LoginApp(root)
    root.title("NAVENIE AMS")
    root.mainloop()