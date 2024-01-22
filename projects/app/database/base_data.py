from app.schemas.work_type_schema import IWorkTypeCreate
from app.schemas.project_status_schema import IProjectStatusCreate
from app.schemas.object_status_schema import IObjectStatusCreate


work_types: list[IWorkTypeCreate] = [
    IWorkTypeCreate(name="Тип работ 1"),
    IWorkTypeCreate(name="Тип работ 2"),
    IWorkTypeCreate(name="Тип работ 3"),
]

project_statuses: list[IProjectStatusCreate] = [
    IProjectStatusCreate(name="Состояние проекта 1"),
    IProjectStatusCreate(name="Состояние проекта 2"),
    IProjectStatusCreate(name="Состояние проекта 3"),
]

object_statuses: list[IObjectStatusCreate] = [
    IObjectStatusCreate(name="Состояние объекта 1"),
    IObjectStatusCreate(name="Состояние объекта 2"),
    IObjectStatusCreate(name="Состояние объекта 3"),
]