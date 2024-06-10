from domain.models.level import Level
from typing import List


class EscalationPolicy:
    def __init__(self, levels:  List[Level]):
        self.levels = levels

