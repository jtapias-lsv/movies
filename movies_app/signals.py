from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import Movie


@receiver(pre_save, sender=Movie)
def create_slug_for_movie(instance, **kwargs):
    """
    function to create a movie slug
    Args:
        instance: movie instance
        **kwargs:

    Returns: return movie instance

    """
    instance.slug = slugify(instance.title)
    return instance