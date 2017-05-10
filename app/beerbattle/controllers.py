#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import flask dependencies
from flask import Blueprint, render_template, request, jsonify, current_app as app

import json

# Import App objects
from app.beerbattle.models import Beer, Battle

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

@beerbattle.route('battle', methods=['GET', 'POST'])
def battle():
    app.logger.info('Hit on /battle endpoint')

    if request.method == 'POST':
        json = request.get_json()

        # Convert a list of dict name= value= into a dict
        json_obj = {}
        model = None

        for j in json:
            json_obj[j['name']] = j['value']

        if 'beer_id_1_win' in json_obj and json_obj['beer_id_1_win'] == 'on':
            model = Battle(json_obj['beer_id_1'], json_obj['beer_id_2'])

        elif 'beer_id_2_win' in json_obj and json_obj['beer_id_2_win'] == 'on':
            model = Battle(json_obj['beer_id_2'], json_obj['beer_id_1'])

        if model:
            model.save()
            return jsonify(result='Battle saved!')
        else:
            return jsonify(result='Something went wrong!')

    else:
        battle_interval = app.config['BEER_BATTLE_ID_INTERVAL'] if 'BEER_BATTLE_ID_INTERVAL' in app.config else None
        beers_for_battle = Beer.get_two_beers(battle_interval=battle_interval)

        return render_template('battles.html', beers=beers_for_battle)

@beerbattle.route('top-beers', methods=['GET'])
def top():
    app.logger.info('Hit on /top-beers endpoint')
    return render_template('top-beers.html', beers=Battle.list_top_beers())
