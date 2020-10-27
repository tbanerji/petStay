"""Helper functions for searching database"""

from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)
import cs304dbi as dbi
import os
import functions as f

"""Function checks if a customer is in the database"""
def customerexists(cname,conn):
    curs=dbi.dict_cursor(conn)
    searched="%"+cname+"%"
    curs.execute('''select person_id from parents where p_name like %s''',searched)
    person_id=curs.fetchone()
    if person_id==None:
        return None
    else:
        return person_id

"""Function inserts customer into database given form info"""
def insertCustomer(cname,conn):
    curs=dbi.dict_cursor(conn)
    curs.execute('''insert into parents(p_name) values(%s)''',cname)
    conn.commit()
    searched="%"+cname+"%"
    curs.execute('''select person_id from parents where p_name like %s''',searched)
    return curs.fetchone()
    
""" Inserts into pet table"""
def insertPet(person_id,pet_name,species,sex,neutered,conn):
    curs=dbi.dict_cursor(conn)
    curs.execute('''insert into pets(person_id,pet_name,species,sex,neutered) values(%s,%s,%s,%s,%s)''',(person_id,pet_name,species,sex,neutered))
    conn.commit()
    curs.execute('''select p_id from pets where person_id=%s''',person_id)
    return curs.fetchone()
   

"""Function inserts booking details into database given form info"""
def makeBooking(num_days,allergies,extra_care,p_id,person_id,conn):
    curs=dbi.dict_cursor(conn)
    curs.execute('''insert into bookings(num_days,allergies,extra_care,p_id,person_id)values(%s,%s,%s,%s,%s)''',(num_days,allergies,extra_care,p_id,person_id))
    conn.commit()


"""Function helps get all info on booking"""
def getbinfo(p_id,conn):
    curs=dbi.dict_cursor(conn)
    curs.execute('''select * from bookings where p_id=%s''',p_id)
    return curs.fetchone()

"""Function gets all info on a pet"""
def getpinfo(p_id,conn):
    curs=dbi.dict_cursor(conn)
    curs.execute('''select * from pets where p_id=%s''',p_id)
    return curs.fetchone()

"""Function will get pet id from person details"""
def getpid(person_id,conn):
    curs=dbi.dict_cursor(conn)
    curs.execute('''select p_id from pets where person_id=%s''',p_id)
    return curs.fetchone()
