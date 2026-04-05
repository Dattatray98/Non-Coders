import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1. Define allowed origins (domains)
origins = [
    "http://localhost:5173",  # Example: React app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,  # Allows cookies/auth headers
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/clash/data")
def clash_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    output_dir = os.path.join(base_dir, "output")
    
    if os.path.exists(output_dir):
        # We only want raw clash data for this endpoint, not the AI rerouting schema
        json_files = [f for f in os.listdir(output_dir) if f.endswith(".json") and f != "ai_reroutes.json"]
        if json_files:
            file_path = os.path.join(output_dir, json_files[0])
            try:
                with open(file_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                
    return []

@app.get("/clash/ai")
def clash_ai_suggestions():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    file_path = os.path.join(base_dir, "output", "ai_reroutes.json")
    
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except Exception as e:
            return []
    return []
