from flask import render_template, redirect, url_for, flash, request,Blueprint 
from app import db
from app.admin.models import User, Role
from werkzeug.security import generate_password_hash
from functools import wraps


admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard', methods=['GET'])
def dashboard():
    
    return render_template('admin/dashboard.html')

