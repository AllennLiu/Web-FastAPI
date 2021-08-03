#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import getenv
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request, APIRouter, Depends

from dotenv import load_dotenv
load_dotenv()

from routers.ApiAuthorize import LoginInstance

manager = LoginInstance()

templates = Jinja2Templates(directory='../templates')

router = APIRouter()

@router.get('/unsplash', response_class=HTMLResponse, include_in_schema=False)
async def unsplash_home(request: Request, user=Depends(manager)):
    key = getenv('unsplash_key')
    print(key)
    return templates.TemplateResponse('unsplash.html',
                                      {"request": request, "user" : user})

