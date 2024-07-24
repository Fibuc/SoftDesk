from django.contrib import admin
from projects.models import Contributor, Project, Issue, Comment


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'type', 'created_time')


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'created_time')


class IssueAdmin(admin.ModelAdmin):
    list_display = ('project', 'name', 'author', 'priority', 'type', 'progress', 'created_time')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'issue', 'author', 'created_time')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)