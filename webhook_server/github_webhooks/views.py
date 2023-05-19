from datetime import datetime

from django.http import HttpResponse, JsonResponse
import json

from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

from .models import PullRequest


def check_pull_request_exists(pk):
    return PullRequest.objects.filter(number=pk).exists()


@csrf_exempt
def webhook_handler(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        # Handle the webhook payload here
        # Example: process the payload and perform necessary actions
        event_type = request.headers.get('X-GitHub-Event')
        if event_type == 'pull_request':
            pull_request = payload['pull_request']
            id = pull_request['id']
            number = payload['number']
            action = payload['action']
            state = pull_request['state']
            if pull_request['updated_at']:
                updated_at = datetime.strptime(pull_request['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
            else:
                updated_at = None
            if not check_pull_request_exists(id):
                PullRequest.objects.create(
                    action=action,
                    id=id,
                    number=number,
                    url=pull_request['html_url'],
                    state=state,
                    title=pull_request['title'],
                    body=pull_request['body'],
                    created_at=datetime.strptime(pull_request['created_at'], "%Y-%m-%dT%H:%M:%SZ"),
                    updated_at=updated_at,
                    merge_commit_sha=pull_request['merge_commit_sha'],
                    user=pull_request['user']['login'],
                )
            else:
                PullRequest.objects.filter(id=id).update(action=action, state=state,
                                                         updated_at=updated_at)
        # Return a response
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)
