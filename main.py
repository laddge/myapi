import os
import json
from urllib.parse import urlparse

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader

from pydantic import BaseModel

import github_kusa
import tsuihai
import access_counter
import waku_icon
import questbox


class WakuIcon(BaseModel):
    waku: str
    username: str
    ratio: float


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/questbox/img", StaticFiles(directory="questbox/img"), name="questbox_img")


@app.middleware("http")
async def middleware(request: Request, call_next):
    if request.method == "HEAD":
        response = Response()
    elif "herokuapp" in urlparse(str(request.url)).netloc:
        domain = os.getenv("DOMAIN")
        if domain:
            url = urlparse(str(request.url))._replace(netloc=domain).geturl()
            response = RedirectResponse(url)
        else:
            response = await call_next(request)
    else:
        response = await call_next(request)
    return response


@app.get("/")
async def read_root():
    env = Environment(
        loader=FileSystemLoader(os.path.dirname(__file__), encoding="utf8")
    )
    html = env.get_template("index.html").render()
    return HTMLResponse(content=html, status_code=200)


@app.get("/github-kusa")
async def read_github_kusa(user: str = ""):
    return HTMLResponse(content=github_kusa.main(user), status_code=200)


@app.get("/tsuihai/{user}")
async def read_tsuihai(user: str = ""):
    return HTMLResponse(content=tsuihai.main(user), status_code=200)


@app.get("/access_counter")
async def read_access_counter(request: Request):
    count, new = access_counter.main(request.client.host)
    return {'count': count, 'ipaddr': request.client.host, 'new': new}


@app.get("/waku_icon")
async def read_waku_icon():
    return HTMLResponse(waku_icon.get())


@app.post("/waku_icon")
async def post_waku_icon(data: WakuIcon):
    return waku_icon.post(data)


@app.get("/questbox")
async def read_questbox(id: str):
    lineid_dict = json.loads(os.getenv('LINE_ID'))
    if id not in lineid_dict.keys():
        return {"error": "not found"}
    return HTMLResponse(questbox.get(id))


@app.post("/questbox")
async def post_questbox(id: str = Form(...), text: str = Form(...)):
    lineid_dict = json.loads(os.getenv('LINE_ID'))
    if id not in lineid_dict.keys():
        return {"error": "not found"}
    lineid = lineid_dict[id]
    return HTMLResponse(questbox.post(id, lineid, text))
