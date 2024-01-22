from uuid import UUID

from fastapi import Path
from typing_extensions import Annotated

from app import crud
from app.exceptions.common import IdNotFoundException
from app.models import StringDefectTypes


async def get_string_defect_type_by_id_from_path(
    string_defect_type_id: Annotated[UUID, Path(description="The UUID id of the StringDefectTypes")]
) -> StringDefectTypes:
    """
    Get a StringDefectType from database by id from the path

    :param string_defect_type_id: UUID
    :return: StringDefectTypes
    """

    string_defect_type = await crud.string_defect_types.get_by_id(id=string_defect_type_id)
    if not string_defect_type:
        raise IdNotFoundException(StringDefectTypes, incoming_id=string_defect_type_id)
    return string_defect_type
