import os
from io import BytesIO
import zipfile
import requests
from bs4 import BeautifulSoup
import base64


def get():
    with open(os.path.join(os.path.dirname(__file__), "template.html")) as f:
        return f.read()


def post(team, passwd):
    buff = BytesIO()
    with zipfile.ZipFile(buff, "w", zipfile.ZIP_DEFLATED) as archive:
        for repo in ["company", "industry"]:
            i = 0
            while True:
                url = "https://harvassoc.com/cgi-bin/reports"
                params = {
                    "contest": "jmc",
                    "locale": "jp",
                    "team": team,
                    "pass": passwd,
                    "period": "Period {}".format(i),
                    "report": repo,
                }
                r = requests.get(url, params=params)
                r.encoding = r.apparent_encoding
                if "Error" in r.text or "エラー" in r.text:
                    break
                else:
                    soup = BeautifulSoup(r.text, features="html.parser")
                    archive.writestr(
                        "reports/P{}/{}.txt".format(i, repo), soup.pre.text)
                i += 1
            if i == 0:
                return False
    return {"output": base64.b64encode(buff.getvalue()).decode()}
