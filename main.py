from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from dotenv import load_dotenv
import os
from dateutil.relativedelta import relativedelta

# Import your models
from models import EMI
from database import create_db_and_tables, get_session

load_dotenv()

app = FastAPI(title="EMI Alert System API")

# --- CORS (Allow access from your future App) ---
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# --- CRUD ENDPOINTS ---

@app.post("/emis/", response_model=EMI)
def create_emi(emi: EMI, session: Session = Depends(get_session)):
    session.add(emi)
    session.commit()
    session.refresh(emi)
    return emi

@app.get("/emis/", response_model=list[EMI])
def read_emis(session: Session = Depends(get_session)):
    emis = session.exec(select(EMI)).all()
    return emis

@app.get("/emis/{emi_id}", response_model=EMI)
def read_emi(emi_id: int, session: Session = Depends(get_session)):
    emi = session.get(EMI, emi_id)
    if not emi:
        raise HTTPException(status_code=404, detail="EMI not found")
    return emi

@app.put("/emis/{emi_id}", response_model=EMI)
def update_emi(emi_id: int, emi_data: EMI, session: Session = Depends(get_session)):
    db_emi = session.get(EMI, emi_id)
    if not db_emi:
        raise HTTPException(status_code=404, detail="EMI not found")
    
    emi_dict = emi_data.dict(exclude_unset=True)
    for key, value in emi_dict.items():
        setattr(db_emi, key, value)
        
    session.add(db_emi)
    session.commit()
    session.refresh(db_emi)
    return db_emi

@app.delete("/emis/{emi_id}")
def delete_emi(emi_id: int, session: Session = Depends(get_session)):
    emi = session.get(EMI, emi_id)
    if not emi:
        raise HTTPException(status_code=404, detail="EMI not found")
    session.delete(emi)
    session.commit()
    return {"message": "EMI deleted successfully"}

@app.post("/emis/{emi_id}/pay", response_model=EMI)
def mark_emi_paid(emi_id: int, session: Session = Depends(get_session)):
    emi = session.get(EMI, emi_id)
    if not emi:
        raise HTTPException(status_code=404, detail="EMI not found")
    
    # Update due date based on frequency
    if emi.frequency == "Monthly":
        emi.next_due_date += relativedelta(months=1)
    elif emi.frequency == "Quarterly":
        emi.next_due_date += relativedelta(months=3)
    elif emi.frequency == "Yearly":
        emi.next_due_date += relativedelta(years=1)
    
    session.add(emi)
    session.commit()
    session.refresh(emi)
    return emi