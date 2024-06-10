from typing import Optional, Union
from enum import Enum

class StatusT(str, Enum):
    healthy = 'healthy'
    unhealthy = 'unhealthy'

class MonitoredService:
    def __init__(self, id: str):
        from domain.models.escalation_policy import EscalationPolicy
        self.id: str = id
        self.status: StatusT = 'healthy'
        self.alert_msg: str = ''
        self.acknowledged: bool = False
        self.current_level: int = 0
        self.policy: Optional[EscalationPolicy] = None

    def load_policy(self):
        """ Loads the Escalation Policy from its service """
        from domain.services.service_provider import ServiceProvider
        policy_service = ServiceProvider.get('escalation')
        
        policy = policy_service.get(self.id)
        if not policy:
            raise ValueError(f"Missing policy for service '{self.id}'")
        self.policy = policy

    def set_unhealthy(self, msg: str):
        self.status = 'unhealthy'
        self.current_level = 0
        self.alert_msg = msg
        self.acknowledged = False

    def set_healthy(self):
        self.status = 'healthy'
        self.current_level = 0
        self.alert_msg = ''
        self.acknowledged = False

    def set_acknowledged(self):
        self.acknowledged = True

    def notify(self):
        """ Notify all targets at the current level """
        if not self.policy:
            raise ValueError("Policy was not loaded")

        targets = self.policy.levels[self.current_level].targets
        for target in targets:
            target.notify(self, self.alert_msg)

    def escalate(self) -> bool:
        """ Escalate the alert to the next level """
        if not self.policy:
            raise ValueError("Policy was not loaded")

        # Last level reached
        if self.current_level == len(self.policy.levels) - 1:
            return False

        self.current_level += 1
        return True
