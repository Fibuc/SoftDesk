import uuid
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Project(models.Model):
    """Modèle de projet."""
    class Type(models.TextChoices):
        BACK_END = 'BACK END'
        FRONT_END = 'FRONT END'
        IOS = 'iOS'
        ANDROID = 'ANDROID'

    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(max_length=8192, blank=True)
    type = models.CharField(choices=Type.choices, max_length=15)
    created_time = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
        )

    def __str__(self) -> str:
        return self.name

    def is_author(self, user):
        return self.author == user

    def is_contributor(self, user):
        return self.contributed_by.filter(user=user).exists()


@receiver(post_save, sender=Project)
def create_contributor(sender, instance, created, **kwargs):
    """Créée une instance de Contributor entre le projet et l'auteur du projet
    lors de la création d'un projet.

    Args:
        sender (Project): La classe Project associée à l'enregistrement.
        instance (Project): Instance de la classe Project créée.
        created (Bool): Retourne l'état de la création de l'instance.
    """
    if created:
        Contributor.objects.create(project=instance, user=instance.author)


class Contributor(models.Model):
    """Modèle d'un contributeur à un projet."""
    created_time = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name='contributed_by'
        )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
        )

    class Meta:
        unique_together = ('user', 'project',)

    def __str__(self) -> str:
        return self.user.username


class Issue(models.Model):
    """Modèle d'une demande d'un projet."""
    class Priority(models.TextChoices):
        LOW = 'LOW'
        MEDIUM = 'MEDIUM'
        HIGH = 'HIGH'

    class Type(models.TextChoices):
        BUG = 'BUG'
        FEATURE = 'FEATURE'
        TASK = 'TASK'

    class Progress(models.TextChoices):
        TO_DO = 'TO DO'
        IN_PROGRESS = 'IN PROGRESS'
        FINISHED = 'FINISHED'

    name = models.CharField(max_length=128)
    description = models.TextField(max_length=4096, blank=True)
    priority = models.CharField(choices=Priority.choices, max_length=15)
    type = models.CharField(choices=Type.choices, max_length=15)
    progress = models.CharField(
        choices=Progress.choices, max_length=15, default=Progress.TO_DO
        )
    created_time = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
        )
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name='issues'
        )

    def __str__(self) -> str:
        return self.name

    def is_contributor(self, user):
        return self.project.is_contributor(user=user)

    def is_author(self, user):
        return self.project.is_author(user=user)


class Comment(models.Model):
    """Modèle d'un commentaire d'une demande."""
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
        )
    description = models.TextField(max_length=4096)
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
        )
    issue = models.ForeignKey(
        to=Issue, on_delete=models.CASCADE, related_name='comments'
        )

    def is_contributor(self, user):
        return self.issue.is_contributor(user=user)

    def is_author(self, user):
        return self.issue.is_author(user=user)
