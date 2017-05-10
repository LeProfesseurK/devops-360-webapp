#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict

from random import sample
from sqlalchemy import ForeignKey, func, or_, desc

from app import db

class Beer(db.Model):
    __tablename__ = 'beer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    type = db.Column(db.String(255))
    abv = db.Column(db.Numeric(2,1))
    brewery = db.Column(db.String(255))

    def __init__(self, beer_name, beer_type, beer_abv, beer_brewery):
        self.name = beer_name
        self.type = beer_type
        self.abv = beer_abv
        self.brewery = beer_brewery

    def __repr__(self):
        return '<Beer %r>' % self.name

    @staticmethod
    def list_beers():
        beers = {}
        for b in Beer.query.all():
            beers[b.id] = dict(
                name = b.name,
                type = b.type,
                abv = b.abv,
                brewery = b.brewery,
            )
        return beers

    @staticmethod
    def get_two_beers(battle_interval=None):
        beers = {}

        beer_max_id = db.session.query(func.max(Beer.id)).first()[0]

        beer_ids = []
        max_id = None

        if battle_interval is not None:
            # Generate two different random ids within the range of beer ids
            beer_ids = sample(range(
                max(1, battle_interval[0]),
                min(beer_max_id, battle_interval[1])), 2)

        records = Beer.query.filter(or_(Beer.id == beer_ids[0], Beer.id == beer_ids[1]))

        for b in records:
            beers[b.id] = dict(
                name = b.name,
                type = b.type,
                abv = b.abv,
                brewery = b.brewery,
            )
        return beers

class Battle(db.Model):
    __tablename__ = 'battle'

    battle_id = db.Column(db.Integer, primary_key=True)
    beer_win_rate = db.Column(db.Integer)

    beer_win_id = db.Column(db.Integer, ForeignKey('beer.id'))
    beer_lose_id = db.Column(db.Integer, ForeignKey('beer.id'))

    beer_win = db.relationship('Beer', foreign_keys=[beer_win_id],
        lazy='select')

    beer_lose = db.relationship('Beer', foreign_keys=[beer_lose_id],
        lazy='select')

    def __init__(self, beer_win_id, beer_lose_id, beer_win_rate=1, battle_id=None):
        self.battle_id = battle_id
        self.beer_win_id = beer_win_id
        self.beer_lose_id = beer_lose_id
        self.beer_win_rate = beer_win_rate

    def __repr__(self):
        return '<Battle %r, %r , %r , %r, %r, %r>' % (self.battle_id,
            self.beer_win_id,
            self.beer_lose_id,
            self.beer_win,
            self.beer_lose,
            self.beer_win_rate)

    @staticmethod
    def list_top_beers():
        beers = OrderedDict()

        records = db.session.query(Battle, func.sum(Battle.beer_win_rate).label('rate')).group_by(Battle.beer_win_id).order_by(desc('rate')).all()
        for r in records:
            battle = r[0]

            beers[battle.battle_id] = dict(
                beer_win = battle.beer_win,
                rate = r[1]
            )

        return beers

    def save(self):
        db.session.add(self)
        db.session.commit()
