from src.app import server
from src.common import Logger
from src.model.job_model import BatchJob
from src.util import (
    get_initial_create_time_dict,
    get_update_time_dict,
    validate_and_dump_in_schema,
)

log = Logger()


def create_one(insert_args):
    insert_data = {**insert_args, **get_initial_create_time_dict()}
    log.info(f"job_repository : create_one : batch_job_id = {insert_data['_id']}")
    batch_job_schema = BatchJob()
    obj = validate_and_dump_in_schema(insert_data, batch_job_schema)
    return server.get_mongo_db().AtxDataBatchJobs.insert_one(obj)


def find_one(batch_job_id):
    return server.get_mongo_db().AtxDataBatchJobs.find_one({"_id": batch_job_id})


def update_one(batch_job_id, update_args):
    update_data = {**update_args, **get_update_time_dict()}
    log.info(f"job_repository : update_one : batch_job_id = {batch_job_id}")
    return server.get_mongo_db().AtxDataBatchJobs.update_one(
        {"_id": batch_job_id}, {"$set": update_data}
    )
