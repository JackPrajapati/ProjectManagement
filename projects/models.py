from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser, Group


class Project(TimeStampedModel):
    STATUS = (
        ('NEW', 'NEW'),
        ('INPROGRESS', 'In-Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=255, choices=STATUS, default='NEW', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        app_label = 'projects'
        verbose_name = "Project"
        verbose_name_plural = "Projects"


class Employee(AbstractUser, TimeStampedModel):
    DESIGNATION = (
        ('NA', 'NA'),
        ('DEVELOPER', 'Developer'),
        ('TEAMLEAD', 'Team Leader'),
        ('PROJECTMANAGER', 'Project Manager'),
    )
    designation = models.CharField(max_length=255, choices=DESIGNATION, default='NA', blank=True, null=True)
    projects = models.ManyToManyField(Project)

    def __str__(self):
        if self.first_name:
            return str(self.first_name + " " + self.last_name + " - " + " ".join([y for x, y in self.DESIGNATION if x == self.designation]))
        return str(self.username + " - " + " ".join([y for x, y in self.DESIGNATION if x == self.designation]))

    class Meta:
        app_label = 'projects'
        verbose_name = "Employee"
        verbose_name_plural = "Employees"


class Group(Group):
    pass

    class Meta:
        app_label = 'projects'
        verbose_name = "Group"
        verbose_name_plural = "Groups"
