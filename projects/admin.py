from django.contrib import admin
from .models import Project, Employee
# Register your models here.


class EmployeeAdmin(admin.ModelAdmin):
    # model = Employee
    # can_delete = True
    # extra = 1
    fieldsets = (
        ('Employee Details', {'fields': (
            'username',
            'email',
            'first_name',
            'last_name',
            'designation',
            # 'password',
        )}),
        ('Permission', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
        ('Assigned Projects', {'fields': (
            'projects',
        )})
    )

    def projects(self, obj, **kwargs):
        return Project.objects.filter(employee=self.employee)


# class ProjectAdmin(admin.ModelAdmin):
#     inlines = [EmployeeAdmin]


# admin.site.register(Project, ProjectAdmin)
admin.site.register(Project)
admin.site.register(Employee, EmployeeAdmin)
