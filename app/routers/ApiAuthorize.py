#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('library')

from FuncCommons import *
from FuncMongodb import ConnectMongo

from re import search
from json import dumps
from os import urandom
from uuid import uuid4
from time import strftime
from requests import post
from base64 import b64decode
from datetime import timedelta
from starlette.responses import Response, RedirectResponse, JSONResponse

from fastapi_login import LoginManager
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi import status, Request, Depends, APIRouter, HTTPException, Form

secret = urandom(24).hex()

class NotAuthenticatedException(Exception):
    pass

class LoginInstance(LoginManager):

    def __init__(self, token_url   = '/auth/token',
                       use_cookie  = True,
                       cookie_name = 'FastAPI-Cookies'):
        self.secret = secret
        LoginManager.__init__(self, secret     = self.secret,
                                    token_url  = token_url,
                                    use_cookie = use_cookie)
        self.cookie_name = cookie_name
        self.not_authenticated_exception = NotAuthenticatedException
        self.user_loader(self.query_user)

    def access_account(self, username, password):
        with ConnectMongo() as m:
            query = m.query(name='users', rule={"mail": username})
            if not query or query.get('password') != password:
                return {}
            query.pop('_id', None)
            datetime = datetimer(strftime('%s'), ts=False, date=True)
            query["access_login"] = [datetime] + query.get('access_login')
            return m.updateDocument('users', {"mail": username}, query)
        return {}

    def access_account_sms(self, username, password):
        payload = {
            "username" : username,
            "password" : password,
            "validate" : True
        }
        res = post('http://ares-script-mgmt.cloudnative.ies.inventec' +
                   '/api/v1/script-management/authenticate',
                   data    = payload,
                   verify  = False)
        res_code = res.status_code
        if res_code == 200:
            try:
                return (res.json(), res_code)
            except:
                return ({}, res_code)
        else:
            return ({}, res_code)

    def query_user(self, user_id: str):
        return user_id

manager = LoginInstance()

templates = Jinja2Templates(directory='../templates')

router = APIRouter()

@router.post('/auth/token', tags=['Login'])
def auth_token(data: OAuth2PasswordRequestForm = Depends()):
    """
    The python-multipart package is required to use
    the type OAuth2PasswordRequestForm.
    """
    username = data.username
    password = data.password

    # password has encrypted by base64 itself twice
    decrypt = b64decode(b64decode(password).decode('utf-8')).decode('utf-8')
    """
    User verification:
    Step1 - Verify with SMS user authentication API
    and it is no need to decrypt the password during
    payload is passed by requests.
    """
    user_data, status_code = manager.access_account_sms(username, password)
    """
    Step2 - Verify authentication by getting user in
    MongoDB and this will need to decrypt the password
    during payload is passed by requests.
    """
    if not user_data:
        user_data = manager.access_account(username, decrypt)
        if not user_data:
            return JSONResponse(content={"message": "Invalid Credentials"},
                                status_code=status.HTTP_401_UNAUTHORIZED)
    """
    By default token's expire after 15 minutes if it
    is not specify by passed argument "expires=?".
    This can be changed using the expires argument
    in the create_access_token method.
    Following remark setting means it expires after
    12 hours.
    """
    token = manager.create_access_token(
        data    = dict(sub=user_data),
        expires = timedelta(hours=1)
    )
    res = {
        "message": "Authentciated User",
        **user_data
    }
    response = JSONResponse(content=res, status_code=status.HTTP_200_OK)
    manager.set_cookie(response, token)
    return response

@router.get('/login', tags=['Login'],
            response_class=HTMLResponse, include_in_schema=False)
def login(request  : Request,
          redirect : str = 'none'):
    return templates.TemplateResponse('login.html',
        context={
            "request"  : request,
            "redirect" : redirect
    })

@router.get('/logout', tags=['Login'])
def logout(response: Response):
    response = RedirectResponse('/login', status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key=manager.cookie_name)
    return response

@router.get('/private', tags=['Login'])
def get_private_endpoint(user=Depends(manager)):
    return JSONResponse(content=user, status_code=status.HTTP_302_FOUND)

@router.get('/protected', tags=['Login'])
def protected_route(user=Depends(manager)):
    ...

@router.post('/user/create', tags=['User'])
async def user_create(
    request  : Request,
    name     : str = Form(...),
    email    : str = Form(...),
    password : str = Form(...)) -> JSONResponse:
    mail_regexp = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not search(mail_regexp, email):
        raise HTTPException(status_code=422, detail='Invalid Email Format')
    ts      = strftime('%s')
    dt      = datetimer(ts, ts=False, date=True)
    ts_cst  = float(datetimer(strftime('%Y-%m-%dT%H:%M:%S')))
    dt_tag  = datetimer(ts, ts=False, date=True, fmt='%B %d, %Y %I:%M %p')
    decrypt = b64decode(b64decode(password).decode('utf-8')).decode('utf-8')
    data    = {
        "uuid"          : str(uuid4()),
        "display"       : name,
        "password"      : decrypt,
        "mail"          : email,
        "user_mail"     : email,
        "user_web_name" : name,
        "create_dates"  : {
            "datetag"   : dt_tag,
            "datetime"  : dt,
            "timestamp" : ts_cst
        },
        "access_login"  : []
    }
    with ConnectMongo() as m:
        query = m.query(name='users', rule={"mail": email})
    if query:
        raise HTTPException(status_code=422, detail='User Exists')
    with ConnectMongo() as m:
        data = m.insertCollection(name='users', data=data)
        data.pop('_id', None)
    return JSONResponse(status_code=200, content={
        "message": "Create User Successfully",
        "data"   : data
    })
