from ._version import version_info, __version__
from .Html import Html
from .VuetifyTemplate import VuetifyTemplate

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'ipyvuetify',
        'require': 'ipyvuetify/extension'
    }]