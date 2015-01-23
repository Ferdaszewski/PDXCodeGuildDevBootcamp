"""Module with classes for List DoTo application.
"""
import datetime


class Collection(object):
    def __init__(self, collection_name, tasks):
        # tasks is a dict with due_date of task as key, then list of
        # tasks organized by entry_time
        self.tasks = tasks # TODO - validate and create the dict
        self.collection_name = collection_name

    def display(self, sort):
        pass

    def add(self, task):
        """Add a task to this collection.
        """
        pass

    def delete(self):
        pass

    def update(self):
        pass

    def find(self):
        pass


class Task(object):
    """A single task. Task takes parameters (WHAT ARE THEY?), validates
    them returning True if successful, throwing an exception otherwise.
    """
    def __init__(self, user, description, due_date=None, tag=[]):
        # Required task elements
        self._entry = description # 0 to 140 characters
        self._due_date = due_date # mm-dd-year

        # Optional task elements
        self.tag = set(user).update(tag) # comma separated strings

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