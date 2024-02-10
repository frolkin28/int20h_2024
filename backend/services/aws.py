import boto3

from backend.config import Config


s3_client = boto3.client("s3")


def configure_aws(config: Config):
    boto3.setup_default_session(
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    )


__all__ = ("s3_client", "configure_aws")
