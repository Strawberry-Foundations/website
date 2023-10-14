import os

import yaml
from yaml import SafeLoader

server_dir = os.path.dirname(os.path.realpath(__file__))

with open(server_dir + "/config.yml", "r") as config_file:
    config = yaml.load(config_file, Loader=SafeLoader)

with open(server_dir + "/secret.key", "r") as secret_file:
    secret = secret_file.read()
    
ip_address          = config["host"]["address"]
port                = config["host"]["port"]

debug_mode          = config["flags"]["debug_mode"]
threaded            = config["flags"]["threaded"]

static_url_path     = config["vars"]["static_url_path"]
static_folder       = config["vars"]["static_folder"]
template_folder     = config["vars"]["template_folder"]
