import json
from datetime import datetime

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import PullRequest


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
            action = payload['action']
            state = pull_request['state']
            url = pull_request['html_url']
            updated_at = None
            if pull_request['updated_at']:
                updated_at = datetime.strptime(pull_request['updated_at'], "%Y-%m-%dT%H:%M:%SZ")

            try:
                existing_pull_request = PullRequest.objects.get(id=id)
                # Update the existing pull request attributes
                existing_pull_request.action = action
                existing_pull_request.state = state
                existing_pull_request.updated_at = updated_at
                existing_pull_request.save()
            except PullRequest.DoesNotExist:
                new_pull_request = PullRequest.objects.create(
                    action=action,
                    number=id,
                    url=url,
                    html_url=pull_request['html_url'],
                    state=state,
                    title=pull_request['title'],
                    body=pull_request['body'],
                    created_at=datetime.strptime(pull_request['created_at'], "%Y-%m-%dT%H:%M:%SZ"),
                    updated_at=updated_at,
                    merge_commit_sha=pull_request['merge_commit_sha'],
                    user=pull_request['user']['login']
                )

                # Save the screenshot
                new_pull_request.save_screenshot()
        # Return a response
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)


def index(request):
    url = 'https://github.com/hens2013/demo-repository/pull/13'

