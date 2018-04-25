from pymodm import fields, MongoModel, errors, connect
import datetime


class User(MongoModel):
    # bc primary_key is True, need to query this field using label _id
    email = fields.EmailField(primary_key=True)
    orig_img_paths = fields.ListField(field=fields.CharField())
    command = fields.ListField(field=fields.IntegerField())
    orig_timestamp = fields.ListField(field=fields.DateTimeField())
    proc_img_paths = fields.ListField(
        field=fields.ListField(field=fields.CharField()))
    proc_time = fields.ListField(field=fields.FloatField())
    proc_status = fields.ListField(field=fields.BooleanField())


def create_user(email, img_paths, comm, times):
    """Create new user and save to db

    :param email: email of user
    :param orig_img_paths: list of image paths
    :param command: array of int corresponding to command
    :param orig_timestamp: array of datetimes corresponding to each input image
    """
    u = User(email, [], [], [], [], [], [])  # create a new User instance
    u.command.extend(comm)
    u.orig_img_paths.extend(img_paths)
    u.orig_timestamp.extend(times)
    u.save(full_clean=False)  # save the user to the database


def add_images(email, img_paths, comms, times):
    """Appends new images to existing User and save to db

    :param email: email of user
    :param orig_img_paths: list of image paths
    :param command: array of int corresponding to command
    :param orig_timestamp: array of datetimes corresponding to each input image
    """
    # Get the first user where _id=email
    user = User.objects.raw({"_id": email}).first()
    user.orig_img_paths.extend(img_paths)
    user.command.extend(comms)
    user.orig_timestamp.extend(times)
    user.save(full_clean=False)  # save the user to the database
