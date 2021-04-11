import os
from typing import Optional
from urllib.parse import urlparse

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from jinja2 import Environment, FileSystemLoader

import github_kusa
import qrtool

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if request.method == 'HEAD':
        return Response()
    elif 'herokuapp' in urlparse(str(request.url)).netloc:
        domain = os.getenv('DOMAIN', 'example.com')
        url = urlparse(str(request.url))._replace(netloc=domain).geturl()
        response = RedirectResponse(url)
    else:
        response = await call_next(request)
    return response


@app.get("/")
async def read_root():
    env = Environment(loader=FileSystemLoader(
        os.path.dirname(__file__), encoding='utf8'))
    html = env.get_template('index.html').render()
    return HTMLResponse(content=html, status_code=200)


@app.get("/github-kusa")
async def read_github_kusa(user: str = ''):
    return HTMLResponse(content=github_kusa.main(user), status_code=200)


@app.get("/qrtool")
async def get_qrtool():
    return HTMLResponse(content=qrtool.main(b64='iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVQIHWP4DwQACfsD/Qy7W+cAAAAASUVORK5CYII='), status_code=200)


@app.post("/qrtool")
async def post_qrtool(string: Optional[str] = Form(''), b64: Optional[str] = Form('')):
    if string != '':
        res_b64 = qrtool.make(string)
        dl = True
        if b64 != '':
            res_string = qrtool.read(b64)
        else:
            res_string = ''
    elif b64 != '':
        res_string = qrtool.read(b64)
        res_b64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVQIHWP4DwQACfsD/Qy7W+cAAAAASUVORK5CYII='
        dl = False
    else:
        res_string = ''
        res_b64 = ''
        dl = False
    return HTMLResponse(content=qrtool.main(res_string, res_b64, dl), status_code=200)
