from flask import Flask, request, jsonify
from flask_cors import CORS
from pymodm import connect, errors
from models import create_user, add_images
import models
import datetime
import numpy as np
import scipy.misc as sp
import os
import base64
from image_processor import run_image_processing
import logging as lg

app = Flask(__name__)
CORS(app)
comp_with_db = "mongodb://vcm-3580.vm.duke.edu:27017/image_processing"
connect(comp_with_db)
main_image_folder = "/home/vcm/images_new/"
jpg_header = "data:image/jpg;base64,"
png_header = "data:image/png;base64,"
tif_header = "data:image/tif;base64,"
zip_header = "data:application/x-zip-compressed;base64,"
lg.basicConfig(filename='process_image_post.log',
               level=lg.DEBUG,
               format='%(asctime)s %(message)s',
               datefmt='%m/%d/%Y %I:%M:%S %p')


@app.route("/process_image", methods=["POST"])
def post_user():
    client_input = request.get_json()
    if os.path.exists(main_image_folder) is False:
        os.makedirs(main_image_folder)
    email_v, command_v, time_v, images_v, num_images, mess = verify_input(
        client_input)
    if email_v == []:
        lg.debug(' | ABORTED: Input Validation failed.')
        data = {"message": mess}
        return jsonify(data), 400
    if is_zip_input(images_v):
        num_images, images_v, base64_orig_images = decode_zip_input(images_v)
    else:
        base64_orig_images = convert_for_front(images_v)

    try:
        user = models.User.objects.raw({"_id": email_v}).first()
        start_i = len(user.orig_img_paths)
        folder_path = access_folder(main_image_folder, email_v)
        image_paths = decode_save_images(
            folder_path, images_v, num_images, start_i)
        comm_arr = create_command_arr(command_v, num_images)
        dt_arr = create_datetime_arr(time_v, num_images)
        proc_data = run_image_processing(image_paths, command_v)
        times = proc_data["processing_times"]
        stat = proc_data["processing_status"]
        orig_hist = proc_data["original_histograms"]
        orig_hist_list = []
        for hh in orig_hist:
            orig_hist_list.append(hh.tolist())
        proc_hist = proc_data["processed_histograms"]
        proc_hist_list = []
        for hh in proc_hist:
            proc_hist_list.append(hh.tolist())
        if not np.any(stat):
            lg.debug(' | ABORTED: No images processed.')
            data = {"message": "Status codes indicate no images processed."}
            return jsonify(data), 400
        img_dims = proc_data["image_dimensions"]
        multi_proc_paths = save_proc_images(
            folder_path, proc_data["processed_images"], num_images,
            start_i, stat)
        add_images(email_v, image_paths, comm_arr, dt_arr, multi_proc_paths,
                   times, stat)
        base64_images = encode_proc_images(multi_proc_paths, num_images)
        if base64_images == []:
            lg.debug(' | ABORTED: base64 encoding of processed images failed.')
            data = {"message": "Encoding processed images in base64 failed."}
            return jsonify(data), 400
        else:
            lg.info(' | SUCCESS: Image processing complete.')
            output = {"proc_images": base64_images,
                      "proc_times": times,
                      "proc_status": stat,
                      "headers": [jpg_header, tif_header, png_header],
                      "orig_hist": orig_hist_list,
                      "proc_hist": proc_hist_list,
                      "image_dims": img_dims,
                      "orig_images": base64_orig_images}
            return jsonify(output), 200

    except:
        folder_path = access_folder(main_image_folder, email_v)
        image_paths = decode_save_images(folder_path, images_v, num_images, 0)
        comm_arr = create_command_arr(command_v, num_images)
        dt_arr = create_datetime_arr(time_v, num_images)
        proc_data = run_image_processing(image_paths, command_v)
        times = proc_data["processing_times"]
        stat = proc_data["processing_status"]
        orig_hist = proc_data["original_histograms"]
        orig_hist_list = []
        for hh in orig_hist:
            orig_hist_list.append(hh.tolist())
        proc_hist = proc_data["processed_histograms"]
        proc_hist_list = []
        for hh in proc_hist:
            proc_hist_list.append(hh.tolist())
        if not np.any(stat):
            lg.debug(' | ABORTED: No images processed.')
            data = {"message": "Status codes indicate no images processed."}
            return jsonify(data), 400
        img_dims = proc_data["image_dimensions"]
        multi_proc_paths = save_proc_images(
            folder_path, proc_data["processed_images"], num_images, 0, stat)
        create_user(email_v, image_paths, comm_arr, dt_arr, multi_proc_paths,
                    times, stat)
        base64_images = encode_proc_images(multi_proc_paths, num_images)
        if base64_images == []:
            lg.debug(' | ABORTED: base64 encoding of processed images failed.')
            data = {"message": "Encoding processed images in base64 failed."}
            return jsonify(data), 400
        else:
            lg.info(' | SUCCESS: Image processing complete.')
            output = {"proc_images": base64_images,
                      "proc_times": times,
                      "proc_status": stat,
                      "headers": [jpg_header, tif_header, png_header],
                      "orig_hist": orig_hist_list,
                      "proc_hist": proc_hist_list,
                      "image_dims": img_dims,
                      "orig_images": base64_orig_images}
            return jsonify(output), 200


def encode_proc_images(paths, num_images):
    """Encode each saved processed image to base64 and returns list of strings

    :param paths: paths to all processed images
    :param num_images: number of input images
    :returns: base64_imgs
    :type paths: list of strings
    :type num_images: int
    :rtype: list of list of strings
    """
    base64_imgs = []
    try:
        for i in range(num_images):
            save_set = paths[i]
            if save_set == ['', '', '']:
                base64_imgs.append(['', '', ''])
            else:
                with open(save_set[0], "rb") as image_file:
                    encoded_string1 = base64.b64encode(image_file.read())
                with open(save_set[1], "rb") as image_file:
                    encoded_string2 = base64.b64encode(image_file.read())
                with open(save_set[2], "rb") as image_file:
                    encoded_string3 = base64.b64encode(image_file.read())
                base64_imgs.append([str(encoded_string1), str(encoded_string2),
                                    str(encoded_string3)])
        return base64_imgs
    except:
        return []


def save_proc_images(folder_path, proc_imgs, num_images, start, stat):
    """Save all processed images of numpy array format to jpg, tif, and png
            returns list of paths to the processed images

    :param folder_path: path to user folder
    :param proc_imgs: numpy array of processed images
    :param num_images: number of input images
    :param start: index used for filename, number of processed images in folder
    :param stat: list of booleans to indicate which images were processed
    :return: image_paths
    :type folder_path: string
    :type proc_imgs: list of numpy arrays
    :type num_images: int
    :type start: int
    :type stat: list
    :rtype: list of list of strings
    """
    image_paths = []
    for i in range(num_images):
        if stat[i] is True:
            image_name = '/proc_image' + str(start + i)
            jpg_img_name = folder_path + image_name + '.jpg'
            tif_img_name = folder_path + image_name + '.tif'
            png_img_name = folder_path + image_name + '.png'
            sp.imsave(jpg_img_name, proc_imgs[i])
            sp.imsave(tif_img_name, proc_imgs[i])
            sp.imsave(png_img_name, proc_imgs[i])
            image_paths.append([jpg_img_name, tif_img_name, png_img_name])
        if stat[i] is False:
            image_paths.append(['', '', ''])
    return image_paths


def access_folder(main, email):
    """Get or create folder for input username/email

    :param main: main image folder holding all user folders
    :param email: email/username input
    :return: folder_path
    :type folder_path: string
    :type main: string
    :type email: string
    :rtype: string
    """
    folder_path = main + email
    if os.path.exists(folder_path) is False:
        os.makedirs(folder_path)
    return folder_path


def decode_save_images(folder_path, images, num_images, start):
    """Decode base64 input images and save to user folder

    :param folder_path: path to user folder
    :param images: input images as base64 strings
    :param num_images: number of input images
    :param start: index used for filename, number of processed images in folder
    :return: image_paths
    :type folder_path: string
    :type images: list of strings
    :type num_images: int
    :type start: int
    :rtype: list of strings
    """
    image_paths = []
    for i in range(num_images):
        img = images[i]
        stripped_img = img.split(",", 1)[1]
        find_ext = img.split(";", 1)[0]
        ext = find_ext.split("/", 2)[1]
        image_dec = base64.b64decode(stripped_img)
        image_name = '/image' + str(start + i)
        full_img_name = folder_path + image_name + '.' + ext
        img_file = open(full_img_name, 'wb')
        img_file.write(image_dec)
        img_file.close()
        image_paths.append(full_img_name)
    return image_paths


def create_command_arr(command_v, num_images):
    """Create list of input command

    :param command_v: input image processing command
    :param num_images: number of input images
    :return: comm_arr
    :type command_v: int
    :type num_images: int
    :rtype: list
    """
    comm_arr = []
    for x in range(num_images):
        comm_arr.append(command_v)
    return comm_arr


def create_datetime_arr(time_v, num_images):
    """Create list of input timestamp

    :param time_v: input timestamp
    :param num_images: number of input images
    :return: dt_arr
    :type time_v: datetime
    :type num_images: int
    :rtype: list
    """
    dt_arr = []
    for x in range(num_images):
        dt_arr.append(time_v)
    return dt_arr


def verify_input(input1):
    """Create list of input timestamp

    :param input1: json input from post request
    :return: email_v, command_v, time_v, images_v, num_images, message
    :type input1: dict
    """
    email_flag = False
    command_flag = False
    time_flag = False
    image_list_flag = False
    email_format_flag = False
    try:
        email_v = input1["email"]
        if not email_v:
            raise ValueError("Empty email/username field.")
        email_flag = isinstance(email_v, str)
        if email_flag:
            check_at_symbol = email_v.find("@")
            check_dot_symbol = email_v[check_at_symbol:].find(".")
            if (check_at_symbol == -1 or check_dot_symbol == -1):
                email_format_flag = True
        command_v = input1["command"]
        command_flag = isinstance(command_v, int)
        time_v = input1["timestamp"]
        time_flag = isinstance(time_v, str)
        images_v = input1["images"]
        image_list_flag = isinstance(images_v, list)
        num_images = len(images_v)
        if num_images is 0:
            raise ValueError("No input images passed to post function.")
        image_flag = np.zeros(num_images, dtype=bool)
        for i in images_v:
            if isinstance(i, str) is False:
                image_flag[i] = True
        if any(image_flag) is True:
            raise TypeError(
                "At least one uploaded image is not of type string.")
        if not image_list_flag:
            raise TypeError("Images not uploaded as list of strings.")
        if not email_flag:
            raise TypeError("User email not of type string.")
        if email_format_flag:
            raise TypeError("User email is in the wrong format.")
        if not command_flag:
            raise TypeError("Command not of type integer.")
        if not time_flag:
            raise TypeError("Timestamp input not of type str.")
        if command_v < 1 or command_v > 5:
            raise ValueError(
                "Input command not associated with a processing function.")

        message = "SUCCESS: Input validation passed."
        try:
            time_v = datetime.datetime.strptime(time_v,
                                                "%Y-%m-%d %H:%M:%S.%f")
        except:
            raise TypeError("Timestamp string not correct format.")
        return email_v, command_v, time_v, images_v, num_images, message
    except ValueError as inst:
        lg.debug(' | ABORTED: ValueError: %s' % str(inst))
        return [], [], [], [], [], str(inst)
    except TypeError as inst:
        lg.debug(' | ABORTED: TypeError: %s' % str(inst))
        return [], [], [], [], [], str(inst)
    except KeyError:
        inst = "Input keys incorrect."
        lg.debug(' | ABORTED: KeyError: %s' % inst)
        return [], [], [], [], [], str(inst)
    except:
        inst = "Unknown syntax error during input validation."
        lg.debug(' | ABORTED: UnknownError: %s' % inst)
        return [], [], [], [], [], str(inst)


def is_zip_input(input_images):
    """ Check if input is a .zip

    :param input_images: base64 images
    :type input_images: list
    :return: True if the header is a .zip header
    """

    first_image = input_images[0]
    if first_image[0:41] == zip_header:
        return True
    else:
        return False


def get_header(file_name):
    """ Get appropriate header for image_type
    """

    dot_positions = [n for n, c in enumerate(file_name) if c == "."]
    n_positions = len(dot_positions)
    image_type = file_name[dot_positions[n_positions-1]:]

    if image_type == ".jpg":
        return jpg_header
    elif image_type == ".png":
        return png_header
    else:
        return tif_header


def decode_zip_input(input_images):
    """ Decode base64 zip to extract images

    :param input_images: base64 images
    :type input_images: list
    :return: number of images, extracted images
    """

    import zipfile

    # Strip header:
    base64_to_decode = input_images[0][41:]

    # Decode base64:
    base64_decoded = base64.b64decode(base64_to_decode)

    # Write zip file:
    temp_zip_filepath = "./temp.zip"
    if os.path.exists(temp_zip_filepath):
        os.remove(temp_zip_filepath)
    with open(temp_zip_filepath, "wb") as wf:
        wf.write(base64_decoded)

    # Unzip file:
    temp_zip_folder = "./temp"
    if os.path.exists(temp_zip_folder):
        all_files = os.listdir(temp_zip_folder)
        for af in all_files:
            os.remove(temp_zip_folder + '/' + af)
    else:
        os.mkdir(temp_zip_folder)

    z = zipfile.ZipFile(temp_zip_filepath, "r")
    z.extractall(temp_zip_folder)
    z.close()

    # Read images and encode as base64 strings:
    image_list = os.listdir(temp_zip_folder)

    base64_for_front = []
    base64_for_back = []
    for i in image_list:
        header_to_add = get_header(i)
        full_path_i = temp_zip_folder + '/' + i
        with open(full_path_i, "rb") as image_file:
            i_base64 = str(base64.b64encode(image_file.read()))
        base64_for_front.append(i_base64)
        base64_for_back.append(header_to_add + i_base64[2:])

    n_images = len(base64_for_back)

    # Return base64 strings:
    return n_images, base64_for_back, base64_for_front


def convert_for_front(input_images):
    """ Strip unnecessary headers
    """

    base64_for_front = []
    for i in input_images:
        stripped_i = i.split(",", 1)[1]
        base64_for_front.append("b'" + stripped_i)

    return base64_for_front
