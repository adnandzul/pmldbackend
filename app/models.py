from sqlalchemy import Column, Integer, String, DateTime, Text
from .database import Base
import datetime

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    nama_perusahaan = Column(String, index=True)
    target_ip = Column(String)
    hasil_pentest = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.now)