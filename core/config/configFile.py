from configparser import ConfigParser

configFilePath = "core\\config\\config.ini"
config = ConfigParser()
config.read(configFilePath)
configData = config["DEFAULT"]