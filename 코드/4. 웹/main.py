# import re
from fastapi import FastAPI
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.requests import Request
# from mimetypes import guess_type
from databases import Database
from fastapi.staticfiles import StaticFiles

database = Database("sqlite:///water.db")
templates = Jinja2Templates(directory="./templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html = True), name="static")

@app.on_event("startup")
async def database_connect():
    await database.connect()

@app.on_event("shutdown")
async def database_disconnect():
    await database.disconnect()

# @app.get("/", response_class=HTMLResponse)
# async def root():
#     return FileResponse("index.htm")

@app.get("/sql")
async def sql_test(): # fetch_data(id: int):
    query = "SELECT * FROM water_total"
    rows = await database.fetch_all(query=query)
    return rows[-1]

# https://tybednext.vercel.app/posts/sqlmodel
@app.get("/", response_class=HTMLResponse)
@app.get("/bridge", response_class=HTMLResponse)
async def bridge(request:Request):
    query = "SELECT * FROM water_total"
    rows = await database.fetch_all(query=query)
    # total_rows = []
    # send_row = {}
    # for row in rows:
    #     send_row['ymdhm'] = row['ymdhm']
    #     send_row['wl_1018662'] = round(float(row['wl_1018662']), 1)
    #     send_row['wl_1018680'] = round(float(row['wl_1018680']), 1)
    #     send_row['wl_1018663'] = round(float(row['wl_1018663']), 1)
    #     send_row['wl_1019630'] = round(float(row['wl_1019630']), 1)
    #     total_rows.append((send_row['ymdhm'],send_row['wl_1018662'],send_row['wl_1018680'],send_row['wl_1018663'],send_row['wl_1019630']))

    return templates.TemplateResponse("bridge.htm", {'request': request, 'rows': rows})
    
@app.get("/charts/{id}", response_class=HTMLResponse)
async def charts(request: Request, id: str):
    if id  == "청담대교":
        return FileResponse("visualization_청담대교.html")
    elif id == "한강대교":
        return FileResponse("visualization_한강대교.html")
    elif id == "잠수교":
        return FileResponse("visualization_잠수교.html")
    elif id == "행주대교":
        return FileResponse("visualization_행주대교.html")
    elif id == "팔당댐":
        return FileResponse("visualization_팔당댐.html")
    return FileResponse("visualization_water_level.html")

# @app.get("/pred/{id}", response_class=HTMLResponse)
# async def pred(request: Request, id: str):
#     if id  == "청담대교":
#         return FileResponse("pred_청담대교.html")
#     elif id == "한강대교":
#         return FileResponse("pred_한강대교.html")
#     elif id == "잠수교":
#         return FileResponse("pred_잠수교.html")
#     elif id == "행주대교":
#         return FileResponse(f"pred_행주대교.html")
#     return FileResponse("pred_청담대교.html")

@app.get("/dashboard/{id}", response_class=HTMLResponse)
async def dashboard(request: Request, id: str):
    query = "SELECT * FROM water_collection"
    rows = await database.fetch_all(query=query)

    if id  == "청담대교":
        return templates.TemplateResponse("dash_청담대교.html", {'request': request, 'rows': rows})
    elif id == "한강대교":
        return templates.TemplateResponse("dash_한강대교.html", {'request': request, 'rows': rows})
    elif id == "잠수교":
        return templates.TemplateResponse("dash_잠수교.html", {'request': request, 'rows': rows})
    elif id == "행주대교":
        return templates.TemplateResponse("dash_행주대교.html", {'request': request, 'rows': rows})
    return templates.TemplateResponse("dash_청담대교.html", {'request': request, 'rows': rows})

@app.get("/more", response_class=HTMLResponse)
async def pred(request: Request):
    query = "SELECT * FROM water_collection"
    rows = await database.fetch_all(query=query)
    return templates.TemplateResponse("more.html", {'request': request, 'rows': rows})

# @app.get("/site/{filename}")
# async def get_site(filename):
#     filename = './' + filename

#     if not isfile(filename):
#         return Response(status_code=404)

#     with open(filename) as f:
#         content = f.read()

#     content_type, _ = guess_type(filename)
#     return Response(content, media_type=content_type)


# @app.get("/site/")
# async def get_site_default_filename():
#     return await get_site('a.htm')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)