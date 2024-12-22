from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.admin.models import  ContactMessage
from app.main.forms import InquiryForm, ContactForm
import math
from functools import wraps
from app import db
from flask import current_app
from flask_login import login_required, login_user, logout_user, current_user
# Create a blueprint for main routes
main_bp = Blueprint('main', __name__)


def login_required_with_message(view):
    """Custom decorator that requires user login with a flash message."""
    @wraps(view)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this feature.', 'warning')
            return redirect(url_for('auth.login')) 
        return view(*args, **kwargs)
    return decorated_view


# ---------------------------------------
# Home Route
# ---------------------------------------


@main_bp.route('/')
def home():
    chunked_partners = chunk_partners(partners_data)
    # Add index to each chunk of partners
    indexed_partners = [(index, chunk) for index, chunk in enumerate(chunked_partners)]
    return render_template('main/home.html', clients_data=clients_data, partners_data=indexed_partners, testimonials_data =testimonials_data )


# ---------------------------------------
# Error Handling
# ---------------------------------------

@main_bp.errorhandler(404)
def not_found(error):
    return render_template('main/404.html'), 404

@main_bp.errorhandler(500)
def internal_error(error):
    current_app.logger.error(f'Server Error: {error}, route: {request.url}')
    return render_template('main/500.html'), 500


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Save contact message to the database
        contact_message = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(contact_message)
        db.session.commit()
        
        # Flash message for success
        flash('Your message has been sent. We will get back to you shortly.', 'success')
        return redirect(url_for('main.contact'))
    
    return render_template('main/contact.html', title='Contact Us', form=form)

@main_bp.route('/privacy-policy')
def privacy_policy():
    return render_template('main/privacy_policies.html')


@main_bp.route('/about_us')
def about_us():
    return render_template('main/about_us.html')


# dictionary for services
services_data = {
    'fleet_management': {
        'id': 'fleet_management',
        'title': 'Fleet Management Solutions',
        'description': 'Advanced GPS tracking, fuel monitoring, and theft detection solutions to optimize your fleet operations.',
        'image_url': 'https://via.placeholder.com/400x300',
        'detailed_description': 'Detailed information about fleet management solutions...',
        'more_info': 'Fleet management can help you save costs, increase efficiency, and improve the safety of your operations.'
    },
    'security_systems': {
        'id': 'security_systems',
        'title': 'Security Systems',
        'description': 'CCTV cameras, access control, and video surveillance solutions to enhance your security infrastructure.',
        'image_url': 'https://via.placeholder.com/400x300',
        'detailed_description': 'Detailed information about security systems...',
        'more_info': 'Security systems provide round-the-clock surveillance and improve the safety of your assets.'
    },
    'software_development': {
        'id': 'software_development',
        'title': 'Software Development',
        'description': 'Custom software solutions tailored to your business needs, from web development to mobile apps.',
        'image_url': 'https://via.placeholder.com/400x300',
        'detailed_description': 'Detailed information about software development...',
        'more_info': 'Our software development services will help you create custom applications that fit your specific business requirements.'
    },
    'it_support': {
        'id': 'it_support',
        'title': 'IT Support and Consultation',
        'description': 'Comprehensive IT support services for businesses to improve efficiency and manage their technological infrastructure.',
        'image_url': 'https://via.placeholder.com/400x300',
        'detailed_description': 'Detailed information about IT support...',
        'more_info': 'Get the best IT support services that will help you solve technical issues, enhance your infrastructure, and improve performance.'
    },
    'cloud_services': {
        'id': 'cloud_services',
        'title': 'Cloud Solutions',
        'description': 'Seamless cloud services to help businesses scale, manage data, and enhance security on the cloud.',
        'image_url': 'https://via.placeholder.com/400x300',
        'detailed_description': 'Detailed information about cloud services...',
        'more_info': 'Our cloud services help you scale your business, store data securely, and ensure high availability of your systems.'
    },
    'data_analytics': {
        'id': 'data_analytics',
        'title': 'Data Analytics',
        'description': 'Advanced data analysis tools to help businesses make data-driven decisions and improve performance.',
        'image_url': 'https://via.placeholder.com/400x300',
        'detailed_description': 'Detailed information about data analytics...',
        'more_info': 'We offer powerful data analytics tools that help you understand your business data better and make informed decisions.'
    }
}


@main_bp.route('/services')
def services():
    # Pass the services data to the template
    return render_template('main/services.html', services=services_data)

@main_bp.route('/service-details/<service_id>')
def service_details(service_id):
    service = services_data.get(service_id)
    if service is None:
        return render_template('main/404.html'), 404
    return render_template('main/service_detail.html', service=service)



# dictionary for clients
clients_data = {
    'client1': {
        'name': 'Davis Express',
        'description': '',
        'image_url': 'clients/davis.jpeg',
    },
    'client2': {
        'name': 'brookfox',
        'description': '',
        'image_url': 'clients/brookfox.jpeg',
    },
    'client3': {
        'name': 'PowerGas',
        'description': '',
        'image_url': 'clients/powergas.jpeg',
    },
    
}



partners_data = {
    'partner1': {
        'name': 'Partner 1',
        'logo_url': 'partners/multichoice.jpeg',
    },
    'partner2': {
        'name': 'Partner 2',
        'logo_url': 'partners/melta.jpeg',
    },
    'partner3': {
        'name': 'Partner 3',
        'logo_url': 'partners/3scort.jpeg',
    },
    'partner4': {
        'name': 'Partner 4',
        'logo_url': 'partners/ruptela.jpeg',
    },
    'partner5': {
        'name': 'Partner 5',
        'logo_url': 'partners/eljunga.jpeg',
    },
    'partner6': {
        'name': 'Partner 6',
        'logo_url': 'partners/telktonika.jpeg',
    },
    'partner7': {
        'name': 'Partner 7',
        'logo_url': 'partners/hkvision.jpeg',
    },
    'partner8': {
        'name': 'Partner 8',
        'logo_url': 'partners/wialon.jpeg',
    },
}

# Function to split dictionary into chunks of 4
def chunk_partners(partners, chunk_size=4):
    partners_items = list(partners.items())
    return [partners_items[i:i + chunk_size] for i in range(0, len(partners_items), chunk_size)]


testimonials_data = [
    {
        "quote": "Kedatrack transformed our fleet management. Highly recommend!",
        "name": "Japheth Maina",
        "position": "CEO",
        "icon_color": "text-primary",
    },
    {
        "quote": "Exceptional service and innovative solutions.",
        "name": "Antony Kilonzi",
        "position": "Logistics Manager",
        "icon_color": "text-success",
    },
    {
        "quote": "Reliable, efficient, and user-friendly.",
        "name": "sukhaima Asha",
        "position": "Operations Head",
        "icon_color": "text-warning",
    },
]

