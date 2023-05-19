import json
from datetime import datetime

from django.http import HttpResponse
import logging
from django.views.decorators.csrf import csrf_exempt

from .models import PullRequest

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO

from django.conf import settings


def check_pull_request_exists(pk):
    return PullRequest.objects.filter(pk=pk).exists()


def capture_screenshot(url):
    # Configure Selenium
    options = Options()
    options.add_argument('--headless')  # Run the browser in headless mode (without GUI)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    # try:
    if True:
        # Load the web page
        driver.get(url)

        # Wait for the page to load (you can adjust the sleep duration as needed)
        time.sleep(2)

        # Capture screenshot
        screenshot = driver.get_screenshot_as_png()

        # Convert the screenshot to a PIL Image object
        image = Image.open(BytesIO(screenshot))

        # Save the image to a file or database
        # Example: Save the image to a file
        image_path = settings.MEDIA_ROOT
        image.save(image_path)

        # Return the image path or image object, depending on your use case
        return image_path
        print('-' * 100)
        print('done')
        print('-' * 100)
    # finally:
    else:
        print('-' * 100)
        print('fail')
        print('-' * 100)
        # Quit the browser
        driver.quit()


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
            if pull_request['updated_at']:
                updated_at = datetime.strptime(pull_request['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
            else:
                updated_at = None
            if not check_pull_request_exists(id):
                url = pull_request['html_url']
                PullRequest.objects.create(
                    action=action,
                    id=id,
                    url=url,
                    state=state,
                    title=pull_request['title'],
                    body=pull_request['body'],
                    created_at=datetime.strptime(pull_request['created_at'], "%Y-%m-%dT%H:%M:%SZ"),
                    updated_at=updated_at,
                    merge_commit_sha=pull_request['merge_commit_sha'],
                    user=pull_request['user']['login'],
                    screenshot=capture_screenshot(url)
                )
            else:
                PullRequest.objects.filter(id=id).update(action=action, state=state,
                                                         updated_at=updated_at)
        # Return a response
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)
