import logging

# configure logging
logging.basicConfig(
    filename="../../log_file.log",
    level=logging.INFO,
    format='%(asctime)s: %(levelname)s: %(message)s',
    datefmt='%d-%m-%Y - %H:%M:%S',
    force=True
)

# suppress logging from 'undetected_chromedriver' to avoid clutter
logging.getLogger('undetected_chromedriver').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
