from Vessel_app import app

from flask import render_template, url_for, flash, redirect, request, session

@app.route("/")
@app.route('/home')
def index():
    return render_template('index.html')



