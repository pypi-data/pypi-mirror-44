import logging


logger = logging.getLogger(__name__)


def handle_raise_exception(payload):
    raise Exception()


def handle_raise_proto_exception(payload):
    raise Exception()


def handle_json(payload):
    logger.info(f"JSON received:\n{payload}")
    logger.info(type(payload))
    logger.info(payload["foo"])


def handle_proto(payload):
    logger.info(f"Proto received:\n{str(payload)}")
    logger.info(type(payload))
    logger.info(payload.id)
