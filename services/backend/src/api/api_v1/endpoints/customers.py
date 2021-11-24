from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.config import get_session
from src.database.models import CustomerOut, Customer, Address, CustomerIn, ProductOut, ProductUpdate, Product
from src.api.api_v1.dependencies.customers import get_customer_by_id_from_path

router = APIRouter()


@router.get('', response_model=List[CustomerOut])
async def get_customers(mobile_number: Optional[str] = None,
                        email: Optional[str] = None,
                        house_number: Optional[str] = None,
                        zip_code: Optional[str] = None,
                        session: AsyncSession = Depends(get_session)):
    query = select(Customer).options(selectinload(Customer.address)).options(selectinload(Customer.products))
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


@router.post('', response_model=CustomerOut)
async def create_customer(customer: CustomerIn,
                          session: AsyncSession = Depends(get_session)):
    customer_obj = Customer.from_orm(customer)
    address_obj = Address.from_orm(customer.address)
    customer_obj.address = address_obj
    session.add(customer_obj)

    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail='Sorry, that customer already exists.'
        )

    await session.refresh(customer_obj)
    return customer_obj


@router.get('/{customer_id}', response_model=CustomerOut)
async def get_one_customer(customer: Customer = Depends(get_customer_by_id_from_path)):
    return customer


@router.get('/{customer_id}/products', response_model=List[ProductOut])
async def get_customer_products(customer: Customer = Depends(get_customer_by_id_from_path)):
    products = customer.products
    return products


@router.patch('/{customer_id}/products', response_model=List[ProductOut])
async def add_customer_product(product: ProductUpdate,
                               customer: Customer = Depends(get_customer_by_id_from_path),
                               session: AsyncSession = Depends(get_session)):
    query = select(Product).where(Product.id == product.product_id)
    result = await session.execute(query)
    try:
        product = result.scalars().one()
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail='Sorry, that product does not exist.'
        )

    customer_obj = customer
    customer_obj.products.append(product)
    session.add(customer_obj)
    await session.commit()
    await session.refresh(customer_obj)

    products = customer_obj.products
    return products
