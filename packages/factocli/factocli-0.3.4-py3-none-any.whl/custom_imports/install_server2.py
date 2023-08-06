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



# Factocli installs the following:
# a headless factorio server
# a flask webserver for the statistics 
# a flask api for the android app 





# Choise is experimental server
# give the path where factorio must be installed
# 











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








def install_server_main():
    install_path = ask_path_to_install_server()
    print(install_path)
    yesorno = confirm_where_to_install(install_path) 
    if yesorno:
        print("Checking path...")
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
                    #download_latest_factorio_headless_server(new_install_path,url_version)  
                      
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
                    #download_latest_factorio_headless_server(install_path,url_version)    
                except FileExistsError:
                    # directory already exists
                    print("Error Creating the directory in " + install_path)        
            if(path_exists == False):
                print("The directory" + install_path + "doesn't exists")
                print("please make sure the directory exists")
    
    else:
        print("Please try again")