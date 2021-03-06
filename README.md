# api_yamdb ![GitHub Actions status](https://github.com/nastyaeremenko/yamdb_final/actions/workflows/yamdb_workflow.yaml/badge.svg)
### Описание
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха. Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.
Благодарные или возмущённые читатели оставляют к произведениям текстовые отзывы (Review) и выставляют произведению рейтинг (оценку в диапазоне от одного до десяти). Из множества оценок автоматически высчитывается средняя оценка произведения.

Пользовательские роли:
- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user)— может читать всё, как и Аноним, дополнительно может публиковать отзывы и ставить рейтинг произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы и ставить им оценки; может редактировать и удалять свои отзывы и комментарии.
- Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять и редактировать любые отзывы и комментарии.
- Администратор (admin) — полные права на управление проектом и всем его содержимым. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Администратор Django — те же права, что и у роли Администратор.
### Технологии
Python 3.8
Django 3.0.5
Django REST Framework 4.6.0
### Запуск проекта в dev-режиме
- Скачайте и запустите образ:
```
docker run earmos/yamdb:lastes
``` 
- Запустите проект:
```
docker-compose up -d
```
- Выполните миграции:
```
docker-compose exec web python manage.py migrate --noinput
```
- Создайте суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```
- Соберите статические файлы в STATIC_ROOT:
```
docker-compose exec web python manage.py collectstatic --no-input 
```
### Авторы
Анастасия Еременко, Игорь Погребняк, Сергей Мусорин
