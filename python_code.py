import json
import tkinter as tk
from tkinter import messagebox, ttk

# ---------- Data Classes ----------

class Student:
    def __init__(self, name, age, stream, admin_num, birth_date):
        self.name = name
        self.age = age
        self.stream = stream
        self.admin_num = admin_num
        self.birth_date = birth_date

    def to_dict(self):
        return self.__dict__

class Course:
    def __init__(self, name, code, description):
        self.name = name
        self.code = code
        self.description = description

    def to_dict(self):
        return self.__dict__

# ---------- File Handler ----------

class FileHandler:
    @staticmethod
    def save_data(filename, data):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def load_data(filename):
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

# ---------- Admin Backend ----------

class Admin:
    def __init__(self):
        self.students = [Student(**s) for s in FileHandler.load_data("students.json")]
        self.courses = [Course(**c) for c in FileHandler.load_data("courses.json")]

    def add_student(self, student):
        self.students.append(student)
        FileHandler.save_data("students.json", [s.to_dict() for s in self.students])

    def add_course(self, course):
        self.courses.append(course)
        FileHandler.save_data("courses.json", [c.to_dict() for c in self.courses])



# ---------- Main App ----------

class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Student Management System")
        self.admin = Admin()

        self.style_root_window()
        self.login_window()

    def style_root_window(self):
        self.root.geometry("600x400")
        self.root.configure(bg="#f5f5f5")

    # ---------- Login ----------
    def login_window(self):
        self.clear_window()

        frame = tk.Frame(self.root, bg="#333333", padx=20, pady=20, relief="raised", bd=2)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Admin Login", font=("Cooper Black", 16, "bold"), bg="#333333",fg="white").grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(frame, text="USERNAME:",bg="#333333",fg="white",font=("High Tower Text",12,"bold")).grid(row=1, column=0, sticky="e")
        self.username_entry = tk.Entry(frame,font=("Times new Roman",12,"bold"),name="username",fg="blue")
        self.username_entry.grid(row=1, column=1)

        tk.Label(frame, text="PASSWORD:",bg="#333333",fg="white",font=("High Tower Text",12,"bold")).grid(row=2, column=0, sticky="e")
        self.password_entry = tk.Entry(frame, show="*",font=("Times new Roman",12,"bold"),name="password",fg="blue")
        self.password_entry.grid(row=2, column=1)

        tk.Button(frame, text="Login", bg="#4CAF50", fg="white", command=self.verify_login, width=15).grid(row=3, column=0, columnspan=2, pady=10)

    def verify_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "CupidVybz" and password == "Cupid@123":
            self.dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    # ---------- Dashboard ----------
    def dashboard(self):
        self.root.title("Dashboard - Student Management System")
        self.clear_window()

        frame = tk.Frame(self.root, bg="#e1e5ea", padx=20, pady=20)
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="Welcome to Student Management System", font=("High Tower text", 18, "bold"), bg="#e1e5ea").pack(pady=20)

        tk.Button(frame, text="Manage Students", width=25, height=2, bg="#007BFF", fg="white", command=self.student_window).pack(pady=10)
        tk.Button(frame, text="Manage Courses", width=25, height=2, bg="#28a745", fg="white", command=self.course_window).pack(pady=10)
        tk.Button(frame, text="Logout", width=25, height=2, bg="crimson", fg="white", command=self.login_window).pack(pady=10)

    # ---------- Students ----------
    def student_window(self):
        self.clear_window()
        self.root.title("Manage Students")

        frame = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=10)
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="Add Student", font=("High Tower Text", 14, "bold"), bg="#f0f0f0").grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["name", "age", "stream", "admin_num", "birth_date"]
        self.entries = {}
        for i, label in enumerate(labels):
            tk.Label(frame, text=label + ":", bg="#f0f0f0").grid(row=i+1, column=0, sticky="e", pady=2)
            entry = tk.Entry(frame,font=("High Tower Text",12))
            entry.grid(row=i+1, column=1, pady=2)
            self.entries[label.lower().replace(" ", "_")] = entry

        tk.Button(frame, text="Add Student", command=self.add_student, bg="#007BFF", fg="white",font=("High Tower Text",10)).grid(row=6, column=0, columnspan=1, pady=10)
        tk.Button(frame, text="List Students", command=self.list_students_window, bg="#6f42c1", fg="white",font=("High Tower Text",10)).grid(row=6, column=1, columnspan=1, pady=5)
        tk.Button(frame, text="Back", command=self.dashboard, bg="grey", fg="white",font=("High Tower Text",10)).grid(row=6, column=2, columnspan=2, pady=5)

    def add_student(self):
        data = {k: e.get() for k, e in self.entries.items()}
        if all(data.values()):
            if not data["age"].isdigit():
                messagebox.showerror("Error", "Age must be a number.")
                return
            student = Student(**data)
            self.admin.add_student(student)
            for entry in self.entries.values():
                entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Student added.")
        else:
            messagebox.showwarning("Missing Fields", "Please fill all fields.")

    def list_students_window(self):
        top = tk.Toplevel(self.root)
        top.title("List of Students")
        top.geometry("500x400")
        top.config(bg="Blue")

        tk.Label(top, text="All Registered Students", font=("High Tower Text", 14, "bold"), bg="blue").pack(pady=10)

        canvas = tk.Canvas(top, bg="white")
        scrollbar = ttk.Scrollbar(top, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="white")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for idx, s in enumerate(self.admin.students, start=1):
            tk.Label(scroll_frame, text=f"{idx}. {s.name}:,\n Age: {s.age},\n Stream: {s.stream},\n Admin#: {s.admin_num},\n DOB: {s.birth_date}",
                     font=("High Tower Text", 15), bg="white", fg = "black",anchor="w", justify="left", wraplength=460,cursor = "hand2").pack(anchor="w", padx=10, pady=2)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # ---------- Courses ----------
    def course_window(self):
        self.clear_window()
        self.root.title("Manage Courses")

        frame = tk.Frame(self.root, bg="#f9f9f9", padx=10, pady=10)
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="Add Course", font=("High Tower Text", 14, "bold"), bg="#f9f9f9").grid(row=0, column=0, columnspan=2, pady=10)

        self.course_entries = {}
        for i, field in enumerate(["Name", "Code", "Description"]):
            tk.Label(frame, text=field + ":", bg="#f9f9f9").grid(row=i+1, column=0, sticky="e", pady=2)
            entry = tk.Entry(frame,font=("High Tower Text",12))
            entry.grid(row=i+1, column=1, pady=2)
            self.course_entries[field.lower()] = entry

        tk.Button(frame, text="Add Course", command=self.add_course, bg="#28a745", fg="white",font=("High Tower text",11)).grid(row=4, column=0, columnspan=1, pady=10)
        tk.Button(frame, text="List Courses", command=self.list_courses_window, bg="#6f42c1", fg="white",font=("High Tower text",11)).grid(row=4, column=1, columnspan=1, pady=5)
        tk.Button(frame, text="Back", command=self.dashboard, bg="grey", fg="white",font=("High Tower text",11)).grid(row=4, column=2, columnspan=2, pady=5)

    def add_course(self):
        data = {k: e.get() for k, e in self.course_entries.items()}
        if all(data.values()):
            course = Course(**data)
            self.admin.add_course(course)
            for entry in self.course_entries.values():
                entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Course added.")
        else:
            messagebox.showwarning("Missing Fields", "Please fill all fields.")

    def list_courses_window(self):

        top = tk.Toplevel(self.root)
        top.title("List of Courses")
        top.geometry("500x500")
        top.config(bg="white")

        tk.Label(top, text="All Courses", font=("High Tower Text", 15, "bold"), bg="blue").pack(pady=10)

        canvas = tk.Canvas(top, bg="white")
        scrollbar = ttk.Scrollbar(top, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="white")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for idx, c in enumerate(self.admin.courses, start=1):
            tk.Label(scroll_frame,
                     text=f"{idx}. {c.name}:\n Code: ({c.code})\n Code_Description: {c.description}", bg="white",
                     font=("High Tower Text", 15), fg="black", anchor="w", justify="left", wraplength=460,
                     cursor="hand2").pack(anchor="w", padx=10, pady=2)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    # ---------- Helpers ----------
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# ---------- Run ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementApp(root)
    root.mainloop()
