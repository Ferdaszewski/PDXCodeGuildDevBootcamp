"""Module with classes for List DoTo application.
"""
import datetime


class Collection(object):
    def __init__(self, tasks):
        self.tasks = tasks

    def display(self, mode, sort='due_date'):
        # TODO: Terminal mode + HTML mode for display
        pass

    def add(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

    def find(self):
        pass

    def sort(self, attribute):
        pass


class Task(object):
    def __init__(self, user, due_date=None):
        self.entry = ""
        self.tag = [user,]
        self.entry_time = datetime.utcnow()
        self.creator = user
        self.due_date = due_date
        self.done = [False,]
        self.id = 0



class Storage(object):
    def __init__(self):
        self.load()
        pass

    def __getitem__(self, index):
        # Return a collection object that is loaded from file
        temp = Collection('tasks')
        return temp
        pass

    def save(self):
        # TODO: save collections to file
        pass

    def load(self):
        # TODO: load collections from file
        pass

    def read(self):
        # static or class methods?
        pass

    def write(self):
        # static or class methods?
        pass

    def change_coll(self, collection):
        # change collection
        pass