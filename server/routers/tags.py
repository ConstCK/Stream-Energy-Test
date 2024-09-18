from fastapi import APIRouter, status, Request, Depends

from crud.tags import TagService
from schemas.tags import Tag

# Маршрут для тегов
router = APIRouter(prefix='/api/v1/tags', )


# Маршрут для получения всех тегов для авторизированных пользователей
@router.get('/', description='Get all tags', response_model=list[Tag],
            status_code=status.HTTP_200_OK, name='get_all_notes_url',
            responses={200: {'description': 'Успешное получение объектов'}, }
            )
async def get_tags(request: Request,service: TagService = Depends()):
    result = await service.get_all_tags()
    return result
