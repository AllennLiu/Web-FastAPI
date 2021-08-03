#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os.path import join
from re import sub, search
from markdown import markdown

def openfile(filename):
    filepath = join('pages/', filename)
    with open(filepath, 'r', encoding='utf-8') as input_file:
        text = input_file.read()

    html = markdown(text)
    data = {
        "text": html
    }
    return data

def readReadme(readme):
    with open(readme, 'r', encoding='utf-8') as rf:
        contents = rf.read()
    try:
        version = sub('[^\d+\.]', '', search('`Rev:\s{0,}(\d+\.){1,2}\d+`',
                                             contents).group(0))
    except:
        version = '0.0.0'
    try:
        project_name = search('^(\w+\-){1,2}\w+\n\={5,}',
                              contents).group(0).split('\n')[0]
    except:
        project_name = 'UnknownProject'
    return {"version": version, "project_name": project_name}
