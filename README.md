# ParseBot (закрытый проект будет разрабатываться заново)

## Информация о проекте

Данные сервисы помогают поользователям быстро получать уведомления о новых объявлениях с Avito с помощью телеграмм ботов

## Документация с разными схемами [Documentation](https://github.com/alex-s2222/ParseBot/tree/dev/Documentation/mainBot)

## Перед запуском

1. Клонируем код пректа

```text
git clone https://github.com/alex-s2222/ParseBot.git
```

2. Переходим в директорию проекта

```text
cd ParseBot
```

3. Отредактируйте [run_apps.yaml](https://github.com/alex-s2222/ParseBot/blob/dev/run_apps.yaml)

```text
#MONGO_USER              -> Пользователь в MongoDB
#MONGOPASSWORD           -> Пароль для пользователя MongoDB
        
#USER_ID_FOR_ADMIN_PANEL -> Ваш ID что бы получить доступ для панели Управления
#TG_TOKEN                -> Телеграмм Токен Полученный в @BotFather для каждого бота свой токен
```

## Запуск

1. Запуск сервисов (для запуска в фоновом режиме установите флаг -d)

```text
docker compose up -f run_apps.yaml --build
```

## Полезные команды

условные обозначения

```
CONTAINER:
mainBot → для настройки
sendMsgBot → для получений уведомлений 
database → база данных

n → количество последний логов
nm → временной интервал пример 45m 
```

Посмотреть последних n логов: 

```
docker logs --tail n CONTAINER
```

Посмотреть логи за n времени:

```
docker logs--until nm CONTAINER
```

Посмотреть все логи 

```
docker logs CONTAINER
```

перезапустить определенного бота:

```
docker restart CONTAINER
```