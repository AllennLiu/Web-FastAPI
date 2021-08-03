#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('library')

from json import dumps
from os import urandom
from requests import post
from base64 import b64decode
from datetime import timedelta
from starlette.responses import Response, RedirectResponse, JSONResponse

from fastapi_login import LoginManager
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi import status, Request, Depends, APIRouter, HTTPException

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
            return (res.json(), res_code)
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
    #decrypt = b64decode(b64decode(password).decode('utf-8')).decode('utf-8')
    """
    User verification is depend on API of SMS user
    authentication, and it is no need to decrypt the
    password during payload is passed by requests.
    """
    user_data, status_code = manager.access_account(username, password)
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
