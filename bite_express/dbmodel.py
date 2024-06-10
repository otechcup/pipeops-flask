#!/usr/bin/env python
# -*- coding: utf-8 -*-
# BiteExpress App


__author__ = "PhoenixITng"
__copyright__ = f"Copyright 2023 - datetime.utcnow().year, {__author__}"
__credits__ = ["Mr. O"]
__version__ = "config('BITE_EXPRESS_VERSION', cast=float)"
__maintainer__ = __author__
__email__ = "info@biteexpress.ng"
__status__ = "config('BITE_EXPRESS_ENVIRONMENT_STATUS', cast=str)"


# import modules
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType

from datetime import datetime

from bite_express import db


"""
BiteExer table is used to store and record all personal information of each and every BiteExer in BiteExpress

All bite id are generated with this format:
00000-BTE-00000
Their unique id, follow by BiteExpress short form

kitchen id column is used to store BitexVendor staffs and it is changable

Account status column helps to define the different states of BiteExer account.
Different rules can be applied to the account based on their account status, in order to better manage data entry.
Examples of account status include:
"Activ", "Inactive", "Pre-Active", "Suspended", "Banned", "Freezed" "Deactivated"...

BiteExer account will be "Pre-Active" if they are yet to verify their email address.
"""
class BiteExer(db.Model):
    __table_args__ = {'mysql_engine': "InnoDB"}
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    referrer_id = db.Column(db.String(15))
    kitchen_id = db.Column(db.String(15))
    bite_id = db.Column(db.String(15), unique=True, nullable=False)
    account_status = db.Column(
        db.String(100), default="Pre-Active", nullable=False
    )
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100), nullable=False)
    last_seen = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    date_updated = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )


    def __repr__(self):
        return f"BiteExer(Bite ID: {self.bite_id})"


    @classmethod
    def get_by_email_address(cls, email_address):
        return (
            BiteExerBasicInfo.query
                .filter_by(email_address=email_address)
                .first()
        )
        
        
    @classmethod
    def get_by_bite_id(cls, bite_id):
        return cls.query.filter_by(bite_id=bite_id).first()
    
    
    def add(self):
        db.session.add(self)
        db.session.commit()
        
        
    def update(self, firstname, middle_name, lastname):
        self.firstname = firstname
        self.middle_name = middle_name
        self.lastname = lastname
        self.date_updated = datetime.utcnow()
        
        db.session.commit()


    def update_account_status(self, account_status):
        self.account_status = account_status
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def update_last_seen(self, last_seen):
        self.last_seen = last_seen
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def update_kitchen_id(self, kitchen_id):
        self.kitchen_id = kitchen_id
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()


    # relationships logic
    privilege = db.relationship(
        "BiteExerAccountPrivilege", backref="account_privilege", uselist=False
    )
    basic_info = db.relationship(
        "BiteExerBasicInfo", backref="_basic_info", uselist=False
    )
    location = db.relationship(
        "BiteExerLocation", backref="_location", uselist=False
    )
    account_security = db.relationship(
        "BiteExerAccountSecurity", backref="_account_security", uselist=False
    )
    wallet = db.relationship("BiteExerWallet", backref="_wallet", uselist=False)
    vendor = db.relationship("BitexVendor", backref="_vendor", uselist=False)
    credit_card = db.relationship(
        "BiteExerCreditCard", backref="_credit_card", lazy=True
    )
    order_history = db.relationship(
        "BiteExerOrderHistory", backref="_order_history", lazy=True
    )
    driver = db.relationship("BitexDriver", backref="_driver", uselist=False)
    expenditure = db.relationship(
        "BiteExpressExpenditure", backref="allocated_expenditure", lazy=True
    )
    transaction_history = db.relationship(
        "BiteExerTransactionHistory", backref="_transaction_history", lazy=True
    )


"""
BiteExer account privilege table this give privileges to BiteExer, giving them access right on BiteExpress.

role: BiteExer, Admin
title: "BitexUser", "BitexVendor", "BitexDriver", "BitexAgent"

Where the permission column consist of list of admin pages they can access and the title column takes the title of the job
assign to them or department they belong too.
"""
class BiteExerAccountPrivilege(db.Model):
    __table_args__ = {'mysql_engine': "InnoDB"}
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    status = db.Column(db.String(100), default="Active", nullable=False)
    bite_id = db.Column(
        db.String(15), db.ForeignKey("bite_exer.bite_id"), unique=True,
        nullable=False,
    )
    role = db.Column(db.String(8), default="BiteExer", nullable=False)
    title = db.Column(db.String(300))
    permission = db.Column(
        MutableList.as_mutable(PickleType), nullable=False, default=[]
    )
    date_assigned = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    date_updated = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    
    
    def add(self):
        db.session.add(self)
        db.session.commit()


    def update_status(self, status):
        self.status = status
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def update_permission(self, permission):
        self.permission.append(permission)
        
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
    
    
    def update_role(self, role):
        self.role = role
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
    
    
    def update_title(self, title):
        self.title = title
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()


class BiteExerBasicInfo(db.Model):
    __table_args__ = {'mysql_engine': "InnoDB"}
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    bite_id = db.Column(
        db.String(15), db.ForeignKey("bite_exer.bite_id"), unique=True,
        nullable=False,
    )
    username = db.Column(db.String(100), unique=True)
    profile_picture = db.Column(
        db.String(20), default="default_avater.png", nullable=False
    )
    gender = db.Column(db.String(6))
    birthday = db.Column(db.Date)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    email_address = db.Column(db.String(500), unique=True, nullable=False)
    date_updated = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    
    
    def add(self):
        db.session.add(self)
        db.session.commit()
        
        
    def update(
        self, username, profile_picture, gender, birthday, phone_number, #######################
        email_address,
    ):
        self.username = username
        self.profile_picture = profile_picture
        self.gender = gender
        self.birthday = birthday
        self.phone_number = phone_number
        self.email_address = email_address
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
    
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()


class BiteExerLocation(db.Model):
    __table_args__ = {'mysql_engine': "InnoDB"}
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    bite_id = db.Column(
        db.String(15), db.ForeignKey("bite_exer.bite_id"), unique=True,
        nullable=False,
    )
    country = db.Column(db.String(100), nullable=False)
    state_region = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    neighbourhood = db.Column(db.String(200), nullable=False)
    post_code = db.Column(db.Integer, nullable=False)
    date_added = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    date_updated = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    
    
    def add(self):
        db.session.add(self)
        db.session.commit()
        
        
    def update(self, country, state_region, city, neighbourhood, post_code):
        self.country = country
        self.state_region = state_region
        self.city = city
        self.neighbourhood = neighbourhood
        self.post_code = post_code
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()


class BiteExerAccountSecurity(db.Model):
    __table_args__ = {'mysql_engine': "InnoDB"}
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    bite_id = db.Column(
        db.String(15), db.ForeignKey("bite_exer.bite_id"), unique=True,
        nullable=False,
    )
    password_hash = db.Column(db.String(60), unique=True, nullable=False)
    date_set = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_updated = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    
    
    def add(self):
        db.session.add(self)
        db.session.commit()
        
        
    def update(self, password_hash):
        self.password_hash = password_hash
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()


"""
account status: Not Verified, Verified
"""
class BitexVendor(db.Model):
    __table_args__ = {'mysql_engine': "InnoDB"}
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    account_status = db.Column(
        db.String(12), default="Not Verified", nullable=False
    )
    bite_id = db.Column(
        db.String(15), db.ForeignKey("bite_exer.bite_id"), unique=True,
        nullable=False,
    )
    kitchen_name = db.Column(db.String(200), unique=True)
    website_url = db.Column(db.Text)  # unique
    logo = db.Column(
        db.String(23), default="default_logo_avater.png", nullable=False
    )
    bio = db.Column(db.String(200))
    opening_hour = db.Column(db.Time)
    closing_hour = db.Column(db.Time)
    rating = db.Column(
        db.Numeric(precision=65, scale=1, decimal_return_scale=1),
        nullable=False, default=0.0
    )
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    date_updated = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    
    def update(self, kitchen_name, website_url, logo, bio):
        self.kitchen_name = kitchen_name
        self.website_url = website_url
        self.logo = logo
        self.bio = bio
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def update_account_status(self, account_status):
        self.account_status = account_status
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def update_rating(self, rating):
        self.rating = rating
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def update_business_hour(self, opening_hour, closing_hour):
        self.opening_hour = opening_hour
        self.closing_hour = closing_hour
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    
    # relationships logic
    menu = db.relationship(
        "BitexVendorMenu", backref="_menu", lazy=True
    )


class BiteExerCreditCard(db.Model):
    __table_args__ = {'mysql_engine': "InnoDB"}
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    bite_id = db.Column(
        db.String(15), db.ForeignKey("bite_exer.bite_id"), nullable=False
    )
    bank_name = db.Column(db.String(100))
    account_name = db.Column(db.String(100))
    account_number = db.Column(db.Integer, unique=True)
    card_name = db.Column(db.String(100))
    card_number = db.Column(db.Integer, unique=True)
    card_expiration_date = db.Column(db.Date)
    cvv = db.Column(db.Integer, unique=True)
    date_added = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    date_updated = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    
    def update(
        self, bank_name, account_name, account_number, card_name, card_number,
        card_expiration_date, cvv
    ):
        self.bank_name = bank_name
        self.account_name = account_name
        self.account_number = account_number
        self.card_name = card_name
        self.card_number = card_number
        self.card_expiration_date = card_expiration_date
        self.cvv = cvv
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()


class BiteExerWallet(db.Model):
    __table_args__ = {'mysql_engine': "InnoDB"}
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    bite_id = db.Column(
        db.String(15), db.ForeignKey("bite_exer.bite_id"), nullable=False,
        unique=True,
    )
    wallet_balance = db.Column(
        db.Numeric(precision=65, scale=2, decimal_return_scale=2),
        nullable=False, default=0.00
    )
    deposit = db.Column(
        db.Numeric(precision=65, scale=2, decimal_return_scale=2),
        nullable=False, default=0.00
    )
    referral = db.Column(db.Integer, nullable=False, default=0)
    total_earning = db.Column(
        db.Numeric(precision=65, scale=2, decimal_return_scale=2),
        nullable=False, default=0.00
    )
    fund_transfer = db.Column(
        db.Numeric(precision=65, scale=2, decimal_return_scale=2),
        nullable=False, default=0.00
    )
    pending_payout = db.Column(
        db.Numeric(precision=65, scale=2, decimal_return_scale=2),
        nullable=False, default=0.00
    )
    payout = db.Column(
        db.Numeric(precision=65, scale=2, decimal_return_scale=2),
        nullable=False, default=0.00
    )
    date_updated = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    
    
    def add(self):
        db.session.add(self)
        db.session.commit()
        
        
    def credit_wallet_balance(self, credit):
        self.wallet_balance += credit
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
    
        
    def debit_wallet_balance(self, debit):
        self.wallet_balance -= debit
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def update_deposit(self, deposit):
        self.deposit = deposit
        self.wallet_balance += deposit
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
    
    def update_referral(self, referral):
        self.referral = referral
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def update_total_earning(self, total_earning):
        self.total_earning = total_earning
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def update_fund_transfer(self, fund_transfer):
        self.fund_transfer = fund_transfer
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def update_pending_payout(self, pending_payout):
        self.pending_payout = pending_payout
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def update_payout(self, payout):
        self.payout = payout
        self.pending_payout -= payout
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()


"""
status: Available, Not Available, Deleted

Only bitem without order history can be deleted permanently from this table, while bitem with order history, if a delete action is
being triggered on it, only the status column will be updated to deleted, which means it will not be visible on search results
or for the BitexVendor. only BitexUser that order the bitem will be able to view the menu.
"""
class BitexVendorMenu(db.Model):
    __table_args__ = {'mysql_engine': "InnoDB"}
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    status = db.Column(db.String(13), default="Available", nullable=False)
    kitchen_name = db.Column(
        db.String(200), db.ForeignKey("bitex_vendor.kitchen_name"),
        nullable=False,
    )
    bitem_id = db.Column(db.String(14), unique=True, nullable=False)
    bitem = db.Column(db.String(20), nullable=False)
    image = db.Column(
        db.String(24), default="default_bitem_avater.png", nullable=False
    )
    description = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(
        db.Numeric(precision=65, scale=2, decimal_return_scale=2),
        nullable=False, default=0.00
    )
    quantity = db.Column(db.Integer, nullable=False, default=1)
    offer = db.Column(db.String(20))
    average_prep_time = db.Column(db.Time, nullable=False)
    liked_by = db.Column(
        MutableList.as_mutable(PickleType), nullable=False, default=[]
    )
    viewed_by = db.Column(
        MutableList.as_mutable(PickleType), nullable=False, default=[]
    )
    date_added = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    date_updated = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    
    def update(
        self, status, bitem, image, description, category, price,
        average_prep_time,
    ):
        self.status = status
        self.bitem = bitem
        self.image = image
        self.description = description
        self.category = category
        self.price = price
        self.average_prep_time = average_prep_time
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
    
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()


"""
status: Cancled, Accepted, Pending

If a BitexVendor refuse to accept an order within a certain time period, the order will be canceled automatically
"""
class BiteExerOrderHistory(db.Model):
    __table_args__ = {'mysql_engine': "InnoDB"}
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    status = db.Column(db.String(8), default="Pending", nullable=False)
    bite_id = db.Column(
        db.String(15), db.ForeignKey("bite_exer.bite_id"), nullable=False
    )
    bitem_id = db.Column(db.String(20), nullable=False)
    price = db.Column(
        db.Numeric(precision=65, scale=2, decimal_return_scale=2),
        nullable=False, default=0.00
    )
    quantity = db.Column(db.Integer, nullable=False, default=0)
    prep_time = db.Column(db.Time)
    destination = db.Column(db.String(200), nullable=False)
    driver = db.Column(db.String(15))
    delivery_time = db.Column(db.Time)
    delivered = db.Column(db.Boolean, nullable=False, default=False)
    received = db.Column(db.Boolean, nullable=False, default=False)
    returned = db.Column(db.Boolean, nullable=False, default=False)
    date_ordered = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    date_updated = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    
    
    def add(self):
        db.session.add(self)
        db.session.commit()
        
        
    def update_status(self, status):
        self.status = status
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
    
    
    def update_prep_time(self, prep_time):
        self.prep_time = prep_time
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def update_driver(self, driver, delivery_time):
        self.driver = driver
        self.delivery_time = delivery_time
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def update_delivered(self, delivered):
        self.delivered = delivered
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def update_received(self, received):
        self.received = received
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
            
            
    def update_returned(self, returned):
        self.returned = returned
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()


"""
active status: Online, Offline

account status: Not Verified, Verified
"""
class BitexDriver(db.Model):
    __table_args__ = {'mysql_engine': "InnoDB"}
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    active_status = db.Column(
        db.String(7), default="Offline", nullable=False
    )
    account_status = db.Column(
        db.String(12), default="Not Verified", nullable=False
    )
    bite_id = db.Column(
        db.String(15), db.ForeignKey("bite_exer.bite_id"), unique=True,
        nullable=False,
    )
    photo = db.Column(db.String(20))
    rating = db.Column(
        db.Numeric(precision=65, scale=1, decimal_return_scale=1),
        nullable=False, default=0.0
    )
    national_identification_number = db.Column(db.Integer)  
    driver_license = db.Column(db.String(100))
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    date_updated = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    
    
    def add(self):
        db.session.add(self)
        db.session.commit()
        
        
    def update_active_status(self, active_status):
        self.active_status = active_status
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def update_account_status(self, account_status):
        self.account_status = account_status
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def update_rating(self, rating):
        self.rating = rating
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def update(self, photo, national_identification_number, driver_license):
        self.photo = photo
        self.national_identification_number = national_identification_number
        self.driver_license = driver_license
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    
    # relationships logic
    vehicle = db.relationship(
        "BitexDriverVehicle", backref="_vehicle", lazy=True
    )


"""
status: Active, Inactive

vehicle type: Car, Motorcycle, Tricycle, Bicycle

verification status: Approved, Pending, Not Approved
"""
class BitexDriverVehicle(db.Model):
    __table_args__ = {'mysql_engine': "InnoDB"}
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    status = db.Column(
        db.String(8), default="Inactive", nullable=False
    )
    bite_id = db.Column(
        db.String(15), db.ForeignKey("bitex_driver.bite_id"), nullable=False
    )
    type = db.Column(db.String(100), nullable=False)
    manufacturer = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    license_number_plate = db.Column(db.String(20))
    color = db.Column(db.String(20), nullable=False)
    photo = db.Column(
        MutableList.as_mutable(PickleType), nullable=False, default=[]
    )
    license_certificate = db.Column(
        MutableList.as_mutable(PickleType), nullable=False, default=[]
    )
    verification_status = db.Column(
        db.String(12), default="Pending", nullable=False
    )
    date_added = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    date_updated = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    
    
    def add(self):
        db.session.add(self)
        db.session.commit()
        
        
    def update_status(self, status):
        self.status = status
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def update(self, license_number_plate, color, photo, license_certificate):
        self.status = "Inactive"
        self.verification_status = "Pending"
        self.license_number_plate = license_number_plate
        self.color = color
        self.photo = photo
        self.license_certificate = license_certificate
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def update_verification_status(self, verification_status):
        self.verification_status = verification_status
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()


class BiteExpressExpenditure(db.Model):
    __table_args__ = {'mysql_engine': "InnoDB"}
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    bite_id = db.Column(
        db.String(15), db.ForeignKey("bite_exer.bite_id"), nullable=False
    )    
    category = db.Column(db.String(100), nullable=False, unique=True)
    creadit = db.Column(
        db.Numeric(precision=65, scale=2, decimal_return_scale=2),
        nullable=False, default=0.00
    )
    debit = db.Column(
        db.Numeric(precision=65, scale=2, decimal_return_scale=2),
        nullable=False, default=0.00
    )
    share = db.Column(
        db.Numeric(precision=65, scale=2, decimal_return_scale=2),
        nullable=False, default=0.00
    )
    date_allocated = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    date_updated = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    
    
    def add(self):
        db.session.add(self)
        db.session.commit()
        
        
    def update(self, category, share):
        self.category = category
        self.share = share
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
    
    def update_creadit(self, credit):
        self.creadit += credit
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def update_debit(self, debit):
        self.debit += debit
        self.creadit -= debit
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    
""""
type: Creadit, Debit

staus: Pending, Confirmed
"""
class BiteExerTransactionHistory(db.Model):
    __table_args__ = {'mysql_engine': "InnoDB"}
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    bite_id = db.Column(
        db.String(15), db.ForeignKey("bite_exer.bite_id"), nullable=False
    )
    type = db.Column(db.String(7), nullable=False)
    amount = db.Column(
        db.Numeric(precision=65, scale=2, decimal_return_scale=2), 
        nullable=False, default=0.00
    )
    hash = db.Column(db.String(18), nullable=False, unique=True)
    status = db.Column(db.String(9))  # backup (status = db.Column(db.String(9), nullable=False, default="Pending"))
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )    
    confirmed_by = db.Column(db.String(15))
    date_confirmed = db.Column(db.DateTime)
    date_updated = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    
    
    def add(self):
        db.session.add(self)
        db.session.commit()
        
        
    def update(self, confirmed_by):
        self.status = "Confirmed"
        self.confirmed_by = confirmed_by
        self.date_confirmed = datetime.utcnow()
        self.date_updated = datetime.utcnow()
        
        db.session.commit()
        
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()


# circular import modules
# from .utils import *
