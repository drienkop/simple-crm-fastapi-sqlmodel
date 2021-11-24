from typing import Optional, List

from sqlalchemy import String
from sqlalchemy.sql.schema import Column
from sqlmodel import SQLModel, Field, Relationship


class AddressBase(SQLModel):
    street_name: str
    house_number: str
    city: str
    zip_code: str


class Address(AddressBase, table=True):
    id: int = Field(default=None, primary_key=True)
    customers: List['Customer'] = Relationship(back_populates='address')


class AddressOut(AddressBase):
    pass


class AddressIn(AddressBase):
    pass


class CustomerBase(SQLModel):
    first_name: str
    last_name: str
    birth_date: str
    gender: str
    mobile_number: str
    email: str


class Customer(CustomerBase, table=True):
    id: int = Field(default=None, primary_key=True)
    address_id: Optional[int] = Field(default=None, foreign_key='address.id')
    address: Optional[Address] = Relationship(back_populates='customers',
                                              sa_relationship_kwargs={'lazy': 'selectin'})
    mobile_number: str = Field(sa_column=Column('mobile_number', String, unique=True))
    email: str = Field(sa_column=Column('email', String, unique=True))


class CustomerOut(CustomerBase):
    id: int
    address: Optional[AddressOut]


class CustomerIn(CustomerBase):
    address: Optional[AddressIn]


class ProductBase(SQLModel):
    name: Optional[str] = None


class Product(ProductBase, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column('name', String, unique=True))


class ProductOut(ProductBase):
    id: int
    name: str


class ProductIn(ProductBase):
    name: str
