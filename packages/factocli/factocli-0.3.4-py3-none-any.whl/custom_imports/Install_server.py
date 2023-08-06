from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator
from examples import custom_style_1
from examples import custom_style_2
from examples import custom_style_3
from pprint import pprint
import os, errno
import wget
import urllib.request
import shutil
from pathlib import Path
import subprocess
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import json
from termcolor import colored

import multiprocessing
import time


settings_file = "settings.json"


settingsjson = {
    "installed_factorio_directory": "",
    "installed_factorio_version": "",
    "installed_factorio_server_service_file_path": "",
    "installed_factorio_api_service_file_path": ""
}



def ask_path_to_install_server():
    where_to_install_prompt = {
        'type': 'input',
        'name': 'install_path',
        'message': 'Where do you want to install factorio? # /opt is recommended!',
    }
    answers = prompt(where_to_install_prompt)
    return answers['install_path']


def confirm_where_to_install(path):
    confirm_where_to_install = {
        'type': 'confirm',
        'name': 'confirm_where_to_install',
        'message': 'Are you sure you want to install in ' + path + " ?",
    }
    answers = prompt(confirm_where_to_install)
    return answers['confirm_where_to_install']
    

def download_latest_factorio_headless_server(install_path, url_version):
    print("Downloading latest release...")
    file_name = wget.download(url_version)
    
    current_directory = os.getcwd()
    print("\n")
    full_path_of_file = current_directory + "/" + file_name
    print(full_path_of_file)

    if(os.path.isfile(full_path_of_file)):
        print("File exists")
        print("Extracting file to the given path")
        import tarfile
        tar = tarfile.open(full_path_of_file) 
        tar.extractall(path=install_path) #untar file to the given install path
        tar.close()
        if(os.path.isdir(install_path)):
            print("File has been extracted to " + install_path)
            print("Removing downloaded tar file...")
            print(full_path_of_file)
            os.remove(full_path_of_file)
            print("File removed")
            create_user_and_group_and_add_user_to_group(install_path)
        elif(os.path.isdir(install_path) == False):
            print("Something wreng wrong check if the extracted directory exists")
        
    elif(os.path.isfile(full_path_of_file) == False):
        print("something went wrong check if the file exists")
        print("please try again")


def create_user_and_group_and_add_user_to_group(install_path):
    print("Creating user & group")
    print("Adding user to created group")
    subprocess.run(["sudo", "adduser", "--disabled-login", "--no-create-home", "--gecos", "factorio", "factorio"])
    #sudo adduser --disabled-login --no-create-home --gecos factorio factorio
    print("Done")
    #sudo chown -R factorio:factorio /opt/factorio
    
    factorio_path = install_path + "/" + "factorio"
    print("Making user owner of the new created directory " + factorio_path)
    subprocess.run(["sudo", "chown", "-R","factorio:factorio", factorio_path])
    print("Done")
    make_copy_of_server_settings_json_file(factorio_path)



def make_copy_of_server_settings_json_file(factorio_path):
    #sudo cp server-settings.example.json server-settings.json
    json_server_settings_example_file_path = factorio_path + "/" + "data" + "/" + "server-settings.example.json"
    json_server_settings_example_path = factorio_path + "/" + "data" + "/" + "server-settings.json"
    shutil.copy(json_server_settings_example_file_path,json_server_settings_example_path)
    if(os.path.isfile(json_server_settings_example_path)):
        print("Server Settings Json Copied and Created")
        waiting_for_save_file(factorio_path)
        #create_service_file_in_systemd(factorio_path)
        #launch_savefile_webserver()
        # create_save_yesorno = ask_for_creating_a_new_save_file_or_upload_your_own()
        # if(create_save_yesorno == True):
        #     create_new_save_file(factorio_path)
        # elif(create_save_yesorno == False):
        #     print("Launching webserver for savefile upload")
            #launch_savefile_webserver()
            # yesorno = ask_for_save_file_config()
            # if(yesorno):
            #     print("Launching save file creator")
            #     save_file_creator_main()
            # elif(yesorno == False):
            #     print("Factorio server needs a save file to run, please provide the save.zip in /factorio/saves directory")

    else:
        print("Something went wrong with copying server-settings.example.json")





def waiting_for_save_file(factorio_path):
    #/opt/factorio
    print("Creating a new saves directory")
    os.mkdir(factorio_path + "/" + "saves")
    saves_directory_path = factorio_path + "/" + "saves"
    if(os.path.isdir(saves_directory_path)):
        print("Done")
        #./bin/x64/factorio --create ./saves/my-save.zip
        print("Changing directory to saves directory")
        os.chdir(saves_directory_path)
        list_dir = os.listdir(saves_directory_path)
        print("Files in saves directory" + str(list_dir))
        print("Factorio can't start without a save file")
        # print("Waiting for a save file to be uploaded")
        print(colored("Please make a new game in factorio and save it", "magenta"))
        print(colored("When done use one of the following commands to copy your save file", "magenta"))
        print(colored("Copy file from a remote host to local host SCP example:", "magenta"))
        print(colored(f"scp username@from_host:file.txt {saves_directory_path}", "magenta"))
        print(colored("Or", "magenta"))
        print(colored("Copy file from local host to a remote host SCP example:", "magenta"))
        print(colored(f"scp file.txt username@to_host:{saves_directory_path}", "magenta"))
        print(colored("Waiting for a save file to be uploaded", "magenta"))
        while not os.listdir(saves_directory_path):
            time.sleep(1)

        if (os.listdir(saves_directory_path)):
            # read file
            #print("Detected file(s)")
            detected_files_list = os.listdir(saves_directory_path)
            print("detected files" + str(detected_files_list))
            
            # files = []
            # for file in detected_files_list:
            #     files.append({"name" : file})
                
            #print(files)
            #if(extensions == ".zip"):
            #print("Zip file(s) detected")
            print("Please choose the save file to use for the factorio server")
            which_save_file_prompt = [
                {
                    'type': 'list',
                    'message': 'Select save file',
                    'name': 'which_save_file',
                    'choices': detected_files_list,
                    # 'validate': lambda answer: 'You must choose at least one save file.' \
                    #     if len(answer) == 0 else True
                }
            ]
            #FIXME: Saving the detected save file
            answer = prompt(which_save_file_prompt, style=custom_style_2)
            #print(answers)
            if(answer == None):
                print("Nothing selected. Please try again.")
            
            if(answer != None):
                print(answer)
                file_name = answer['which_save_file']
                print(file_name)
                create_service_file_in_systemd(factorio_path, file_name)
                
            
            
        else:
            raise ValueError("%s isn't a file!" % saves_directory_path)


    else:
        print("Something went wrong creating saves directory")
    
    



def ask_for_creating_a_new_save_file_or_upload_your_own():
    create_new_save_or_use_own_save_prompt = {
            'type': 'confirm',
            'name': 'save_file',
            'message': 'Do you want to create a new save file?',
        }
    answers = prompt(create_new_save_or_use_own_save_prompt)
    return answers['save_file']



def ask_for_save_file_config():
    save_file_config = {
            'type': 'confirm',
            'name': 'save_file_creator',
            'message': 'Do you want to run the save file creator?',
        }
    answers = prompt(save_file_config)
    return answers['save_file_creator']


def create_new_save_file(factorio_path):
    print("Creating a new saves directory")
    os.mkdir(factorio_path + "/" + "saves")
    saves_directory_path = factorio_path + "/" + "saves"
    if(os.path.isdir(saves_directory_path)):
        print("Done")
        #./bin/x64/factorio --create ./saves/my-save.zip
        print("Changing directory to create save file")
        os.chdir(factorio_path)
        print(factorio_path)
        print("Creating a new save file")
        subprocess.run(["./bin/x64/factorio", "--create", "./saves/my-save.zip"])
        #if(os.path.isfile(factorio_path + "/" + "saves" + ))
        print("New save file created")
        #create_service_file_in_systemd(factorio_path)
        #waiting_for_save_file
    else:
        print("Something went wrong creating saves directory")






def create_service_file_in_systemd(factorio_path, file_name):
    #create a new service file /etc/systemd/system/factorio.service
    systemd_path = "/etc/systemd/system"
    os.chdir(systemd_path)
    
    execstart_string = (f"{factorio_path}/bin/x64/factorio --start-server {factorio_path}/saves/{file_name} --server-settings {factorio_path}/data/server-settings.json --rcon-port 25575 --rcon-password factory")

    service_file_string =(f"""
        [Unit]
        Description=Factorio Headless Server

        [Service]
        Type=simple
        User=factorio
        ExecStart={execstart_string}
        """)

    with open("factorio.service", "w") as file:
        file.write(service_file_string)

    if(os.path.isfile(systemd_path + "/" + "factorio.service")):
        print("Service file factorio.service created in /etc/systemd/system")
        chown_factorio_map_for_factorio_user(factorio_path)

    else:
        print("Something went wrong creating the service file")


def chown_factorio_map_for_factorio_user(factorio_path):
    #sudo chown -R factorio: /opt/factorio
    print("Performing factorio user access")
    print(factorio_path)
    #subprocess.run(["chown", "-R", "factorio:factorio " + factorio_path])
    #subprocess.run(["chown", "-R", "factorio: ", factorio_path])
    subprocess.run(["chown", "-R", "factorio:factorio", factorio_path])    
    reload_daemon(factorio_path)
    #write_factorio_path_to_json(factorio_path)




def write_factorio_path_to_json(factorio_path):
    with open(settings_file, 'r') as f:
        array = json.load(f)
    

def reload_daemon(factorio_path):
    #systemctl daemon-reload
    print("Reloading daemon")
    subprocess.run(["systemctl", "daemon-reload"])
    start_factorio_service()
    #waiting_for_save_file(factorio_path)

def start_factorio_service():
    #systemctl start factorio
    print("Starting factorio service")
    subprocess.run(["systemctl", "start", "factorio"])
    #check_if_service_is_running()


def check_if_service_is_running():
    #systemctl is-active --quiet service
    is_service_running = subprocess.run(["systemctl", "is-active", "--quiet", "factorio.service"])
    if(is_service_running == 0):
        print("Congratulations factorio is up and running!")
    elif(is_service_running != 0):
        print("Something went wrong checking if factorio.service is running")  




def install_server(url_version):
    install_path = ask_path_to_install_server()
    print(install_path)
    yesorno = confirm_where_to_install(install_path) 
    if(yesorno):
        #Check wether the path exists
        print("Checking Path...")
        if(install_path[0] == "~"):
            install_path = install_path.replace("~", "")
            home_path = str(Path.home())
            new_install_path = home_path + install_path
            path_exists = os.path.isdir(new_install_path)
            print(new_install_path)
            if(path_exists):
                print("The directory " + new_install_path + " exists...")
                try:
                    #os.makedirs(install_path, exist_ok=False)
                    print("Proceeding with the install...")
                    #Download the latest factorio expermimental headless server file
                    download_latest_factorio_headless_server(new_install_path,url_version)    
                except FileExistsError:
                    # directory already exists
                    print("Error Creating the directory in " + new_install_path)        
            if(path_exists == False):
                print("The directory" + new_install_path + "doesn't exists")
                print("please make sure the directory exists")

        else: 
            path_exists = os.path.isdir(install_path)
            if(path_exists):
                print("The directory " + install_path + " exists...")
                try:
                    #os.makedirs(install_path, exist_ok=False)
                    print("Proceeding with the install...")
                    #Download the latest factorio expermimental headless server file
                    download_latest_factorio_headless_server(install_path,url_version)    
                except FileExistsError:
                    # directory already exists
                    print("Error Creating the directory in " + install_path)        
            if(path_exists == False):
                print("The directory" + install_path + "doesn't exists")
                print("please make sure the directory exists")

    if(yesorno == False):
        print("Please Try Again")





def experimental_server_main():
    url_latest_version = "https://www.factorio.com/get-download/latest/headless/linux64"
    install_server(url_latest_version)



def stable_server_main():
    url_stable_version = "https://www.factorio.com/get-download/stable/headless/linux64"
    install_server(url_stable_version)