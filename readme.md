## SISTEM INFORMASI MANAJEMENT KLINIK

make virtual env

```
python -m venv venv
```

start virtual env (windows)

```
venv/Scripts/activate
```

start virtual env (macos/linux)

```
source/bin/activate
```
(Make sure `(venv)` indicator is appear on your terminal)\
\
\
install django

```
pip install django
```

install tailwindcss

```
pip install django-tailwind
```
or you can do this for install depencencies
```
pip install -r requirements.txt
```
\
\
init & install tailwind
```
python manage.py tailwind init
```
```
python manage.py tailwind install
```
\
\
start server

```
py manage.py runserver
```

start tailwindcss

```
py manage.py tailwind start
```
