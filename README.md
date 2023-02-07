# Signal's handler microservice

### Описание:
Приложение, в задачи которого входит обработка сигналов, приходящих по http протоколу
от OPC-клиента.

### Требования:
* Python 3.10
* Docker/Compose

### Установка:
Получение приложения
```bash
git clone ssh://git@git.unios.io:11220/unios-v1/opc-microservice.git && cd opc-microservice
```
Или
```bash
git clone http://git.unios.io/unios-v1/opc-microservice.git && cd opc-microservice
```
Сборка приложения
```bash
make build
```
### Запуск сервера:
```bash
make runserver
```

### data_seeker.py
В data_seeker.py находится скрипт, который необходимо добавить как задачу в crontab,
указав оптимальное время запуска.

### settings.py
В settings.py указывается IP-адрес, на котором будет работать приложение, а также перечисляется белый
список адресов для CORS.
