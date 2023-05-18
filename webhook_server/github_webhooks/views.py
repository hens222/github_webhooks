from django.http import HttpResponse, JsonResponse
import json

from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def webhook_handler(request):
    # if request.method == 'POST':
    #     print('-' * 100)
    #     print(request)
    #     print('-' * 100)
    #     payload = json.loads(request.body)
    #     # Handle the webhook payload here
    #     # Example: process the payload and perform necessary actions
    #     event_type = request.headers.get('X-GitHub-Event')
    #     print(f'Received {event_type} event: {payload}')
    #     # Return a response
    #     return HttpResponse(status=200)
    # else:
    #     return HttpResponse(status=405)
    print('-' * 100)
    print(json.loads(request.body))
    print('-' * 100)
    if request.method == 'POST':

        csrf_token = request.GET.get('csrfmiddlewaretoken', '')
        if csrf_token == get_token(request):
            payload = json.loads(request.body)
            # Handle the webhook payload here
            # Example: process the payload and perform necessary actions
            event_type = request.headers.get('X-GitHub-Event')
            print(f'Received {event_type} event: {payload}')
            # Return a response as JSON
            response_data = {
                'status': 'success',
                'message': 'Webhook received and processed successfully.'
            }
            return JsonResponse(response_data, status=200)
        else:
            response_data = {
                'status': 'error',
                'message': 'CSRF verification failed.'
            }
            return JsonResponse(response_data, status=403)
    else:
        response_data = {
            'status': 'error',
            'message': 'Invalid request method.'
        }
        return JsonResponse(response_data, status=405)


def index(request):
    print(request)
    return HttpResponse("tech with team")
