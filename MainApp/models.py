from django.db import models
from django.db.models import Manager
from django.contrib.auth.models import User

LANGS = (
    ("py", "Python"),
    ("js", "JavaScript")
)

class Snippet(models.Model):
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=30, choices=LANGS)
    code = models.TextField(max_length=5000)
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    is_public = models.BooleanField(default=True)
    objects: Manager

    def __str__(self):
        return self.name

class Comment(models.Model):
    text = models.TextField(max_length=1000)
    creation_date = models.DateTimeField
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    snippet = models.ForeignKey(to=Snippet, on_delete=models.CASCADE)
    objects: Manager