# api.py
from fastapi import FastAPI
#import subprocess
import requests
app = FastAPI()

def run_httpie():
    try:
        # Running `uv` with `httpie` inside Vercel
#         result = subprocess.run(
#     ["uv", "run", "--with", "httpie", "--", "http", "get", "https://httpbin.org/get?email=22f3002723@ds.study.iitm.ac.in"],
#     capture_output=True,
#     text=True
# )
#         result = subprocess.run(
#     ["http", "get", "https://httpbin.org/get?email=22f3002723@ds.study.iitm.ac.in"],
#     capture_output=True,
#     text=True
# )
            url = "https://httpbin.org/get"
            params = {"email": "22f3002723@ds.study.iitm.ac.in"}
            response = requests.get(url, params=params)
        # result = subprocess.run(
        # ["httpie", "get", "https://httpbin.org/get?email=22f3002723@ds.study.iitm.ac.in"],
        # capture_output=True,
        # text=True
        # )
 
            return  response.json()
    except Exception as e:
        return {"error": str(e)}

#run_httpie()
#run_httpie

@app.get("/api")
def read_root():
   return run_httpie()
   #return {"message": "Health check  successfull!"}