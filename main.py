import fsearch_core as fsc

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.requests import Request

import uvicorn
import os


app = FastAPI()


@app.get("/")
async def root() -> FileResponse:
    return FileResponse("./static/index.html")
    

@app.get("/search")
async def search(q:str) -> JSONResponse:
    tpb_results = fsc.search_tpb(q)
    google_results = fsc.search_google(q)
    
    results = []
    
    results.extend(google_results)
    results.extend(tpb_results)
    
    
    results_json = [r.to_json() for r in results]
    
    return JSONResponse(content=results_json)

@app.get("/static/{file}")
async def static(file:str) -> FileResponse:
    return FileResponse(f"./static/{file}")



uvicorn.run(app, host="127.0.0.1", port=8000)