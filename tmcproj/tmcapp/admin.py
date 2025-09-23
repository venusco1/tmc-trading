
from django.contrib import admin
from .models import AllowCourse
from .models import Video, UserProgress


class AllowCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course_allowed')
    list_filter = ('course_allowed',)
admin.site.register(AllowCourse, AllowCourseAdmin)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'is_unlocked', 'watched_previous')



