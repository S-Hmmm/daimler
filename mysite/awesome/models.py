from django.db import models


class Cases(models.Model):
    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    case_name = models.CharField(max_length=50)
    method = models.CharField(max_length=10)
    url_path = models.CharField(max_length=200)
    data = models.TextField(null=True)
    expected = models.TextField(null=True)
    create_time = models.DateTimeField(auto_now_add=True, auto_created=True)
    modify_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.case_name
