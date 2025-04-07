import json

from pydantic import BaseModel


class Entity(BaseModel):
    id: str
    speckle_type: str
    area: float = 0.0
    data: dict


class ParserService:

    @classmethod
    def parse(cls, file: bytes) -> list[Entity]:
        result = []
        data = json.loads(file)
        for d in data:

            prepared = {}
            if 'speckle_type' not in d:
                continue
            prepared['speckle_type'] = d.get('speckle_type', '')
            quanitites = d.get('materialQuantities', [])
            if len(quanitites) != 0:
                prepared['area'] = quanitites[0].get('area', 0.0)
            prepared['data'] = d
            prepared['id'] = d.get('id', "")

            result.append(Entity(**prepared))

        return result
