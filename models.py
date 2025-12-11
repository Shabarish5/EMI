from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field

class EMI(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # e.g., "Home Loan", "Car Loan"
    amount: float
    currency: str = "INR"
    
    # Frequency: "Monthly", "Quarterly", "Yearly"
    frequency: str = "Monthly"
    
    # Dates
    start_date: date
    next_due_date: date
    end_date: Optional[date] = None
    
    # Status
    active: bool = True
    bank_name: Optional[str] = None
    
    # Reminder Settings (how many days before to alert)
    reminder_days: int = 3