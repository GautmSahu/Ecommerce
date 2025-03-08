from django.apps import apps
import logging
import os
import sys

logger = logging.getLogger(__name__)

APP_NAME = apps.get_app_config('EcomApp').name

ERROR_MESSAGE = {"error" :"Something went wrong, please try again later."}

def handle_error_log(e,view_name,app_name,extra_values=None):
    try:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error("Error on 'FileName: {}', '{}' %s at %s, extra_values : %s ".format(str(fname),view_name), str(e), str(exc_tb.tb_lineno), str(extra_values), extra={'AppName': app_name})
    except Exception as e:
        print(e)


def handle_info_log(msg,view_name,app_name,extra_values=None):
    try:
        logger.info("{}, on view '{}', extra_values : %s".format(msg,view_name), str(extra_values), extra={"AppName": app_name})
    except Exception as e:
        print(e)