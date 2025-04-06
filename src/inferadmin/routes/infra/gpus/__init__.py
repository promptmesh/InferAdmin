from fastapi import APIRouter

router = APIRouter(
    prefix='/gpus'
)

@router.get('/')
async def get_gpus():
    pass

@router.put('/')
async def put_gpus():
    pass

@router.delete('/')
async def delete_gpus():
    pass