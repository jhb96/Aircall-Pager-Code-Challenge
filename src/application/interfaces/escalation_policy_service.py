from abc import ABC, abstractmethod
from domain.models.escalation_policy import EscalationPolicy

class IEscalationPolicyService(ABC):
    @abstractmethod
    def get(self, service_id: str) -> EscalationPolicy:
        pass
