from flask import Flask, request, jsonify
from flask_cors import CORS

from pymodm import connect, errors
# need to make models of the class we create
import models
import datetime

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
        user = models.User.objects.raw({"_id": user_email}).first()
        #user exists
        cd to folder in vm
        pwd
        realtive path /images/user
        #create image paths and save them

        import uuid
        name each iamge a uuid

        add_images(email_v, img_paths, command_v, time_v)

    except:
        create_user(email=email_v, age=age_v, heart_rate=hr_v)




        user = models.User.objects.raw({"_id": email_v}).first()
        interval_average = calculate_interval_avg(user.heart_rate,
                                                  user.heart_rate_times,
                                                  since_v)
        tachy_flag = check_tachycardia(interval_average, user.age)
        done = {"user": email_v,
                "status": "verified and average calculated",
                "interval_average": interval_average,
                "tachycardia_check": tachy_flag
                }
    #check if user exists
        #save image in existing folder

    #if not
        #create user
        #create folder
        #save image

    #send jessica image paths to process
#jessica returns image and i need to save it
#save proc imag path

    return jsonify(input), 200
