## -*- Code : Utf -*-

'''checking logger and excpetion file'''

import sys
import os
from US_visa.logger import logging
from US_visa.exception import USVisaException


logging.info("Welcome to custom Logger file..!!")

'''check excpetion'''
try:
    a= 1/0
except Exception as e:
    logging.info("Exception is working well..!!")
    raise USVisaException(e,sys)