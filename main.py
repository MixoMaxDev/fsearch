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
    
    results = []
    
    for result in tpb_results:
        results.append(result.to_json())
    
    return JSONResponse(content=results)

@app.get("/static/{file}")
async def static(file:str) -> FileResponse:
    return FileResponse(f"./static/{file}")



uvicorn.run(app, host="127.0.0.1", port=8000)