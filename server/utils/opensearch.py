import os

import boto3
from dotenv import load_dotenv
from opensearchpy import AWSV4SignerAuth, OpenSearch, RequestsHttpConnection
from server.utils.config import settings

load_dotenv()

host = os.getenv("OPENSEARCH_HOST")
region = os.getenv("AWS_REGION")

service = "es"
credentials = boto3.Session(
    aws_access_key_id=settings.ACCESS_KEY,
    aws_secret_access_key=settings.SECRET_KEY,
).get_credentials()
auth = AWSV4SignerAuth(credentials, region)

index_name = os.getenv("OPENSEARCH_INDEX_NAME")
suggestion_index_name = os.getenv("OPENSEARCH_SUGGESTION_INDEX_NAME")

client = OpenSearch(
    hosts=[{"host": host, "port": 443}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    timeout=30,
    max_retries=5,
    retry_on_timeout=True,
)
