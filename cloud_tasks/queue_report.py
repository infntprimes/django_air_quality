from google.cloud import tasks_v2
from django_air_quality.privatesettings import GOOGLE_LOCATION_ID, GOOGLE_PROJECT_ID, GOOGLE_QUEUE_NAME, TASKS_KEY
import json


def queue_report(form_instance):
    """
    Calls google's tasks api for report generation, with user data passed through as a payload
    Once this function completes, google's task queue will call generate_report_handler() in views.py
    """
    client = tasks_v2.CloudTasksClient()
    parent = client.queue_path(GOOGLE_PROJECT_ID, GOOGLE_LOCATION_ID, GOOGLE_QUEUE_NAME)

    task = {
        'app_engine_http_request': {  # Specify the type of request.
            'http_method': 'POST',
            'relative_uri': '/tasks/generate_report/'
        }
    }

    payload = json.dumps({
            'zipcode': str(form_instance.zipcode),
            'start_date': str(form_instance.start_date),
            'end_date': str(form_instance.end_date),
            'key': str(TASKS_KEY) #used to prevent a user from manually POSTing
        })

    converted_payload = payload.encode()

    task['app_engine_http_request']['body'] = converted_payload

    response = client.create_task(parent, task)
    print('Created task {}'.format(response.name))
    return response
