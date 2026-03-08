from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.features.grievance import routes as grievance_routes
from app.features.form import routes as form_routes
from app.features.image_validation import routes as image_validation_routes

app = FastAPI(title="CIVIC.AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://main.d2rueo5r10xv7x.amplifyapp.com",
        "https://d1gvv7q2zsapho.cloudfront.net",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(grievance_routes.router)
app.include_router(form_routes.router)
app.include_router(image_validation_routes.router)

@app.get("/")
def root():
    return {"message": "CIVIC.AI Backend Running 🚀"}