from tkinter import *
import tkinter as tk
import json
import re

LARGE_FONT= ("Verdana", 18)

class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)
       
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, LoginPage, SignUpPage, AddressBook):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.username = self.frames[LoginPage].username_entry.get()
        frame.tkraise()
        
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Contact Book", font=LARGE_FONT)
        label.pack(pady=20,padx=10)
        
        button = tk.Button(self, text="Log-In", command=lambda: controller.show_frame(LoginPage))
        button.pack()
        
        button2 = tk.Button(self, text="Sign-Up", command=lambda: controller.show_frame(SignUpPage))
        button2.pack()
    
class LoginPage(tk.Frame):
    """Defines the user account with a login information and the corresponding address book for the account
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Enter login information:", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5, padx=10)

        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.pack(pady=5, padx=10)
        
        login_button = tk.Button(self, text="Login", command=self.login)
        login_button.pack(pady=5, padx=10)
        
        alt_button = tk.Button(self, text="Sign-Up Page", command=lambda: controller.show_frame(SignUpPage))
        alt_button.pack()
    
    def login(self):
        """Checks to see if username and password match to any existing user"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        try:
            with open('users.json', 'r') as f:
                data = json.loads(f.read())
        except FileNotFoundError:
            error_label = tk.Label(self, text="Error: the user database file was not found.")
            error_label.pack(pady=5, padx=10)
            return
        except json.JSONDecodeError:
            error_label = tk.Label(self, text="Error: the user database file contains invalid data.")
            error_label.pack(pady=5, padx=10)
            return
        
        for login in data["logins"]:
            if login["username"] == username and login["password"] == password:
                self.controller.frames[AddressBook].username_entry = self.username_entry
                self.controller.show_frame(AddressBook)
                return

        # login failed, show an error message
        error_label = tk.Label(self, text="Incorrect username or password.")
        error_label.pack(pady=5, padx=10)     
            
class SignUpPage(tk.Frame):  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Enter registration information:", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5, padx=10)

        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.pack(pady=5, padx=10)
        
        signUp_button = tk.Button(self, text="Sign Up", command=self.signUp)
        signUp_button.pack(pady=5, padx=10)
        
        alt_button = tk.Button(self, text="Log-In Page", command=lambda: controller.show_frame(LoginPage))
        alt_button.pack()
        
    def signUp(self):
        """Registers the login information into database unless username already exists
        """
        with open('users.json', 'r') as f:
            data = json.loads(f.read())
            
        username = self.username_entry.get()
        password = self.password_entry.get()
            
        for login in data['logins']:
            if login['username'] == self.username_entry.get():
                error_label = tk.Label(self, text="Username already exists.")
                error_label.pack(pady=5, padx=10)
                return
                        
        newUser = {"username": username, "password": password, "addressBook": []}
        data['logins'].append(newUser)
        
        with open('users.json', 'w') as f:
           json.dump(data, f, indent=2)
           
        success_label = tk.Label(self, text="User created successfully.")
        success_label.pack(pady=5, padx=10)

class AddressBook(tk.Frame):
    """Collection of contacts that belong to the corresponding user
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Contacts", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        self.contact_list = tk.Listbox(self)
        self.contact_list.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(self, orient="vertical")
        scrollbar.config(command=self.contact_list.yview)
        scrollbar.pack(side="right", fill="y")
        self.contact_list.config(yscrollcommand=scrollbar.set)
        
        add_button = tk.Button(self, text="Add Contact", command=self.add_contact)
        add_button.pack(side="top", pady=10)
        edit_button = tk.Button(self, text="Edit Contact", command=self.edit_contact)
        edit_button.pack(side="top", pady=10)
        delete_button = tk.Button(self, text="Delete Contact", command=self.delete_contact)
        delete_button.pack(side="top", pady=10)
        home = tk.Button(self, text="Home", command=lambda: controller.show_frame(StartPage))
        home.pack(side="top", pady=10)
        
        self.sync_contacts()
        
    def sync_contacts(self):
        """ Load the user's address book from the database
        """
        username = self.controller.frames[LoginPage].username_entry.get()
        try:
            with open('users.json', 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            error_label = tk.Label(self, text="Error: user database file was not found.")
            error_label.pack(pady=5, padx=10)
            return
        except json.JSONDecodeError:
            error_label = tk.Label(self, text="Error: user database file contains invalid data.")
            error_label.pack(pady=5, padx=10)
            return
        
        address_book = None
        for login in data["logins"]:
            if login["username"] == username:
                address_book = login["addressBook"]
                self.contacts_listbox.delete(0, tk.END)
                for contact in address_book:
                    self.contacts_listbox.insert(tk.END, f"{contact['first_name']} {contact['last_name']}")
                break
            
        if address_book is None:
            error_label = tk.Label(self, text="Error: Address book not found.")
            error_label.pack(pady=5, padx=10)
            return

        self.contact_list.delete(0, tk.END)
        
        # Add each contact to the listbox
        for contact in address_book:
            self.contact_list.insert(tk.END, f"Name: {contact['name']}, Phone: {contact['phone_number']}")

    def add_contact(self):
        """Adds a new contact"""
        name = input("Enter the name of the contact: ")
        phone_number = input("Enter the phone number of the contact: ")
        email = input("Enter the email of the contact: ")
        new_contact = {"name": name, "phone_number": phone_number}
        username = self.controller.frames[LoginPage].username_entry.get()
        
        with open('users.json', 'r') as f:
            data = json.load(f)

        for login in data["logins"]:
            if login["username"] == username:
                login["addressBook"].append(new_contact)
                break

        with open('users.json', 'w') as f:
            json.dump(data, f, indent=2)

        self.sync_contacts()

        
    def edit_contact(self):
        """Edits an existing contact"""
        selected_contact = self.contact_list.get(tk.ACTIVE)
        username = self.controller.frames[LoginPage].username_entry.get()

        name, phone_number = selected_contact.split(", ")
        name = name.split(": ")[1]
        phone_number = phone_number.split(": ")[1]
        new_name = input(f"Enter a new name for {name}: ")
        new_phone_number = input(f"Enter a new phone number for {name}: ")

        with open('users.json', 'r') as f:
            data = json.load(f)

        for login in data["logins"]:
            if login["username"] == username:
                address_book = login["addressBook"]
                for contact in address_book:
                    if contact["name"] == name and contact["phone_number"] == phone_number:
                        if new_name:
                            contact["name"] = new_name
                        if new_phone_number:
                            contact["phone_number"] = new_phone_number
                        break
                break

        with open('users.json', 'w') as f:
            json.dump(data, f, indent=2)

        self.sync_contacts()

    def delete_contact(self):
        """Deletes an existing contact"""
        selected_contact = self.contact_list.get(tk.ACTIVE)
        username = self.controller.frames[LoginPage].username_entry.get()
        name, phone_number = selected_contact.split(", ")
        name = name.split(": ")[1]
        phone_number = phone_number.split(": ")[1]

        with open('users.json', 'r') as f:
            data = json.load(f)

        for login in data["logins"]:
            if login["username"] == username:
                address_book = login["addressBook"]
                for contact in address_book:
                    if contact["name"] == name and contact["phone_number"] == phone_number:
                        address_book.remove(contact)
                        break
                break

        with open('users.json', 'w') as f:
            json.dump(data, f, indent=2)

        self.sync_contacts()

    def parse_input(self):
        """Parses and matches the user input for searching contacts
        """
        query = self.search_entry.get()
        username = self.controller.frames[StartPage].username_entry.get()
        result = []

        with open('users.json', 'r') as f:
            data = json.load(f)

        for login in data["logins"]:
            if login["username"] == username:
                address_book = login["addressBook"]
                for contact in address_book:
                    if query.lower() in contact["name"].lower() or query.lower() in contact["phone_number"].lower():
                        result.append(contact)
                break

        # Clear the listbox
        self.contact_list.delete(0, tk.END)

        # Add each matching contact to the listbox
        for contact in result:
            self.contact_list.insert(tk.END, f"Name: {contact['name']}, Phone: {contact['phone_number']}")

if __name__ == "__main__":
    app = Main()
    app.mainloop()
    
######################### TESTS ######################### 

def test_valid_login():
    app = Main()
    app.frames[LoginPage].username_entry.insert(0, "valid_username")
    app.frames[LoginPage].password_entry.insert(0, "valid_password")
    app.frames[LoginPage].login()
    assert app.frames[LoginPage].username_entry.get() == "valid_username"
    assert isinstance(app.frames[AddressBook], AddressBook)

def test_invalid_login():
    app = Main()
    app.frames[LoginPage].username_entry.insert(0, "invalid_username")
    app.frames[LoginPage].password_entry.insert(0, "invalid_password")
    app.frames[LoginPage].login()
    assert isinstance(app.frames[LoginPage].winfo_children()[-1], tk.Label)

def test_sign_up_new_username():
    app = Main()
    app.frames[SignUpPage].username_entry.insert(0, "new_username")
    app.frames[SignUpPage].password_entry.insert(0, "new_password")
    app.frames[SignUpPage].signUp()
    assert isinstance(app.frames[SignUpPage].winfo_children()[-1], tk.Label)

def test_sign_up_existing_username():
    app = Main()
    app.frames[SignUpPage].username_entry.insert(0, "existing_username")
    app.frames[SignUpPage].password_entry.insert(0, "existing_password")
    app.frames[SignUpPage].signUp()
    assert isinstance(app.frames[SignUpPage].winfo_children()[-1], tk.Label)

test_valid_login()
test_invalid_login()
test_sign_up_new_username()
test_sign_up_existing_username()