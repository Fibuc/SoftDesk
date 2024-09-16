from django.contrib import admin
from projects.models import Contributor, Project, Issue, Comment


class ProjectAdmin(admin.ModelAdmin):
    """
    Classe de personnalisation de l'affichage des projets dans l'interface
    d'administration Django.
    """
    list_display = ('name', 'author', 'type', 'created_time')


class ContributorAdmin(admin.ModelAdmin):
    """
    Classe de personnalisation de l'affichage des contributeurs dans
    l'interface d'administration Django.
    """
    list_display = ('user', 'project', 'created_time')


class IssueAdmin(admin.ModelAdmin):
    """
    Classe de personnalisation de l'affichage des demandes dans l'interface
    d'administration Django.
    """
    list_display = (
        'name', 'project', 'author', 'priority', 'type', 'progress',
        'created_time', 'assigned_user'
        )


class CommentAdmin(admin.ModelAdmin):
    """
    Classe de personnalisation de l'affichage des commentaires dans
    l'interface d'administration Django.
    """
    list_display = ('id', 'issue', 'author', 'created_time')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
