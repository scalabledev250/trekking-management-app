from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from enum import Enum
from datetime import datetime, UTC
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Role(Enum):
    admin = "Admin"
    staff = "Staff"
    trekker = "Trekker"

class Diff(Enum):
    easy = "Easy"
    moderate = "Moderate"
    hard = "Hard"

class UserStatus(Enum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"
    blacklisted = "Blacklisted"

class TrekStatus(Enum):
    pending = "Pending"
    approved = "Approved"
    open = "Open"
    closed = "Closed"
    completed = "Completed"

class BookStatus(Enum):
    open = "Open"
    booked = "Booked"
    cancelled = "Cancelled"
    completed = "Completed"

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(Role), nullable=False)
    staff = db.relationship('Staff', back_populates='user', uselist=False)
    trekker = db.relationship('Trekker', back_populates='user', uselist=False)
    def set_hash_password(self, pwd):
        self.password = generate_password_hash(pwd)
    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

class Staff(db.Model):
    __tablename__ = "staff"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    status = db.Column(db.Enum(UserStatus), default=UserStatus.pending)
    is_deleted = db.Column(db.Boolean, default=False)
    user = db.relationship('User', back_populates='staff')
    treks = db.relationship("Trek", back_populates="staff")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=False)

class Trekker(db.Model):
    __tablename__ = "trekker"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    status = db.Column(db.Enum(UserStatus), default=UserStatus.approved)
    is_deleted = db.Column(db.Boolean, default=False)
    user = db.relationship('User', back_populates='trekker')
    bookings = db.relationship("Booking", back_populates="trekker")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=False)

class Trek(db.Model):
    __tablename__ = "treks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    completion_date = db.Column(db.Date, nullable=True)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(2048), nullable=True)
    difficulty = db.Column(db.Enum(Diff))
    status = db.Column(db.Enum(TrekStatus), nullable=False, default=TrekStatus.pending)
    is_deleted = db.Column(db.Boolean, default=False)
    staff = db.relationship("Staff", back_populates="treks")
    bookings = db.relationship("Booking", back_populates="treks")
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.id"), nullable=False)

class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.DateTime(timezone=True), default=lambda:datetime.now(UTC))
    status = db.Column(db.Enum(BookStatus), default=BookStatus.open)
    participants = db.Column(db.Integer, default=0, nullable=False)
    treks = db.relationship("Trek", back_populates="bookings")
    trekker = db.relationship("Trekker", back_populates="bookings")
    trekker_id = db.Column(db.Integer, db.ForeignKey("trekker.id"), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey("treks.id"), nullable=False)
