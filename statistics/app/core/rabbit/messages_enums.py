from enum import Enum


class EntityType(str, Enum):
    PROJECT = "Project"
    SUBPROJECT = "Subproject"
    TOWER_ENTITY = "TowerEntity"
    SPAN_ENTITY = "SpanEntity"
    TOWER_DEFECTS = "TowerDefects"


class ActionType(str, Enum):
    CREATE = "Create"
    UPDATE = "Update"

