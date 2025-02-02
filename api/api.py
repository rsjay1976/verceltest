from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Enable CORS for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Load data from JSON file
def load_data():
    with open("q-vercel-python.json", "r", encoding="utf-8") as file:
        return json.load(file)

students_data = load_data()

@app.get("/api")
def get_marks(name: list[str] = Query(None)):
    if name:
        marks_list = [student["marks"] for student in students_data if student["name"] in name]
        return {"marks": marks_list}
    return {"marks": []}

# Local run (not required for Vercel)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
