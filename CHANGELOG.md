## Рефактор CSS
Раздробил style.css файлы и изменил его название на index.css убрал файл "header...че о там", вы поймёте, в static всёго два файла лежало 
Изменена структура папки static:
- ```common``` - элементы/состовные части
- ```components``` - компоненты
- ```css``` - точка входа css стилей
- ```vendor``` - utils файлы/шфриты/файлы сброса/всякая поебота

## Рефактор templates/organ
Изменил названия теплейтов, на более локаничные  

- ```faq_page.html``` → ```about.html```
- ```for_auth.html``` → ```dashboard.html```
- ```header.html``` → ```base.html```
- ```home.html``` → ```index.html```
- ```list_tasks.html``` → ```tasks.html```
- ```login.html``` → ```auth_login.html```
- ```noauth.html``` → ```guest.html```
- ```register.html``` → ```auth_register.html```
- ```task_calendar.html → calendar.html```

## Рефактор views.py
Изменил названия темплейтов

## Рефактор urls.py
Изменил названия темплейтов


