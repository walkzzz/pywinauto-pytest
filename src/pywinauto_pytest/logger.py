import logging
import logging.config
import os
from pathlib import Path

# 默认日志配置
DEFAULT_LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': 'pywinauto-pytest.log',
            'mode': 'a',
            'encoding': 'utf-8'
        }
    },
    'loggers': {
        'pywinauto_pytest': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False
        }
    },
    'root': {
        'level': 'WARNING',
        'handlers': ['console']
    }
}

def setup_logging(config_path=None, log_level=None):
    """配置日志系统"""
    # 如果提供了配置文件路径，则使用该配置文件
    if config_path and os.path.exists(config_path):
        try:
            logging.config.fileConfig(config_path, disable_existing_loggers=False)
            return
        except Exception as e:
            print(f"Failed to load logging configuration from {config_path}: {e}")
            print("Using default logging configuration instead.")
    
    # 否则使用默认配置
    config = DEFAULT_LOG_CONFIG.copy()
    
    # 如果指定了日志级别，则覆盖默认级别
    if log_level:
        config['handlers']['console']['level'] = log_level
        config['loggers']['pywinauto_pytest']['level'] = log_level
    
    # 配置日志系统
    logging.config.dictConfig(config)

# 初始化日志系统
setup_logging()

# 创建并导出 logger 实例
logger = logging.getLogger('pywinauto_pytest')
