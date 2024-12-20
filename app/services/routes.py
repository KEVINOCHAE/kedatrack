# app/services/routes.py
from flask import Blueprint, request, jsonify, abort, render_template, url_for
from app import db 
import os
import uuid


services_bp = Blueprint('services', __name__, url_prefix='/api/services')

""