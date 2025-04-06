from fastapi import APIRouter

router = APIRouter(
    prefix='/volumes'
)

@router.get('/')
async def get_volumes():
    pass

@router.put('/')
async def put_volumes():
    pass

@router.delete('/')
async def delete_volumes():
    pass