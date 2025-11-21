from configparser import ConfigParser
import streamlit as st

configFilePath = "core\\config\\config.ini"
config = ConfigParser()
config.read(configFilePath)
configData = {}
for key in config["DEFAULT"]:
    configData[key] = [value.strip() for value in config["DEFAULT"][key].split(",")]
