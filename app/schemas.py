from pydantic import BaseModel
from typing import List, Optional
import datetime

class ReportBase(BaseModel):
    target_ip: str
    cve_list: str
    status: str
    hasil_pentest_json: str

class Report(ReportBase):
    id: int
    company_id: int
    timestamp: datetime.datetime

    class Config:
        orm_mode = True

class CompanyBase(BaseModel):
    nama_perusahaan: str
    detail_perusahaan: str
    kendala: str

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    created_at: datetime.datetime
    reports: List[Report] = []

    class Config:
        orm_mode = True

class PentestRequest(BaseModel):
    company_id: int
    target_ip: str
    cve_list: List[str]