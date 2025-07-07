from cloud_tasks import launch_task
from google.cloud import bigquery

import os
from flask import Flask

app = Flask(__name__)

project_id = os.environ.get('project_id')
analyze_url = os.environ.get('analyze_url')
queue_name_analyze = os.environ.get('queue_name_analyze')
queue_region = os.environ.get('queue_region')
service_account = os.environ.get('service_account')

# bigquery client
client_bigquery = bigquery.Client()


@app.post("/")
def analyze_sharepoint():
  
  sharepoint_application_name = 'TRD077-BuscadorCognitivo-GCP-spo-api4'
  process_queue = 'process-sharepoint-4'

  # check sites/drives marked to be processed daily if their data ingest is finalized
  query="""
        SELECT DISTINCT t1.*
        FROM `rg-trd077-pro.configuration_details.daily_update` AS t1
              JOIN `rg-trd077-pro.configuration_details.stats_all_detail_summary` AS t2 
              ON t1.site_name = t2.site_name
        WHERE
          t2.ejecucion_finalizada = 'Si'
            AND NOT EXISTS (
              -- Check that no record exists for the same name with 'No'
              SELECT 1
              FROM `rg-trd077-pro.configuration_details.stats_all_detail_summary` AS t2_check
              WHERE t2_check.site_name = t1.site_name
              AND t2_check.ejecucion_finalizada = 'No'
            );
    """

  try:
    query_job = client_bigquery.query(query)
    query_result = query_job.result()
  except:
    print("ERROR IN SQL QUERY")
    return "ERROR IN SQL QUERY", 200
  
  # get query results in the correct format
  sites_list = [dict(row) for row in query_result]



  for site in sites_list:
    #Build task object
    task_object={}
    if site['drive_name']:
      task_object['site_name'] = site['site_name']
      task_object['site_id_short'] = site['site_id_short']
      task_object['drive_name'] = site['drive_name']
      print('Launched site with site_id_short: '  + site['site_id_short'] + ' and drive_name: ' + site['drive_name'])
    else:
      task_object['site_name'] = site['site_name']
      task_object['site_id_short'] = site['site_id_short']
      print('Launched site with site_id_short: '  + site['site_id_short'])

    # add quee details to task object
    task_object['sharepoint_application_name'] = sharepoint_application_name
    task_object['process-queue'] = process_queue

    launch_task(project_id, analyze_url, queue_name_analyze, queue_region, task_object, service_account)
    
  print('End of process')


  return 'OK', 200

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=False)