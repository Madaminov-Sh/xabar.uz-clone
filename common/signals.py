from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from register.models import User, Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    """User uchun Profile yaratish uchun signal."""
    exists_user = Profile.objects.filter(user_id=instance.id).exists()
    if instance.is_superuser:
        return False
    elif instance.is_admin:
        Profile.objects.create(user=instance)
    elif not instance.is_admin and exists_user:
        Profile.objects.get(user_id=instance.id).delete()
