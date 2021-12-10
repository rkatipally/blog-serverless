import json

import reader_service as reader
import logging

log = logging.getLogger()
if log.handlers:
    for handler in log.handlers:
        log.removeHandler(handler)
logging.basicConfig(level=logging.DEBUG)


def lambda_handler(event, context):
    log.info("========== Reader Event===========")
    log.info(event)
    log.info("========== Reader Context===========")
    log.info(context)
    response = reader.handle_reader_request(event)
    log.info("Response for reader is {}".format(response))
    return response
    # return handle_reader_api(event, context)


def handle_reader_api(event, context):
    log.info("Calling handle_api() for reader!")
    return reader.handle_reader_request(event)
