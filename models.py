import re
import json

from app import db


class Pizza(db.Model):
    pizza_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(500))
    choices = db.relationship('Choice', backref='pizza', lazy='dynamic')
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return self.title


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.pizza_id'))
    price = db.Column(db.Integer)

    def __repr__(self):
        return '{}см, {}гр, {}р'.format(self.height, self.weight, self.price)


def create_db():
    engine = db.get_engine()
    db.create_all()
    db.Index('idx_title', Pizza.title).create(engine)


def get_catalog_json():
    with open('catalog.json', 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def add_initial_records():
    catalog = get_catalog_json()
    for pizza_type in catalog:
        pizza_record = Pizza(title=pizza_type['title'], description=pizza_type['description'])
        db.session.add(pizza_record)
        db.session.commit()
        for pizza in pizza_type['choices']:
            height, weight = re.findall(r'\d+', pizza['title'])
            new_record = Choice(
                height=int(height),
                weight=int(weight),
                pizza_id=pizza_record.pizza_id,
                price=pizza['price']
            )
            db.session.add(new_record)
            db.session.commit()


if __name__ == '__main__':
    create_db()
    add_initial_records()
