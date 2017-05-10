#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import flask dependencies
from flask import Blueprint, request, current_app as app

# Define a blueprint
heartbeat = Blueprint('heatbeat', __name__, url_prefix='/heartbeat')

# http://<hostname>/heartbeat endpoint
@heartbeat.route('', methods=['GET'])
def check_heartbeat():
    app.logger.debug("HEARTBEAT")
    return "The Flask WebApp healthy"
