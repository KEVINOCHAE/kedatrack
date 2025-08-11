from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_mail import Message
from flask_login import current_user
from app import db, mail
from app.admin.models import User, EmailLog
from flask_login import login_required
from functools import wraps

admin_bp = Blueprint('admin', __name__)



@admin_bp.route('/admin/dashboard', methods=['GET'])
def dashboard():
    
    return render_template('admin/dashboard.html')
    
@admin_bp.route('/admin/users', methods=['GET'])
@login_required
def users_page():
    """Fetch all users and display them in a DataTable."""
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    """Delete a user."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully.", "success")
    return redirect(url_for('admin.users_page'))

@admin_bp.route('/admin/user/<int:user_id>/email', methods=['GET', 'POST'])
@login_required
def email_user(user_id):
    """Email an individual user."""
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        subject = request.form['subject']
        body = request.form['body']

        # Send the email
        msg = Message(subject, recipients=[user.email])
        msg.body = body
        mail.send(msg)

        # Log the email
        email_log = EmailLog(subject=subject, body=body, recipients=user.email)
        db.session.add(email_log)
        db.session.commit()

        flash("Email sent successfully.", "success")
        return redirect(url_for('admin.users_page'))

    return render_template('admin/email_user.html', user=user)

@admin_bp.route('/admin/users/email', methods=['POST'])
@login_required
def email_multiple_users():
    """Send email to selected or all users."""
    user_ids = request.form.getlist('user_ids')  # IDs of selected users
    users = User.query.filter(User.id.in_(user_ids)).all()

    subject = request.form['subject']
    body = request.form['body']
    recipient_emails = [user.email for user in users]

    # Send the email
    msg = Message(subject, recipients=recipient_emails)
    msg.body = body
    mail.send(msg)

    # Log the email
    email_log = EmailLog(subject=subject, body=body, recipients=", ".join(recipient_emails))
    db.session.add(email_log)
    db.session.commit()

    flash("Email sent successfully to selected users.", "success")
    return redirect(url_for('admin.users_page'))


@admin_bp.route('/admin/newsletter', methods=['GET'])
@login_required
def newsletter_page():
    """Show newsletter overview with recent messages."""
    recent_emails = EmailLog.query.order_by(EmailLog.sent_at.desc()).limit(5).all()
    return render_template('admin/newsletter.html', recent_emails=recent_emails)

@admin_bp.route('/admin/newsletter/messages', methods=['GET'])
@login_required
def all_messages():
    """Paginated view of all email logs."""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    messages = EmailLog.query.order_by(EmailLog.sent_at.desc()).paginate(page=page, per_page=per_page)
    return render_template('admin/all_messages.html', messages=messages)
    
    
    
