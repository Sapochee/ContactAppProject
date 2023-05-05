import tkinter
import sqlite3
import re
import json

class LoginApplication():
    """Class to create the gui
    """
    def __init__(self, window):
        self.window = window
        self.window.title("Contact Book")

        self.label_username = tkinter.Label(window, text = "Username")
        self.label_username.grid(row = 0, column = 0)

        self.entry_username = tkinter.Entry(window)
        self.entry_username.grid(row = 0, column = 1)

        self.label_password = tkinter.Label(window, text = "Password")
        self.label_password.grid(row = 1, column = 0)

        self.entry_password = tkinter.Entry(window, show = "*")
        self.entry_password.grid(row = 1, column = 1)

        self.button_login = tkinter.Button(window, text = "Login", command = User.login())
        self.button_login.grid(row = 2, column = 0)

        self.button_signup = tkinter.Button(window, text = "Sign Up", command = User.signUp())
        self.button_signup.grid(row = 2, column = 1)
    
    def createWidgets(self):
        pass    
    
class User:
    """Defines the user account with a login information and the corresponding address book for the account
    """
    def __init__(self):
        pass
    
    def login(self, username, password):
        """Checks to see if username and password match to any existing user"""
        f = open('users.json', 'r')
        data = json.loads(f.read())
        for login in data['logins']:
            if login['username'] == username and login['password'] == password:
                self.window.destroy()
                root = tkinter.TK()
                contactGUI = BookGUI(root)
                root.mainloop()
            else:
                tkinter.messagebox.showerror("Error", "Incorrect username or Password")        
    
    def signUp(self, username, password):
        """Registers the login information into database unless username already exists
        """
        with open('users.json') as f:
            data = json.loads(f.read())
        newUser = {"username": username, "password": password, "addressBook": []}
        for login in data['logins']:
            if login['username'] == username:
                return None
        data['logins'].append(newUser)
        with open('users.json', 'w') as f:
           json.dump(data,f, indent=2)
           
class BookGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Contact Book")
        
    def widgets(self):
        pass

class Contact:
    """Defines an individual contact and the details that are included in the contact"""
    def __init__(self, FirstName, LastName, number, address, email):
        self.FirstName = FirstName
        self.LastName = LastName
        self.number = number
        self.address = address
        self.email = email
    
    def add_contact(self, contact):
        """Adds a contact to the list"""
        contact.append(self)
    
    def edit_contact(self, contact, field, value):
        """Edit a field of the contact with a new value"""
        if field  == 'FirstName':
            self.FirstName = value
        elif field == 'LastName':
            self.LastName = value
        elif field == 'number':
            self.number = value
        elif field == 'address':
            self.number = value
        elif field == 'email':
            self.email = value
    
    def delete_contact(self, contact):
        """Delete the contact"""
        contact.remove(self)
    
    def search_contact(self, query):
        """Return True if the contact matches the query, False otherwise"""
        return (query in self.first_name or query in self.last_name or
                query in self.number or query in self.address or
                query in self.email)
    
    pass

class AddressBook:
    """Collection of contacts that belong to the corresponding user
    """
    def __init__(self):
        pass
    
    def sync_addressBook():
        pass
    
    pass

def parse_input():
    """Parses and matches the user input for searching contacts
    """
    pass

def load_data():
    """Loads the address book from a data source corresponding to user
    """
    pass

def save_data():
    """Saves the address book to a data source corresponding to user
    """
    pass

def main():
    pass

root = tkinter.Tk()
gui = LoginApplication(root)
root.mainloop()

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
