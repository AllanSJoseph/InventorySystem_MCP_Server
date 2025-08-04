from pydantic import BaseModel, Field, field_validator
from enum import Enum

import re

# User Validation
class UserType(str, Enum):
    admin = "Admin"
    stocker = "Stocker"
    cashier = "Cashier"

class User(BaseModel):
    username: str = Field(..., min_length=1, max_length=24, description="Username between 1-24 characters")
    password: str = Field(f"{username}123", min_length=1, max_length=24, description="Password between 1-24 characters")
    email: str = Field(..., min_length=1, max_length=255, description="Email address")
    phone: str = Field(..., min_length=10, max_length=10 , description="Valid Phone Number, must be 10 digit and no special characters")
    address: str = Field(..., min_length=10, max_length=255, description="Full address with minimum 10 characters")
    type: UserType = Field(..., min_length=1, max_length=24, description="Type of user: Can be Admin, Stocker or Cashier")

    @field_validator("username")
    def validate_username(cls, value):
        if not value.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username can only contain letters, numbers, hyphens, and underscores')
        return value

    @field_validator("email")
    def validate_email(cls, value):
        pattern = r'^[^@]+@[^@]+\.[^@]+$'
        if not re.match(pattern, str(value)):
            raise ValueError("Custom error: Please enter a valid email address in format name@example.com")
        return value

    @field_validator("phone", mode="before")
    def validate_phone_number(cls, value):
        if not re.fullmatch(r"[6-9]\d{9}", value):
            raise ValueError('Phone number must be 10 digit and no special characters')
        return value

    @field_validator("type")
    def validate_type(cls, value):
        allowed = {
            "admin": UserType.admin,
            "stocker": UserType.stocker,
            "cashier": UserType.cashier,
        }
        formatted_value = value.strip().lower()
        if formatted_value not in allowed:
            raise ValueError('Invalid User type, Only Admin, Stocker or Cashier allowed')
        return allowed[formatted_value]

    class Config:
        extra = "forbid"


# Inventory Item Validation

class InventoryItemInsert(BaseModel):
    name: str = Field(..., min_length=1, max_length=24, description="Name of the product.")
    price: int = Field(..., gt=0, description="Price of the product.")
    stock: int = Field(..., gt=0, description="Stock of the product.")
    description: str = Field(..., min_length=1, max_length=255, description="Description of the product.")

class InventoryItemUpdate(BaseModel):
    prod_id: int = Field(..., gt=0, description="ID of the product.")
    name: str = Field(..., min_length=1, max_length=24, description="Name of the product.")
    price: int = Field(..., gt=0, description="Price of the product.")
    stock: int = Field(..., gt=0, description="Stock of the product.")
    description: str = Field(..., min_length=1, max_length=255, description="Description of the product.")

class InventoryItemUpdateStock(BaseModel):
    prod_id: int = Field(..., gt=0, description="ID of the product.")
    new_stock: int = Field(..., gt=0, description="Stock of the product.")


# Bill Item Validation

class BillItems(BaseModel):
    prod_id: int = Field(..., gt=0, description="ID of the product.")
    quantity: int = Field(..., gt=0, description="Quantity of the product.")

class DraftBill(BaseModel):
    products: list[BillItems]

class PayMethod(str, Enum):
    cash = "CASH"
    card = "CARD"
    upi = "UPI"

class IssueBill(BaseModel):
    invoice_no: int = Field(..., gt=0, description="Invoice No.")
    pay_method: PayMethod = Field(PayMethod.cash, description="Payment Method")

    @field_validator("pay_method")
    def validate_payment_method(cls, value):
        allowed={PayMethod.cash, PayMethod.card, PayMethod.upi}
        formatted_value = value.strip().upper()
        if formatted_value not in allowed:
            raise ValueError('Payment method can only be Cash, Card, or Upi.')
        return value

class BillItemAddOrUpdate(BaseModel):
    invoice_no: int = Field(..., gt=0, description="Invoice no of the bill.")
    prod_id: int = Field(..., gt=0, description="ID of the product.")
    quantity: int = Field(..., gt=0, description="Quantity of the product.")

class BillItemDelete(BaseModel):
    invoice_no: int = Field(..., gt=0, description="ID of the invoice.")
    prod_id: int = Field(..., gt=0, description="ID of the product.")
