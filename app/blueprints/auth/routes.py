from .import bp as auth
from .forms import LoginForm, RegisterForm, EditProfileForm
from flask import render_template, request, flash, redirect, url_for
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required

@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        email = request.form.get('email').lower()   
        password = request.form.get('password')
        u = User.query.filter_by(email=email).first()
        if u and u.check_hashed_password(password):
            login_user(u)
            flash('Welcome back!', 'is-success')
            return redirect(url_for('main.index'))
        flash('Incorrect Email password Combo','is-danger')
        return render_template('login.html.j2',form=form)
    return render_template('login.html.j2',form=form)

@auth.route('/logout')
def logout():
    if current_user:
        logout_user()
        flash('You have been logged out, Goodbye!', 'is-warning',)
        return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if request.method =='POST' and form.validate_on_submit():
        try:
            new_user_data = {
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data

            }
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
            new_user_object.save()
        except:
            flash('There was an unexpected Error creating your Account Please Try Again.','is-danger')
            #Error Return
            return render_template('register.html.j2', form = form)
        # If it worked
        flash('You have registered successfully', 'is-success')
        return redirect(url_for('auth.login'))
    #Get Return
    return render_template('register.html.j2', form = form)

@auth.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user_data={
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data
        }
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.email != current_user.email:
            flash('Email already in use','is-danger')
            return redirect(url_for('auth.edit_profile'))
        try:
            current_user.from_dict(new_user_data)
            current_user.save()
            flash('Profile Updated', 'is-success')
        except:
            flash('There was an unexpected Error. Please Try again', 'is-danger')
            return redirect(url_for('auth.edit_profile'))
        return redirect(url_for('main.index'))
    return render_template('register.html.j2', form = form)