import dj_database_url

DATABASES = {
    'default': dj_database_url.config(default='postgresql://localhost/augeo')
}