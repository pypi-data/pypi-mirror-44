# django-fm-minio

1. pre-create bucket, policy and keys
2. add fixtures_minio to installed apps and configure plugin

```
INSTALLED_APPS += ['fixtures_minio']

FM_MINIO_ACCESS_KEY = 'fixtures'  ###
FM_MINIO_BUCKET = 'fixtures'  ###
FM_MINIO_SECRET_KEY = 'fixtures'  ###
FM_MINIO_SECURE = False  ###
FM_MINIO_URL = 'localhost:9000'  ###
```

## usage

### list remote fixtures

```
DJANGO_SETTINGS_MODULE=settings.production python manage.py fm_list
fixture_1553728345.json 2019-03-27 23:12:25.896000+00:00 33222
fixture_1553728357.json 2019-03-27 23:12:37.600000+00:00 33222
fixture_1553733559.json 2019-03-28 00:39:19.712000+00:00 33669
fixture_1553736829.json 2019-03-28 01:33:51.626000+00:00 4444449
```

### push fixture

```
DJANGO_SETTINGS_MODULE=settings.production python manage.py fm_push users
[...........................................................................]
filename: fixture_1553766625.json
```

### load fixture

```
DJANGO_SETTINGS_MODULE=settings.production python manage.py fm_load fixture_1553759118.json
Installed 67 object(s) from 1 fixture(s)
```
