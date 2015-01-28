"""List Do To
Small program to manage a to do list.

Main control structure.

Joshua Ferdaszewski
ferdaszewski@gmail.com
"""
import datetime
import sys

import doto


class DoToApp(object):
    def __init__(self):
        # TODO Storage selector, local or cloud
        self.storage = doto.LocalStorage()
        self.user = None
    
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
        self.master_collection = self.storage.load()
        self.current_collection = self.master_collection[0]

        # TODO: if this is a new user, prompt create a new user?
        self.main()

    def display(self, tag_filter=None):
        """Display the current collection of Tasks if task has all of
        the tag filter tags. Default is to display all tasks.

        Args:
            tag_filter (list): A list of tags (str) to filter the tasks
            by. if None, print out all tasks.
        """
        # TODO: Deal with done tasks (archived in collection)
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
        checked = " "
        if task.done is True: checked = "X"
        print "[{0}] {1}\n*Tags* | {2} |\n".format(
            checked, task._entry, ' | '.join(task.tags))

    def find_task(self):
        """Searches for and returns task, if error, returns false"""
        date_input = raw_input("Enter Due Date of task mm-dd-year > ")
        try:
            if date_input.strip() != '':
                month, day, year = (int(i) for i in date_input.split('-'))
                date = datetime.date(year, month, day)
            else:
                date = None
            task_list = self.current_collection.get_task_list(date)
        except (ValueError, IndexError) as e:
            print raw_input("Error. Not a valid date: %s\nPress Enter" % e)
            return False
        self.clear_screen()
        for i, task in enumerate(task_list):
            print "Task ID: {0}".format(i)
            self.display_task(task)
        index_input = raw_input("Enter task ID. > ")
        try:
            index = int(index_input)
            sel_task = task_list[index]
        except ValueError:
            raw_input("Not a valid index.\nPress Enter.")
            return False
        return sel_task

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
                print "Create a new task."
                description = raw_input(
                    "Enter task (140 characters max) > ")
                due_date = raw_input(
                    "Enter due date as 'mm-dd-year' (optional). > ")
                tags = raw_input(
                    "Enter tags for the task (comma separated) (optional). > ")
                tag_list = [tag.strip() for tag in tags.split(',')]
                try:
                    new_task = doto.Task(self.user, description,
                        due_date, tag_list)
                except (NameError, ValueError) as e:
                    print "Task not created. Error: ", e
                    raw_input("Press Enter to continue.")
                    continue
                self.current_collection.add(new_task)
            elif command in ('e', 'select'):
                sel_task = self.find_task()
                if sel_task is False:
                    continue
                self.clear_screen()
                self.display_task(sel_task)
                print "\n'd': Mark this task done"
                print "'t': Change tags of this task"
                print "'x': Remove this task permanently (cannot be undone)"
                print "'c': Cancel and return to main menu."
                selection = None
                while selection != 'c':
                    selection = raw_input(
                        "Enter command for selected task > ").strip().lower()
                    if selection == 'd':
                        sel_task.mark_done(self.user)
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
            elif command in ('c', 'change'):
                # Print out all collections with index numbers
                self.clear_screen()
                print "**Collections**\n"
                for i, collection in enumerate(self.master_collection):
                    print "Collection ID: %d | %s" % (i, collection.name)
                print ""
                
                # Select collection and validate
                selection = raw_input(
                    "Enter Collection ID or 'new' for a new collection. > ")
                if selection.strip().lower() == 'new':
                    collection_name = raw_input("Name for new collection. > ")
                    self.master_collection.append(
                        doto.Collection(collection_name))
                    self.current_collection = self.master_collection[-1]
                    continue
                try:
                    index = int(selection)
                    self.current_collection = self.master_collection[index]
                except (ValueError, IndexError) as e:
                    raw_input("Invalid selection: %s\nPress Enter." % e)
                    continue

                # With selected collection, offer options
                print "'r': Rename collection"
                print "'x': Delete collection (cannot be undone)"
                print "'v': View current collection tasks"
                selection = ''
                while selection != 'v':
                    selection = raw_input("Enter command. > ")
                    selection = selection.strip().lower()
                    
                    # Rename collection and set to current collection
                    if selection == 'r':
                        new_name = raw_input("Enter new collection name. > ")
                        self.current_collection.name = new_name
                        break

                    # Delete collection and set current to default
                    elif selection =='x':

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
            elif command in ('f', 'filter'):
                user_input = raw_input(
                    "Enter tag(s) to display (comma separated). > ")
                tag_filter = [tag.strip() for tag in user_input.split(',')
                    if tag is not '']

            elif command == '?':
                self.clear_screen()
                print "\nList of Commands"
                print "'s' or 'save': Save current collections."
                print "'l' or 'load': Load collections."
                print "'n' or 'new': Create a new task."
                print "'e' or 'select': Select a task and change or delete it."
                print "'c' or 'change': Change collections or create one."
                print "'f' or 'filter': Filter tasks by tags."
                print "'q' or 'quit': Save current collections then quit"
                print "'?': View this help again.\n"
                raw_input("Press enter to return.")

            elif command in ('q', "quit"):
                self.storage.save(self.master_collection)
                return
            else:
                self.clear_screen()
                raw_input("Invalid command. Press Enter to try again ")


# bootstrap DoTo application
app = DoToApp()
app.load()