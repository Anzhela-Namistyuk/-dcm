import argparse
import logging
import os
from logging.handlers import RotatingFileHandler

BASE_DIR = os.getcwd()


LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'

parser = argparse.ArgumentParser(
    description='Парсит имя или путь к директориям. '
                'Первый аргумент содержит имя/путь '
                'из какой директории считывать. '
                'Второй аргумент содержит имя'
                'директории в которую будут записаны данные, '
                'директория будет создана в корне проекта.'
)
parser.add_argument('name_dir_from',
                    help='Имя директории или полный путь откуда брать данные '
                         'Пример: src.'
                         'Пример: /Users/username/recruit/src'
                    )
parser.add_argument('name_dir_to', help='Имя директории куда будут '
                                        'записываться данные. '
                                        '(директория в корне проекта). '
                                        'Пример: output.'
                    )


def configure_logging():
    """Создает директорию и файл для логирования. """
    log_dir = os.path.join(BASE_DIR, 'logs')
    try:
        os.mkdir(log_dir)
    except FileExistsError:
        logging.info(f'Директория уже существует {log_dir}')
    log_file = os.path.join(log_dir, 'write_file.log')
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6, backupCount=1
    )

    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler,)
    )
