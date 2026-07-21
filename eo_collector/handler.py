from config.settings import load_config
from services.collector_service import CollectorService


def lambda_handler(event, context):
    cfg = load_config()
    CollectorService(cfg).run()

    return {
        "statusCode": 200,
        "body": "Collection completed successfully."
    }