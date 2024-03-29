import os
import json
from urllib.parse import urlparse

from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Optional
from jinja2 import Environment, FileSystemLoader

from pydantic import BaseModel

import github_kusa
import tsuihai
import access_counter
import waku_icon
import questbox
import sentmaker
import maritozzo_icon
import tw_sn2id
import dlmese
import blogimg
import mesenot
import badge
import chocolate
import ua_frame
import profile
import stegano


class WakuIcon(BaseModel):
    waku: str
    username: str
    ratio: float


class MaritozzoIcon(BaseModel):
    username: str


class Sn2Id(BaseModel):
    username: str


class Mese(BaseModel):
    team: str
    passwd: str


class UAIcon(BaseModel):
    username: str


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
    if "herokuapp" in urlparse(str(request.url)).netloc:
        domain = os.getenv("DOMAIN")
        if domain:
            url = urlparse(str(request.url))._replace(netloc=domain).geturl()
            response = RedirectResponse(url)
        else:
            response = await call_next(request)
    else:
        if request.method == "HEAD":
            if urlparse(str(request.url)).path == "/":
                response = Response()
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
    return {"count": count, "ipaddr": request.client.host, "new": new}


@app.get("/waku_icon")
async def read_waku_icon():
    return HTMLResponse(waku_icon.get())


@app.post("/waku_icon")
async def post_waku_icon(data: WakuIcon):
    return waku_icon.post(data)


@app.get("/questbox")
async def read_questbox(id: str):
    lineid_dict = json.loads(os.getenv("LINE_ID"))
    if id not in lineid_dict.keys():
        return {"error": "not found"}
    return HTMLResponse(questbox.get(id))


@app.post("/questbox")
async def post_questbox(id: str = Form(...), text: str = Form(...)):
    lineid_dict = json.loads(os.getenv("LINE_ID"))
    if id not in lineid_dict.keys():
        return {"error": "not found"}
    lineid = lineid_dict[id]
    return HTMLResponse(questbox.post(id, lineid, text))


@app.get("/sentmaker")
async def read_sentmaker():
    return HTMLResponse(content=sentmaker.main(), status_code=200)


@app.get("/maritozzo_icon")
async def read_maritozzo_icon():
    return HTMLResponse(maritozzo_icon.get())


@app.post("/maritozzo_icon")
async def post_maritozzo_icon(data: MaritozzoIcon):
    return maritozzo_icon.post(data.username)


@app.get("/tw_sn2id")
async def read_tw_sn2id():
    return HTMLResponse(tw_sn2id.get())


@app.post("/tw_sn2id")
async def post_tw_sn2id(data: Sn2Id):
    return tw_sn2id.post(data.username)


@app.get("/dlmese")
async def read_dlmese():
    return HTMLResponse(dlmese.get())


@app.post("/dlmese")
async def post_dlmese(data: Mese):
    return dlmese.post(data.team, data.passwd)


@app.get("/blogimg")
async def read_blogimg(
    text: str,
    bgcolor: Optional[str] = None,
    fgcolor: Optional[str] = None,
    logourl: Optional[str] = None,
):
    try:
        content = blogimg.get(text, bgcolor, fgcolor, logourl)
    except Exception as e:
        print(e)
        return Response(content="Something wrong!")
    else:
        return Response(content=content, media_type="image/png")


@app.get("/mesenot")
async def read_mesenot():
    mesenot.main()


@app.get("/badge")
async def read_badge(
    params: str,
    width: str,
):
    try:
        content = badge.get(params, width)
    except Exception as e:
        print(e)
        return Response(content="Something wrong!")
    else:
        return Response(content=content, media_type="image/png")


@app.get("/chocolate")
async def read_chocolate():
    return HTMLResponse(chocolate.get())


@app.post("/chocolate")
async def post_chocolate(request: Request):
    return await chocolate.post(request)


@app.get("/ua_frame")
async def read_ua_frame():
    return HTMLResponse(ua_frame.get())


@app.post("/ua_frame")
async def post_ua_frame(data: UAIcon):
    return ua_frame.post(data.username)


@app.get("/profile")
async def get_profile():
    return profile.get()


@app.get("/stegano")
async def get_stegano():
    return HTMLResponse(content=stegano.get(), status_code=200)


@app.post("/stegano/encode")
async def post_stegano_encode(file: UploadFile = File(...),  text: str = Form(...)):
    return stegano.post_encode(await file.read(), text)


@app.post("/stegano/decode")
async def post_stegano_decode(file: UploadFile = File(...)):
    return stegano.post_decode(await file.read())
