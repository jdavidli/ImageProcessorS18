from models import create_user, add_images
import models
import datetime
import numpy as np
import os
import base64
import pytest
from api_import import save_proc_images, access_folder
from api_import import decode_save_images, create_command_arr
from api_import import create_datetime_arr, verify_input
from api_import import encode_proc_images


def test_verify_input():
    t = "2018-03-09 10:00:36.372339"
    t1 = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f")
    encoded_string = "b'/9j/4AAQSkZJRgABAQICEIUIf/2Q=='"
    input1 = {
        "email": "suyash@suyashkumar.com",
        "command": 1,
        "timestamp": t1,
        "images": encoded_string
    }
    email_v, command_v, time_v, images_v, num_images, mess = verify_input(input1)
    assert(email_v == input1["email"])
    assert(command_v == input1["command"])
    assert(time_v == input1["timestamp"])
    assert(images_v == input1["images"])
    assert(num_images == 1)
    input2 = {
        "email": "suyash@suyashkumar.com",
        "command": 1,
        "timestamp": t1,
        "images": []
    }
    with pytest.raises(ValueError):
        email_v, command_v, time_v, images_v, num_images, mess = verify_input(input2)
    input3 = {
        "email": "suyash@suyashkumar.com",
        "command": 1,
        "timestamp": t1,
        "image": encoded_string
    }
    with pytest.raises(KeyError):
        email_v, command_v, time_v, images_v, num_images, mess = verify_input(input3)
    input4 = {
        "email": 234,
        "command": 1,
        "timestamp": t1,
        "images": encoded_string
    }
    with pytest.raises(TypeError):
        email_v, command_v, time_v, images_v, num_images, mess = verify_input(input4)
    input5 = {
        "email": "suyash@suyashkumar.com",
        "command": 7,
        "timestamp": t1,
        "images": encoded_string
    }
    with pytest.raises(ValueError):
        email_v, command_v, time_v, images_v, num_images, mess = verify_input(input5)
    return


def test_access_folder():
    email = 'email@email.com'
    main_image_folder = os.getcwd()
    path = access_folder(email)
    assert(path == main_image_folder+email)
    assert(os.path.exists(path) is True)
    os.rmdir(path)
    return


def test_create_command_arr():
    com1 = 1
    com2 = 3
    num1 = 1
    num2 = 5
    ans1 = create_command_arr(com1, num1)
    ans2 = create_command_arr(com2, num2)
    assert(ans1 == [1])
    assert(ans2 == [3, 3, 3, 3, 3])


def test_create_datetime_arr():
    t = "2018-03-09 10:00:36.372339"
    t1 = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f")
    num1 = 1
    num2 = 2
    dt1 = create_datetime_arr(t1, num1)
    dt2 = create_datetime_arr(t1, num2)
    assert(dt1 == [t1])
    assert(dt2 == [t1, t1, t1])


def test_decode_save_images():
    folder_path = os.getcwd()
    start = 0
    text_file = open("pupbase64.txt", "r")
    string = text_file.read()
    jpg_header = "data:image/jpg;base64,"
    img = jpg_header + string
    image_paths = decode_save_images(folder_path, [img], 1, start)
    assert(isinstance(image_paths, list) is True)
    assert(isinstance(image_paths[0], str) is True)
    assert(os.path.exists(image_paths[0]) is True)
    file_name = os.path.split(image_paths[0])[1]
    assert(file_name == "image0.jpg")
    os.remove(file_name)

def test_encode_proc_images():
    paths = [["pup.jpg", "pup.tif", "pup.png"]]
    text_file = open("pupbase64.txt", "r")
    string = text_file.read()
    num_images =  1
    base64img = encode_proc_images(paths, num_images)
    assert(string == base64img[0][0])
    paths= [['', '', '']]
    base64img = encode_proc_images(paths, num_images)
    assert(paths == base64img)
