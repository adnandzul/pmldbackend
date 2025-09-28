from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    nama_perusahaan = Column(String, index=True, unique=True)
    detail_perusahaan = Column(Text)
    kendala = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.now)

    reports = relationship("Report", back_populates="company")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    target_ip = Column(String, index=True)
    cve_list = Column(String) 
    status = Column(String, default="Selesai")
    hasil_pentest_json = Column(Text) 
    timestamp = Column(DateTime, default=datetime.datetime.now)
    
    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship("Company", back_populates="reports")