from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models import UserInfo
from users.models import User

@receiver(post_save, sender=User)

def update_user_info(sender, instance, **kwargs):
    # Get the UserInfo object or create a new one if it doesn't exist
    try:
        user_info = UserInfo.objects.get(user=instance)
    except UserInfo.DoesNotExist:
        user_info = UserInfo(user=instance)
    
    # Save the updated UserInfo object
    user_info.save()
