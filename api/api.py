# api.py
from fastapi import FastAPI, Form, File, UploadFile
from typing import Dict, Any,Optional
#import subprocess
import requests
import json
app = FastAPI()

def run_uvhttpie():
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

def function_gpt(user_input: str, tools: list[Dict[str, Any]]) -> Dict[str, Any]:
    proxy_url="http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    auth_token ="eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIyZjMwMDI3MjNAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.wGu8bVE0Tod-xXNmm3PJqCXqmgWSshwNqp6Tl1kexbs"	
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": user_input},
                
        ],      
	"tools": tools,
    "tool_choice": "auto",
    "max_tokens": 500,
    "temperature": 0.7
    }
	
    response = requests.post(
            proxy_url,
            headers={"Content-Type": "application/json",                     
            "Authorization": f"Bearer {auth_token}"},
            data=json.dumps(payload)
        )
    response_json = response.json()
    print("*******************")
    print (response_json )
    return response.json()["choices"][0]["message"]

#run_httpie()
#run_httpie

tools = [
    {
        "type": "function",
        "function": {
            "name": "run_uvhttpie",
            "description": "uv call to http url",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_path": {
                        "type": "string",
                        "description": "input file path hardcoded to ./data/email.txt"
                    }
                },
                "required": ["input_path"],
                "additionalProperties": False
                },
            "strict": True
        }
    }
]
@app.post("/api")
async def run_task(
    question: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
  print ("************")
  print (question)
  response=function_gpt(question,tools)
  print("response=" + str(response))
  tool_calls = response.get('tool_calls', [])

  for tool_call in tool_calls:
        function_name = tool_call['function']['name']
        arguments_json = tool_call['function']['arguments']
        arguments = json.loads(arguments_json)
    
        print (function_name)
        function_map = {
            "run_uvhttpie": run_uvhttpie
        }

        if function_name in function_map:
            result = function_map[function_name]()
        else:
            result = f"Function '{function_name}' not found"
        #extract_recent_log_lines()
        
        return  result
        
#def read_root():
#   return run_httpie()
   #return {"message": "Health check  successfull!"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)