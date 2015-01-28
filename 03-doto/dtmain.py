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

    def display(self, tag_filter=None):
        """Display the current collection of Tasks if each task has one
        of the tag filter tags. Default is to display all tasks.

        Args:
            tag_filter (list): A list of tags (str) to filter the tasks
            by. if None, print out all tasks.
        """
        # TODO: implement tag filtering
        print "\t\t" + self.current_collection.collection_name
        for date in self.current_collection.get_due_dates():
            print "\nDue Date:", date
            for task in self.current_collection.get_task_list(date):
                checked = " "
                if task.done is True:
                    checked = "X"
                print "[{0}] {1}\n*Tags* | {2} |\n".format(
                    checked, task._entry, ' | '.join(task.tags))

    def main(self, user):
        """Command control loop for the application. Displays the first
        collection in master_collection and loops until user quits.
        """
        while True:
            self.clear_screen(user)            
            self.display()
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
                    "Enter tags for the task (comma separated) (optional). > ")
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
                # TODO: get due date of task to delete (or None)
                # TODO: print out the list of tasks with index number
                # TODO: user selects index of task
                # TODO: prompt user to delete, change tags, or mark as done.
                pass
            elif command in ('c', 'change'):
                # TODO: print collection names with index next to them
                # TODO: Get index of collection that user wants to switch to or create new collection
                # TODO: Write current collection to file then open new collection
                index = 0
                self.current_collection = self.master_collection[index]
            elif command in ('f', 'filter'):
                # TODO: prompt user for tag to sort by
                tag_filter = ""
            elif command in ('q', "quit"):
                # TODO: write current collection to file.
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