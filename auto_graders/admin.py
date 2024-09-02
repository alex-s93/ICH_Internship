from django.contrib import admin
from auto_graders.models import (
    Task,
    Submission,
    UserProfile,
    TaskTests,
    TaskParameters,
)

admin.site.register(Submission)
admin.site.register(UserProfile)


class TaskParametersInline(admin.TabularInline):
    model = TaskParameters
    classes = ('collapse',)
    extra = 1


@admin.register(TaskParameters)
class TaskParametersAdmin(admin.ModelAdmin):
    list_display = (
        'input_params',
        'output_params',
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'description',
    )
    list_display_links = ('id', 'title')
    readonly_fields = ('id',)
    ordering = ('-id',)
    search_fields = ('title', 'description')
    inlines = [
        TaskParametersInline,
    ]
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'id',
                    'title',
                    'description',
                )
            },
        ),
    )


@admin.register(TaskTests)
class TaskTestsAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'file_path')
    list_display_links = ('id', 'task')
    readonly_fields = ('id',)
    ordering = ('-id',)
    search_fields = ('task__title',)
    fieldsets = ((None, {'fields': ('id', 'task', 'file_path')}),)
