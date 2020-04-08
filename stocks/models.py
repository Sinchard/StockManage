from django.db import models


# Create your models here.
class BaseModel(models.Model):
    note = models.CharField(max_length=200, null=True, blank=True)
    modify_date = models.DateTimeField('date modified', auto_now=True)

    class Meta:
        abstract = True


class Department(BaseModel):
    name = models.CharField(max_length=200)


class Team(BaseModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)


class Type(BaseModel):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self',
                               related_name="child",
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)

    def __str__(self):
        return self.name


class Item(BaseModel):
    type1 = models.ForeignKey(Type,
                              related_name="type1",
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True)
    type2 = models.ForeignKey(Type,
                              related_name="type2",
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True)
    type3 = models.ForeignKey(Type,
                              related_name="type3",
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True)
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    mark = models.CharField(max_length=200)
    sn = models.CharField(max_length=200)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return self.name + " " + self.brand + " " + self.mark + " " + self.sn
