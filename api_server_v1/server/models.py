from sqlalchemy import Column, Integer, String, Float, PrimaryKeyConstraint

from db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=False)
    person = Column(String(50), nullable=False)
    current_age = Column(Integer, nullable=False)
    retirement_age = Column(Integer, nullable=False)
    birth_year = Column(Integer, nullable=False)
    birth_month = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    address = Column(String(100), nullable=False)
    apartment = Column(String(50), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)
    zipcode = Column(String(20), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    per_capita_income_1_zipcode = Column(String(100), nullable=False)
    yearly_income_1_person = Column(String(100), nullable=False)
    total_debt = Column(String(100), nullable=False)
    fico_score = Column(Integer, nullable=False)
    num_credit_cards = Column(Integer, nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class Card(Base):
    __tablename__ = "cards"

    user = Column(Integer, nullable=False)
    card_index = Column(Integer, nullable=False)
    card_brand = Column(String(50), nullable=False)
    card_type = Column(String(50), nullable=False)
    card_number = Column(String(50), nullable=False)
    expires = Column(String(10), nullable=False)
    cvv = Column(String(10), nullable=False)
    has_chip = Column(String(100), nullable=False)
    cards_issued = Column(Integer, nullable=False)
    credit_limit = Column(String(50), nullable=False)
    acct_open_date = Column(String(100), nullable=False)
    year_pin_last_changed = Column(String(10), nullable=False)
    card_on_dark_web = Column(String(10), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("user", "card_index", name="pk_user_card_index"),
    )

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)