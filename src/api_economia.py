import requests
import json
import os
import re


class APIEconomia:

    def __init__(self):
        self.base_url = "https://api.worldbank.org/v2"