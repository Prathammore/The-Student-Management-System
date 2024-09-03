import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# Database Connection
conn = sqlite3.connect('data12.db')
c = conn.cursor()

# Functionality
def add_entry():
    def save_entry():
        rollno = entry1.get()
        name = entry2.get()
        marks1 = entry3.get()
        marks2 = entry4.get()
        marks3 = entry5.get()
        
        if rollno and name and marks1 and marks2 and marks3:
            try:
                c.execute("INSERT INTO entries (rollno, name, marks1, marks2, marks3) VALUES (?, ?, ?, ?, ?)",
                          (rollno, name, marks1, marks2, marks3))
                conn.commit()
                messagebox.showinfo("Success", "Entry added successfully")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Roll number already exists")
        else:
            messagebox.showwarning("Input Error", "All fields must be filled out")
    
    def go_back():
        add_window.destroy()
    
    add_window = tk.Toplevel(root)
    add_window.title("Add Entry")
    add_window.geometry('700x700')

    tk.Label(add_window, text="Enter Rollno:").place(x=100, y=100)
    tk.Label(add_window, text="Enter Name:").place(x=100, y=150)
    tk.Label(add_window, text="Enter sub Marks 1:").place(x=100, y=200)
    tk.Label(add_window, text="Enter sub Marks 2:").place(x=100, y=250)
    tk.Label(add_window, text="Enter sub Marks 3:").place(x=100, y=300)

    entry1 = tk.Entry(add_window)
    entry2 = tk.Entry(add_window)
    entry3 = tk.Entry(add_window)
    entry4 = tk.Entry(add_window)
    entry5 = tk.Entry(add_window)

    entry1.place(x=250, y=100, width=200)
    entry2.place(x=250, y=150, width=200)
    entry3.place(x=250, y=200, width=200)
    entry4.place(x=250, y=250, width=200)
    entry5.place(x=250, y=300, width=200)

    tk.Button(add_window, text="Save", command=save_entry, width=20, height=2).place(x=150, y=400)
    tk.Button(add_window, text="Back", command=go_back, width=20, height=2).place(x=350, y=400)

def view_entries():
    def go_back():
        view_window.destroy()

    view_window = tk.Toplevel(root)
    view_window.title("View Entries")
    view_window.geometry('700x700')

    # Create Treeview
    tree = ttk.Treeview(view_window, columns=("Rollno", "Name", "Marks1", "Marks2", "Marks3"), show='headings')
    tree.heading("Rollno", text="Roll No")
    tree.heading("Name", text="Name")
    tree.heading("Marks1", text="Marks 1")
    tree.heading("Marks2", text="Marks 2")
    tree.heading("Marks3", text="Marks 3")
    
    # Set column widths
    tree.column("Rollno", width=100)
    tree.column("Name", width=150)
    tree.column("Marks1", width=100)
    tree.column("Marks2", width=100)
    tree.column("Marks3", width=100)

    # Fetch data from the database and insert into Treeview
    c.execute("SELECT * FROM entries")
    rows = c.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    
    tree.place(x=50, y=50, width=600, height=500)

    # Back button
    tk.Button(view_window, text="Back", command=go_back, width=20, height=2).place(relx=0.5, y=600, anchor=tk.CENTER)

def update_entry():
    update_window = tk.Toplevel(root)
    update_window.title("Update Entry")
    update_window.geometry('700x700')

    tk.Label(update_window, text="Enter Rollno to update").place(x=100, y=100)
    entry_rollno = tk.Entry(update_window)
    entry_rollno.place(x=300, y=100, width=200)

    def load_entry():
        rollno_value = entry_rollno.get()
        c.execute("SELECT * FROM entries WHERE rollno=?", (rollno_value,))
        row = c.fetchone()
        if row:
            entry2.delete(0, tk.END)
            entry3.delete(0, tk.END)
            entry4.delete(0, tk.END)
            entry5.delete(0, tk.END)
            entry2.insert(0, row[1])
            entry3.insert(0, row[2])
            entry4.insert(0, row[3])
            entry5.insert(0, row[4])
        else:
            messagebox.showerror("Error", "Entry not found")

    def save_update():
        name = entry2.get()
        marks1 = entry3.get()
        marks2 = entry4.get()
        marks3 = entry5.get()
        rollno_value = entry_rollno.get()
        
        c.execute("UPDATE entries SET name=?, marks1=?, marks2=?, marks3=? WHERE rollno=?",
                  (name, marks1, marks2, marks3, rollno_value))
        conn.commit()
        messagebox.showinfo("Success", "Entry updated successfully")

    tk.Button(update_window, text="Load Entry", command=load_entry, width=20, height=2).place(x=200, y=150)
    
    tk.Label(update_window, text="Enter Name:").place(x=100, y=200)
    tk.Label(update_window, text="Enter sub Marks 1:").place(x=100, y=250)
    tk.Label(update_window, text="Enter sub Marks 2:").place(x=100, y=300)
    tk.Label(update_window, text="Enter sub Marks 3:").place(x=100, y=350)

    entry2 = tk.Entry(update_window)
    entry3 = tk.Entry(update_window)
    entry4 = tk.Entry(update_window)
    entry5 = tk.Entry(update_window)

    entry2.place(x=300, y=200, width=200)
    entry3.place(x=300, y=250, width=200)
    entry4.place(x=300, y=300, width=200)
    entry5.place(x=300, y=350, width=200)

    tk.Button(update_window, text="Save", command=save_update, width=20, height=2).place(x=150, y=450)
    tk.Button(update_window, text="Back", command=update_window.destroy, width=20, height=2).place(x=350, y=450)

def delete_entry():
    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Entry")
    delete_window.geometry('700x700')

    tk.Label(delete_window, text="Enter Rollno to delete").place(x=100, y=100)
    entry_rollno = tk.Entry(delete_window)
    entry_rollno.place(x=300, y=100, width=200)

    def delete():
        rollno_value = entry_rollno.get()
        c.execute("DELETE FROM entries WHERE rollno=?", (rollno_value,))
        conn.commit()
        messagebox.showinfo("Success", "Entry deleted successfully")

    tk.Button(delete_window, text="Delete", command=delete, width=20, height=2).place(x=150, y=200)
    tk.Button(delete_window, text="Back", command=delete_window.destroy, width=20, height=2).place(x=350, y=200)

# Main Window
root = tk.Tk()
root.title("Student Database Manager")
root.geometry('700x700')

tk.Button(root, text="Add", command=add_entry, width=20, height=2).place(relx=0.5, rely=0.3, anchor=tk.CENTER)
tk.Button(root, text="View", command=view_entries, width=20, height=2).place(relx=0.5, rely=0.4, anchor=tk.CENTER)
tk.Button(root, text="Update", command=update_entry, width=20, height=2).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
tk.Button(root, text="Delete", command=delete_entry, width=20, height=2).place(relx=0.5, rely=0.6, anchor=tk.CENTER)

root.mainloop()

conn.close()
