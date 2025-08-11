from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.admin.models import  ContactMessage, ServiceRequest, NewsletterSubscriber
from app.main.forms import  ContactForm, ServiceRequestForm, NewsletterForm
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

@main_bp.route('/', methods=['GET', 'POST'])
def home():
    # Chunk partners data (assuming chunk_partners is defined properly)
    chunked_partners = chunk_partners(partners_data)

    # Create the newsletter form instance
    form = NewsletterForm()

    # Add index to each chunk of partners
    indexed_partners = [(index, chunk) for index, chunk in enumerate(chunked_partners)]

    # Process the newsletter subscription form
    if form.validate_on_submit():
        email = form.email.data

        # Check if the email is already in the database
        if NewsletterSubscriber.query.filter_by(email=email).first():
            flash("You are already subscribed!", 'warning')
            return redirect(url_for('main.home'))  # Redirect to home page

        # Add new subscriber to the database
        new_subscriber = NewsletterSubscriber(email=email)
        try:
            db.session.add(new_subscriber)
            db.session.commit()
            flash("Subscription successful! Welcome to the loop.", 'success')
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while subscribing. Please try again.", 'danger')

        return redirect(url_for('main.home'))  # Redirect to home page

    # Render the home page template with the necessary data
    return render_template(
        'main/home.html',
        clients_data=clients_data,
        partners_data=indexed_partners,
        testimonials_data=testimonials_data,
        form=form
    )

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

# Full team list
team = [
    {
        "name": "KEVIN OCHAE",
        "role": "Founder-Chief Technology Officer (CTO)",
        "image_url": "static/team/kevin.jpeg",
        "social_links": {
            "linkedin": "https://www.linkedin.com/in/kevin-ochae-909b64190",
            "X": "https://x.com/KOchae?t=A7j37WOwP20TkL_oUK4skA&s=09",
            "github": "https://github.com/kevinochae"
        }
    },
    {
        "name": "DAVID OCHAYE",
        "role": "Co-Founder - Chief Operating Officer (COO)",
        "image_url": "static/team/dave.jpeg",
        "social_links": {
            "linkedin": "#",
            "X": "#",
            "github": "#"
        }
    },
    {
        "name": "HENRY AFUYA",
        "role": "Lead Developer",
        "image_url": "static/team/henry1.jpeg",
        "social_links": {
            "linkedin": "https://www.linkedin.com/in/henry-bulimo-100024229",
            "X": "https://x.com/JSync35300?t=I_VT9O-QlDbLJMX71WAoZA&s=09",
            "github": "https://github.com/afuyah"
        }
    }
]


# About Us route
@main_bp.route('/about_us')
def about_us():
    # Pass only the first three team members to the template
    about_page_team = team[:3]
    
    return render_template('main/about_us.html', team=about_page_team)

# dictionary for services
services_data = {
    'fleet_management': {
        'id': 'fleet_management',
        'title': 'Advanced Fleet Management/Assets Tracking Solutions',
        'description': (
            'Kedatrack GPS is a device-agnostic vehicle tracking solution that provides real-time and historical '
            'views of vehicle movement and usage through mobile and web-based applications.'
        ),
        'image_url': 'services/fleet_monitoring.jpeg',
        'detailed_description': 'Detailed information about fleet management solutions...',
        'more_info': (
            'The solution comprises a device-agnostic platform that integrates tracking devices and sensors from all major '
            'manufacturers in the world.\n\n'
            'Salient features of Kedatrack GPS:\n'
            '  - Real-Time Tracking & History Playback:\n'
            '  - Standard reports\n'
            '  - Geozone customization\n\n'
            '  -Last Mile Delivery Management System:\n'
            '  - Order dispatch automation & monitoring\n'
            '  - Route management\n'
            '  - Fleet maintenance\n\n'
            '  - Additional Features:\n'
            '  - 24/7 live vehicle tracking\n'
            '  - Instant notifications/alarms via email, SMS, or app notifications\n'
            '  - Data analysis and flexible custom reporting\n'
            '  - Driver management and control using iButton technology\n'
            '  - Engine immobilization through mobile apps or SMS\n'
            '  - SOS panic buttons and optional voice monitoring\n\n'
            'Comprehensive fleet management reports include fuel utilization, parking reports, speed monitoring, '
            'driver performance analysis, and more. Kedatrack GPS empowers fleet managers to enhance operations, '
            'reduce costs, and improve security.'
        )
    },
    'fuel_monitoring_solutions': {
        'id': 'fuel_monitoring_solutions',
        'title': 'Advanced Fuel Monitoring Solutions',
        'description': (
            'Kedatrack Fuel Monitoring System is a highly accurate solution designed to eliminate fuel-related '
            'expenses caused by theft or dishonesty.'
        ),
        'image_url': 'services/fuel_monitoring.jpeg',
        'detailed_description': 'Detailed information about fuel monitoring solutions...',
        'more_info': (
            'Kedatrack FUEL Monitoring System offers:\n'
            '- Real-time fuel level monitoring\n'
            '- Detailed fuel consumption statistics\n'
            '- Notifications for fuel fills and theft incidents\n'
            '- Graphical representation of fuel consumption data\n\n'
            'This state-of-the-art system helps fleet managers gain full control over fuel costs, '
            'ensuring transparency and operational efficiency.'
        )
    },
    'refrigerated_truck_and_coldroom_temperature_monitoring_system': {
        'id': 'refrigerated_truck_and_coldroom_temperature_monitoring_system',
        'title': 'Refrigerated Truck & Cold-Room Temperature Monitoring System',
        'description': (
            'This Temperature & Humidity Management System provides real-time monitoring for cold-chain vehicles, '
            'cold rooms, and other sensitive environments.'
        ),
        'image_url': 'services/tmonitoring.jpg',
        'detailed_description': 'Detailed information about temperature monitoring systems...',
        'more_info': (
            '- Real-time temperature and humidity monitoring\n'
            '- Door opening detection\n'
            '- Notifications for temperature deviations\n'
            '- Ideal for cold-chain logistics, warehouses, and data centers'
        )
    },
    'video_telematics': {
        'id': 'video_telematics',
        'title': 'AI-Powered Video Telematics',
        'description': (
            'Video telematics combines sensors and AI-powered dashcams to enhance driver safety and fleet management.'
        ),
        'image_url': 'services/dashcam.png',
        'detailed_description': 'Detailed information about video telematics solutions...',
        'more_info': (
            'Key functions include:\n'
            '- Detecting distracted or drowsy driving\n'
            '- Contextual event analysis (e.g., harsh braking causes)\n'
            '- Automated driver coaching and verbal notifications\n\n'
            'Advanced AI dashcams enable fleet managers to digitize and automate safety programs, reducing risks effectively.'
        )
    },
    'security_systems': {
        'id': 'security_systems',
        'title': 'Security Systems',
        'description': (
            'CCTV cameras, access control, and video surveillance solutions to enhance your security infrastructure.'
        ),
        'image_url': 'services/security systems.jpg',
        'detailed_description': 'Detailed information about security systems...',
        'more_info': (
            '- Professional CCTV installation and maintenance\n'
            '- Access control systems setup and upgrades\n'
            '- Comprehensive repair and security infrastructure solutions'
        )
    },
    'software_development': {
        'id': 'software_development',
        'title': 'Software Development',
        'description': (
            'Custom software solutions tailored to your business needs, from web development to mobile apps.'
        ),
        'image_url': 'services/sotware_dev.jpg',
        'detailed_description': 'Detailed information about software development...',
        'more_info': 'Our expert developers create innovative software to solve your unique business challenges.'
    },
    'aerial_and_satellite_installation_solutions': {
        'id': 'aerial_and_satellite_installation_solutions',
        'title': 'Aerial & Satellite Installation Solutions',
        'description': 'Professional TV aerial and satellite installation services.',
        'image_url': 'services/satelite.jpeg',
        'detailed_description': 'Detailed information about aerial and satellite solutions...',
        'more_info': (
            '- Indoor and outdoor aerial installations\n'
            '- Quick and efficient repair services\n'
            '- Full range of high-quality equipment and upgrades'
        )
    },
    'it_support': {
        'id': 'it_support',
        'title': 'IT Support and Consultation',
        'description': (
            'Comprehensive IT support services to improve efficiency and manage technological infrastructure.'
        ),
        'image_url': 'services/it_support.avif',
        'detailed_description': 'Detailed information about IT support...',
        'more_info': (
            'We offer end-to-end IT support, helping you solve technical issues, enhance performance, and ensure system stability.'
        )
    },
    'cloud_services': {
        'id': 'cloud_services',
        'title': 'Cloud Solutions',
        'description': (
            'Seamless cloud services to help businesses scale, manage data, and enhance security on the cloud.'
        ),
        'image_url': 'services/cloud.jpg',
        'detailed_description': 'Detailed information about cloud services...',
        'more_info': (
            'Our cloud solutions include secure data storage, scalable architectures, and high-availability services tailored to your business needs.'
        )
    },
    'data_analytics': {
        'id': 'data_analytics',
        'title': 'Data Analytics',
        'description': (
            'Advanced data analysis tools to help businesses make data-driven decisions and improve performance.'
        ),
        'image_url': 'services/data_analytics.jpg',
        'detailed_description': 'Detailed information about data analytics...',
        'more_info': (
            'Our analytics tools provide actionable insights, empowering businesses to identify trends and optimize strategies effectively.'
        )
    },
    'general_merchandise_supplies_services': {
        'id': 'general_merchandise_supplies_services',
        'title': 'General Merchandise Supplies Services',
        'description': (
            'Providing a wide range of product supply services to private and public sectors.'
        ),
        'image_url': 'services/about.jpeg',
        'detailed_description': 'Detailed information about merchandise supplies...',
        'more_info': (
            'We supply IT hardware, office furniture, staff uniforms, and more. '
            'Our goal is to build long-term partnerships by consistently exceeding expectations.'
        )
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
        "name": "Nicholas Kikuvi",
        "position": "Transport Manager-Davies Express Lt",
        "icon_color": "text-primary",
    },
    {
        "quote": "Exceptional service and innovative solutions.",
        "name": "Albert Muchai",
        "position": "Managing Director- Chev Energies Ltd.",
        "icon_color": "text-success",
    },
    {
        "quote": "Reliable, efficient, and user-friendly.",
        "name": "Philemon Langat",
        "position": "Logistics Manager - Brookfox Enterprise Ltd.",
        "icon_color": "text-warning",
    },
]

@main_bp.route('/request-service/<service_id>', methods=['GET', 'POST'])
def request_service(service_id):
    service = services_data.get(service_id)
    if not service:
        return redirect(url_for('main.services'))

    form = ServiceRequestForm()
    if form.validate_on_submit():
        try:
            new_request = ServiceRequest(
                service_id=service_id,
                service_title=service['title'],
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                description=form.description.data,
                subscribe_to_newsletter=form.subscribe_to_newsletter.data,
            )
            db.session.add(new_request)
            db.session.commit()
            flash("Your request has been submitted successfully!", "success")
            return redirect(url_for('main.request_service', service_id=service_id))
        except Exception as e:
            flash("An error occurred while submitting your request. Please try again.", "danger")
            return redirect(url_for('main.request_service', service_id=service_id))

    return render_template('main/request_service.html', service=service, form=form)
