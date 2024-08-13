from ninja import NinjaAPI, Schema
from ninja.responses import StreamingResponse
from django_sse.views import BaseSseView
from .models import TempHumidityRecord
import json
import time

api = NinjaAPI()

class TempHumiditySchema(Schema):
    temperature: float
    humidity: float

# Endpoint to add temperature and humidity records
@api.post("/add/")
def add_record(request, payload: TempHumiditySchema):
    record = TempHumidityRecord.objects.create(
        temperature=payload.temperature,
        humidity=payload.humidity
    )
    # Trigger an SSE event for real-time updates
    send_event_to_clients(record)
    return {"success": True, "record_id": record.id}

# SSE function to send updates to connected clients
def send_event_to_clients(record):
    # You can implement a more sophisticated event-pushing mechanism here
    latest_event = {
        "temperature": record.temperature,
        "humidity": record.humidity,
        "timestamp": record.timestamp.isoformat()  # Ensure the timestamp is JSON serializable
    }
    # Example of broadcasting the event to connected clients
    # You might use a more advanced method depending on your architecture
    broadcast_to_clients(json.dumps(latest_event)) # type: ignore

# Real-time data streaming endpoint using SSE
@api.get("/realtime/")
def realtime(request):
    def event_stream():
        while True:
            # Wait for new events (implement waiting logic)
            event = wait_for_new_event()  # You need to implement this to block until a new event is ready
            if event:
                yield f"data: {event}\n\n"
            time.sleep(1)  # Adjust the frequency as needed
    
    return StreamingResponse(event_stream(), media_type="text/event-stream")

# Example function to get the latest event (needs implementation)
def wait_for_new_event():
    # Implement logic to retrieve and block until the latest event data is available
    return None
