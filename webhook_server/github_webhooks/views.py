from django.http import HttpResponse
import json


def webhook_handler(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        # Handle the webhook payload here
        # Example: process the payload and perform necessary actions
        event_type = request.headers.get('X-GitHub-Event')
        print(f'Received {event_type} event: {payload}')
        # Return a response
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)
