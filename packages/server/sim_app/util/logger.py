# log_helper.py
import inspect
import json
import os
import logging
import sys
import dotenv


# def setup_gcloud_logging():
#     dotenv.load_dotenv()
#     GCLOUD_KEY_JSON = os.getenv("GCLOUD_KEY_JSON")
#     if not GCLOUD_KEY_JSON:
#         raise ValueError("GCLOUD_KEY_JSON is not set")
#     GCLOUD_KEY_JSON = GCLOUD_KEY_JSON.replace("\n", "\\n")
#     credentials_dict = json.loads(GCLOUD_KEY_JSON)

#     import google.cloud.logging
#     client = google.cloud.logging.Client.from_service_account_info(credentials_dict)
#     # client.setup_logging()

#     from google.cloud.logging.handlers import CloudLoggingHandler
#     # Create a CloudLoggingHandler instance
#     handler = CloudLoggingHandler(client)
#     google.cloud.logging.handlers.setup_logging(handler, log_level=logging.DEBUG) # Set your desired log level

#     # Create a standard library logging handler that streams to stdout
#     stdout_handler = logging.StreamHandler()
#     stdout_handler.setLevel(logging.DEBUG)

#     # Get the root logger
#     root_logger = logging.getLogger()
#     root_logger.setLevel(logging.DEBUG)

#     # Add both handlers to the root logger
#     root_logger.addHandler(handler)
#     root_logger.addHandler(stdout_handler)


def get_logger(name=None, level=logging.WARNING) -> logging.Logger:
    if name is None:
        # Get the caller's frame and its filename
        caller_frame = inspect.currentframe().f_back    # type: ignore
        caller_filename = caller_frame.f_globals['__file__']    # type: ignore
        name = os.path.splitext(os.path.basename(caller_filename))[0]
        
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    handler = logging.StreamHandler() #sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


if __name__ == "__main__":
    import asyncio
    import time
    logger = get_logger(level=logging.INFO)

    async def main():
        while True:
            logger.info(f"Hello, world! {time.time()}")
            await asyncio.sleep(1)

    asyncio.run(main())