#
# Address Book Manager
#
# A simple program that creates and manages an address book.
# Names, phone numbers, etc. are saved as a pickle data file.
#
# Joshua Ferdaszewski
# PDX Code Guild Student - January 8, 2015
#

# TODO: Add ability to enter arbitrary keys for specific contacts
# TODO: PEP 8 style guide adjustments

import sys
import re
import cPickle

# Program settings
file_name = "./contacts.dat" # File name for data
entry_types = ('Name', 'Phone Number', 'Email', 'Street Address', 'City', 
    'State', 'Zipcode') # Default list of address book fields. DO NOT CHANGE!

def display():
    # Open file and read into memory
    address_book = loadfile()
    clear()

    # Display names only or complete address book?
    if raw_input("Display a list of names only? y/n: ") in ('y', 'Y'):
        clear()
        print "\t\tAddress Book: Names List\n\n"
        print "\n".join(sorted(address_book.keys()))

    # Print entire address book to screen in alpha order
    else:
        clear()
        print "\t\tAddress Book: All Contacts\n"
        for name in sorted(address_book.keys()):
            print_contact(address_book[name])
    pause()


def print_contact(contact):
    # Display a contact's information line by line
    print ""
    for entry in entry_types:
        print "%-14s : %s" % (entry, contact[entry])

def find():
    # Load address book
    address_book = loadfile()
        
    # Loop untill user has only one name or gives up
    clear()
    while True:
        query = raw_input("\nEnter contact name: ")

        # Find partial matches
        names_match = []
        for name in sorted(address_book.keys()):

            # compare lower case strings
            if len(re.findall(query.lower(), name.lower())) > 0:
                names_match.append(name)

        # We found a match!
        if query in address_book:
            print "\n:)"
            print_contact(address_book[query])
            pause()
            break

        # Display partial matches
        elif len(names_match) > 0:
            print "Did you mean?\n"
            for name in names_match:
                print name
            print "\nType name exactly as it appears above."
            continue    

        # Name not found and no match
        else:
            print "\n:(\t%s is NOT a contact in your address book." % (query)

            # Try again?
            if not raw_input("Try again? y/n: ") in ('y', 'Y'):
                break
    return query


def delete():
    # Find user name to delete
    name = find()
    address_book = loadfile()

    # Verify that this entry should be removed
    if raw_input("Delete %s? (y/n): " % (name)) in ('y', 'Y'):
        
        # Remove and write to file
        del address_book[name]
        writefile(address_book)
        print "Removed %s from address book." % name
    else:
        print "Delete aborted", name, "NOT removed."
    pause()


def add():
    # Open file and load address book
    address_book = loadfile()

    # Continue while user is entering new contacts
    while True:
        
        # Gather information about new contact
        clear()        
        print "Enter information for your new contact."
        new_contact = {}
        for entry in entry_types:
            new_contact[entry] = raw_input("Enter %s: " % entry)

        # Check if name exists already
        if new_contact["Name"] in address_book:
            print "\nThis contact alread in address book!"
            print_contact(new_contact)

            # If it does, update this existing contact?
            if not raw_input("\nUpdate %s with contact info above? y/n: " 
                % new_contact["Name"]) in ('y', 'Y'):
                break

        # Add the new contact to the address book
        address_book[new_contact["Name"]] = new_contact

        # Do it again?
        if not raw_input("\nAdd another name? y/n: ") in ('y', 'Y'):
            break

    # Write updated address book to file
    writefile(address_book)


def delete_all():
    # Clear screen and verify that user wants to remove entire address book
    clear()
    print "Delete entire Address Book?\nThis cannot be undone!"
    if raw_input("Delete all contacts from Address Book? y/n: ") in ('y', 'Y'):
        os.remove(file_name)
        print "All contacts deleted"
    else:
        print "Delete aborted.  Contacts NOT removed."
    pause()



def loadfile():    
    # Open address file, create it if needed
    f = open(file_name, 'a+')
    
    # Read file into memory, if a file is empty, create and empty dict
    try:
        address_data = cPickle.load(f)
    except(ValueError, EOFError):
        address_data = {}

    # Close file and return the address book
    f.close()
    return address_data


def writefile(address_data):
    # open file to overwrite
    f =  open(file_name, 'w')

    # Write the address book to file as pickle data
    cPickle.dump(address_data, f)

    # Close file
    f.close()


def pause():
    raw_input ("\nPress Enter")


def clear():
    # Clear screen, return cursor to top left
    # Thank you to Graham King http://www.darkcoding.net/
    # For this code snippit
    sys.stdout.write('\033[2J')
    sys.stdout.write('\033[H')
    sys.stdout.flush()


def menu():
    # clear terminal then display menu
    clear()
    sel = None
    print "\t  Welcome to ADDRESS BOOK!\n\n"
    print "\t1) List All Contacts"
    print "\t2) Find Contact by Name"
    print "\t3) Add Contact"
    print "\t4) Remove a contact"
    print "\t5) Delete All contacts"
    print "\t6) Quit\n\n"

    # Wait for valid user input
    while sel not in ('1', '2', '3', '4', '5', '6'):   
        sel = raw_input("Select an option: ")

    # Return valid menu selection
    return sel


def main():
    # Display menu and wait for user selection
    while True:
        selection = menu()
        if selection == '1':
            display()
        elif selection == '2':
            find()
        elif selection == '3':
            add()
        elif selection == '4':
            delete()
        elif selection == '5':
            delete_all()
        else:
            break

main()