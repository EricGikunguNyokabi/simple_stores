# from decouple import config  # For environment variables
import os

class Config:
    SECRET_KEY = "9fdde50cf248cc178bac18fa6cb3e6de1510bcd207c5a4e3a1ec3d832eb44af0"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/wenstores"
    # SQLALCHEMY_DATABASE_URI= "mysql+pymysql://root:@localhost:3307/TJ_dinhive"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload folders
    UPLOAD_FOLDER = "app/static/images"
    PRODUCT_UPLOAD_FOLDER = "app/static/images/products"
    CATEGORY_UPLOAD_FOLDER = "app/static/images/category"

    # Company details
    COMPANY_NAME = "WENDY-WINE STORES"
    COMPANY_PHONE_1 = "+254 769 805233"
    COMPANY_PHONE_2 = "+254 769 805233"
    COMPANY_EMAIL_1 = "wendybolo84@gmail.com"
    COMPANY_EMAIL_2 = "wendybolo84@gmail.com"
    COMPANY_URL = "https://wendy.pythonanywhere.com/"

    # Email setup
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "wendybolo84@gmail.com"
    MAIL_PASSWORD = "bekx dhiy umud rnst"
    MAIL_DEFAULT_SENDER = ("Wendy Pending-Order :Details", MAIL_USERNAME)



