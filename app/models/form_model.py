from pydantic import BaseModel, Field


class ExtractedFormFields(BaseModel):
    full_name: str | None = None
    date_of_birth: str | None = None
    address: str | None = None
    id_number: str | None = None
    document_type: str | None = None


class GeneratePdfRequest(BaseModel):
    fields: ExtractedFormFields
    application_title: str = Field(default="Government Scheme Application")
    scheme_name: str | None = None
    language_hint: str | None = None
