# rg-trd077-pro-cr-daily-analysis
Function that trigger daily the analisis of the Sharepoint site

## TODO:
- Cambiar el parametro process-queue para que sea con barra baja

## Deploy to Cloud Run:
```

gcloud run deploy rg-trd077-pro-cr-daily-analysis \
--source . \
--project=rg-trd077-pro \
--region=europe-west1 \
--platform managed \
--no-allow-unauthenticated \
--max-instances=1 \
--min-instances=0 \
--cpu=0.5 \
--memory=512Mi \
--timeout=1800 \
--concurrency=1 \
--service-account=id-rg-trd077-pro-cloud-functio@rg-trd077-pro.iam.gserviceaccount.com \
--set-env-vars "project_id=rg-trd077-pro, analyze_url=https://rg-trd077-pro-cr-analyze-sharepoint-306697089404.europe-west1.run.app, queue_name_analyze=analyze-sharepoint, queue_region=europe-west1, service_account=id-rg-trd077-pro-cloud-functio@rg-trd077-pro.iam.gserviceaccount.com"

```