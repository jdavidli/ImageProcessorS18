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
comp_with_db = "mongodb://vcm-3580.vm.duke.edu:27017/heart_rate_app"
connect(comp_with_db)

@app.route("/api/process_image", methods=["POST"])
def post_user():
    input = request.get_json()

    #verify input
    #extract image as base64
    #command
    try:
        email_v= input["ip_email"]
        command_v = input["command"]
        time_v = input["timestamp"] #in datetime format
        image = input["images"] #list of base64 strings

        num_images = len(image)
        user = models.User.objects.raw({"_id": user_email}).first()
        start_i = len(user.orig_img_paths)   #index where new iamges start in array 
        #user exists

        filename = email.split("@")[0]
        folder_path = "/home/vcm/images/" + filename
        image = base64.b64decode(image)
        #save image


        #for input list of images save them in the folder
        #create image paths and save them
        #create array of command
        #create array of times

        add_images(email_v, img_paths, command_v, time_v)

    except:
        create_user(email=email_v, age=age_v, heart_rate=hr_v)
        #create folder
        filename = email.split("@")[0]
        folder_path = "/home/vcm/images/" + filename

        os.makedirs(folder_path)


    #check if user exists
        #save image in existing folder

    #if not
        #create user
        #create folder
        #save image

    #send jessica image paths to process adn command
#jessica returns image and i need to save it
#save proc imag path

    return jsonify(input), 200
