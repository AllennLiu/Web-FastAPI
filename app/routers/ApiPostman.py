#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('library')

from typing import List
from json import loads, dumps
from starlette.responses import JSONResponse

from pydantic.errors import EmailError
from pydantic import BaseModel, EmailStr

from jinja2 import Template
from jinja2.exceptions import TemplateNotFound

from fastapi.templating import Jinja2Templates
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi import (APIRouter,
                     Request,
                     Response,
                     HTTPException,
                     UploadFile,
                     File,
                     Form,
                     Body,
                     BackgroundTasks)

mailTemp = {
    "sender"   : "SMS Notification Center <SMS.NOTIFICATION.CENTER@inventec.com>",
    "subject"  : "FastAPI Mail Notification",
    "mailto"   : ['Liu.AllenJH@inventec.com'],
    "body"     : '<p><font color="blue">Test Mail</font></p>',
    "payload"     : {"key": "value"},
    "response" : {
        "success": JSONResponse(status_code=200, content={
            "message": "Sent E-mail Successfully"
        }),
        "failure": HTTPException(status_code=404,
                                 detail='Unexpectedly Exception')
    }
}

class Payload(BaseModel):
    data: str = ""

templates = Jinja2Templates(directory='../templates/mail/')

def configMail(base_url):

    # IPT Mail-relay settings
    conf = ConnectionConfig(
        MAIL_SERVER     = 'mailrelay-b.ies.inventec',
        MAIL_PORT       = 25,
        MAIL_SSL        = False,
        MAIL_TLS        = False,
        MAIL_FROM       = mailTemp["sender"],
        MAIL_USERNAME   = '',
        MAIL_PASSWORD   = '',
        USE_CREDENTIALS = False,

        # if no indicated SUPPRESS_SEND defaults to 0 (false) as below
        # SUPPRESS_SEND=1
    )

    # Google SMTP settings
    if '10.99.104.251' in base_url:
        conf.MAIL_SERVER   = 'smtp.gmail.com'
        conf.MAIL_PORT     = 465
        conf.MAIL_SSL      = True
        conf.MAIL_USERNAME = 'tom951086@gmail.com'
        conf.MAIL_PASSWORD = '@a080281200'
        conf.USE_CREDENTIALS    = True

    return conf

router = APIRouter()

@router.post('/api/v1/mail/body', tags=['Send Mail by Body'])
async def send_with_html_body(
    request    : Request,
    subject    : str            = Form(mailTemp["subject"]),
    sender     : str            = Form(mailTemp["sender"]),
    recipients : List[EmailStr] = Form(...),
    cc         : List[EmailStr] = Form(mailTemp["mailto"]),
    body       : str            = Form(mailTemp["body"]),
    attachment : UploadFile     = File(None)) -> JSONResponse:
    try:
        [EmailStr.validate(m) for m in recipients]
    except EmailError as err:
        raise HTTPException(status_code=404, detail=str(err))
    conf = configMail(str(request.base_url))
    msg  = MessageSchema(subject    = subject,
                         recipients = recipients,
                         cc         = cc,
                         body       = body,
                         subtype    = 'html')
    if attachment:
        msg.attachment = [attachment]
    conf.MAIL_FROM = sender
    mail = FastMail(conf)
    await mail.send_message(msg)
    return mailTemp["response"]["success"]

@router.post('/api/v1/mail/template/exists',
             tags=['Send Mail by exists Template'])
async def send_with_html_exists_template(
    request    : Request,
    subject    : str            = Form(mailTemp["subject"]),
    sender     : str            = Form(mailTemp["sender"]),
    recipients : List[EmailStr] = Form(...),
    cc         : List[EmailStr] = Form(mailTemp["mailto"]),
    template   : str            = Form(default='template_file.html',
                                       description='html extension file only',
                                       regex='^\w+\.html$'),
    payload    : str            = Form(default=mailTemp["payload"],
                                       description='this entry is for object' +
                                                   ' format only'),
    attachment : UploadFile     = File(None)) -> JSONResponse:
    return JSONResponse(status_code=200, content={
        "message": loads(payload)
    })
    conf = configMail(str(request.base_url))
    msg  = MessageSchema(subject    = subject,
                         recipients = recipients,
                         cc         = cc,
                         subtype    = 'html')
    if attachment:
        msg.attachments = [attachment]
    conf.MAIL_FROM = sender
    try:
        payload = loads(payload)
    except:
        raise HTTPException(status_code=422, detail='Invalid Payload')
    try:
        body = templates.TemplateResponse(template, context={
            "request": request,
            **payload
        })
    except TemplateNotFound as err:
        raise HTTPException(status_code=404, detail=str(err) + ' Not Found')
    msg.body = body.template.render(payload)
    mail = FastMail(conf)
    await mail.send_message(msg)
    return mailTemp["response"]["success"]

@router.post('/api/v1/mail/template/uploaded',
             tags=['Send Mail by uploaded Template'])
async def send_with_html_uploaded_template(
    request    : Request,
    subject    : str            = Form(mailTemp["subject"]),
    sender     : str            = Form(mailTemp["sender"]),
    recipients : List[EmailStr] = Form(...),
    cc         : List[EmailStr] = Form(mailTemp["mailto"]),
    template   : UploadFile     = File(...),
    payload  : str            = Form(default=mailTemp["payload"],
                                       description='this entry is for object' +
                                                   ' format only'),
    attachment : UploadFile     = File(None)) -> JSONResponse:
    conf = configMail(str(request.base_url))
    msg  = MessageSchema(subject    = subject,
                         recipients = recipients,
                         cc         = cc,
                         subtype    = 'html')
    conf.MAIL_FROM = sender
    try:
        payload = loads(payload)
    except:
        raise HTTPException(status_code=422, detail='Invalid Payload')
    if attachment:
        msg.attachments = [attachment]
    if template.content_type != 'text/html':
        raise HTTPException(status_code=422, detail='Expected HTML File')
    contents = await template.read()
    t = Template(contents.decode('utf-8'))
    msg.body = t.render(payload)
    mail = FastMail(conf)
    await mail.send_message(msg)
    return mailTemp["response"]["success"]

