from eo_runner.config import load_config
from eo_runner.services import RunnerService


def lambda_handler(event, context):

    cfg = load_config()

    RunnerService(cfg).run()

    return {
        "statusCode": 200,
        "body": "EO Runner completed successfully."
    }