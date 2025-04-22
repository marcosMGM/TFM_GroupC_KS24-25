from config_bd import get_connection, add_house
import pandas as pd
import numpy as np
import datetime
import os
import requests
from bs4 import BeautifulSoup as bs
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc


for i in range(1, 15001):
    add_house({
        "address": "Calle Falsa "+str(i),
        "price": 250000,
        "bedroom": 3,
        "bathroom": 2
    })