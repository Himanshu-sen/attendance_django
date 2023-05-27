from django.contrib import admin
from home.models import Contact
from home.models import Attendance
from home.models import faces

# Register your models here.

class MemberAdmin(admin.ModelAdmin):
  list_display = ("name", "status", "department","year", "date", "time")


class Me(admin.ModelAdmin):
  list_display = ("name", "image")

admin.site.register(Contact)
admin.site.register(faces, Me)
admin.site.register(Attendance,MemberAdmin)