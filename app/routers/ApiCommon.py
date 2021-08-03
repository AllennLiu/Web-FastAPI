#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('library')

from FuncGitLab import *
from FuncCommons import *
from FuncMongodb import ConnectMongo

from time import strftime
from starlette.responses import JSONResponse
from fastapi import FastAPI, APIRouter, HTTPException, Request, Form

router = APIRouter()

@router.post('/api/v1/test', tags=['Test'])
async def test_database_create(request: Request):
    ts     = strftime('%s')
    dt     = datetimer(ts, ts=False, date=True)
    ts_cst = float(datetimer(strftime('%Y-%m-%dT%H:%M:%S')))
    dt_tag = datetimer(ts, ts=False, date=True, fmt='%B %d, %Y %I:%M %p')
    data   = {
        "datetag"   : dt_tag,
        "datetime"  : dt,
        "timestamp" : ts_cst
    }
    with ConnectMongo() as m:
        data = m.insertCollection(name='tests', data=data)
    data.pop('_id', None)
    return data

@router.get('/api/v1/test/{timestamp}', tags=['Test'])
async def test_database_search(timestamp: float):
    with ConnectMongo() as m:
        query = m.query(name='tests', rule={"timestamp": timestamp})
    if not query:
        raise HTTPException(status_code=404, detail="Timestamp Not Found")
    query.pop('_id', None)
    return query

@router.put('/api/v1/test/{timestamp}', tags=['Test'])
async def test_database_update(timestamp: float):
    with ConnectMongo() as m:
        query = m.query(name='tests', rule={"timestamp": timestamp})
        data  = m.updateDocument('tests',
                                  {"uuid": query.get('uuid')},
                                  {"timestamp": timestamp + 1})
    return data

@router.delete('/api/v1/test/{timestamp}', tags=['Test'])
async def test_database_delete(timestamp: float):
    with ConnectMongo() as m:
        query = m.query(name='tests', rule={"timestamp": timestamp})
        data  = m.deleteDocument(name='tests', rule={"uuid": query["uuid"]})
    return data

@router.get('/api/v1/calendar/holidays', tags=['Calendar Holidays'])
async def get_holidays_by_calendar(year   : int  = int(strftime('%Y')),
                                   detail : bool = True,
                                   weekend: bool = True):
    holidays = getCalendarHoliday(year, detail=detail)
    if not weekend:
        holidays = getCalendarHoliday(year, detail=True)
        holidays = [
            (e if detail else e["date"]) for e in holidays
            if e["holiday_name"] not in ['Sunday', 'Saturday']
        ]
    if not holidays:
        raise HTTPException(status_code=404, detail="Not Implemented")
    return {"holidays": holidays}

@router.get('/api/v1/gitlab/readme/info', tags=['GitLab Project Readme'])
async def get_readme_by_gitlab_project(project_name: str = 'SIT-Web-FastAPI'):
    project = getProject(name=project_name)
    if not project:
        raise HTTPException(status_code=404, detail="Project Not Found")
    return getReadme(project, ref='master')
