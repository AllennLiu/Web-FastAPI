#!/usr/bin/python3
# -*- coding: utf-8 -*-

# built-in
from argparse import ArgumentParser

# fastapi module
from jinja2 import Template
from uvicorn import run as runSrv
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

# self-define module
from library.helpers import *
from library.FuncCommons import *
from library.FuncMongodb import ConnectMongo

# include routers
from routers.ApiTagsDesc import TagsMetadata
from routers.ApiAuthorize import LoginInstance, NotAuthenticatedException
from routers import (twoforms,
                     unsplash,
                     accordion,
                     ApiCommon,
                     ApiPostman,
                     ApiComments,
                     ApiAuthorize)

# parsing arguments
argparser = ArgumentParser()
argparser.add_argument('--prod', action='store_true')
argparser.add_argument('--stag', action='store_true')
args, unknown = argparser.parse_known_args()
is_prod = args.prod
is_stag = args.stag
readme  = readReadme('../README.md')

if is_stag:
    env_name = 'Staging'
    root_url = 'http://10.99.104.251:8787'
else:
    env_name = 'Production'
    root_url = 'http://web-fastapi.cloudnative.ies.inventec'

app = FastAPI(
    title=' '.join(readme["project_name"].split('-')),
    description='This is a very useful API collection, ' +
                'with auto docs for the API and everything.',
    version=readme["version"],
    openapi_tags=TagsMetadata().__repr__(),
    servers=[
        {"url": root_url, "description": f"{env_name} Environment"},
    ]
)

templates = Jinja2Templates(directory='../templates')

app.mount('/static', StaticFiles(directory="../static"), name='static')

# create login instance
manager = LoginInstance()

@app.exception_handler(NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    """
    Redirect the user to the login page if not logged
    in, then record the request's endpoint, If it has
    been authenticated and redirect to passed endpoint
    directly.
    """
    endpoint = request.url.path
    return RedirectResponse(url=f'/login?redirect={endpoint}')

# include router instance
app.include_router(unsplash.router)
app.include_router(twoforms.router)
app.include_router(accordion.router)
app.include_router(ApiCommon.router)
app.include_router(ApiPostman.router)
app.include_router(ApiComments.router)
app.include_router(ApiAuthorize.router)

@app.get('/', response_class=HTMLResponse, include_in_schema=False)
async def home(request: Request, user=Depends(manager)):
    data = openfile('home.md')
    return templates.TemplateResponse('page.html',
        {"request": request, "data": data, "user": user})

@app.get('/page/{page_name}',
         response_class=HTMLResponse,
         include_in_schema=False)
async def show_page(request: Request, page_name: str, user=Depends(manager)):
    data = openfile(page_name + '.md')
    if page_name == 'contact':
        with ConnectMongo() as m:
            comments = m.listCollection('comments')
        data = {
            k: Template(data[k]).render(user=user, comments=comments)
            for k, v in data.items() if v
        }
    else:
        data = {k:Template(data[k]).render(user=user) for k, v in data.items()}
    return templates.TemplateResponse('page.html',
        {"request": request, "data": data, "user": user})

if __name__ == '__main__':
    runSrv('main:app', host='0.0.0.0', port=8000, reload=True)
