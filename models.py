from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field

class EMI(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Basic Info
    person_name: str
    name: str  # e.g., "Car Loan"
    bank_name: str
    amount: float
    currency: str = "INR"
    
    # "Duration" is the Frequency here
    # Options: "Monthly", "Quarterly", "Half-Yearly", "Yearly"
    frequency: str = "Monthly"
    
    # Dates
    start_date: date
    next_due_date: date
    end_date: date
    
    # Settings
    reminder_days: int = 3 # Custom alert days
    active: bool = True
