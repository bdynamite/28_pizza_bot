import re
import json

from app import db


class Pizza(db.Model):
    pizza_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(500))
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    price = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)


def create_db():
    db.create_all()
    engine = db.get_engine()
    db.Index('idx_title', Pizza.title).create(engine)


def get_catalog_json():
    with open('catalog.json', 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def add_initial_records():
    catalog = get_catalog_json()
    for pizza_type in catalog:
        for pizza in pizza_type['choices']:
            height, weight = re.findall(r'\d+', pizza['title'])
            new_record = Pizza(title=pizza_type['title'],
                               description=pizza_type['description'],
                               height=int(height),
                               weight=int(weight),
                               price=pizza['price'])
            db.session.add(new_record)
            db.session.commit()


if __name__ == '__main__':
    create_db()
    add_initial_records()
