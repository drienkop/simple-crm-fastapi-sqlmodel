from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.config import get_session
from src.database.models import CustomerOut, Customer, Address

router = APIRouter()


@router.get('', response_model=List[CustomerOut])
async def get_customers(mobile_number: Optional[str] = None,
                        email: Optional[str] = None,
                        house_number: Optional[str] = None,
                        zip_code: Optional[str] = None,
                        session: AsyncSession = Depends(get_session)):
    query = select(Customer).options(selectinload(Customer.address))
    if mobile_number:
        query = query.where(Customer.mobile_number == mobile_number)
    if email:
        query = query.where(Customer.email == email)

    if house_number or zip_code:
        query = query.join(Customer.address)
    if house_number:
        query = query.where(Address.house_number == house_number)
    if zip_code:
        query = query.where(Address.zip_code == zip_code)

    result = await session.execute(query)
    customers = result.scalars().all()
    return customers
