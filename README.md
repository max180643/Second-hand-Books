# Second-hand Books
This repository consists of codes of "Web programming (Web Pro)" Project, Faculty of Information Technology, King Mongkut's Institute of Technology Ladkrabang (KMITL).

# Config
Edit database config in settings.py

```
 DATABASES = {
    'default': {
        'ENGINE': '',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
``` 

Then

```
$ python3 manage.py makemigrations

&&

$ python3 manage.py migrate
```

