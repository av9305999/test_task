from core.service import BaseModelService
from equipment.models import Equipment


class EquipmentService(BaseModelService):

    model = Equipment
