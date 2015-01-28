"""Do To application.
Main control structure.
"""
import sys
import datetime

import doto


class DoToApp(object):
    def __init__(self):
        self.storage = doto.Storage()
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
        # TODO: User class needed?
        self.main()

    def display(self, tag_filter=None):
        """Display the current collection of Tasks if task has all of
        the tag filter tags. Default is to display all tasks.

        Args:
            tag_filter (list): A list of tags (str) to filter the tasks
            by. if None, print out all tasks.
        """
        print "\t\t" + self.current_collection.collection_name
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
            month, day, year = (int(i) for i in date_input.split('-'))
            date = datetime.date(year, month, day)
            task_list = self.current_collection.get_task_list(date)
            self.clear_screen()
            for i, task in enumerate(task_list):
                print "Task ID: {0}".format(i)
                self.display_task(task)
        except (ValueError, IndexError) as e:
            print raw_input("Error. Not a valid date: %s\nPress Enter" % e)
            return False
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
            elif command in ('l', 'load'):
                self.master_collection = self.storage.load(self.user)
                self.current_collection = self.master_collection[0]
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
                sellection = None
                while sellection != 'c':
                    sellection = raw_input(
                        "Enter command for selected task > ").strip().lower()
                    if sellection == 'd':
                        sel_task.mark_done(self.user)
                        break
                    if sellection == 't':
                        #TODO change tags for task
                        pass
                    if sellection == 'x':
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
                # TODO: print collection names with index next to them
                # TODO: Get index of collection that user wants to switch to or create new collection
                # TODO: Write current collection to file then open new collection
                index = 0
                self.current_collection = self.master_collection[index]
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
                # TODO: write current collection to file.
                return
            else:
                self.clear_screen()
                raw_input("Invalid command. Press Enter to try again ")


# bootstrap DoTo application
app = DoToApp()
app.load()