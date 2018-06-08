from django.apps import AppConfig
import os


VERBOSE_APP_NAME = 'Quality Entry'
class EntrynocConfig(AppConfig):
    name = 'EntryNOC'

def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]

class PrimaryBlogConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = VERBOSE_APP_NAME