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


def create_user(email, img_paths, comm, times, proc_paths, proc_times, stat):
    """Create new user with images and metadata and save to db

    :param email: email of user
    :param img_paths: list of image paths
    :param proc_paths: list of processed image paths
    :param stat: list of processing status for each image
    :param comm: list of int corresponding to command
    :param times: list of datetimes corresponding to each input image
    :param proc_times: list of processing times for each image
    """
    u = User(email, [], [], [], [], [], [])
    u.command.extend(comm)
    u.orig_img_paths.extend(img_paths)
    u.orig_timestamp.extend(times)
    u.proc_time.extend(proc_times)
    u.proc_status.extend(stat)
    u.proc_img_paths.extend(proc_paths)
    u.save()  # save the user to the database


def add_images(email, img_paths, comms, times,  proc_paths, proc_times, stat):
    """Appends new images and metadata to existing User and save to db

    :param email: email of user
    :param img_paths: list of image paths
    :param proc_paths: list of processed image paths
    :param stat: list of processing status for each image
    :param comm: list of int corresponding to command
    :param times: list of datetimes corresponding to each input image
    :param proc_times: list of processing times for each image
    """
    # Get the first user where _id=email
    user = User.objects.raw({"_id": email}).first()
    user.orig_img_paths.extend(img_paths)
    user.command.extend(comms)
    user.orig_timestamp.extend(times)
    user.proc_time.extend(proc_times)
    user.proc_status.extend(stat)
    user.proc_img_paths.extend(proc_paths)
    user.save()  # save the user to the database
