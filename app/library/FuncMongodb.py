#!/usr/bin/python3
# -*- coding: utf-8 -*-

from uuid import uuid4
from pymongo import MongoClient
from urllib.parse import quote_plus

class ConnectMongo:

    def __init__(self, host         = '10.99.104.251:8789',
                       username     = 'root',
                       password     = 'sit2@ipt',
                       authenticate = True):
        self.host     = host
        self.url_head = 'mongodb://'
        self.db_url   = f'{self.url_head}{self.host}'
        if authenticate:
            self.username = username
            self.password = quote_plus(password)
            self.db_url   = '{0}{1}:{2}@{3}'.format(self.url_head,
                                                    self.username,
                                                    self.password,
                                                    self.host)

    def __enter__(self):
        self.client = MongoClient(self.db_url)
        self.db     = self.client.fastapi
        return self

    def __exit__(self, type, value, traceback):
        self.client.close()
        if type and value:
            assert False, value

    def query(self, name='', rule={}, all=False):
        collection = self.db[name]
        if all:
            return collection.find(rule)
        return collection.find_one(rule)

    def listCollection(self, name='', rule={}):
        collection = self.db[name]
        return [
            {k:v for k, v in e.items() if k != '_id'}
            for e in collection.find(rule)
        ]

    def insertCollection(self, name='', data={}):
        data = {"uuid": str(uuid4()), **data}
        collection = self.db[name]
        collection.insert_one(data)
        return data

    def deleteDocument(self, name='', rule={}, many=False):
        collection = self.db[name]
        if many:
            collection.delete_many(rule)
            return True
        query = collection.find_one(rule)
        if not query:
            return {}
        collection.delete_one(rule)
        query.pop('_id', None)
        return query

    def updateDocument(self, name='', rule={}, data={}):
        collection = self.db[name]
        query = collection.find_one(rule)
        collection.update_one(query, {"$set": {**query, **data}})
        query.pop('_id', None)
        return {**query, **data}
