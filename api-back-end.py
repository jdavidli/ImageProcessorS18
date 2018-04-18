from flask import Flask, request, jsonify
from flask_cors import CORS
from pymodm import connect, errors
import models
import datetime
import numpy as np
import os
import base64

app = Flask(__name__)
CORS(app)
comp_with_db = "mongodb://vcm-3580.vm.duke.edu:27017/image_processor"
connect(comp_with_db)

@app.route("/process_image", methods=["POST"])
def post_user():
    input = request.get_json()

    #verify input
    email_v= input["email"]
    command_v = input["command"] #check int between what numbers
    time_v = input["timestamp"] #in datetime format
    images = input["images"] #list of base64 strings
    num_images = len(image)
    try:
        user = models.User.objects.raw({"_id": user_email}).first()
        start_i = len(user.orig_img_paths)   #index where new iamges start in array
        folder_path = get_folder_path(email_v)
        image_paths = decode_save_images(folder_path, images, num_images, start_i)
        comm_arr = create_command_arr(command_v, num_images)
        dt_arr = create_datetime_arr(time_v, num_images)
        add_images(email_v, image_paths, comm_arr, dt_arr)

    except:
        folder_path = create_folder_path(email_v)
        image_paths = decode_save_images(folder_path, images, num_images, 0)
        comm_arr = create_command_arr(command_v, num_images)
        dt_arr = create_datetime_arr(time_v, num_images)
        create_user(email=email_v, orig_img_paths=image_paths, command=comm_arr, orig_timestamp = dt_arr)

        #send jessica image paths to process adn command
        #jessica returns image and i need to save it

    return jsonify(input), 200


def get_folder_path(email):
    filename = email.split("@")[0]
    folder_path = "/home/vcm/images/" + filename
    return folder_path

def decode_save_images(folder_path, images, num_images, start):
    fext = '.jpg'
    image_paths= []
    for i in images:
        image_dec = base64.b64decode(images[i])
        image_name = 'image' + str(start + i)
        full_img_name = folder_path + image_name + fext
        img_file = open(full_img_name, 'wb')
        img_file.write(image_dec)
        image_paths[i] = full_img_name
    return image_paths

def create_folder_path(email):
    filename = email.split("@")[0]
    folder_path = "/home/vcm/user_images/" + filename
    os.makedirs(folder_path)
    return folder_path

def create_command_arr(command_v, num_images):
    return command_v*np.ones([1,num_images])

def create_datetime_arr(time_v, num_images):
    for x in xrange(num_images):
        dt_arr[x]= time_v
    return dt_arr
