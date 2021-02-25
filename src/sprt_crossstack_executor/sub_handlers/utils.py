import boto3
from ..models import ResourceModel
from cloudformation_cli_python_lib import (
    SessionProxy
)
import logging

LOG = logging.getLogger(__name__)


def get_cross_cfn_client(session: SessionProxy, model: ResourceModel, session_name):
    session = _get_cross_session(session, model, session_name)
    return session.client("cloudformation", region_name=model.Region)


def get_cross_cfn_resource(session: SessionProxy, model: ResourceModel, session_name):
    session = _get_cross_session(session, model, session_name)
    return session.resource("cloudformation", region_name=model.Region)


def _get_cross_session(session: SessionProxy, model: ResourceModel, session_name):
    """Returns session object for cross-account access.

    :return: Can be used to obtain session.client() or session.resource()
    """
    LOG.setLevel(model.LogLevel)

    role_arn = "arn:aws:iam::{}:role{}{}".format(model.AccountId, model.AssumeRolePath, model.AssumeRoleName)

    LOG.debug("Assuming Cross session role: %s", role_arn)
    assumed_role = session.client("sts").assume_role(
        RoleArn=role_arn,
        RoleSessionName=session_name
      )

    session = boto3.Session(
        aws_access_key_id=assumed_role["Credentials"]["AccessKeyId"],
        aws_secret_access_key=assumed_role["Credentials"]["SecretAccessKey"],
        aws_session_token=assumed_role["Credentials"]["SessionToken"]
    )

    return session
