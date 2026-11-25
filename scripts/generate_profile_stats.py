"""Generate profile graphics from public personal repositories only."""
import base64
import collections
import html
import json
import os
from pathlib import Path
import re
import tomllib
import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/stats"
CONFIG = json.loads((ROOT / "config/technologies.json").read_text())
OWNER = "JackOrmston"
GREEN, PAPER, RUST, SLATE, INK = "#253D35", "#F1EBDD", "#BB785A", "#82969D", "#292B2D"

def get(url, github=True, optional=False):
    headers = {"User-Agent": "portfolio-stats"}
    if github:
        headers["Accept"] = "application/vnd.github+json"
        if os.getenv("GITHUB_TOKEN"):
            headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        if optional and exc.code == 404:
            return None
        raise

def api(path):
    return json.loads(get("https://api.github.com" + path))

def repositories():
    page = 1
    while True:
        batch = api(f"/users/{OWNER}/repos?type=owner&per_page=100&page={page}")
        for repo in batch:
            if (repo["owner"]["login"].lower() == OWNER.lower()
                and not repo["private"] and not repo["fork"] and not repo["archived"]
                and repo["name"].lower() != OWNER.lower()):
                yield repo
        if len(batch) < 100:
            break
        page += 1

def dependencies(repo):
    names = set()
    for filename in ("pyproject.toml", "requirements.txt", "package.json"):
        raw = get(f"https://api.github.com/repos/{repo['full_name']}/contents/{filename}", optional=True)
        if raw is None:
            continue
        obj = json.loads(raw)
        if obj.get("encoding") != "base64":
            continue
        content = base64.b64decode(obj["content"]).decode("utf-8")
        if filename == "pyproject.toml":
            try:
                project = tomllib.loads(content).get("project", {})
                items = project.get("dependencies", [])
            except tomllib.TOMLDecodeError:
                continue
        elif filename == "package.json":
            try:
                package = json.loads(content)
                items = list(package.get("dependencies", {})) + list(package.get("devDependencies", {}))
            except json.JSONDecodeError:
                continue
        else:
            items = content.splitlines()
        for item in items:
            match = re.match(r"^([A-Za-z0-9][A-Za-z0-9_.-]*)", item.strip())
            if match:
                name = re.sub(r"[-_.]+", "-", match.group(1).lower())
                if name in CONFIG["dependencies"]:
                    names.add(CONFIG["dependencies"][name])
    return names

def text(x,y,value,size=16,color=GREEN,serif=False):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-family="{"Georgia,serif" if serif else "Arial,sans-serif"}">{html.escape(str(value))}</text>'

def rect(x,y,w,h,fill,rx=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>'

def svg(body,height,bg,title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{height}" viewBox="0 0 800 {height}"><title>{html.escape(title)}</title>{rect(0,0,800,height,bg,6)}{body}</svg>\n'

def icon(name,x,y):
    slug = CONFIG["icons"].get(name)
    if slug:
        try:
            raw = get(f"https://cdn.jsdelivr.net/npm/simple-icons@14.15.0/icons/{slug}.svg", github=False, optional=True)
            if raw:
                # Extract only the path data, not arbitrary external markup.
                match = re.search(r'<path d="([^"]+)"', raw.decode())
                if match and re.fullmatch(r"[MmZzLlHhVvCcSsQqTtAa0-9., +eE-]+", match.group(1)):
                    return f'<g transform="translate({x},{y}) scale(1.2)"><path fill="{PAPER}" d="{match.group(1)}"/></g>'
        except (OSError, UnicodeError):
            pass
    return text(x+1,y+20,name[:2].upper(),14,PAPER)

def toolkit(detected):
    groups = {k:list(v) for k,v in CONFIG["groups"].items()}
    curated = {n for v in groups.values() for n in v}
    extra = sorted(detected-curated)
    if extra:
        groups["Additional detected technologies"] = extra
    body = text(30,35,"TECHNICAL TOOLKIT / 01",13)+text(30,72,"Languages & technologies",30,serif=True)+rect(30,88,740,1,RUST)
    y=120
    for label,names in groups.items():
        body += text(30,y,label,20,serif=True)
        for i,name in enumerate(names):
            x=30+(i%4)*185
            yy=y+18+(i//4)*65
            body += rect(x,yy,38,38,GREEN,5)+icon(name,x+5,yy+5)+text(x+46,yy+24,name,14)
        y += 30+((len(names)+3)//4)*65
    body += text(30,y,"Curated experience and recognised public-project dependencies.",12)
    return svg(body,y+25,PAPER,"Technical toolkit")

def insights(count,langs,detected):
    body=text(30,35,"REPOSITORY INSIGHTS / 02",13,PAPER)+text(30,72,"Language distribution",30,PAPER,True)
    total=sum(langs.values())
    if total:
        top=langs.most_common(5)
        if len(langs)>5:
            top.append(("Other",total-sum(v for _,v in top)))
        colors=[PAPER,RUST,SLATE,"#A9AD92","#D4B8A0","#687D70"]
        x=30
        for i,(name,value) in enumerate(top):
            w=740*value/total
            body+=rect(x,92,w,20,colors[i])
            x+=w
            xx=30+(i%2)*370; yy=145+(i//2)*28
            body+=rect(xx,yy-10,10,10,colors[i],2)+text(xx+18,yy,f"{name} — {value/total:.1%}",15,PAPER)
    else:
        body+=text(30,110,"No public project language data yet.",18,PAPER)
        body+=text(30,138,"Statistics will appear as projects are published.",14,PAPER)
    body+=rect(30,235,740,1,SLATE)+text(30,273,count,30,PAPER)+text(30,295,"Public repositories",14,PAPER)+text(400,273,len(detected),30,PAPER)+text(400,295,"Recognised dependencies",14,PAPER)+text(30,330,"Public personal repositories only · language share by GitHub-reported bytes",12,PAPER)
    return svg(body,350,GREEN,"Public repository insights")

def main():
    repos=list(repositories())
    langs=collections.Counter()
    detected=set()
    for repo in repos:
        langs.update(api(f"/repos/{repo['full_name']}/languages"))
        detected.update(dependencies(repo))
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"technologies.svg").write_text(toolkit(detected),encoding="utf-8")
    (OUT/"languages.svg").write_text(insights(len(repos),langs,detected),encoding="utf-8")

if __name__ == "__main__":
    main()
