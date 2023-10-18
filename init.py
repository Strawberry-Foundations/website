import os

import yaml
from yaml import SafeLoader


server_dir = os.path.dirname(os.path.realpath(__file__))

with open(server_dir + "/config.yml", "r") as config_file:
    config = yaml.load(config_file, Loader=SafeLoader)

with open(server_dir + "/secret.key", "r") as secret_file:
    secret = secret_file.read()
    
    
with open(server_dir + "/lang/de_DE.yml", "r") as lang_file:
    de_lang = yaml.load(lang_file, Loader=SafeLoader)
    
with open(server_dir + "/lang/en_US.yml", "r") as lang_file:
    en_lang = yaml.load(lang_file, Loader=SafeLoader)


ip_address          = config["host"]["address"]
port                = config["host"]["port"]

debug_mode          = config["flags"]["debug_mode"]
threaded            = config["flags"]["threaded"]

static_url_path     = config["vars"]["static_url_path"]
static_folder       = config["vars"]["static_folder"]
template_folder     = config["vars"]["template_folder"]

def strloader(lang, string="", argument_1="", argument_2=""):
    match lang:
        case "de":  Str = de_lang
        case "en":  Str = en_lang
        case _:     Str = en_lang
            
    string = Str[string]
    string = string \
    .replace("%s", str(argument_1)) \
    .replace("%c", str(argument_2))
    
    return string