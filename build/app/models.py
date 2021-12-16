#!/usr/bin/env python3
""" models """
from dataclasses import dataclass
from io import BytesIO
from flask_sqlalchemy import SQLAlchemy
import qrcode

db = SQLAlchemy()

@dataclass
class piyot(db.Model):
    """ user model """
    __tablename__ = "piyot"
    user_id: str
    user_name: str
    secret_otp: str

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger, index=False, unique=True, nullable=False)
    user_name = db.Column(db.String, index=False, unique=True, nullable=False)
    create_date = db.Column(db.BigInteger, index=False, unique=False, nullable=True)
    secret_otp = db.Column(db.String, index=False, unique=True, nullable=False)

    def get_qr_code(self):
        """ generate otp qr code """
        qr_code = BytesIO()
        image = qrcode.make(
            "otpauth://totp/Piyot Auth Service:"
            + self.user_name + "@" + str(self.user_id)
            + "?secret=" + self.secret_otp
        )
        image.save(qr_code, "PNG")
        qr_code.seek(0)
        return qr_code

    def __init__(self, user_id, user_name, secret_otp, create_date):
        self.user_id = user_id
        self.user_name = user_name
        self.secret_otp = secret_otp
        self.create_date = create_date

    def __repr__(self):
        return "<piyot {}>".format(self.user_id)
