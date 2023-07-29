from django.contrib import admin
from .models import *
from employee.forms import EmployeeForm

# admin.site.register(Role)
admin.site.register(CustomUser)
admin.site.register(Department)
admin.site.register(Designation)
# admin.site.register(Employee)
admin.site.register(Competency)
admin.site.register(Onboarding)
admin.site.register(Task)
admin.site.register(Probation)
admin.site.register(Termination)
admin.site.register(Course)
admin.site.register(Training)
admin.site.register(DevelopmentPlan)
admin.site.register(Matrix)
admin.site.register(Question)
admin.site.register(Appraisal)
admin.site.register(Document)
admin.site.register(News)
admin.site.register(Promotion)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeForm

# @admin.register(Venue)
# class VenueAdmin(admin.ModelAdmin):
# 	list_display = ('name', 'address', 'phone')
# 	ordering = ('name',)
# 	search_fields = ('name', 'address')


# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
# 	fields = (('name', 'venue'), 'event_date', 'description', 'manager', 'approved')
# 	list_display = ('name', 'event_date', 'venue')
# 	list_filter = ('event_date', 'venue')
# 	ordering = ('event_date',)
# Register your models here.
