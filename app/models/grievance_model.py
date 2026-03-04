from pydantic import BaseModel

class Grievance(BaseModel):
    complaint_text: str
    state: str
    issue: str