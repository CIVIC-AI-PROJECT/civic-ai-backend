from pydantic import BaseModel
from datetime import datetime

class Grievance(BaseModel):
    complaint_text: str
    state: str
    issue: str


class IncomingGrievance(BaseModel):
    complaint_text: str
    state: str | None = None
    issue: str | None = None
    village: str | None = None
    block: str | None = None
    official_name: str | None = None
    received_at: datetime | None = None


class GrievanceBatchRequest(BaseModel):
    complaints: list[IncomingGrievance]