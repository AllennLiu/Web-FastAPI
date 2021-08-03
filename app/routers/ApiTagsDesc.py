#!/usr/bin/python3
# -*- coding: utf-8 -*-

class TagsMetadata:

    def __init__(self):
        self.tags_metadata = [
            {
                "name": "Calendar Holidays",
                "description": ("Response with specify **year** to " +
                                "retrieve all _holiday dates_ by calendar.")
            },
            {
                "name": "GitLab Project Readme",
                "description": ("Get **project's readme info** with " +
                                "specify **project name** in _GitLab_.")
            },
            {
                "name": "Send Mail by Body",
                "description": ("User could pass contents of **HTML** body " +
                                "to send _customize_ freestyle mail.")
            },
            {
                "name": "Send Mail by exists Template",
                "description": ("Passing **JSON object** data to render" +
                                "already exists **HTML** template with " +
                                "_Jinja2_ variables.")
            },
            {
                "name": "Send Mail by uploaded Template",
                "description": ("Uploading **HTML** template and pass " +
                                "**JSON object** data to render it with " +
                                "_Jinja2_ variables.")
            },
            {
                "name": "Login",
                "description": ("Sign in/out with specified username " +
                                "and password")
            },
            {
                "name": "Comment",
                "description": ("Operation to **Post/Delete/Put/Get** " +
                                "comment in _Mongodb_.")
            },
            {
                "name": "Test",
                "description": ("Pytest will using these functions to " +
                                "test the connection of _MongoDB_ by " +
                                "operation **Post/Delete/Put/Get** in " +
                                "test collection.")
            }
        ]

    def __call__(self, name='', desc=''):
        print('Call this function with passing argument name and description.')
        if name and desc:
            self.tags_metadata.append({"name": name, "desc": desc})

    def __repr__(self):
        return self.tags_metadata

    def __str__(self):
        return self.tags_metadata.__str__()
