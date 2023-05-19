from datetime import datetime

from django.http import HttpResponse
import logging
from django.views.decorators.csrf import csrf_exempt

from .models import PullRequest


def check_pull_request_exists(pk):
    return PullRequest.objects.filter(id=pk).exists()


@csrf_exempt
def webhook_handler(request):
    if request.method == 'POST':
        payload = request.json()

        event_type = request.headers.get('X-GitHub-Event')
        if event_type == 'pull_request':
            pull_request = payload['pull_request']
            id = pull_request['id']
            action = payload['action']
            state = pull_request['state']
            updated_at = None

            if pull_request['updated_at']:
                updated_at = datetime.strptime(pull_request['updated_at'], "%Y-%m-%dT%H:%M:%SZ")

            try:
                obj, created = PullRequest.objects.get_or_create(
                    id=id,
                    defaults={
                        'action': action,
                        'url': pull_request['html_url'],
                        'state': state,
                        'title': pull_request['title'],
                        'body': pull_request['body'],
                        'created_at': datetime.strptime(pull_request['created_at'], "%Y-%m-%dT%H:%M:%SZ"),
                        'updated_at': updated_at,
                        'merge_commit_sha': pull_request['merge_commit_sha'],
                        'user': pull_request['user']['login'],
                    }
                )

                if not created:
                    obj.action = action
                    obj.state = state
                    obj.updated_at = updated_at
                    obj.save()

            except PullRequest.DoesNotExist:
                logging.error(f"PullRequest with id={id} does not exist: {str(e)}")

        return HttpResponse(status=200)
    return HttpResponse(status=405)
