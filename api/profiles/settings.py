# Settings Models
def profile_pictures_per_user_directory(instance, filename):
    return 'media/images/profiles/user_{0}/{1}'.format(instance.user.id, filename)