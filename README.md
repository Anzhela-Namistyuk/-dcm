# Преобразование и сохранение данных формата dcm

Программа выполняет преобразования входных данных из директории `src`, используя модуль `pydicom`:
1) Считывает данные из файла с расширением `dcm`.
2) Удаляет информацию, хранящуюся в ключе `PatientName` (анонимизирует файлы)
3) Используя информацию в ключах `StudyInstanceUID`, `SeriesInstanceUID`, `SOPInstanceUID` 
преобразует структуру хранения файлов к следующей:
* на первом уровне `StudyInstanceUID`
* на втором уровне `SeriesInstanceUID`
* именем файла будет значение `SOPInstanceUID` с расширением `.dcm`
* путь к каждому файлу будет выглядеть так: `$StudyInstanceUID/$SeriesInstanceUID/$SOPInstanceUID.dcm`

4) Cоздает файл "file_with_diff_path.txt", в котором путь к каждому файлу исходной структуры сопоставлен пути к файлу в конечной структуре.

### Технологии:

> Python 3, pydicom
#####

## Запуск скрипта:

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/MacOS

```
source venv/bin/activate
```

* Если у вас windows

 ```
source venv/scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Пример команды для запуска с указанием директории относительно корня проекта:
#####
`src` - начальная директория с файлами,
#####
`output` - конечная директория для сохранения фалов по новому пути.

```
python3 comand.py src output 
```
Пример команды для запуска с указанием абсолютного пути к директории:
#####
`/Users/anzela/recruit/src` - абсолютный путь к директории с файлами,
#####
`output`- конечная директория для сохранения фалов по новому пути.

```
python3 comand.py /Users/anzela/recruit/src output 
```

### Автор
Намистюк Анжела
