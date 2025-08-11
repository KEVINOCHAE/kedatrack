from flask import Blueprint, render_template

services_bp = Blueprint('services', __name__, url_prefix='/api/services')

# Dictionary holding the services data
services_data = {
'software_development': {
        'id': 'software_development',
        'title': 'Software Development',
        'description': 'Custom software solutions tailored to your business needs, from web development to mobile apps.',
        'image_url': 'https://via.placeholder.com/400x300',
    },
    'fleet_management': {
        'id': 'fleet_management',
        'title': 'Fleet Management Solutions',
        'description': 'Advanced GPS tracking, fuel monitoring, and theft detection solutions to optimize your fleet operations.',
        'image_url': 'https://via.placeholder.com/400x300',
    },
    'security_systems': {
        'id': 'security_systems',
        'title': 'Security Systems',
        'description': 'CCTV cameras, access control, and video surveillance solutions to enhance your security infrastructure.',
        'image_url': 'https://via.placeholder.com/400x300',
    },
    'it_support': {
        'id': 'it_support',
        'title': 'IT Support and Consultation',
        'description': 'Seamless IT support services for businesses to improve efficiency and manage their technological infrastructure.',
        'image_url': 'https://via.placeholder.com/400x300',
    },
    'cloud_services': {
        'id': 'cloud_services',
        'title': 'Cloud Solutions',
        'description': 'Seamless cloud services to help businesses scale, manage data, and enhance security on the cloud.',
        'image_url': 'https://via.placeholder.com/400x300',
    },
    'data_analytics': {
        'id': 'data_analytics',
        'title': 'Data Analytics',
        'description': 'Advanced data analysis tools to help businesses make data-driven decisions and improve performance.',
        'image_url': 'https://via.placeholder.com/400x300',
    }
}

@services_bp.route('/')
def services_page():
    return render_template('services.html', services=services_data)