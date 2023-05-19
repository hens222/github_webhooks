from django.db import models


class PullRequest(models.Model):
    ACTION_CHOICES = [
        ('opened', 'Open'),
        ('closed', 'Closed'),
        ('reopened', 'Reopened'),
    ]

    STATE_CHOICES = [
        ('open', 'Open'),
        ('close', 'Close'),
    ]
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    number = models.PositiveIntegerField(primary_key=True)
    url = models.URLField()
    state = models.CharField(max_length=10, choices=STATE_CHOICES)
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(default=None, null=True)
    merge_commit_sha = models.CharField(max_length=40)
    user = models.CharField(max_length=100)

    class Meta:
        db_table = 'pull_requests'
