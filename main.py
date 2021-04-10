from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from urllib.parse import urlparse
import os

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if 'herokuapp' in urlparse(str(request.url)).netloc:
        domain = os.getenv('DOMAIN', 'example.com')
        url = url.parse(str(request.url))._replace(netloc=domain)
        response = RedirectResponse(url)
    else:
        response = await call_next(request)
    return response


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
