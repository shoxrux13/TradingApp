from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from operations.models import operation
from operations.schemas import OperationCreate

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)


@router.get("/")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(operation).where(operation.c.type == operation_type)
    result = await session.execute(query)
    response_data = [
        {
            "id": row.id,
            "quantity": row.quantity,
            "figi": row.figi,
            "instrument_type": row.instrument_type,
            "date": row.date,
            "type": row.type
        }
        for row in result.all()
    ]
    return response_data


@router.post("/")
async def add_pecific_operation(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(
        **new_operation.dict()
    )
    try:
        await session.execute(stmt)
        await session.commit()
        response_data = {
            "status": "success",
            "code": 201, 
            "message": "Operation added successfully",
            "data": {
                "id": new_operation.id,
                "quantity": new_operation.quantity,
                "figi": new_operation.figi,
                "instrument_type": new_operation.instrument_type,
                "date": new_operation.date,
                "type": new_operation.type
            }
        }
    except Exception as e:
        response_data = {
            "status": "error",
            "code": 400,
            "message": "Operation could not be added",
            "data": str(e)
        }

    return response_data
