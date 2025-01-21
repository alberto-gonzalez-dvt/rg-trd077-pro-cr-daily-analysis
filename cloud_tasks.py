from google.cloud import tasks_v2
from google.protobuf.duration_pb2 import Duration
from google.api_core.retry import Retry

import json

tasks_client = tasks_v2.CloudTasksClient()

#Added retry_policy to avoid error google.api_core.exceptions.ServiceUnavailable: 503 GOAWAY received; Error code: 0; Debug Text: session_timed_out
retry_policy = Retry(initial=1.0, maximum=60.0, multiplier=2.0, deadline=300.0)

def launch_task(project_id, cf_tasks_url,queue_sh_to_cs_name, queue_sh_to_cs_region, task_object, service_account):


    parent = tasks_client.queue_path(project_id, queue_sh_to_cs_region, queue_sh_to_cs_name)
    task = {
      "http_request": { 
          "http_method": tasks_v2.HttpMethod.POST,
          "url": cf_tasks_url, 
          "body": json.dumps(task_object, default=str).encode(), 
          "headers" : {"Content-type": "application/json"},
          "oidc_token": tasks_v2.OidcToken(
                service_account_email=service_account,
                audience=None,
            ),
      },
      "dispatch_deadline" : Duration(seconds=1800)  #In seconds, max 30 min
    }
    response = tasks_client.create_task(request={"parent": parent, "task": task}, retry=retry_policy)
    #response = tasks_client.create_task(request={"parent": parent, "task": task})