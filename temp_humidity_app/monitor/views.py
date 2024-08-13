from django.shortcuts import render
from ninja import Router, Schema
from django.http import StreamingHttpResponse
from .models import TempHumidityRecord
import json
import time

router = Router()

# Schema for temperature and humidity data submission
class TempHumiditySchema(Schema):
    temperature: float
    humidity: float

# View to handle adding new temperature and humidity records
@router.post("/add/")
def add_record(request, payload: TempHumiditySchema):
    record = TempHumidityRecord.objects.create(
        temperature=payload.temperature,
        humidity=payload.humidity
    )
    # Trigger an SSE event for real-time updates
    broadcast_new_record(record)
    return {"success": True, "record_id": record.id}

# Function to broadcast new records to SSE clients
def broadcast_new_record(record):
    # Convert the record to a JSON-serializable dictionary
    event_data = {
        "temperature": record.temperature,
        "humidity": record.humidity,
        "timestamp": record.timestamp.isoformat()
    }
    # Store or send the event to clients (e.g., via a queue, a cache, etc.)
    send_event_to_clients(json.dumps(event_data))

# Function to send events to clients (this is a placeholder and needs real implementation)
def send_event_to_clients(event):
    # Implementation for sending the event to connected clients via SSE
    pass

# View to handle real-time data streaming via SSE
def realtime_stream(request):
    def event_stream():
        while True:
            # Fetch the latest event (you need to implement this)
            event = get_latest_event()
            if event:
                yield f"data: {event}\n\n"
            time.sleep(1)  # Adjust the delay as necessary
    
    return StreamingHttpResponse(event_stream(), content_type="text/event-stream")

# Function to get the latest event (needs actual implementation)
def get_latest_event():
    # This should be implemented to return the latest event from wherever you're storing it
    return None

# Django view to render the main page with the chart
def index(request):
    return render(request, 'index.html')


