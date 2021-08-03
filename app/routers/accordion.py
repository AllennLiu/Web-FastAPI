#!/usr/bin/python3
# -*- coding: utf-8 -*-

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request, Form, APIRouter, Depends

from routers.ApiAuthorize import LoginInstance

manager = LoginInstance()

router = APIRouter()
templates = Jinja2Templates(directory='../templates/')

@router.get('/accordion', response_class=HTMLResponse, include_in_schema=False)
def get_accordion(request: Request, user=Depends(manager)):
    tag = 'flower'
    result = 'Type a number'
    return templates.TemplateResponse('accordion.html',
                                      context={
                                        "request" : request,
                                        "result"  : result,
                                        "tag"     : tag,
                                        "user"    : user
                                      })

@router.post('/accordion', response_class=HTMLResponse, include_in_schema=False)
def post_accordion(request : Request,
                   tag     : str = Form(...),
                   user    = Depends(manager)):
    return templates.TemplateResponse('accordion.html',
                                      context={
                                        "request" : request,
                                        "tag"     : tag,
                                        "user"    : user
                                      })

