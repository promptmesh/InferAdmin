from fastapi import APIRouter

router = APIRouter(
    prefix='/llms'
)

@router.get('/')
async def get_llms():
    pass

@router.put('/')
async def put_llms():
    pass

@router.delete('/')
async def delete_llms():
    pass