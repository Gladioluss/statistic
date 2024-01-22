from uuid import UUID

from fastapi import Path
from typing_extensions import Annotated

from app import crud
from app.exceptions.common import IdNotFoundException
from app.models import StringDefectsHistory


async def get_string_defects_history_by_id_from_path(
    string_defects_history_id: Annotated[UUID, Path(description="The UUID id of the StringDefectsHistory")]
) -> StringDefectsHistory:
    """
    Get a StringDefectsHistory from database by id from the path

    :param string_defects_history_id: UUID
    :return: StringDefectsHistory
    """

    string_defects_history= await crud.string_defects_history.get_by_id(id=string_defects_history_id)
    if not string_defects_history:
        raise IdNotFoundException(StringDefectsHistory, incoming_id=string_defects_history_id)
    return string_defects_history
