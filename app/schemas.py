from pydantic import BaseModel
import datetime

class ReportBase(BaseModel):
    nama_perusahaan: str
    target_ip: str
    hasil_pentest: str

class ReportCreate(ReportBase):
    pass

class Report(ReportBase):
    id: int
    timestamp: datetime.datetime

    class Config:
        orm_mode = True