# coding=utf-8
__version__ = '4.0.2'

import logging

logging.basicConfig()
dclogger = logging.getLogger('dt-challenges-runner')
dclogger.setLevel(logging.DEBUG)
dclogger.info('dt-challenges-runner %s' % __version__)

from .exceptions import *


from .runner import dt_challenges_evaluator

from .runner_local import runner_local_main
