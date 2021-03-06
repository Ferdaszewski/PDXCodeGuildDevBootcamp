"""List Do To
Small program to manage a to do list.

Main control structure.

Joshua Ferdaszewski
ferdaszewski@gmail.com
"""
# TODO: comment code and write all docstrings
# TODO: assignment of tasks with @username - new task attribute?
# TODO: load assigned tasks to cloud, pull my assigned tasks to collection
import datetime
import sys

import doto


class DoToApp(object):
    def __init__(self):
        """The termenal/text display and control structure of the app.

        Args:
            storage (Storage object): Holds the local or cloud storage
                object.
            user (str): User name
            master_collection (list): List of Collection objects
            current_collection (Collection object): Holds the currently
                selected Collection for display and manipulation.
        """
        self.storage = None
        self.user = None
        self.master_collection = None
        self.current_collection = None

    def clear_screen(self,):
        """Clear screen, return cursor to top left, and display banner.
        Thanks to Graham King http://www.darkcoding.net for code snippet
        """
        sys.stdout.write('\033[2J')
        sys.stdout.write('\033[H')
        sys.stdout.flush()
        print "\n\t\tDo To - %s\n\n" % self.user

    def load(self):
        """Initial loading screen, user selects where to load/save data.
        """
        self.clear_screen()
        print "Welcome to Do To! What is your name?"
        self.user = raw_input("> ")

        # Set local or cloud storage
        print "\nDefault file storage is local. Use cloud storage?"
        cloud = raw_input("'cloud': Cloud Storage. Otherwise press enter. > ")
        if cloud.strip().lower() in ('y', 'cloud'):
            self.storage = doto.CloudStorage()
        else:
            self.storage = doto.LocalStorage()

        # Load list of collections and set current to the default
        if raw_input("Load collections? y/n > ").strip().lower() == 'y':
            self.master_collection = self.storage.load()
        else:
            self.master_collection = [doto.Collection("My List")]
        self.current_collection = self.master_collection[0]
        self.main()

    def display(self, tag_filter=None):
        """Display the current collection of Tasks if task has all of
        the tag filter tags. Default is to display all tasks.

        Args:
            tag_filter (list): A list of tags (str) to filter the tasks
            by. if None, print out all tasks.
        """
        print "\t\t" + self.current_collection.name
        if tag_filter not in (None, []):
            print "Filter:", tag_filter
        for date in self.current_collection.get_due_dates():

            # create list of tasks that match all tag filters
            filtered_tasks = []
            if tag_filter in (None, []):
                filtered_tasks = self.current_collection.get_task_list(date)
            else:
                for task in self.current_collection.get_task_list(date):
                    if set(tag_filter) <= set(task.tags):
                        filtered_tasks.append(task)

            # don't print the due date if not tasks match tag list
            if len(filtered_tasks) > 0:
                print "\n** Due Date:", date, "**"
                for task in filtered_tasks:
                    self.display_task(task)

    def display_task(self, task):
        """Displays a task object passed in as an arg."""
        # Visual check for completed tasks
        checked = " "
        if task.done is True:
            checked = "X"
        # print a formated task
        print "[{0}] {1}\n*Tags* | {2} |\n".format(
            checked, task._entry, ' | '.join(task.tags))

    def find_task(self):
        """Searches for and returns task, if error, returns false"""
        date_input = raw_input("Enter Due Date of task year-mm-dd > ")
        try:
            if date_input.strip() != '':
                year, month, day = (int(i) for i in date_input.split('-'))
                date = datetime.date(year, month, day)
            else:
                date = None
            task_list = self.current_collection.get_task_list(date)
        except (ValueError, IndexError) as e:
            print raw_input("Error. Not a valid date: %s\nPress Enter" % e)
            return False

        # We have a valid date, print out the tasks
        self.clear_screen()
        for i, task in enumerate(task_list):
            print "Task ID: {0}".format(i)
            self.display_task(task)

        # Return a valid task
        index_input = raw_input("Enter task ID. > ")
        try:
            index = int(index_input)
            sel_task = task_list[index]
        except ValueError:
            raw_input("Not a valid index.\nPress Enter.")
            return False
        return sel_task

    def new_task(self):
        """Creates a new task object in the current collection."""
        print "Create a new task."

        # Collect new task info from user
        description = raw_input("Enter task (140 characters max) > ")
        due_date = raw_input("Enter due date as 'year-mm-dd' (optional). > ")
        tags = raw_input(
            "Enter tags for the task (comma separated) (optional). > ")
        tag_list = [tag.strip() for tag in tags.split(',')]
        try:
            new_task = doto.Task(self.user, description, due_date, tag_list)
        except (NameError, ValueError) as e:
            # On error, print and return.
            print "Task not created. Error: ", e
            raw_input("Press Enter to continue.")
            return
        self.current_collection.add(new_task)
        return

    def change_task(self):
        """Get a task from the user and update it."""
        sel_task = self.find_task()
        if sel_task is False:
            return

        # We have a valid task, let's change it.
        self.clear_screen()
        self.display_task(sel_task)
        print "\n'd': Mark this task done"
        print "'t': Change tags of this task"
        print "'x': Remove this task permanently (cannot be undone)"
        print "'c': Cancel and return to main menu."
        selection = None

        # Continue until user cancels
        while selection != 'c':
            selection = raw_input(
                "Enter command for selected task > ").strip().lower()

            if selection == 'd':
                sel_task.mark_done(self.user)
                self.current_collection.archive()
                break

            if selection == 't':
                user_input = raw_input(
                    "Overwrite existing tags? y/n > "
                    ).strip().lower()
                if user_input in ('y', 'yes'):
                    del sel_task.tags
                user_tags = raw_input(
                    "Enter new tags (comma separated) (optional). > ")
                sel_task.tags = [
                    tag.strip() for tag in user_tags.split(',')]
                break

            if selection == 'x':
                if raw_input("Delete this task? y/n > ") in ('y', 'Y'):
                    delete = self.current_collection.delete(sel_task)
                    if delete:
                        raw_input("Task deleted. Press Enter")
                        break
                    else:
                        raw_input("Task not deleted. Try again.")
                        continue
            else:
                print "Please enter valid command."
        return

    def change_collection(self):
        """User selects a collection and then can adjust that collection
        or create a new collection.
        """

        # Print out all collections with index numbers
        self.clear_screen()
        print "**Collections**\n"
        for i, collection in enumerate(self.master_collection):
            print "Collection ID: %d | %s" % (i, collection.name)
        print ""

        # User select collection
        selection = raw_input(
            "Enter Collection ID or 'new' for a new collection. > ")

        # Create a new collection and add to master collection list.
        if selection.strip().lower() == 'new':
            collection_name = raw_input("Name for new collection. > ")
            self.master_collection.append(
                doto.Collection(collection_name))
            self.current_collection = self.master_collection[-1]
            return

        # Validate user selection
        try:
            index = int(selection)
            self.current_collection = self.master_collection[index]
        except (ValueError, IndexError) as e:
            raw_input("Invalid selection: %s\nPress Enter." % e)
            return

        # With selected collection, offer options
        print "'r': Rename collection"
        print "'x': Delete collection (cannot be undone)"
        print "'v': View current collection tasks"
        selection = ''

        # Continue until user selects to view collection
        while selection != 'v':
            selection = raw_input("Enter command. > ")
            selection = selection.strip().lower()

            # Rename collection and set to current collection
            if selection == 'r':
                new_name = raw_input("Enter new collection name. > ")
                self.current_collection.name = new_name
                break

            # Delete collection and set current to default
            elif selection == 'x':

                # There must be at least one collection
                if len(self.master_collection) <= 1:
                    print "One collection remaining, cannot delete.",
                    print "Create new collection first."
                    raw_input("Press Enter to continue.")
                    break
                delete = raw_input("Delete this collection? y/n > ")
                if delete.strip().lower() in ('y', 'yes'):
                    del self.master_collection[index]
                    self.current_collection = self.master_collection[0]
                    break
            else:
                print "Invalid command. Try again."
        return

    def main(self):
        """Command control loop for the application. Displays the first
        current collection continues until user quits.
        """
        tag_filter = None
        while True:
            self.clear_screen()
            self.display(tag_filter)
            command = raw_input(
                "Enter command (? for help) > ").strip().lower()

            if command in ('s', 'save'):
                self.storage.save(self.master_collection)
                raw_input("Tasks Saved\nPress Enter to continue.")

            elif command in ('l', 'load'):
                self.master_collection = self.storage.load()
                self.current_collection = self.master_collection[0]
                raw_input("Tasks Loaded\nPress Enter to continue.")

            elif command in ('n', 'new'):
                self.clear_screen()
                self.new_task()

            elif command in ('e', 'select'):
                self.change_task()

            elif command in ('c', 'change'):
                self.change_collection()

            elif command in ('f', 'filter'):
                # Set tag filter to user input
                user_input = raw_input(
                    "Enter tag(s) to display (comma separated). > ")
                tag_filter = [tag.strip() for tag in user_input.split(',')
                              if tag is not '']

            elif command in ('a', 'archive'):
                # Display tasks marked as done
                self.clear_screen()
                print "%s - Archive" % self.current_collection.name
                archive = self.current_collection.getarchive()
                for task in archive:
                    print "\n%s" % task
                raw_input("Press Enter to continue.")

            elif command == '?':
                self.clear_screen()
                print "\nList of Commands"
                print "'s' or 'save': Save current collections."
                print "'l' or 'load': Load collections."
                print "'n' or 'new': Create a new task."
                print "'e' or 'select': Select a task and change or delete it."
                print "'c' or 'change': Change collections or create one."
                print "'f' or 'filter': Filter tasks by tags."
                print "'a' or 'archive': Display finished tasks"
                print "'q' or 'quit': Save current collections then quit"
                print "'?': View this help again.\n"
                raw_input("\nPress enter to return.")

            elif command in ('q', "quit"):
                return

            else:
                self.clear_screen()
                raw_input("Invalid command. Press Enter to try again ")


# bootstrap DoTo application
app = DoToApp()
app.load()
