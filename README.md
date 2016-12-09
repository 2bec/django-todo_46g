# django-todo_46g
[ INCOMPLETO ] Para ver a aplicação online, acesse: https://bga23sjcok.execute-api.us-west-2.amazonaws.com/dev.

# Requirements
- Django 1.9.8
- Djangorestframework 3.5.3
- Zappa 0.31.0
- Django-redis 4.6.0
- Webpack Loader
- [https://github.com/jschneier/django-storages](Django Storages)

# Desenvolvimento
Por ter pouco, ou nenhum conhecimento, de: Redis, AWS, React e Zappa, resolvi focar em ter uma aplicação funcional, utilizando os requerimentos mencionados.
Tive algumas dificuldades, mas buscando orientação na documentação oficial foi fácil resolver. Pesquisei bastante sobre redis, aws, react, zappa e djangorestframework.
Não utilizei o exemplo pronto do react pois acredito que desenvolvendo todos os passos dos tutoriais iniciais consigo aprender melhor e mais rápido.


## Fix warnings and exceptions
Utilizando python 2.7 precisei instalar urllib3 com argumento extra ``` pip install urllib3[secure] ``` e atualizar curl
``` pip install --upgrade curl ```.

## Redis
Segui orientações da [https://niwinz.github.io/django-redis/latest/#_configure_as_cache_backend](documentação 1) e [https://niwinz.github.io/django-redis/latest/#_configure_as_session_backend](documentação 2). Alterar ``` LOCATION ``` para seu redis-server e porta.
```
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
```
## Webpack Loader
Segui orientações da [https://webpack.github.io/docs/usage.html](documentação).
```
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}
```

## React
Segui as indicações de https://facebook.github.io/react/docs/installation.html e cheguei na seguinte instalação de dependências.
```
npm install --save-dev jquery react react-dom webpack webpack-bundle-tracker babel-loader babel-core babel-preset-es2015 babel-preset-react
```

Para os arquivos estáticos usei Django Storages para armazenar num S3, alterei o settings.py. Incluir as chaves e o bucket S3.
```
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
AWS_STORAGE_BUCKET_NAME = ""
AWS_QUERYSTRING_AUTH = False
```

## Deploy Zappa
Segui orientações da [https://github.com/Miserlou/Zappa#running-the-initial-setup--settings](documentação). Incluir o bucket S3.
```
{
    "dev": {
        "django_settings": "todo_46g.settings",
        "s3_bucket": "",
        "debug": true,
        "cache_cluster_enabled": true,
    }
}
```