from fastapi import Path, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.config import get_session
from src.database.models import Customer


async def get_customer_by_id_from_path(customer_id: int = Path(...),
                                       session: AsyncSession = Depends(get_session)):
    query = select(Customer).where(Customer.id == customer_id)
    result = await session.execute(query)
    try:
        customer = result.scalars().one()
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail='Sorry, that customer does not exist.'
        )
    return customer
