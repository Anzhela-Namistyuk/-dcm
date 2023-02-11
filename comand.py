import logging
import os
import pydicom
from configs import configure_logging, parser, BASE_DIR


class DoPathAndWriteDS:
    """
    Класс принимает путь до директории в которой хранятся
    файлы с "dcm" расширением и имя директории в которую будут
    сохранены файлы после изменения.
    Считывает файл по заданному пути "path_from".
    Удаляет информацию, хранящуюся в ключе PatientName.
    Записывает файл в заданную директорию "name_dir_to",
    по новому пути "$StudyInstanceUID/$SeriesInstanceUID/$SOPInstanceUID.dcm".
    """

    def __init__(self, path_from, name_dir_to):
        self.path_from = path_from
        self.name_dir_to = name_dir_to
        self.ds = None
        self.path_to = None

    def get_ds(self):
        """
        Считывает файл по заданному пути "path_from".
        """
        try:
            self.ds = pydicom.dcmread(self.path_from)
        except FileNotFoundError:
            logging.exception(f'Нет такого пути {self.path_from}')

    @staticmethod
    def make_dirs(path_to):
        """
        Создает директории для сохранения измененного файла.
        """
        try:
            os.makedirs(path_to, exist_ok=True)
        except:
            logging.exception('Не получилось ')


    def get_path_for_file(self):
        """
        Получает из DS имена по ключу и по данным именам
        формирует директории. Записывает путь до конечного
        файла в "self.path_to" по примеру:
        "path_main_dir/$StudyInstanceUID/$SeriesInstanceUID/$SOPInstanceUID.dcm".
        """
        try:
            StudyInstanceUID = self.ds.StudyInstanceUID
            SeriesInstanceUID = self.ds.SeriesInstanceUID

            path_to_dir = os.path.join(
                BASE_DIR,
                f'{self.name_dir_to}/{StudyInstanceUID}/{SeriesInstanceUID}'
            )
            self.make_dirs(path_to_dir)

            SOPInstanceUID = f'{self.ds.SOPInstanceUID}.dcm'
            self.path_to = os.path.join(path_to_dir, SOPInstanceUID)

        except AttributeError:
            logging.exception('Нет такой записи')

    def do_anonymous_name(self):
        """
        Удаляет информацию, хранящуюся в ключе PatientName.
        """
        try:
            self.ds.PatientName = None
        except AttributeError:
            logging.exception(f'Нет такой записи "PatientName"')

    def save_file(self):
        """
        Записывает файл в заданную директорию
        по новому пути "path_to".
        """
        try:
            self.ds.save_as(self.path_to)
        except:
            logging.exception('Не удалось записать файл')

    def make_file_with_list(self):
        """Создает файл и записывает старый
        и новый пути к файлу."""
        with open('file_with_diff_path.txt', 'a') as f:
            f.write(f'Первоначальный путь: {self.path_from} \n'
                    f'Новый путь: {self.path_to} \n \n')


def is_path_or_name_dir(name_from):
    """Проверяет аргумент из команды,
    является ли он путем до директории или
    именем директории. Возвращает абсолютный
    путь.
    """
    if '/' in name_from:
        return name_from
    else:
        return os.path.join(BASE_DIR, name_from)


def is_dir_exist(path):
    """Функция проверяет существование директории по пути path."""
    return os.path.isdir(path)


def is_dcm_file(filename):
    """Функция проверяет, является ли файл с расширением 'dcm'."""
    try:
        format_file = filename.split('.', 1)[1]
        if format_file == 'dcm':
            return True
    except IndexError:
        logging.info(f'Файл без расширения {filename}')


def main(path_dir_from, name_dir_to):
    """Перебирает все файлы в директории и для каждого
    файла вызывает методы: для получения DS, удаления значения
    по ключу, и сохранения файла с обновленным DS по новому пути.
    """
    list_files = os.listdir(path_dir_from)
    if list_files:
        for file_name in list_files:
            if is_dcm_file(file_name):
                path_to_file = os.path.join(path_dir_from, file_name)
                elem = DoPathAndWriteDS(path_to_file, name_dir_to)
                elem.get_ds()
                if elem.ds:
                    elem.do_anonymous_name()
                    elem.get_path_for_file()
                    elem.save_file()
                    elem.make_file_with_list()
                else:
                    print(f'Не получилась получить Dataset по адресу {path_to_file}')
    else:
        logging.warning(f'В директории {path_dir_from} нет файлов')


if __name__ == '__main__':
    configure_logging()  # вызываем функцию для логирования в файл

    args = parser.parse_args()  # парсим командную строку
    name_or_path_dir_from = args.name_dir_from  # получаем имя или путь директории откуда брать файлы
    name_dir_to = args.name_dir_to  # получаем имя директории куда записывать файлы
    logging.info('Аргументы командной строки: '
                 f'Имя/ путь директории откуда брать данные{name_or_path_dir_from} '
                 f'Имя директории куда записывать файлы {name_dir_to}')

    path_dir_from = is_path_or_name_dir(name_or_path_dir_from)  # Путь до директории с исходными файлами
    if is_dir_exist(path_dir_from):  # Проверяет существование директории по заданному пути
        main(path_dir_from, name_dir_to)
    else:
        logging.warning(f'Не существуют такого пути {path_dir_from}')
        print('Не существуют такого пути {path_dir_from}')
