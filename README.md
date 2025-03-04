# Сокращение ссылок с помощью Vk API

### Как установить

**Вам необходим токен приложения VK**
1. [Социальная сеть ВК](https://vk.com/) - зарегистрируйтесь
1. [Сервисный токен приложения](https://id.vk.com/about/business/go/docs/ru/vkid/latest/vk-id/tokens/service-token)
    - [Создание приложения](https://id.vk.com/about/business/go/docs/ru/vkid/latest/vk-id/connection/create-application)
    - Тип приложения - Web
    - Базовый домен - example.com
    - Доверенный Redirect URL - https://example.com
    - Вы увидите сервисный токен приложения на подобии такого: _82a02da882a02da882a02da8a981b7f3cc882a082a02da8e4af9c41e8551329276dde72_

Вставте полученный токен в файл **.env**  

Запустите проект например с помощю cmd:

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

```
D:
```
>Вместо **D** напишите диск на котором расположен проект
```
cd _путь к директории с файлами проекта_
```
```
python short_link.py URL
```

### Пример запуска

```
python main.py https://youtu.be/dQw4w9WgXcQ?si=RIyQYg54bjmtJPOS
https://vk.cc/cDWVsZ
```

```
python main.py https://vk.cc/cDWVsZ
По ссылке переходили 12 раз
```