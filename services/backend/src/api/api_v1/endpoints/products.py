from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.config import get_session
from src.database.models import Product, ProductOut, ProductIn

router = APIRouter()


@router.get('', response_model=List[ProductOut])
async def get_products(session: AsyncSession = Depends(get_session)):
    query = select(Product)
    result = await session.execute(query)
    products = result.scalars().all()
    return products


@router.post('', response_model=ProductOut)
async def create_product(product: ProductIn,
                         session: AsyncSession = Depends(get_session)):
    product_obj = Product.from_orm(product)
    session.add(product_obj)

    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail='Sorry, that product already exists.'
        )

    await session.refresh(product_obj)
    return product_obj


@router.get('/{product_id}', response_model=ProductOut)
async def get_one_product(product_id: int,
                          session: AsyncSession = Depends(get_session)):
    query = select(Product).where(Product.id == product_id)
    result = await session.execute(query)
    try:
        product = result.scalars().one()
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail='Sorry, that product does not exist.'
        )
    return product
