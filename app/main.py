from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
import random

from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pentest API", description="API untuk simulasi alur penetration testing")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def simulate_pentest(target_ip: str, cve_list: List[str]) -> str:
    """Fungsi ini mensimulasikan hasil pentest dan mengembalikannya sebagai JSON string."""
    vulnerabilities = []
    for cve in cve_list:
        vulnerabilities.append({
            "cve_id": cve,
            "severity": random.choice(["Critical", "High", "Medium", "Low"]),
            "description": f"Ditemukan potensi kerentanan {cve} pada service di port {random.randint(1, 65535)}.",
            "remediation": "Segera lakukan patching atau update sistem sesuai rekomendasi vendor."
        })
    
    report_data = {
        "target_ip": target_ip,
        "summary": f"Pentest selesai. Ditemukan {len(vulnerabilities)} potensi kerentanan.",
        "vulnerabilities": vulnerabilities,
        "report_generated_at": datetime.datetime.now().isoformat()
    }
    
    return json.dumps(report_data, indent=4)

# === ENDPOINTS ===

@app.post("/companies/", response_model=schemas.Company, summary="1. Mendaftarkan Perusahaan Baru")
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    """
    Endpoint pertama yang digunakan perusahaan untuk mendaftar.
    - **nama_perusahaan**: Nama unik perusahaan.
    - **detail_perusahaan**: Deskripsi atau identitas.
    - **kendala**: Apa saja yang ingin diperiksa.
    """
    db_company = db.query(models.Company).filter(models.Company.nama_perusahaan == company.nama_perusahaan).first()
    if db_company:
        raise HTTPException(status_code=400, detail="Nama perusahaan sudah terdaftar")
    
    new_company = models.Company(**company.model_dump())
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company

@app.post("/pentest/", response_model=schemas.Report, summary="2. Memulai Proses Pentest")
def start_pentest(request: schemas.PentestRequest, db: Session = Depends(get_db)):
    """
    Setelah perusahaan terdaftar, gunakan endpoint ini untuk memulai pentest.
    - **company_id**: ID perusahaan yang didapat setelah mendaftar.
    - **target_ip**: Alamat IP yang akan di-pentest.
    - **cve_list**: Daftar CVE yang ingin diperiksa.
    """
    db_company = db.query(models.Company).filter(models.Company.id == request.company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company ID tidak ditemukan")
    
    hasil_json = simulate_pentest(request.target_ip, request.cve_list)
    
    cve_string = ", ".join(request.cve_list) 
    
    new_report = models.Report(
        company_id=request.company_id,
        target_ip=request.target_ip,
        cve_list=cve_string,
        hasil_pentest_json=hasil_json
    )
    
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    
    return new_report

@app.get("/history/reports/", response_model=List[schemas.Report], summary="3. Melihat Semua Riwayat Laporan")
def get_all_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Melihat semua riwayat laporan pentest yang pernah dibuat.
    """
    reports = db.query(models.Report).offset(skip).limit(limit).all()
    return reports

@app.get("/history/companies/", response_model=List[schemas.Company], summary="Melihat Semua Perusahaan Terdaftar")
def get_all_companies(db: Session = Depends(get_db)):
    """
    Melihat semua perusahaan yang sudah terdaftar beserta laporannya.
    """
    return db.query(models.Company).all()