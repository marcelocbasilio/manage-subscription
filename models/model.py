from sqlmodel import Field, Relationship, SQLModel
from typing import Optional
from datetime import date
from decimal import Decimal

class Subscription(SQLModel, table=True):
    id: int = Field(primary_key=True)
    enterprise: str
    site: Optional[str] = None
    dateSignature: date
    price: Decimal


class Payments(SQLModel, table=True):
    id: int = Field(primary_key=True)
    subscriptionId: int = Field(foreign_key='subscription.id')
    subscription: Subscription = Relationship()
    date: date

    