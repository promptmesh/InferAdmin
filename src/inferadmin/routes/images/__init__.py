from fastapi import APIRouter

router = APIRouter(
    prefix='/images'
)

@router.get('/')
async def get_images():
    pass

@router.put('/')
async def put_images():
    pass

@router.delete('/')
async def delete_images():
    pass