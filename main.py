from fastapi import FastAPI
from routes import products
from security import DEV_KEY


app = FastAPI()

# include product routes
app.include_router(products.router)
