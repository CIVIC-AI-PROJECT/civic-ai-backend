from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from app.features.grievance import routes as grievance_routes
from app.features.form import routes as form_routes
from app.features.image_validation import routes as image_validation_routes

app = FastAPI(title="CIVIC.AI Backend")

app.include_router(grievance_routes.router)
app.include_router(form_routes.router)
app.include_router(image_validation_routes.router)

@app.get("/")
def root():
    return {"message": "CIVIC.AI Backend Running 🚀"}