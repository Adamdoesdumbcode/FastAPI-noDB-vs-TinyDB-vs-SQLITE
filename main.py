from fastapi import FastAPI
from routes import products

app = FastAPI()

# include product routes
app.include_router(products.router)
