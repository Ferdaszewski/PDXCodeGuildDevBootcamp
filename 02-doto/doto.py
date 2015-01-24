"""Module with classes for List DoTo application.
"""
import datetime


class Collection(object):
    def __init__(self, collection_name, task_list):
        # tasks is a dict with due_date of task as key, then list of
        # tasks organized by entry_time
        self.tasks = self.add(task_list)
        self.collection_name = collection_name

    def display(self, sort):
        print "\t\t" + self.collection_name
        for date, task_list in self.tasks.items():
            print "\nDue Date:", date
            for task in task_list:
                print task

    def add(self, task_list):
        """Add a task to this collection.

        Args:
        task_list (list of Tasks): A list of at least one Task object
        """
        try:
            task_dict = self.tasks
        except AttributeError:
            task_dict = {}

        for task in task_list:
            try:
                task_dict[task.due_date].append(task)
            except KeyError:
                task_dict[task.due_date] = [task]
        return task_dict

    def delete(self):
        pass

    def update(self):
        pass

    def find(self):
        pass


class Task(object):
    def __init__(self, user, description, date_due=None, tag=None):
        """Create a new task.

        Paramaters:
            _entry (str, internal): The body of the task. Will be 0 to 140
                characters, inclusive. Accessed publicly as entry.
            entry (str, public): Supports get, set, and del. If the
                string is over 140 characters it will raise and
                a ValueError.
            _due_date (datetime.date or None, internal): The due date of
                the task. Accessed publicly as due_date.
            due_date (datetime.date or None, public): Supports get, set,
                and del. Will raise an exception if date is not formated
                correctly (mm-dd-year) or is after the date of entry.
            tag (set): A set of strings to orgonize and catagorize the
                task. the user that created the task will be tagged.
            entry_time (datetime.datetime): Timestamp when created
            id (??): A hash of...???
            creator (str): Name of user that created the task.
            done (bool): False while not finished.
            done_date (datetime.datetime): Timestamp when task is done.
            done_user (str): User who marked task as done.


        Args:
            user (str): Name of application user and owner of the task.
            description (str): Body of the task, limited to 140 chars.
            due_date (str, optional): Due date for task in "mm-dd-year"
                format, or None if there is not due date for the task.
            tag (list of str, optional): List of tags to add to task.
                The user is always a tag on a new task.

        Methods:

        """
        # Required task elements
        self._entry = self.setentry(description) # 0 to 140 characters
        self._due_date = self.setdue_date(date_due) # mm-dd-year

        # Optional task elements
        self.tags = [user]
        if tag is not None:
            [self.tags.append(item) for item in tag]

        # Generated task elements
        self.entry_time = datetime.datetime.today()
        self.id = 0 # TODO - Hash to match cloud storage?
        self.creator = user
        self.done = False
        self.done_date = None
        self.done_user= None

    
    # Entry required to be string of length 0 to 140 characters.
    def getentry(self):
        return self._entry

    def setentry(self, value):
        chars = len(value)
        if chars > 140:
            raise ValueError("Task entry cannot be more than 140 characters")
        self._entry = value

    def delentry(self):
        self._entry = ""

    entry = property(getentry, setentry, delentry)


    def getdue_date(self):
        return self._due_date

    def setdue_date(self, value):
        """due_date in mm-dd-year format and it cannot be before today.
        """
        if value is not None:
            month, day, year = (int(i) for i in value.split('-'))
            self._due_date = datetime.date(year, month, day)
            if self._due_date < datetime.date.today():
                raise ValueError("Due date cannot be before today")
        else:
            self._due_date = None

    def deldue_date(self):
        self._due_date = None

    due_date = property(getdue_date, setdue_date, deldue_date)

    def __str__(self):
        if self.done:
            check = 'X'
        else:
            check = ' '

        s = "[%1s] %s *Tags* %s" % (check, self.entry, self.tags)

        return s


    



class Storage(object):
    def __init__(self):
        pass

    def save(self, collection_list):
        # TODO: save collections in collection_list to file
        pass

    def load(self, user):
        # TODO: load collections from file
        # TEMP - load collection with one temp task
        new_task = Task(user, "This is a temporary task with no due date.")
        return [Collection("temp collection", [new_task])]

    def read(self):
        # static or class methods?
        pass

    def write(self):
        # static or class methods?
        pass