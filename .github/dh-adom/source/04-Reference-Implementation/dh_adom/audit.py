from .models import AuditEvent
from datetime import datetime, timezone

class AuditLog:
    def __init__(self): self.events=[]
    def record(self, actor, action, resource, result, delegation_id=None, **details):
        event=AuditEvent(
            event_id=f"EVT-{len(self.events)+1:05d}", actor=actor, action=action,
            resource=resource, result=result, delegation_id=delegation_id,
            details={"timestamp": datetime.now(timezone.utc).isoformat(), **details}
        )
        self.events.append(event)
        return event
