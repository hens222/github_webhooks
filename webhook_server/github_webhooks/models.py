
from django.db import models


class PullRequest(models.Model):
    action = models.CharField(max_length=50)
    number = models.PositiveIntegerField()
    url = models.URLField()
    html_url = models.URLField()
    state = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    merge_commit_sha = models.CharField(max_length=40)
    user_login = models.CharField(max_length=100)
    user_avatar_url = models.URLField()

    class Meta:
        db_table = 'pull_requests'
