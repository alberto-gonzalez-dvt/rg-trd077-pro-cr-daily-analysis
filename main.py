from cloud_tasks import launch_task

import os
from flask import Flask

app = Flask(__name__)

project_id = os.environ.get('project_id')
analyze_url = os.environ.get('analyze_url')
queue_name_analyze = os.environ.get('queue_name_analyze')
queue_region = os.environ.get('queue_region')
service_account = os.environ.get('service_account')

@app.post("/")
def analyze_sharepoint():
  
  sharepoint_application_name = 'TRD077-BuscadorCognitivo-GCP-spo-api4'
  process_queue = 'process-sharepoint-4'

  sites_list =[
    {
      "site_name": "IstanbulOffice",
      "site_id_short": "IstanbulOffice"
    },
    {
      "site_name": "",
      "site_id_short": "TR-SIM"
    },
    {
      "site_name": "Buscador Cognitivo",
      "site_id_short": "BuscadorCognitivo"
    },
    {
      "site_name": "setupCognitiveSearch",
      "site_id_short": "setupCognitiveSearch"
    },
    {
      "site_name": "Biblioteca",
      "site_id_short": "Biblioteca"
    },
    {
      "site_name": "FTP_8595ASEVASA",
      "site_id_short": "FTP_8595ASEVASA"
    }
  ]

  for site in sites_list:
    site['sharepoint_application_name'] = sharepoint_application_name
    site['process-queue'] = process_queue

    launch_task(project_id, analyze_url, queue_name_analyze, queue_region, site, service_account)
    print('Launched site with site_id_short: '  + site['site_id_short'])

  print('End of process')


  return 'OK', 200

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=False)