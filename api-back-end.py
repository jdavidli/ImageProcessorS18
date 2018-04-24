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
    if os.path.exists(main_image_folder) is False:
        os.makedirs(main_image_folder)
    email_v, command_v, time_v, images_v, num_images, message = verify_input(input)
    if email_v == []:
        data = {"message": message}
        return jsonify(data), 400

    try:
        user = models.User.objects.raw({"_id": user_email}).first()
        start_i = len(user.orig_img_paths)
        folder_path = access_folder(main_image_folder, email_v)
        image_paths = decode_save_images(
            folder_path, images_v, num_images, start_i)
        comm_arr = create_command_arr(command_v, num_images)
        dt_arr = create_datetime_arr(time_v, num_images)
        add_images(email_v, image_paths, comm_arr, dt_arr)
        init_proc_status(user, num_images)
        proc_data = run_image_processing(image_paths, command_v)
        times = proc_data["processing_times"]
        stat = proc_data["processing_status"]
        multi_proc_paths = save_proc_images(
            folder_path, proc_data["processed_images"], num_images, start_i, stat)
        add_proc_data(user, multi_proc_paths, times, stat, num_images, start_i)
        base64_images = encode_proc_images(multi_proc_paths, num_images)
        output = { "proc_images": base64_images, "proc_times": times, "proc_status": stat}
        return jsonify(output), 200
    except:
        folder_path = access_folder(main_image_folder, email_v)
        image_paths = decode_save_images(folder_path, images_v, num_images, 0)
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
        base64_images = encode_proc_images(multi_proc_paths, num_images)
        output = { "proc_images": base64_images, "proc_times": times, "proc_status": stat}
        return jsonify(output), 200

def encode_proc_images(paths, num_images):
    base64_imgs = [[]]
    for i in range(num_images):
        save_set = paths[i]
        with open(save_set[0], "rb") as image_file:
            encoded_string1 = base64.b64encode(image_file.read())
        with open(save_set[1], "rb") as image_file:
            encoded_string2 = base64.b64encode(image_file.read())
        with open(save_set[2], "rb") as image_file:
            encoded_string3 = base64.b64encode(image_file.read())
        base64_imgs.append([encoded_string1, encoded_string2, encoded_string3])
    return base64_imgs

def add_proc_data(u, paths, times, stati, num_images, start_i):
    u.proc_img_paths.extend(paths)
    u.proc_time.extend(times)
    u.proc_status[start_i: start_i + num_images] = stati
    u.save()
    return(input, 200)


def save_proc_images(folder_path, proc_imgs, num_images, start, stat):
    image_paths = [[]]
    for i in range(num_images):
        if stat[i] is True:
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
        if stat[i] is False:
            image_paths.append(['','',''])
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
        command_flag = isinstance(command_v, int)
        time_v = input["timestamp"]
        time_flag = isinstance(time_v, str)
        images_v = input["images"]
        num_images = len(images_v)
        if num_images is 0:
            raise ValueError("No input images passed to post function.")
        image_flag = np.zeros((num_images, 1), dtype=bool)
        for i in images_v:
            if isinstance(i, str) is False:
                image_flag[i] = True
        if any(image_flag) is True:
            raise TypeError(
                "At least one uploaded image is not of type string.")
        if not email_flag:
            raise TypeError("User email not of type string.")
        if not command_flag:
            raise TypeError("Command not of type integer.")
        if not time_flag:
            raise TypeError("Timestamp input not of type str.")
        if command_v < 1 or command_v > 5:
            raise ValueError(
                "Integer command passed is not associated with a processing function.")
        message = "SUCCESS: Input validation passed."
        time_v = datetime.datetime.strptime(time_v, "%Y-%m-%d %H:%M:%S.%f")
        return email_v, command_v, time_v, images_v, num_images, message
    except ValueError as inst:
        return [], [], [], [], [], str(inst)
    except TypeError as inst:
        return [], [], [], [], [], str(inst)
    except KeyError:
        inst = "Input keys incorrect. Pass email, image processing command, timestamp and image."
        return [], [], [], [], [], str(inst)
    except:
        inst = "Unknown syntax error during validation of expected input type and value."
        return [], [], [], [], [], str(inst)
