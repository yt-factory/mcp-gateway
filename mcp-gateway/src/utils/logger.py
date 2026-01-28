import os

import structlog


def setup_logger():
    log_level = os.getenv("LOG_LEVEL", "INFO")

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(getattr(structlog, log_level, structlog.INFO)),
    )
    return structlog.get_logger()


logger = setup_logger()
