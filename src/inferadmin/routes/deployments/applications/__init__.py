from fastapi import APIRouter

router = APIRouter(
    prefix='/applications'
)

@router.get('/')
async def get_applications():
    pass

@router.put('/')
async def put_applications():
    pass

@router.delete('/')
async def delete_applications():
    pass