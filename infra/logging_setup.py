import logging


class LoggingSetup:
    """
    A class to manage logging configuration for the project.
    """
    logging.basicConfig(
        filename="../../log_file.log",
        level=logging.INFO,
        format='%(asctime)s: %(levelname)s: %(message)s',
        datefmt='%d-%m-%Y - %H:%M:%S',  # Exclude milliseconds
        force=True  # The configuration will override any existing logging setup,
        # ensuring that these settings are applied regardless of previous configurations.
    )
    # Suppress logging from 'undetected_chromedriver' to avoid clutter
    logging.getLogger('undetected_chromedriver').setLevel(logging.WARNING)


# Create an instance of LoggingSetup to configure logging when this module is imported
