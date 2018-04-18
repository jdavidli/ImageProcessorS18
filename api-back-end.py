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

@app.route("/api/process_image", methods=["POST"])
def post_user():
    input = request.get_json()

    #verify input
    email_v= input["ip_email"]
    command_v = input["command"]
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
    for i in image
        image = base64.b64decode(images[i])
        #save image with approp index#
        #save path to image in array of strings
    return image_paths

def create_folder_path(email):
    filename = email.split("@")[0]
    folder_path = "/home/vcm/images/" + filename
    os.makedirs(folder_path)
    return folder_path

def create_command_arr(command_v, num_images):
    #create array
    return comm_arr

def create_datetime_arr(time_v, num_images):
    #create array
    return dt_arr
