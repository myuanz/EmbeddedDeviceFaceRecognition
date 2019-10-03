# 此处是经删减安全化的配置文件, 真正的 config 在 gitignore 里

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://*:*@127.0.0.1:3306/lab_access_control?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
SECRET_KEY = b'*'