#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict

from random import sample

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
