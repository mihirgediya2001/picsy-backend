import os
import time
import json

import boto3
from opensearchpy import AWSV4SignerAuth, OpenSearch, RequestsHttpConnection

host = "search-picsy-search-prod-qtfn5s5r2y5oimpqxli7bowppi.us-east-1.es.amazonaws.com"
region = "us-east-1"

service = "es"
credentials = boto3.Session().get_credentials()
auth = AWSV4SignerAuth(credentials, region)

opensearch_client = OpenSearch(
    hosts=[{"host": host, "port": 443}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    timeout=30,
    max_retries=5,
    retry_on_timeout=True,
)

# print(json.dumps(os.info(), indent=4, sort_keys=True))


def crete_txt_file(filename, data, index_name):
    # read _dataset_iteration_41817 json file and create txt file
    # f = open("_dataset_iteration_41817.json", "r", encoding="utf-8")
    # data = json.load(f)
    datalist = []
    for i in data:
        datalist.append({"index": {"_index": f"{index_name}", "_id": i["id"]}})
        # Replace "upscaled": False with "upscaled": "false" and "upscaled": True with "upscaled": "true"
        updated_data = []
        for scl in i["images"]:
            scl["upscaled"] = str(scl["upscaled"]).lower()
            updated_data.append(scl)
