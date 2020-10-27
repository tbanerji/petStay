"""Tarini Banerji, PetPamperer App version1"""
"""This app helps make bookings for my pet-sitting job, takes in key details about pets,parents,booking"""
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)
import cs304dbi as dbi
import os
import functions as f
app= Flask(__name__)

"""Roues to the main booking page """
@app.route('/')
def index():
    return render_template('bookings.html')

"""Routes to the page with details on a booking and pet as a confirmation """
@app.route('/booked/<person_id>/<p_id>')
def booked(person_id,p_id):
    conn=dbi.connect()
    pinfo=f.getpinfo(p_id,conn)
    species=str(pinfo['species'])
    sex=str(pinfo['sex']) 
    binfo=f.getbinfo(p_id,conn)
    extra_care=str(binfo['extra_care'])

    
    return render_template('booked.html',pinfo=pinfo,binfo=binfo,species=species,sex=sex,extra_care=extra_care)    

"""Facilitates a booking by taking info from form"""
@app.route('/booking',methods=["GET", "POST"])
def booking():
    conn = dbi.connect()
    customer=request.form['customer']
    num_days=request.form['num_days']
    allergies=request.form['allergies']
    extra_care=request.form['extracare']
    pet_name=request.form['pname']
    species=request.form['ptype']
    sex=request.form['gender']
    neutered=request.form['neutered']
    """If the customer is already in system"""
    if f.customerexists(customer,conn)!=None:
            person_id=f.customerexists(customer,conn)
            person_id=person_id['person_id']
            """Inserts the pet into dict from form details"""
            p_id=f.insertPet(person_id,pet_name,species,sex,neutered,conn)
            p_id=p_id['p_id']
            print(p_id)
            f.makeBooking(num_days,allergies,extra_care,p_id,person_id,conn)
            """Completes booking process"""
            return redirect(url_for('booked',person_id=person_id,p_id=p_id))
    else:
            person_id=f.insertCustomer(customer,conn)
            """ inserts customer if doesn't exist"""
            person_id=person_id['person_id']
            pp_id=f.insertPet(person_id,pet_name,species,sex,neutered,conn)
            """Inserts info on a pet from form"""
            p_id=f.getpid(person_id,conn)
            p_id=p_id['p_id']
            f.makeBooking(num_days,allergies,extra_care,p_id,person_id,conn)
            """Completes booking process"""
            return redirect(url_for('booked',person_id=person_id,p_id=p_id))

"""This function sets up the use of the dictionary """
@app.before_first_request
def startup():
   dbi.cache_cnf()
   dbi.use('tbanerji_db')

if __name__ == '__main__':
    import sys, os
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)