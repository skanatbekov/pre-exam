from flask import request, render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required

from app import db
from .models import Course, Student, User
from .forms import CourseForm, StudentForm, UserRegisterForm, UserLoginForm


def index():
    students = Student.query.all()
    return render_template('index.html', students=students)


@login_required
def course_create():
    form = CourseForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_course = Course()
            form.populate_obj(new_course)
            db.session.add(new_course)
            db.session.commit()
            flash('Курс успешно добавлен', 'Успешно!')
            return redirect(url_for('index'))
        else:
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При добавлении курса произошла ошибка. {". ".join(text_list)}', 'Ошибка!')
    return render_template('form.html', form=form)


def course_update(course_id):
    course = Course.query.get(course_id)
    form = CourseForm(obj=course)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(course)
            db.session.add(course)
            db.session.commit()
            flash('Курс успешно изменен', 'Успешно!')
            return redirect(url_for('index'))
        else:
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При изменении курса произошла ошибка. {". ".join(text_list)}', 'Ошибка!')

    return render_template('form.html', form=form)


@login_required
def course_delete(course_id):
    course = Course.query.get(course_id)
    if request.method == 'POST':
        db.session.delete(course)
        db.session.commit()
        flash('Курс успешно удален', 'Успешно!')
        return redirect(url_for('index'))
    return render_template('course_delete.html', course=course)


@login_required
def student_create():
    form = StudentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_student = Student()
            form.populate_obj(new_student)
            db.session.add(new_student)
            db.session.commit()
            flash('Студент успешно добавлен', 'Успешно!')
            return redirect(url_for('index'))
        else:
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При добавлении студента произошла ошибка. {". ".join(text_list)}', 'Ошибка!')
    return render_template('form.html', form=form)


def student_update(student_id):
    student = Student.query.get(student_id)
    form = StudentForm(obj=student)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(student)
            db.session.add(student)
            db.session.commit()
            flash('Студент успешно изменен', 'Успешно!')
            return redirect(url_for('index'))
        else:
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При изменении студента произошла ошибка. {". ".join(text_list)}', 'Ошибка!')

    return render_template('form.html', form=form)


@login_required
def student_delete(student_id):
    student = Student.query.get(student_id)
    if request.method == 'POST':
        db.session.delete(student)
        db.session.commit()
        flash('Студент успешно удален', 'Успешно!')
        return redirect(url_for('index'))
    return render_template('student_delete.html', student=student)


def user_register():
    form = UserRegisterForm()
    title = 'Регистрация'
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User()
            form.populate_obj(new_user)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Пользователь {new_user.username} успешно зарегистрирован', 'Успех!')
            return redirect(url_for('user_login'))
        else:
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При регистрации произошла ошибка. {". ".join(text_list)}', 'Ошибка!')
    return render_template('account/index.html', form=form, title=title)


def user_login():
    form = UserLoginForm()
    title = 'Авторизация'
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Вы успешно вошли в систему', 'Успех!')
                return redirect(url_for('index'))
            else:
                flash('Невеные логин и пароль', 'Ошибка!')
    return render_template('account/index.html', form=form, title=title)


def user_logout():
    logout_user()
    return redirect(url_for('user_login'))