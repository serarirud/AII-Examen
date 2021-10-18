from bs4 import BeautifulSoup
import sqlite3
import tkinter
from tkinter import *
from tkinter import messagebox
import urllib
from urllib import request
import re
from datetime import datetime
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context