"""Module with classes for List DoTo application.
"""
import collections
import datetime
import json
import os
import pickle

# Program constants
LOCAL_FILE = './dotolist.dat'

class Collection(object):
    def __init__(self, collection_name):
        """A collection of Task objects.

        Args:
            collection_name (str): The name of this collection

        Paramaters:
            _tasks (dict, private): A dictionary with datetime.date
                objects as keys and a list of Task objects as values.
            collection_name (str): The name of this collection
        """
        self._tasks = collections.defaultdict(list)
        self.collection_name = collection_name

    def get_due_dates(self):
        """Returns a sorted list of due dates in the collection."""

        # None cannot be compared to datetime.date
        if None in self._tasks:
            sorted_keys = [None] + sorted(
                [i for i in self._tasks.iterkeys() if i != None])
        else:
            sorted_keys = sorted(self._tasks.keys())
        return sorted_keys

    def get_task_list(self, due_date):
        """Returns a list of tasks for a specific due date. If date is
        not in collection, passes down the error.

        Args:
            due_date (datetime.date): Takes a datetime.date object
        """
        return self._tasks[due_date]

    def add(self, new_task):
        """Add a task to this collection.

        Args:
        new_task (a Task object): A Task object to add to collection
        """
        self._tasks[new_task.due_date].append(new_task)

    def delete(self, task):
        """Remove a Task object from the collection.

        This module will search for task in collection and remove and
        return True. If the task is not found, it will return False.

        Args:
            task (Task object): The Task object to be deleted from the
            collection
        """
        task_list = self._tasks.get(task.due_date, [])
        try:
            i = task_list.index(task)
        except ValueError:
            return False
        del task_list[i]
        return True


class Task(object):
    def __init__(self, user, description, date_due=None, tag_list=None):
        """Create a new task.

        Paramaters:
            _entry (str, internal): The body of the task. Will be 0 to
                140 characters, inclusive. Accessed publicly as entry.
            entry (str, public): Supports get, set, and del. If the
                string is over 140 characters it will raise and
                a ValueError.
            _due_date (datetime.date or None, internal): The due date of
                the task. Accessed publicly as due_date.
            due_date (datetime.date or None, public): Supports get, set,
                and del. Will raise an exception if date is not formated
                correctly (mm-dd-year) or is after the date of entry.
            _tags (list, private): A set of strings to orgonize and
                catagorize the task. the user that created the task will
                be tagged.
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
            tag_list (list, optional): List of tags (str) to add to task.
                The user is always a tag on a new task.

        Methods:

        """
        # Generated elements
        self.entry_time = datetime.datetime.now()
        self.id = 0 # TODO - Hash to match cloud storage?
        self.creator = user
        self.done = False
        self.done_date = None
        self.done_user= None

        # Required elements
        self._entry = None
        self.setentry(description)
        self._due_date = None
        self.setdue_date(date_due)

        # Optional element
        self._tags = [user]
        self.settags(tag_list)

    def gettags(self):
        return self._tags
    def settags(self, tag_list):
        if tag_list is not None:
            for item in tag_list:
                if item not in (None, ''):
                    self._tags.append(item)
        # Creator of task must always be a tag
        if self.creator not in self._tags:
            self._tags.append(self.creator)
    def deltags(self):
        # Creator of a task must always be a tag
        self._tags = [self.creator]
    tags = property(gettags, settags, deltags)

    def getentry(self):
        return self._entry
    def setentry(self, value):
        if len(value) > 140:
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
        if value not in (None, ''):
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
        s = "ID: " + str(self.id)
        s += "\nTask: {0}\nDue Date: {1}\nTags: {2}\n".format(self._entry,
            self._due_date, self.tags)
        s += "Created By: {0} {1}\nDone?: {2}\nMarked Done By: {3} {4}".format(
            self.creator, self.entry_time, self.done,
            self.done_user, self.done_date)
        return s

    def mark_done(self, user):
        """Mark task as finished."""
        self.done = True
        self.done_date = datetime.datetime.now()
        self.done_user = user


class LocalStorage(object):
    """Local storage of collections using pickle."""
    
    def save(self, collections):
        """Saves a list of collections to file."""
        with open(LOCAL_FILE, 'w') as f:
            pickle.dump(collections, f)

    def load(self):
        """Load list of collections from file."""
        if os.path.isfile(LOCAL_FILE):
            with open(LOCAL_FILE, 'r') as f:
                return pickle.load(f)
        else:
            print "Cannot find file:", LOCAL_FILE
            raw_input("Loading empty collection.")
            return [Collection("My List")]
        return collections