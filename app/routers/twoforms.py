#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import getenv
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request, Form, APIRouter, Depends

from routers.ApiAuthorize import LoginInstance

manager = LoginInstance()

router = APIRouter()
templates = Jinja2Templates(directory='../templates/')

@router.get('/twoforms', response_class=HTMLResponse, include_in_schema=False)
def form_get(request: Request, user=Depends(manager)):
    key = getenv('unsplash_key')
    print(key)
    result = 'Type a number'
    return templates.TemplateResponse('twoforms.html',
                                      context={
                                        "request" : request,
                                        "result"  : result,
                                        "user"    : user
                                      })

@router.post('/form1', response_class=HTMLResponse, include_in_schema=False)
def form_post1(request: Request, number: int = Form(...)):
    result = number + 2
    return templates.TemplateResponse('twoforms.html',
                                      context={
                                        "request": request,
                                        "result" : result,
                                        "yournum": number
                                      })

@router.post('/form2', response_class=HTMLResponse, include_in_schema=False)
def form_post2(request: Request, number: int = Form(...)):
    result = number + 100
    return templates.TemplateResponse('twoforms.html',
                                      context={
                                        "request": request,
                                        "result" : result,
                                        "yournum": number
                                      })

