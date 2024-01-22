from uuid import UUID

from fastapi import Path
from typing_extensions import Annotated

from app import crud
from app.exceptions.common import IdNotFoundException
from app.models import StringDefects


async def get_string_defect_by_id_from_path(
    string_defect_id: Annotated[UUID, Path(description="The UUID id of the StringDefects")]
) -> StringDefects:
    """
    Get a StringDefects from database by id from the path

    :param string_defect_id: UUID
    :return: StringDefects
    """

    string_defect = await crud.string_defects.get_by_id(id=string_defect_id)
    if not string_defect:
        raise IdNotFoundException(StringDefects, incoming_id=string_defect_id)
    return string_defect
