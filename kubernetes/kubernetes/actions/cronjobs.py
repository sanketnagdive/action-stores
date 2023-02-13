import logging

from pydantic import BaseModel

from . import actionstore as action_store
from .clients import get_batch_client

logging.basicConfig(level=logging.INFO)


class Namespace(BaseModel):
    name: str


@action_store.kubiya_action()
def list_suspended_cronjobs(args):
    api_client = get_batch_client()
    api_response = api_client.list_cron_job_for_all_namespaces()
    suspended_cronjobs = [cj for cj in api_response.items if cj.spec.suspend == True]
    return [item.metadata.name for item in suspended_cronjobs]


@action_store.kubiya_action()
def list_suspended_cronjobs_for_namespace(args: Namespace):
    api_client = get_batch_client()
    api_response = api_client.list_namespaced_cron_job(args.name)
    suspended_cronjobs = [cj for cj in api_response.items if cj.spec.suspend == True]
    return [item.metadata.name for item in suspended_cronjobs]


@action_store.kubiya_action()
def list_disabled_cronjobs_for_all_namespaces(args):
    api_client = get_batch_client()
    api_response = api_client.list_cron_job_for_all_namespaces()
    return [
        item.metadata.name for item in api_response.items if item.spec.schedule == ""
    ]


@action_store.kubiya_action()
def list_disabled_cronjobs_for_namespace(args):
    api_client = get_batch_client()
    api_response = api_client.list_cron_job_for_all_namespaces()
    return [
        item.metadata.name for item in api_response.items if item.spec.schedule == ""
    ]


@action_store.kubiya_action()
def list_disabled_cronjobs(args):
    api_client = get_batch_client()
    api_response = api_client.list_cron_job_for_all_namespaces()
    return [
        item.metadata.name for item in api_response.items if item.spec.schedule == ""
    ]


@action_store.kubiya_action()
def delete_stuck_cronjob(args):
    api_client = get_batch_client()
    api_response = api_client.list_cron_job_for_all_namespaces()
    stuck_cronjobs = [cj for cj in api_response.items if cj.spec.suspend == True]
    for cronjob in stuck_cronjobs:
        api_client.delete_namespaced_cron_job(
            cronjob.metadata.name, cronjob.metadata.namespace
        )

    return [item.metadata.name for item in stuck_cronjobs]
