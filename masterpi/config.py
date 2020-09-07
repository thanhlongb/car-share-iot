import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = '''wrg)_4')@(<VcJxc37"lG;.hC^LT.7X_+Flv2X0w7W&je3>HDTXA*)Ff'xk#D*5'''

SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_HOST = 'nwhazdrp7hdpd4a4.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
DATABASE_PORT = 3306
DATABASE_USER = 'dwnmrp5llieowj19'
DATABASE_PASSWORD = 'i1dtel962z0lo3jy'
DATABASE_NAME = 'ejdr1o1zohrodiw4'
SQLALCHEMY_DATABASE_URI = (
    'mysql+mysqlconnector://{user}:{pasw}@{host}:{port}/{name}').format(
    user=DATABASE_USER,
    pasw=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    name=DATABASE_NAME
)
DATABASE_CONNECT_OPTIONS = {}

CSRF_ENABLED = True
CSRF_SESSION_KEY = '''lur$F1de)*Cxy;SA>fxvwqF=!R`F?m`PPO4~a;>,4t:yLEr*n6~0aStU:?;?x6n'''

GOOGLE_CLIENT_ID = '''798556033482-18bih5lt883gvriclvr7fdger63hcnb4.apps.googleusercontent.com'''
GOOGLE_CLIENT_SECRET = '''3azjWEwWkaMvMHPA_ue7FfR-'''
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# RECAPTCHA_USE_SSL = False
# RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
# RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
# RECAPTCHA_OPTIONS = {'theme': 'white'}