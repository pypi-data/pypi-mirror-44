import os

import yaml
from cerberus import Validator

from .helpers import fail, success, configure_logger, enable_debug, get_logger


logger = configure_logger()


class Pipe:

    def fail(self, message):
        fail(message=message)

    def success(self, message, do_exit=False):
        success(message, do_exit=do_exit)

    def __init__(self, pipe_metadata=None):
        if pipe_metadata is None:
            pipe_metadata = os.path.join(os.path.dirname(__file__), 'pipe.yml')
        with open(pipe_metadata, 'r') as f:
            self.metadata = yaml.safe_load(f.read())

    
    @classmethod
    def from_pipe_yml(cls, ):
        pass

    def validate(self):
        validator = Validator(schema=self.metadata['variables'], purge_unknown=True)
        env = dict(os.environ)

        if not validator.validate(env):
            self.fail(message=f'Parameters validation errors: \n{yaml.dump(validator.errors, default_flow_style = False)}')
        validated = validator.validated(env)
        return validated

    def run(self):
        pass