
# Описание
Docker образ для REST API сервиса **YaMDB** на базе **Django**, **PostgreSql 12.4** и **nginx**.

![yamdb_status](https://github.com/plaunezkiy/yamdb_final/workflows/yamdb_worflow/badge.svg)
## Начало работы
Эти инструкции помогут установить и настроить проект на локальной машине.
### Зависимости
* Python >3.8
    * **https://www.python.org/downloads/**
* Docker >3.10
    * **https://www.docker.com/products/docker-desktop**

### Установка
1. Установите docker и docker-compose на ваш сервер.
    * ```sudo apt install docker docker-compose -y```

2. Склонировать репозиторий.
    * ```git clone https://github.com/plaunezkiy/yamdb_final.git```
    
3. Заполнить файл .env.example своими данными для сервера.

4. Перейти в проект, собрать и запустить образ.
    * ```cd yamdb_final/```
    * ```docker-compose up -d --build```

5. Сделать миграции и собрать статические файлы для общего пользования между контейнерами.
    * ```sudo docker container exec **ID** python manage.py migrate```
    * ```sudo docker container exec **ID** mkdir static
    * ```sudo docker container exec **ID** python manage.py collectstatic --no-input --clear```

6. Удаление образа из памяти.
    * Узнать **название** контейнера. 
        * ```docker container ls```
    * Удалить образ по **названию**.
        * ```docker image rm -f *название*```
### Работа с контейнером
* Создание суперпользователя
    * Узнать **ID** контейнера. 
        * ```docker container ls```
    * Подключиться к консоли работающего контейнера.
        * ```docker exec -it *ID* bash```
    * Создать пользователя.
        * ```python manage.py createsuperuser```
* Загрузка начальных данных.
    * Узнать **ID** контейнера. 
        * ```docker container ls```
    * Подключиться к консоли работающего контейнера.
        * ```docker exec -it *ID* bash```
    * Загрузить данные в базу из файла *fixtures.json*.
        * ```python manage.py loaddata fixtures.json```


    

