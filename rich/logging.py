import logging


class RichHandler(logging.StreamHandler):
    def __init__(self, *args, **kwargs):
        super().__init__()
