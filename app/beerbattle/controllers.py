#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import flask dependencies
from flask import Blueprint, render_template, current_app as app

import json

# Import App objects
from app.beerbattle.models import Beer

# Define a blueprint
beerbattle = Blueprint('beerbattle', __name__, url_prefix='/')

################################################################################
# beerbattle blueprint functions
################################################################################

@beerbattle.route('home', methods=['GET'])
def display():
    app.logger.info('Hit on /home endpoint')
    return render_template('home.html')

@beerbattle.route('catalog', methods=['GET', 'POST'])
def catalog():
    app.logger.info('Hit on /catalog endpoint')
    return render_template('catalog.html', beers=Beer.list_beers())
