import urllib.parse
from flask import render_template, request, redirect, url_for, flash
from pathsix import app, mail, bcrypt, db
from pathsix.forms import ContactForm, RegistrationForm, LoginForm, UpdateAccountForm, ClientForm, RequestResetForm, ResetPasswordForm
from flask_mail import Message
from pathsix.models import User, Client, Address, Contact, ContactNote, Sale, BillingCycle, WebsiteUpdate, MailingList, ClientWebsite, Reminder
from flask_login import login_user, current_user, logout_user, login_required

