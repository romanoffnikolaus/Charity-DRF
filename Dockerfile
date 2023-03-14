FROM python:3.10 
#какой базовый образ питона
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
#отключение буферизации логов, позволяет выводить все ошибки
COPY . /SaveTheDay
WORKDIR /SaveTheDay
#копирование всех файлов из текущей директории и назначание ее рабочей директорией
RUN pip install -r requirements.txt

#запустить команду d
