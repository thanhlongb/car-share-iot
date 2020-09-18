import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = '''wrg)_4')@(<VcJxc37"lG;.hC^LT.7X_+Flv2X0w7W&je3>HDTXA*)Ff'xk#D*5'''

SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_HOST = '35.187.227.56'
DATABASE_PORT = 3306
DATABASE_USER = 'root'
DATABASE_PASSWORD = 'C3lz4Jemuga0LNFK'
DATABASE_NAME = 'carshareiot'

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
GOOGLE_MAP_API_KEY = "AIzaSyC4l8KgttHz2TGU96K88shTXGpm17xvF20"

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'buith4nhlong@gmail.com'
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_PASSWORD = 'cdoqpguqcktubuxu'
MAIL_DEFAULT_SENDER = 'buith4nhlong@gmail.com'
