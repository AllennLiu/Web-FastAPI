#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('library')

from FuncCommons import *
from FuncMongodb import ConnectMongo

from time import strftime
from uuid import uuid4, UUID
from starlette.responses import JSONResponse
from fastapi import APIRouter, HTTPException, Request, Form

router = APIRouter()

@router.post('/api/v1/contact/post-comment', tags=['Comment'])
async def contact_post_comment(
    request  : Request,
    username : str = Form(...),
    sex      : str = Form(default='male',
                          description='value should be male or female',
                          regex='^(male|female)$'),
    comment  : str = Form(...)) -> JSONResponse:
    ts     = strftime('%s')
    dt     = datetimer(ts, ts=False, date=True)
    ts_cst = float(datetimer(strftime('%Y-%m-%dT%H:%M:%S')))
    dt_tag = datetimer(ts, ts=False, date=True, fmt='%B %d, %Y %I:%M %p')
    data   = {
        "username"    : username,
        "sex"         : sex,
        "datetag"     : dt_tag,
        "datetime"    : dt,
        "timestamp"   : ts_cst,
        "comment"     : comment,
        "like"        : 0,
        "like_people" : []
    }
    with ConnectMongo() as m:
        data = m.insertCollection(name='comments', data=data)
        data.pop('_id', None)
    return JSONResponse(status_code=200, content={
        "message": "Post Commnet Successfully",
        "data"   : data
    })

@router.delete('/api/v1/contact/delete-comment', tags=['Comment'])
async def contact_delete_comment(
    request : Request,
    uuid    : str = Form(default     = str(uuid4()),
                         description = 'uuid v4 only')) -> JSONResponse:
    try:
        UUID(uuid, version=4)
    except ValueError:
        raise HTTPException(status_code=422, detail='Invalid UUID Format')
    with ConnectMongo() as m:
        data = m.deleteDocument(name='comments', rule={"uuid": uuid})
    if not data:
        raise HTTPException(status_code=404, detail='UUID Not Found')
    return JSONResponse(status_code=200, content={
        "message": f"Delete Commnet {uuid} Successfully",
        "data"   : data
    })

@router.put('/api/v1/contact/like-comment', tags=['Comment'])
async def contact_like_comment(
    request  : Request,
    uuid     : str = Form(default     = str(uuid4()),
                          description = 'uuid v4 only'),
    username : str = Form(...),
    operate  : str = Form(default='increase',
                          description='value should be increase or decrease',
                          regex='^(increase|decrease)$')) -> JSONResponse:
    with ConnectMongo() as m:
        query = m.query(name='comments', rule={"uuid": uuid})
        if operate == 'increase':
            query["like"] += 1
            query["like_people"].append(username)
        else:
            query["like"] -= 1
            query["like_people"].remove(username)
        data = {
            "like"        : query["like"],
            "like_people" : query["like_people"]
        }
        rdata = m.updateDocument('comments', {"uuid": uuid}, data)
    return JSONResponse(status_code=200, content={
        "message": "Edit Commnet Successfully",
        "data"   : rdata
    })

@router.get('/api/v1/contact/list-comment', tags=['Comment'])
async def contact_list_comment():
    with ConnectMongo() as m:
        data = m.listCollection('comments')
    return JSONResponse(status_code=200, content=data)
