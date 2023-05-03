import tkinter
import sqlite3
import re
import json

class Application():
    """Class to create the gui
    """
    def __init__(self):
        pass
    
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
                return login
        return None
        
    
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

class Contact:
    """Defines an individual contact and the details that are included in the contact
    """
    def __init__(self, FirstName, LastName, number, address, email):
        self.FirstName = FirstName
        self.LastName = LastName
        self.number = number
        self.address = address
        self.email = email
    
    def add_contact():
        pass
    
    def edit_contact():
        pass
    
    def delete_contact():
        pass
    
    def search_contact():
        pass
    
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