"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Optional, List

# Example schemas (you can keep or remove as needed)

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: Optional[str] = Field(None, description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Agency app schemas

class Project(BaseModel):
    """
    Creative projects for the portfolio grid/carousel
    Collection name: "project"
    """
    title: str = Field(..., description="Project title")
    subtitle: Optional[str] = Field(None, description="Short punchy subtitle")
    description: Optional[str] = Field(None, description="Brief description of the project")
    thumbnail: Optional[HttpUrl] = Field(None, description="Preview image URL")
    tags: List[str] = Field(default_factory=list, description="Tech/discipline tags")
    case_study_url: Optional[HttpUrl] = Field(None, description="Link to full case study")
    client: Optional[str] = Field(None, description="Client name")
    featured: bool = Field(False, description="Show in featured row")

class ContactMessage(BaseModel):
    """
    Messages from the contact form
    Collection name: "contactmessage"
    """
    name: str = Field(..., min_length=2, description="Sender name")
    email: EmailStr = Field(..., description="Reply-to email")
    company: Optional[str] = Field(None, description="Company or organization")
    message: str = Field(..., min_length=10, max_length=2000, description="Inquiry details")
