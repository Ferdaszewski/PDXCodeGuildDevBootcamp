"""Do To application.
Main control structure.
"""
import sys

import doto


class DoToApp(object):
    def __init__(self):
        self.storage = doto.Storage()
    
    def load(self):
        """Initial loading screen, user selects where to load/save data.
        """
        self.clear_screen()
        print "Welcome to Do To! What is your name?"
        name = raw_input("> ")

        # List of collections, index 0 is default
        self.master_collection = [self.storage.load(name)]
        self.current_collection = self.master_collection[0]

        # TODO: if this is a new user, prompt create a new user?
        # TODO: User class needed?
        self.main(name)


    def main(self, user):
        """Command control loop for the application. Displays the first
        collection in master_collection and loops until user quits.
        """
        command = ""
        sort_var = "due_date"
        while True:
            self.clear_screen(user)
            self.current_collection.display(sort_var)
            command = raw_input(
                "\nEnter command (? for help) > ").strip().lower()

            if command in ('s', 'save'):
                self.storage.save(self.master_collection)
            elif command in ('l', 'load'):
                self.master_collection = self.storage.load(user)
                self.current_collection = self.master_collection[0]
            elif command in ('n', 'new'):
                
                # Continue until a new task is created correctly
                self.clear_screen(user)
                print "Create a new task."
                description = raw_input(
                    "Enter task (140 characters max) > ")
                due_date = raw_input(
                    "Enter due date as 'mm-dd-year' (optional). > ")
                tags = raw_input(
                    "Enter tags for the task separated by commas (optional). > ")
                tag_list = [tag.strip() for tag in tags.split(',')]

                try:
                    new_task = doto.Task(user, description,
                        due_date, tag_list)
                except (NameError, ValueError) as e:
                    print "Task not created. Error: ", e
                    raw_input("Press Enter to continue.")
                    continue
                self.current_collection.add(new_task)
            elif command in ('e', 'select'):
                selcted_task = self.current_collection.find()
                # TODO: prompt user to delete or change selected task, mark as done.
            elif command in ('c', 'change'):
                # TODO: Get index of collection that user wants to switch to or create new collection
                index = 0
                self.current_collection = self.master_collection[index]
            elif command in ('o', 'order'):
                # TODO: prompt user for attribute to sort by
                sort_var = ""
            elif command in ('q', "quit"):
                return
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