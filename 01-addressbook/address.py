#
# Phone Book Manager
#
# A simple program that creates and manages a phone book file.
# Names and phone numbers are saved as a JSON text file in the
# same directory as this program.
#
# Joshua Ferdaszewski
# PDX Code Guild Student - January 8, 2015
#

import sys
import json
import re


def display():
    # Open file and read into memory
    tel = loadfile()

    # clear screen
    clear()

    # Print phone book to screen in alpha order
    print "      NAME%-15s -  PHONE NUMBER" %('')
    for name in sorted(tel.keys()):
        print "%-25s - %s" % (name, tel[name])
    pause()


def find(delete):
    # Load phone book and clear screen
    tel = loadfile()
        
    # Prompt user for name to search
    clear()
    
    # Loop untill user has only one name or gives up
    looking = True
    while looking:
        query = raw_input("\nWhat name would you like to search for? ")

        # Find partial matches
        names_match = []
        for name in sorted(tel.keys()):
            if len(re.findall(query, name)) > 0:
                names_match.append(name)

        # If only one name found, display that one name
        if len(names_match) == 1:            
            # Make sure query matches key exactly and print
            query = names_match[0]
            print "\n:)  ", query, ":", tel[query]
            looking = False
            pause()

        # Display partial matches and 
        elif len(names_match) > 0:
            print "Did you mean?"
            for name in names_match:
                print name
            print "Type name exactly as it appears above."

        # Name not found and no match
        else:
            print "\n:(\t%s is NOT in your phonebook" % (query)

        # Try again?
        searching = raw_input("Search again? y/n >")
        if searching in ('y', 'Y'):
            looking = True
        else:
            return

    # If user wants to remove this entry
    if delete:
        # Verify that this entry should be removed
        confirm = raw_input("Delete %s? (y/n) >" % (query))
        if confirm in ('y', 'Y'):
            # Remove and write to file
            del tel[query]
            writefile(tel)
            print query, "removed from phone book."
        else:
            print "Delete aborted", query, "NOT removed."
        pause()


def add():
    # Open file and load phone book
    tel = loadfile()

    # Continue while user is entering new names
    while True:
        # Clear screen and prompt user for name to enter
        clear()
        newName = raw_input("\tName for new entry: ")

        # Check for existing name
        if newName in tel:
            print "Already in Phone Book!"
            print newName, ":", tel[newName]
            if not raw_input("Update phone number? y/n >") in ('y', 'Y'):
                return

        # Prompt user for phone number and validate
        while True:
             # Prompt user for phone number
            print "\t(Enter 10 digit phone number with no spaces or other characters)"
            newPhone = raw_input("\tPhone number for %s: " % (newName))

            # 10 digits only
            if len(newPhone) == 10 and newPhone.isdigit():
                break

            # Throw error at user, invalid phone number
            print "Invalid phone number. Please enter as [1234567890]"

        # add new item to dict with formated phone number
        tel[newName] = newPhone[0:3] + "-" + newPhone[3:6] + "-" + newPhone[6:]

        # Do it again?
        if not raw_input("Add another name? y/n>") in ('y', 'Y'):
            break

    # Write updated phone book to file
    writefile(tel)


def delete_all():
    # Clear screen and verify that user wants to remove entire phonebook
    clear()
    print "Delete entire Phonebook.\nThis cannot be undone!"
    if raw_input("Are you sure? y/n >") in ('y', 'Y'):
        
        # open file and overwrite
        f = open("./addresses.txt", 'w')
        f.truncate()
        f.close()
        print "Phonebook deleted"
    else:
        print "Delete aborted.  Phonebook NOT removed."

    pause()



def loadfile():    
    # Open address file, create it if needed
    f = open("./addresses.txt", 'a+')
    
    # Read file into memory, if a file is empty, create and empty dict 'tel'
    try:
        tel = json.load(f)
    except ValueError:
        tel = {}

    # Close file and return the phone book
    f.close()
    return tel


def writefile(tel):
    # open file to overwrite
    f =  open("./addresses.txt", 'w')

    # Write the phone book to file as JSON text
    json.dump(tel, f)

    # Close file
    f.close()


def pause():
    print "\n"
    raw_input ("Press Enter")


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
    print "\t  Welcome to PHONEBOOK!\n\n"
    print "\t1) List Phone Numbers"
    print "\t2) Find Name"
    print "\t3) Add Phone Number"
    print "\t4) Remove a Phone Number"
    print "\t5) Delete All Phone Numbers"
    print "\t6) Quit\n\n\t"

    # Wait for valid user input
    while sel not in ('1', '2', '3', '4', '5', '6'):   
        sel = raw_input("select an option: ")

    # Return valid menu selection
    return sel


def main():
    # Display menu and wait for user selection
    while True:
        selection = menu()
        if selection == '1':
            display()
        elif selection == '2':
            find(False)
        elif selection == '3':
            add()
        elif selection == '4':
            find(True)
        elif selection == '5':
            delete_all()
        else:
            break

main()