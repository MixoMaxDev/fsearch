from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse

import uvicorn

import json
import requests

app = FastAPI()


def jsonify(data):
    payload_response = json.dumps(data)
    header = {"Content-Type": "application/json"}
    return json.loads(payload_response)


#static file serving

@app.get("/static/{file_path:path}")
def static_get(file_path: str) -> FileResponse:
    """This function will serve static files"""
    #url = /static/css/style.css
    return FileResponse(f"./static/{file_path}")


#http error code pages
@app.get("/error/{code}")
def error_get(code: int) -> HTMLResponse:
    """This function will return an error page"""
    #url = /error/404
    return HTMLResponse(content=open(f"./static/html/{code}.html").read(), status_code=code)



@app.get("/math")
def math_get(request: Request) -> JSONResponse:
    """This function will return the result of a math formula"""
    #url = /math?formula=2+2*sin(2*pi)
    formula = request.query_params.get("formula", None)
    
    if formula is None:
        return jsonify({"error": "No formula provided"})
    
    
    #replace pi with math.pi, sin with math.sin and so on
    replacements = [
        ("pi", "math.pi"),
        ("sin", "math.sin"),
        ("cos", "math.cos"),
        ("tan", "math.tan"),
        ("sqrt", "math.sqrt")
    ]
    
    for old, new in replacements:
        formula = formula.replace(old, new)
    
    #sanitize the input to avoid code injection
    
    banned_words = [
        "__",
        "import",
        "open",
        "globals"]
    
    for word in banned_words:
        if word in formula:
            return jsonify({"error": "Invalid formula"})
    
    #evaluate the formula
    
    try:
        r = eval(formula)
    except Exception as e:
        return jsonify({"error": f"Invalid formula: {e}"})
    
    #return the result
    return jsonify({"result": r})


@app.get("/search")
def search_get(request: Request) -> HTMLResponse:
    """Main page"""
    #url = /search?query=python
    query = request.query_params.get("q", None)
    
    if query is None:
        #return ./static/html/404.html
        return HTMLResponse(content=open("./static/html/404.html").read(), status_code=404)
    
    return jsonify({"query": query})
        
    
@app.get("/search_results")
def search_results_get(request: Request) -> JSONResponse:
    """
    get standard web results from duckduckgo
    """

    #return_data =  [ #title of result, url of result, description of result
    #{"title": "DuckDuckGo", "url": "https://duckduckgo.com", "description": "The search engine that doesn't track you."},
    #{"title": "DuckDuckGo — Privacy, simplified.", "url": "https://duckduckgo.com/about", "description": "The Internet privacy company that empowers you to seamlessly take control of your personal information online, without any tradeoffs."},
    #]
    
    query = request.query_params.get("q", None)
    
    if query is None:
        return jsonify({"error": "No query provided"})
    
    #get the results from duckduckgo
    
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    r = requests.get(url)
    data = r.json()
    
    #parse the results
    
    return_data = []
    
    for result in data["RelatedTopics"]:
        if "FirstURL" in result:
            return_data.append({
                "title": result["Text"],
                "url": result["FirstURL"],
                "description": result["Text"]
            })
    
    #return the results
    return jsonify({"results": return_data})





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port = 80)