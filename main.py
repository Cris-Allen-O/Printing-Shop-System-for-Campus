from fastapi import FastAPI
from routes.orders import router as orders_router

app = FastAPI(title="Printing Shop Order Management System", version="1.0.0")

app.include_router(orders_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Printing Shop Order Management System"}