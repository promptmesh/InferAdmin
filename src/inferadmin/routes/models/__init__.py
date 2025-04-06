from fastapi import APIRouter

router = APIRouter(
    prefix='/models'
)

@router.get('/')
async def get_models():
    pass

@router.put('/')
async def put_models():
    pass

@router.delete('/')
async def delete_models():
    pass