# В этом файле описаные глобальные изменения фронта для работяг которые будут пилить бекенд

## Рефактор CSS
Раздробил style.css файлы и изменил его название на index.css убрал файл "header...че о там", вы поймёте, в static всёго два файла лежало. Все классы переписанны на методологию БЭМ.  
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

## Добавленные темплейты
- ```header.html``` - вынес шапку в отдельный компонент

## Рефактор views.py
Изменил названия подключаемых темплейтов  
Пример:  
```python
def about(request):
  return render(request, 'organ/about.html') <- новое название
```

## Рефактор urls.py
Изменил названия темплейтов  
Пример:
```python
urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls, name='admin'),
    path('login/', views.auth_login, name='auth_login'),
    path('register/', views.auth_register, name='auth_register'),
    path('about/', views.about, name='about'),
    path('guest/', views.guest, name='guest'),
    ...
```


