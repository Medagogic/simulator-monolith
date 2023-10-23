# log_helper.py
import inspect
import json
import os
import logging
import dotenv


# dotenv.load_dotenv()
# GCLOUD_KEY_JSON = os.getenv("GCLOUD_KEY_JSON")
# if not GCLOUD_KEY_JSON:
#     raise ValueError("GCLOUD_KEY_JSON is not set")
# GCLOUD_KEY_JSON = GCLOUD_KEY_JSON.replace("\n", "\\n")
# credentials_dict = json.loads(GCLOUD_KEY_JSON)

# import google.cloud.logging
# client = google.cloud.logging.Client.from_service_account_info(credentials_dict)
# client.setup_logging()

from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.formatted_text import FormattedText

def prompt_toolkit_logging_handler(record):
    level = record.levelname
    timestamp = record.asctime
    logger_name = record.name
    message = record.message
    
    if level == 'DEBUG':
        level_color, message_color = 'ansigreen', '#222222'
    elif level == 'INFO':
        level_color, message_color = 'ansiblue', 'ansiwhite'
    elif level == 'WARNING':
        level_color, message_color = 'ansiyellow', 'ansiyellow'
    elif level == 'ERROR':
        level_color, message_color = 'ansired', 'ansired'
    else:
        level_color, message_color = 'ansiwhite', 'ansiwhite'
    
    formatted_record = [
        ('ansiwhite', f"{timestamp} {logger_name} "),
        (level_color, f"{level} "),
        (message_color, f"{message}")
    ]
        
    print(FormattedText(formatted_record))

class CustomHandler(logging.Handler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.setFormatter(formatter)
    
    def emit(self, record):
        self.format(record)
        prompt_toolkit_logging_handler(record)


logging.basicConfig(
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[CustomHandler()])

def get_logger(name=None, level=logging.WARNING) -> logging.Logger:
    if name is None:
        # Get the caller's frame and its filename
        caller_frame = inspect.currentframe().f_back    # type: ignore
        caller_filename = caller_frame.f_globals['__file__']    # type: ignore
        name = os.path.splitext(os.path.basename(caller_filename))[0]
        
    logger = logging.getLogger(name)
    logger.setLevel(level)

    return logger



if __name__ == "__main__":
    import asyncio
    import time
    from packages.medagogic_sim.gpt import MODEL_GPT4, gpt, UserMessage, SystemMessage
    logger = get_logger(level=logging.DEBUG)

    async def main():
        while True:
            logger.debug(f"Debug message")
            logger.info(f"Hello, world! {time.time()}")
            logger.warning(f"Warning! Warning!")
            logger.error("This is an error")
            await asyncio.sleep(1)

    asyncio.run(main())