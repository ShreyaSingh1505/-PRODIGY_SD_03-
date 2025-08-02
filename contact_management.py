import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# Contact data storage
FILE_NAME = "contacts.json"

def load_contacts():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return {}

def save_contacts():
    with open(FILE_NAME, "w") as file:
        json.dump(contacts, file, indent=4)

def add_contact():
    name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    email = entry_email.get().strip()

    if not name or not phone or not email:
        messagebox.showwarning("Missing Details", "Please fill in all the fields.")
        return

    contacts[name] = {"phone": phone, "email": email}
    save_contacts()
    refresh_contact_list()

    messagebox.showinfo("Contact Added ", f"{name} has been added to your contacts!")
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)

def view_contact():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("No Contact Selected", "Please select a contact to view.")
        return

    name = listbox.get(selected)
    info = contacts.get(name)
    messagebox.showinfo(f"👤 {name}", f"📞 Phone: {info['phone']}\n✉️ Email: {info['email']}")

def edit_contact():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("No Selection", "Please choose a contact to edit.")
        return

    name = listbox.get(selected)
    contact = contacts[name]

    new_phone = simpledialog.askstring("Edit Phone", f"Update phone for {name}:", initialvalue=contact["phone"])
    new_email = simpledialog.askstring("Edit Email", f"Update email for {name}:", initialvalue=contact["email"])

    if new_phone and new_email:
        contacts[name] = {"phone": new_phone, "email": new_email}
        save_contacts()
        messagebox.showinfo("Updated 🎉", f"{name}'s details have been updated.")

def delete_contact():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("No Selection", "Please choose a contact to delete.")
        return

    name = listbox.get(selected)
    confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {name}?")
    if confirm:
        del contacts[name]
        save_contacts()
        refresh_contact_list()
        messagebox.showinfo("Deleted", f"{name} has been removed.")

def refresh_contact_list():
    listbox.delete(0, tk.END)
    for name in sorted(contacts.keys()):
        listbox.insert(tk.END, name)

# Main App Window
root = tk.Tk()
root.title("Personal Contact Manager")
root.geometry("430x510")
root.configure(bg="#f8f9fa")
root.resizable(False, False)

contacts = load_contacts()

# 🧾 Entry Frame
entry_frame = tk.Frame(root, bg="#f8f9fa")
entry_frame.pack(pady=10)

tk.Label(entry_frame, text="Full Name:", bg="#f8f9fa", anchor="w").grid(row=0, column=0, sticky="w", pady=2)
entry_name = tk.Entry(entry_frame, width=35)
entry_name.grid(row=0, column=1, pady=2)

tk.Label(entry_frame, text="Phone Number:", bg="#f8f9fa", anchor="w").grid(row=1, column=0, sticky="w", pady=2)
entry_phone = tk.Entry(entry_frame, width=35)
entry_phone.grid(row=1, column=1, pady=2)

tk.Label(entry_frame, text="Email Address:", bg="#f8f9fa", anchor="w").grid(row=2, column=0, sticky="w", pady=2)
entry_email = tk.Entry(entry_frame, width=35)
entry_email.grid(row=2, column=1, pady=2)

tk.Button(root, text="Add Contact", width=30, bg="#28a745", fg="white", font=("Segoe UI", 10, "bold"), command=add_contact).pack(pady=10)

# 📜 Contact List Frame
list_frame = tk.Frame(root, bg="#f8f9fa")
list_frame.pack(fill=tk.BOTH, expand=True, padx=15)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(list_frame, height=10, width=50, font=("Segoe UI", 10), yscrollcommand=scrollbar.set)
listbox.pack(side=tk.LEFT, fill=tk.BOTH)
scrollbar.config(command=listbox.yview)

# 🔧 Button Controls
button_frame = tk.Frame(root, bg="#f8f9fa")
button_frame.pack(pady=10)

tk.Button(button_frame, text="👁️ View", width=12, command=view_contact).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="✏️ Edit", width=12, command=edit_contact).grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="🗑️ Delete", width=12, command=delete_contact).grid(row=0, column=2, padx=5, pady=5)

# Start with loaded contacts
refresh_contact_list()

# Run app
root.mainloop()
