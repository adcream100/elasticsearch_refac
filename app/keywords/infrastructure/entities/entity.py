from core.infrastructure.entities.entity import Entity

class PopularSearchEntity(Entity):
    term: str
    category: str
    count: int