from django.db import models


# Create your models here.
class BaseModel(models.Model):
    note = models.CharField(max_length=200)
    modify_date = models.DateTimeField('date modified')

    class Meta:
        abstract = True


class Department(BaseModel):
    name = models.CharField(max_length=200)


class Team(BaseModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)


class Type1(BaseModel):
    name = models.CharField(max_length=200)


class Type2(BaseModel):
    type1 = models.ForeignKey(Type1)
    name = models.CharField(max_length=200)


class Type3(BaseModel):
    type2 = models.ForeignKey(Type2)
    name = models.CharField(max_length=200)


class item(BaseModel):
    type1 = models.ForeignKey(Type1)
    type2 = models.ForeignKey(Type2)
    type3 = models.ForeignKey(Type3)
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    mark = models.CharField(max_length=200)
    sn = models.CharField(max_length=200)
    amount = models.IntegerField(default=0)
