import sys, os
from fastapi import FastAPI, HTTPException, Path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
print(sys.path)
from src.domain.services.pager_service import ServicePager
from src.domain.models.alert import Alert


app = FastAPI()



# Custom adapters for your system
# Mocked for now
from unittest.mock import MagicMock

pager_service = ServicePager(
    escalation_system = MagicMock(),
    mail_system=MagicMock(),
    sms_system=MagicMock(),
    timer_system=MagicMock(),
    repository=MagicMock()
)

@app.post('/alert')
def receive_alert(alert: Alert):
    # TODO
    pager_service.handle_alert(alert.service_id, alert.message)
    return {"message": "Alert received"}


@app.post("/health/{service_id}")
async def service_health(service_id: str):
    # TODO
    pager_service.mark_service_healthy(service_id)
    return {"message": "Service marked as healthy"}

@app.post("/acknowledge/{service_id}")
async def acknowledge_alert(service_id: str):
    # TODO
    pager_service.acknowledge_alert(service_id)
    return {"message": "Alert acknowledged"}

@app.post("/timeout/{service_id}")
async def timeout(service_id: str):
    # TODO
    pager_service.handle_timeout(service_id)
    return {"message": "Timeout handled"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)