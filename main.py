import os
from urllib.parse import urlparse

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from jinja2 import Environment, FileSystemLoader

import github_kusa
import tsuihai
import access_counter

app = FastAPI()


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
