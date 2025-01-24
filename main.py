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

  # check sites already proccessed for new files
  query = """
          SELECT DISTINCT SD.site_name, SD.site_web_url 
          FROM `rg-trd077-pro.configuration_details.stats_all_detail_summary` AS S JOIN `rg-trd077-pro.configuration_details.sites_and_drives` AS SD ON S.site_name=SD.site_name 
        """

  try:
    query_job = client_bigquery.query(query)
    query_result = query_job.result()
  except:
    print("ERROR IN SQL QUERY")
    return "ERROR IN SQL QUERY", 200
  
  # get query results in the correct format
  rows = [dict(row) for row in query_result]
  sites_list=[]
  for i in rows:
    sites_list.append({'site_name':i['site_name'], 'site_id_short': i['site_web_url'].split("/")[-1]})



  for site in sites_list:
    site['sharepoint_application_name'] = sharepoint_application_name
    site['process-queue'] = process_queue

    launch_task(project_id, analyze_url, queue_name_analyze, queue_region, site, service_account)
    print('Launched site with site_id_short: '  + site['site_id_short'])

  print('End of process')


  return 'OK', 200

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=False)