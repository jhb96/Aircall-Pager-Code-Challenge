from domain.models.target import Target
from typing import List

class Level:
    def __init__(self, level: int, targets: List[Target]):
        self.level = level
        self.targets = targets
