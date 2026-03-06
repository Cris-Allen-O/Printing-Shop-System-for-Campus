from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
import os

from routes.orders import router as orders_router

app = FastAPI(title="Printing Shop Order Management System", version="1.0.0")

# mount a directory for frontend assets
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(orders_router)

@app.get("/", response_class=HTMLResponse)
def read_root():
    # serve the static index.html if it exists
    index_path = os.path.join(os.getcwd(), "static", "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    # fallback message
    return {"message": "Welcome to the Printing Shop Order Management System"}