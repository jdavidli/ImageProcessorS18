from flask import Flask, request, jsonify
from flask_cors import CORS
from pymodm import connect, errors
from models import create_user, add_images
import models
import datetime
import numpy as np
import os
import base64
from image_processor import run_image_processing

app = Flask(__name__)
CORS(app)
comp_with_db = "mongodb://vcm-3580.vm.duke.edu:27017/image_processor"
connect(comp_with_db)
main_image_folder = "/home/vcm/images/"


@app.route("/process_image", methods=["POST"])
def post_user():
    input = request.get_json()
    email_v, command_v, time_v, images_v, num_images = verify_input(input)
    if os.path.exists(main_image_folder) is False:
        os.makedirs(main_image_folder)
    try:
        user = models.User.objects.raw({"_id": user_email}).first()
        start_i = len(user.orig_img_paths)
        folder_path = access_folder(main_image_folder, email_v)
        image_paths = decode_save_images(
            folder_path, images, num_images, start_i)
        comm_arr = create_command_arr(command_v, num_images)
        dt_arr = create_datetime_arr(time_v, num_images)
        add_images(email_v, image_paths, comm_arr, dt_arr)
        init_proc_status(user, num_images)
        proc_data = run_image_processing(image_paths, command_v)
        times = proc_data["processing_times"]
        stat = proc_data["processing_status"]
        multi_proc_paths = save_proc_images(
            folder_path, proc_data["processed_images"], num_images, start_i)
        add_proc_data(user, multi_proc_paths, times, stat, num_images, start_i)

    except:
        folder_path = access_folder(main_image_folder, email_v)
        image_paths = decode_save_images(folder_path, images, num_images, 0)
        comm_arr = create_command_arr(command_v, num_images)
        dt_arr = create_datetime_arr(time_v, num_images)
        create_user(email_v, image_paths, comm_arr, dt_arr)
        user = models.User.objects.raw({"_id": user_email}).first()
        init_proc_status(user, num_images)
        proc_data = run_image_processing(image_paths, command_v)
        times = proc_data["processing_times"]
        stat = proc_data["processing_status"]
        multi_proc_paths = save_proc_images(
            folder_path, proc_data["processed_images"], num_images, start_i)
        add_proc_data(user, multi_proc_paths, times, stat, num_images, start_i)
    return jsonify(input), 200


def add_proc_data(u, paths, times, stati, num_images, start_i):
    u.proc_img_paths.extend(paths)
    u.proc_time.extend(times)
    u.proc_status[start_i: start_i + num_images] = stati
    u.save()
    return


def save_proc_images(folder_path, proc_imgs, num_images, start):
    image_paths = [[] for _ in range(num_images)]
    for i in proc_imgs:
        image_name = '/proc_image' + str(start + i)
        jpg_img_name = folder_path + image_name + '.jpg'
        tif_img_name = folder_path + image_name + '.tif'
        png_img_name = folder_path + image_name + '.png'
        img_file = open(jpg_img_name, 'wb')
        img_file.write(proc_imgs[i])
        img_file.close()
        img_file = open(tif_img_name, 'wb')
        img_file.write(proc_imgs[i])
        img_file.close()
        img_file = open(png_img_name, 'wb')
        img_file.write(proc_imgs[i])
        img_file.close()
        image_paths.append([jpg_img_name, tif_img_name, png_img_name])
    return image_paths


def access_folder(main, email):
    folder_path = main + email
    if os.path.exists(folder_path) is False:
        os.makedirs(folder_path)
    return folder_path


def init_proc_status(u, num):
    status = np.zeros([1, num_images])
    u.proc_status.extend(status)
    u.save(full_clean=False)
    return


def decode_save_images(folder_path, images, num_images, start):
    fext = '.png'
    image_paths = []
    for i in range(num_images):  # want i to start at 0, double check this is true
        image_dec = base64.b64decode(images[i])
        image_name = '/image' + str(start + i)
        full_img_name = folder_path + image_name + fext
        img_file = open(full_img_name, 'wb')
        img_file.write(image_dec)
        img_file.close()
        image_paths.append(full_img_name)
    return image_paths


def create_command_arr(command_v, num_images):
    return command_v*np.ones([1, num_images])


def create_datetime_arr(time_v, num_images):
    dt_arr =[]
    for x in range(num_images):
        dt_arr.append(time_v)
    return dt_arr


def verify_input(input):
    email_flag = False
    command_flag = False
    time_flag = False
    try:
        email_v = input["email"]
        email_flag = isinstance(email_v, str)
        command_v = input["command"]
        if command_v < 1 or command_v > 5:
            raise ValueError(
                "Integer command passed is not associated with a processing function.")
        command_flag = isinstance(command_v, int)
        time_v = input["timestamp"]
        time_flag = isinstance(time_v, datetime.datetime)
        images_v = input["images"]
        num_images = len(images_v)
        if num_images is 0:
            raise ValueError("No input images passed to post function.")
        image_flag = np.zeros((num_images, 1), dtype=bool)
        for i in images_v:
            if isinstance(images_v[i], str) is False:
                image_flag[i] = True
        if any(image_flag) is True:
            raise TypeError(
                "At least one uploaded image is not of type string.")
        if email_flag:
            raise TypeError("User email not of type string.")
        if command_flag:
            raise TypeError("Command not of type integer.")
        if time_flag:
            raise TypeError("Timestamp input not of type datetime.")
        print("SUCCESS: Input validation passed.")
    except ValueError as inst:
        print(inst.message)
        raise ValueError("ValueError: Input validation failed.")
    except TypeError as inst:
        print(inst.message)
        raise TypeError("TypeError: Input validation failed.")
    except KeyError:
        print("Input keys incorrect. Pass email, image processing command, timestamp and image.")
        raise KeyError(
            "KeyError: Passed inputs do not have correct components (key assignments).")
    except:
        print("Unknown error during validation of expected input type and value.")
        raise UnknownError("UnknownError: Input validation failed.")
    return email_v, command_v, time_v, images_v, num_images
