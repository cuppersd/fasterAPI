import os
import socket
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# logs
log_save_path = os.path.join(os.path.dirname(BASE_DIR), 'logs')
if not os.path.exists(log_save_path):
    os.makedirs(log_save_path)

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def get_date_str():
    now = datetime.datetime.now()
    return now.strftime('%Y_%m_%d_%H_%M_%S')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'sys_log_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_save_path, '{}_sys_{}.log'.format(get_host_ip(), get_date_str())),
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },

        'agent_log_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_save_path, '{}_agent_{}.log'.format(get_host_ip(), get_date_str())),
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },

        'root_log_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_save_path, '{}_root_{}.log'.format(get_host_ip(), get_date_str())),
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'sys_log': {
            'handlers': ['console', 'sys_log_file'],
            'propagate': True,
            'level': 'INFO',
        },
        'agent_log': {
            'handlers': ['console', 'agent_log_file'],
            'propagate': True,
            'level': 'INFO',
        },
        'root_log': {
            'handlers': ['console', 'root_log_file'],
            'propagate': True,
            'level': 'INFO',
        },
    }
}
