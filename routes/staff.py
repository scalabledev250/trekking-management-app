from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from models import *

staff_Bp = Blueprint('staff', __name__)

@staff_Bp.route('/staffdashboard')
@login_required
def staffdashboard():
    assigned_treks = Trek.query.filter_by(staff_id=current_user.id, is_deleted=False).all()
    alen = len(assigned_treks)
    total_users = User.query.filter_by(role=Role.trekker).count()
    open_treks = Trek.query.filter_by(status=TrekStatus.open).count()
    participants = Booking.query.filter_by(trek_id=current_user.id).count()
    return render_template('staff_dashboard.html', name=current_user.username, assigned_treks=assigned_treks, total_users=total_users, 
                           open_treks=open_treks, participants=participants, alen=alen)

@staff_Bp.route('/stafftrek')
@login_required
def stafftrek():
    assigned_treks = Trek.query.filter_by(staff_id=current_user.id, is_deleted=False).all()
    return render_template('staff_trek.html', assigned_treks=assigned_treks)

@staff_Bp.route('/participants')
@login_required
def participants():  
    trek = Trek.query.filter_by(id=current_user.id).first()
    participants = Booking.query.filter_by(trek_id=current_user.id).all()
    return render_template('participants.html', participants=participants, plen=len(participants))

@staff_Bp.route('/edittrek/<int:trek_id>', methods=['GET', 'POST'])
@login_required
def edittrek(trek_id):

    trek = Trek.query.filter_by(
        id=trek_id,
        is_deleted=False
    ).first_or_404()

    if request.method == 'POST':

        try:
            trek.available_slots = int(
                request.form['available_slots']
            )

            trek.status = TrekStatus(
                request.form['status']
            )

        except (ValueError, TypeError):
            return "Invalid input", 400

        if trek.available_slots < 0:
            return "Slots cannot be negative", 400

        db.session.commit()

        return redirect(url_for('staff.stafftrek'))

    return render_template(
        'staff_edit_trek.html',
        trek=trek
    )
