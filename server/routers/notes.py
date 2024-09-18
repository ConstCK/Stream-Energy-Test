from fastapi import APIRouter, status, Depends, Request

from crud.notes import NoteService

from schemas.notes import Note, NoteCreation, NoteUpdate
from services.auth import access_granted

# Маршрут для заметок
router = APIRouter(prefix='/api/v1/notes')


# Маршрут для получения всех заметок для авторизированных пользователей
@router.get('/', description='Get all notes', response_model=list[Note],
            status_code=status.HTTP_200_OK, name='get_all_notes_url',
            responses={200: {'description': 'Успешное получение объектов'}, }
            )
async def get_notes(tg_id: int, tag_id: int = None, service: NoteService = Depends(),
                    permission: bool = Depends(access_granted)):
    if permission:
        result = await service.get_all_notes(tg_id=tg_id, tag_id=tag_id)
        return result


# Маршрут для получения заметки по id для авторизированных пользователей
@router.get('/{note_id}', description='Get single note', response_model=Note,
            status_code=status.HTTP_200_OK, name='get_note_url',
            responses={200: {'description': 'Успешное получение объекта'}, }
            )
async def get_notes(note_id: int, tg_id: int, service: NoteService = Depends(),
                    permission: bool = Depends(access_granted)):
    if permission:
        result = await service.get_note_by_id(note_id=note_id, tg_id=tg_id)
        return result


# Маршрут для создания заметки для авторизированных пользователей
@router.post('/', description='Create note',
             status_code=status.HTTP_201_CREATED, name='note_creation',
             responses={201: {'description': 'Успешное создание объекта'},
                        409: {'description': 'Объект уже существует'}}
             )
async def post_note(data: NoteCreation, service: NoteService = Depends(),
                    permission: bool = Depends(access_granted)) -> dict[str, str]:
    if permission:
        result = await service.create_note(data)
        return result


# Маршрут для удаления заметки для авторизированных пользователей
@router.delete('/{note_id}', description='Delete note',
               status_code=status.HTTP_200_OK, name='note_deletion',
               responses={201: {'description': 'Успешное удаление объекта'},
                          404: {'description': 'Объект не найден'},
                          422: {'description': 'Ошибка валидации данных'}}
               )
async def delete_note(note_id: int, service: NoteService = Depends(),
                      permission: bool = Depends(access_granted)) -> dict[str, str]:
    if permission:
        result = await service.delete_note(note_id)
        return result


# Маршрут для обновления заметки для авторизированных пользователей
@router.patch('/{note_id}', description='Update note',
              status_code=status.HTTP_200_OK, name='note_update',
              responses={201: {'description': 'Успешное обновление объекта'},
                         404: {'description': 'Объект не найден'},
                         422: {'description': 'Ошибка валидации данных'}}
              )
async def patch_note(note_id: int, data: NoteUpdate, service: NoteService = Depends(),
                     permission: bool = Depends(access_granted)) -> dict[str, str]:
    if permission:
        result = await service.update_note(note_id=note_id, data=data)
        return result
