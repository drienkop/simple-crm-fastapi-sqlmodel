from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.config import get_session
from src.database.models import Product, ProductOut

router = APIRouter()


@router.get('', response_model=List[ProductOut])
async def get_products(session: AsyncSession = Depends(get_session)):
    query = select(Product)
    result = await session.execute(query)
    products = result.scalars().all()
    return products
