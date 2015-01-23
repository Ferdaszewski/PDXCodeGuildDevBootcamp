"""Do To application.
Main control structure.
"""
import sys

import doto


class DoToApp(object):
    def __init__(self):
        self.master_collection = doto.Storage()
        self.cur_collection = self.master_collection[0]
    
    def load(self):
        """Initial loading screen, user selects where to load/save data.
        """
        self.clear_screen()
        print "Welcome to Do To! What is your name?"
        name = raw_input("> ")

        # TODO: if this is a new user, prompt create a new user?
        # TODO: User class needed?

        self.main(name)



    def main(self, user):
        """Command control loop for the application. Displays the first
        collection in master_collection and loops until user quits.
        """
        command = ""
        while command not in ('q', "quit"):
            self.clear_screen(user)
            self.cur_collection.display('term')
            command = raw_input(
                "\nEnter command (? for help) > ").strip().lower()

            if command in ('s', 'save'):
                self.master_collection.save()
            elif command in ('l', 'load'):
                self.master_collection.load()
                self.cur_collection = self.master_collection[0]
            elif command in ('n', 'new'):
                self.cur_collection.add()
            elif command in ('e', 'select'):
                selcted_task = self.cur_collection.find()
                # TODO: prompt user to delete or change selected task
            elif command in ('c', 'change'):
                # TODO: Get index of collection that user wants to switch to
                coll_index = 0
                self.cur_collection = self.master_collection.change_coll(coll_index)
            elif command in ('o', 'order'):
                # TODO: prompt user for attribute to sort by
                # TODO: figure out best way to handle default sort
                self.cur_collection.sort
            else:
                self.clear_screen(user)
                raw_input("Invalid command. Press Enter to try again ")


                



    def clear_screen(self, user=""):
        """Clear screen, return cursor to top left, and display banner.
        Thanks to Graham King http://www.darkcoding.net for code snippet
        """
        sys.stdout.write('\033[2J')
        sys.stdout.write('\033[H')
        sys.stdout.flush()
        print "\n\t\tDo To - %s\n\n" % user


# bootstrap DoTo application
app = DoToApp()
app.load()