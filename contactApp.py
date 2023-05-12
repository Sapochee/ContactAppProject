from tkinter import *
import tkinter as tk
import json

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
        try:
            with open('users.json', 'r') as f:
                data = json.loads(f.read())
        except FileNotFoundError:
            # show an error message if the file is not found
            error_label = tk.Label(self, text="Error: the user database file was not found.")
            error_label.pack(pady=5, padx=10)
            return
        except json.JSONDecodeError:
            # show an error message if the file is not valid JSON
            error_label = tk.Label(self, text="Error: the user database file contains invalid data.")
            error_label.pack(pady=5, padx=10)
            return

        # check if the username and password match
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        for login in data["logins"]:
            if login["username"] == username and login["password"] == password:
                self.controller.show_frame(AddressBook)

        # login failed, show an error message
        error_label = tk.Label(self, text="Incorrect username or password.")
        error_label.pack(pady=5, padx=10)     
            
class SignUpPage(tk.Frame):  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Enter registration information:", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        self.username = tk.Entry(self)
        self.username.pack(pady=5, padx=10)

        self.password = tk.Entry(self, show='*')
        self.password.pack(pady=5, padx=10)
        
        signUp_button = tk.Button(self, text="Sign Up", command=self.signUp)
        signUp_button.pack(pady=5, padx=10)
        
        alt_button = tk.Button(self, text="Log-In Page", command=lambda: controller.show_frame(LoginPage))
        
        alt_button.pack()
        
    def signUp(self):
        """Registers the login information into database unless username already exists
        """
        with open('users.json', 'r') as f:
            data = json.loads(f.read())
            
        newUser = {"username": self.username.get(), "password": self.password.get(), "addressBook": []}
        for login in data['logins']:
            if login['username'] == self.username.get():
                return None
        data['logins'].append(newUser)
        with open('users.json', 'w') as f:
           json.dump(data,f, indent=2)
           
        success_label = tk.Label(self, text="User created successfully.")
        success_label.pack(pady=5, padx=10)

class Contact:
    """A contact in an address book"""
    def __init__(self, name, phone_number, email):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        
    def __str__(self):
        return f"Name: {self.name}, Phone: {self.phone_number}, Email: {self.email}"
        
    def add_contact():
        """Adds a new contact"""
        name = input("Enter the name of the contact: ")
        phone_number = input("Enter the phone number of the contact: ")
        email = input("Enter the email of the contact: ")
        new_contact = Contact(name, phone_number, email)
        address_book = AddressBook.get_instance()
        address_book.add_contact(new_contact)
        
    def edit_contact():
        """Edits an existing contact"""
        name = input("Enter the name of the contact to edit: ")
        address_book = AddressBook.get_instance()
        contact = address_book.get_contact_by_name(name)
        if contact:
            print(f"Editing contact: {contact}")
            new_name = input(f"Enter a new name for {name} (or press enter to keep as {name}): ")
            new_phone_number = input(f"Enter a new phone number for {name} (or press enter to keep as {contact.phone_number}): ")
            new_email = input(f"Enter a new email for {name} (or press enter to keep as {contact.email}): ")
            if new_name:
                contact.name = new_name
            if new_phone_number:
                contact.phone_number = new_phone_number
            if new_email:
                contact.email = new_email
            address_book.save()
        else:
            print(f"Contact {name} not found.")

    def delete_contact():
        """Deletes an existing contact"""
        name = input("Enter the name of the contact to delete: ")
        address_book = AddressBook.get_instance()
        contact = address_book.get_contact_by_name(name)
        if contact:
            print(f"Deleting contact: {contact}")
            address_book.delete_contact(contact)
            address_book.save()
        else:
            print(f"Contact {name} not found.")
    pass

class AddressBook(tk.Frame):
    """Collection of contacts that belong to the corresponding user
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Contacts", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        # Create a listbox to display the contacts
        self.contact_list = tk.Listbox(self)
        self.contact_list.pack(side="left", fill="both", expand=True)
        
        # Create a scrollbar for the listbox
        scrollbar = tk.Scrollbar(self, orient="vertical")
        scrollbar.config(command=self.contact_list.yview)
        scrollbar.pack(side="right", fill="y")
        self.contact_list.config(yscrollcommand=scrollbar.set)
        
        # Create buttons to add, edit and delete contacts
        add_button = tk.Button(self, text="Add Contact", command=Contact.add_contact)
        add_button.pack(side="top", pady=10)
        edit_button = tk.Button(self, text="Edit Contact", command=Contact.edit_contact)
        edit_button.pack(side="top", pady=10)
        delete_button = tk.Button(self, text="Delete Contact", command=Contact.delete_contact)
        delete_button.pack(side="top", pady=10)
        home = tk.Button(self, text="Home", command=lambda: controller.show_frame(StartPage))
        home.pack(side="top", pady=10)
        
        # Load the contacts from the user's address book
        self.sync_contacts()
        
    def sync_contacts(self):
        """ Load the user's address book from the database
        """
        with open('users.json', 'r') as f:
            data = json.load(f)

    def parse_input():
        """Parses and matches the user input for searching contacts
        """
        pass

app = Main()
app.mainloop()

#Tests to implement
"""
Pseudocode for future possible tests:

A test for login function to see if it accesses the proper address book
    login(username, password)
    user.login.addressbook = this.addressbook

Testing the add_contact function
    add_contact(Tom, Sawyer)
    Use regex to see if Tom Sawyer is in the addressbook

Testing the edit_contact function
    edit_contact(Tom, Bob)
    Use regex to see if Tom Sawyer is still in addressbook
    Use Regex to see if Tom Bob is in addressbook

Testing the delete_contact function
    delete_contact(Tom, Bob)
    Use regex to see if tom Bob is still in addressbook
"""
