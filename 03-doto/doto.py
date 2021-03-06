"""Module with classes for List DoTo application.

Joshua Ferdaszewski
ferdaszewski@gmail.com
"""
# TODO: comment code and write all docstrings
# TODO: verify pep8 compliance
import collections
import datetime
import jsonpickle
import os
from bson.objectid import ObjectId
import pickle
import pymongo

LOCAL_FILE = './dotolist.dat'

# Login credentials for testing cloud database
MONGOHQ_URL = os.environ["DOTO_MONGODB"]

class Collection(object):
    def __init__(self, collection_name):
        """A collection of Task objects.

        Args:
            collection_name (str): The name of this collection

        Paramaters:
            _tasks (dict, private): A default dictionary with
                datetime.date objects as keys and a list of Task objects as
                values.
            _archive_tasks (list, private): A list of tasks that have
                been marked done.
            collection_name (str): The name of this collection.
        """
        self._tasks = collections.defaultdict(list)
        self._archive_tasks = []
        self.name = collection_name
        self.db_id = None

    def get_due_dates(self):
        """Returns a sorted list of due dates in the collection."""

        # None cannot be compared to datetime.date
        if None in self._tasks:
            sorted_keys = [None] + sorted(
                [i for i in self._tasks.iterkeys() if i is not None])
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

    def archive(self):
        """Moves any task object marked as done in tasks to the
        _archive_tasks list.
        """
        for date in self.get_due_dates():
            # Add done tasks to archive list
            done_tasks = [task for task in self._tasks[date] if task.done]
            self._archive_tasks.extend(done_tasks)

            # Remove done_tasks from task_list
            self._tasks[date] = [task for task in self._tasks[date]
                                 if task not in done_tasks]

    def getarchive(self):
        """Returns a list of tasks that have been marked done."""
        self.archive()
        return self._archive_tasks

    def serialize(self):
        """Serialize attributes as key/value pairs to a dict. Serialize
        all tasks contained in collection. Return the dictionary.
        """
        # Clean collection and archive done tasks.
        self.archive()

        collection_dict = {}
        collection_dict['name'] = self.name
        collection_dict['db_id'] = self.db_id

        # Serialize all current tasks and put in dictionary
        tasks_dict = {}
        for date in self.get_due_dates():
            tasks_dict[date] = [
                task.serialize() for task in self._tasks[date]]
        collection_dict['tasks'] = tasks_dict

        # Serialize all archive tasks and put in dictionary
        archive_list = [task.serialize() for task in self._archive_tasks]
        collection_dict['archive'] = archive_list

        return collection_dict

    @staticmethod
    def deserialize(data):
        """De-serialize data and return an instance of the class.

        Args:
            data (dict): Dictionary with key/values to create the
                collection.
        """
        new_collection = Collection(data['name'])
        new_collection.db_id = data['db_id']

        # Deserialize tasks and assign to collection attribute
        for date in data['tasks'].keys():
            new_collection._tasks['date'] = [
                Task.deserialize(task) for task in data['tasks'][date]]

        # Deserialize archived tasks and assign to collection attribute
        new_collection._archive = [
            Task.deserialize(task) for task in data['archive']]

        new_collection.archive()
        return new_collection


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
            tags (list, public): Supports get, set and del.
            entry_time (datetime.datetime): Timestamp when created
            task_id (??): A hash of...???
            creator (str): Name of user that created the task.
            done (bool): False while not finished.
            done_date (datetime.datetime): Timestamp when task is done.
            done_user (str): User who marked task as done.


        Args:
            user (str): Name of application user and owner of the task.
            description (str): Body of the task, limited to 140 chars.
            due_date (str, or datetime.date optional): Due date for task
                in "year-mm-dd" format, or None if there is not due date
                for the task.
            tag_list (list, optional): List of tags (str) for task.
                The user is always a tag on a new task.

        Methods:

        """
        # Generated elements
        self.entry_time = datetime.datetime.now()
        self.task_id = 0  # TODO - task_id to match cloud storage?
        self.creator = user
        self.done = False
        self.done_date = None
        self.done_user = None

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
        """due_date in year-mm-dd format and it cannot be before today.
        """
        if value not in (None, ''):
            # Can take a string or a datetime.date object
            if isinstance(value, datetime.date):
                self._due_date = value
            else:
                year, month, day = (int(i) for i in value.split('-'))
                self._due_date = datetime.date(year, month, day)
            if self._due_date < datetime.date.today():
                raise ValueError("Due date cannot be before today")
        else:
            self._due_date = None

    def deldue_date(self):
        self._due_date = None
    due_date = property(getdue_date, setdue_date, deldue_date)

    def __str__(self):
        """String representation of all task attributes."""
        s = "task_id: " + str(self.task_id)
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

    def serialize(self):
        """Serialize attributes as key/value pairs to a dict."""
        task_dict = {}
        task_dict['entry_time'] = self.entry_time
        task_dict['task_id'] = self.task_id
        task_dict['creator'] = self.creator
        task_dict['done'] = self.done
        task_dict['done_date'] = self.done_date
        task_dict['done_user'] = self.done_user
        task_dict['entry'] = self._entry
        task_dict['due_date'] = self._due_date
        task_dict['tags'] = self._tags
        return task_dict

    @staticmethod
    def deserialize(data):
        """De-serialize data and return an instance of the class.

        Args:
            data (dict): Dictionary with key/values to create a task.
        """
        # Internal object attribures
        new_entry_time = data['entry_time']
        new_task_id = data['task_id']
        new_creator = data['creator']
        new_done = data['done']
        new_done_date = data['done_date']
        new_done_user = data['done_user']

        # External object attributes
        new_entry = data['entry']
        new_due_date = data['due_date']
        new_tags = data['tags']

        # Instantiate a new Task object
        new_task = Task(new_creator, new_entry, new_due_date, new_tags)

        # Assign other attributes to new task
        new_task.entry_time = new_entry_time
        new_task.task_id = new_task_id
        new_task.creator = new_creator
        new_task.done = new_done
        new_task.done_date = new_done_date
        new_task.done_user = new_done_user

        return new_task


class LocalStorage(object):
    """Local storage of collections using pickle."""

    def save(self, coll_to_save):
        """Saves a list of collections to file."""
        with open(LOCAL_FILE, 'w') as f:
            pickle.dump(coll_to_save, f)

    def load(self):
        """Load list of collections from file."""
        if os.path.isfile(LOCAL_FILE):
            with open(LOCAL_FILE, 'r') as f:
                loaded_colls = pickle.load(f)
        else:
            print "Cannot find file:", LOCAL_FILE
            raw_input("Loading empty collection.")
            loaded_colls = [Collection("My List")]

        # Clean collection of all done tasks and move to archive
        for collection in loaded_colls:
            collection.archive()
        return loaded_colls


class CloudStorage(object):
    """Cloud storage of collections in MongoDB database."""
    def __init__(self):
        # Connect to the database and collection
        self._dbcollection = pymongo.MongoClient(MONGOHQ_URL).qscfadm.josh

    def save(self, coll_to_save):
        """Saves a list of collections to the cloud."""
        # Serialize collections
        id_list = []
        for collection in coll_to_save:
            coll_dict = {}
            coll_dict['jp_collection'] = jsonpickle.encode(collection,
                                                           keys=True)

            new_id = self._dbcollection.save(coll_dict)

            # Add _id if it exists
            if collection.db_id not in (None, ''):
                coll_dict['_id'] = ObjectId(collection.db_id)
                id_list.append(coll_dict['_id'])
            else:
                # new entry in cloud, update id_list
                id_list.append(new_id)

        # Delete documents that are in cloud but not in local
        to_del = [doc_id['_id'] for doc_id in
                  self._dbcollection.find(fields=['_id'])
                  if doc_id['_id'] not in id_list]

        if len(to_del) > 0:
            for doc_id in to_del:
                self._dbcollection.remove({'_id': ObjectId(doc_id)})

    def load(self):
        """Load list of collections from the cloud."""
        # Get each document and place in collections list
        loaded_colls = []
        for doc in self._dbcollection.find():

            # decode and deserialize data
            collection = jsonpickle.decode(doc['jp_collection'], keys=True)

            # Add database id to collection object
            collection.db_id = doc['_id']
            loaded_colls.append(collection)
        if len(loaded_colls) <= 0:
            # Return empty collection
            return [Collection("My Collection")]
        return loaded_colls
