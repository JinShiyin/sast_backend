import os
import yaml
import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler
from easydict import EasyDict
import shutil

from utils.misc import create_dirs

DEBUG = True


def setup_logging(log_dir, logger_name='main', level=logging.INFO):
    log_file_format = '[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s in %(pathname)s:%(lineno)d'
    log_console_format = '[%(levelname)s]: %(message)s'

    # Main logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(Formatter(log_console_format))

    exp_file_handler = RotatingFileHandler('{}exp_debug.log'.format(log_dir), maxBytes=10 ** 6, backupCount=5)
    exp_file_handler.setLevel(logging.DEBUG)
    exp_file_handler.setFormatter(Formatter(log_file_format))

    exp_errors_file_handler = RotatingFileHandler('{}exp_error.log'.format(log_dir), maxBytes=10 ** 6, backupCount=5)
    exp_errors_file_handler.setLevel(logging.WARNING)
    exp_errors_file_handler.setFormatter(Formatter(log_file_format))

    logger.addHandler(console_handler)
    logger.addHandler(exp_file_handler)
    logger.addHandler(exp_errors_file_handler)
    return logger


def get_config_from_yaml(yaml_file):
    with open(yaml_file, 'r') as config_file:
        try:
            # config_dict = yaml.load(config_file)
            config_dict = yaml.load(config_file, Loader=yaml.FullLoader)
            config = EasyDict(config_dict)
            return config
        except ValueError:
            print('INVALID YAML file format.. Please provide a good yaml file')
            exit(-1)


def process_config(yaml_file):
    config = get_config_from_yaml(yaml_file)

    print(' *************************************** ')
    print(' The experiment name is {} '.format(config.exp_name))
    print(' The experiment model is {} '.format(config.model_name))
    print(' The experiment mode is {} '.format(config.mode))
    print(' The experiment common is: [{}] '.format(config.common))
    print(' *************************************** ')

    # create some important directories to be used for that experiments
    base_dir = 'experiments'
    config.log_dir = os.path.join('experiments', config.exp_name, 'log/')
    config.val_sample_dir = os.path.join('experiments', config.exp_name, 'val/')
    config.test_sample_dir = os.path.join('experiments', config.exp_name, 'test/')
    config.model_save_dir = os.path.join('experiments', config.exp_name, 'model/')
    create_dirs(
        [base_dir, config.log_dir, config.val_sample_dir, config.test_sample_dir, config.model_save_dir])
    shutil.copyfile(yaml_file, os.path.join('experiments', config.exp_name, os.path.basename(yaml_file)))

    # setup logging in the project
    setup_logging(config.log_dir)

    # logging.getLogger().info('Hi, This is root.')
    # logging.getLogger().info('After the configurations are successfully processed and dirs are created.')
    # logging.getLogger().info('The pipeline of the project will begin now.')

    return config
