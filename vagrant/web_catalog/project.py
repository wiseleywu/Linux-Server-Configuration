from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from werkzeug import secure_filename
from sqlalchemy import create_engine, MetaData, Table, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy_imageattach.stores.fs import FileSystemStore
from sqlalchemy_imageattach.context import store_context, push_store_context, pop_store_context
from database_setup import Base, User, UserImg, Antibody, Cytotoxin, AntibodyImg, AntibodyLot, CytotoxinImg, CytotoxinLot, Adc, AdcLot, AdcImg
from urllib2 import urlopen
import datetime
import os
import random
import string
from werkzeug import secure_filename
from werkzeug.contrib.atom import AtomFeed
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from flask import session as login_session

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Biologics Catalog"

fs_store = FileSystemStore(
    path='static/images/',
    base_url='http://localhost:5000/static/images/')

engine = create_engine('sqlite:///biologicscatalog.db')
Base.metadata.bind = engine
meta = MetaData(bind=engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output

# User Helper Functions

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/recent.atom')
def recent_feed():
    feed = AtomFeed('Recent Articles',
                    feed_url=request.url, url=request.url_root)
    articles = lots=session.query(AntibodyLot).all()
    for article in articles:
        feed.add(article.id,
                 content_type='html',
                 id=article.id,
                 updated=article.date)
    return feed.get_response()

# Making an JSON Endpoint (GET Request)
@app.route('/antibodyLot/JSON')
def antibodyLotJSON():
    lots=session.query(AntibodyLot).all()
    return jsonify(AntibodyLots=[i.serialize for i in lots])

@app.route('/antibody/JSON')
def antibodyJSON():
    antibodies=session.query(Antibody).all()
    return jsonify(Antibodies=[i.serialize for i in antibodies])

@app.route('/')
@app.route('/home')
def home():
    username=None
    loggedIn=False
    if 'username' in login_session:
        username=login_session['username']
        loggedIn=True
    return render_template('home.html', title='Home', loggedIn=loggedIn, username=username)

@app.route('/antibody/')
def antibody():
    userID, username = None, None
    if 'username' in login_session:
        userID=getUserID(login_session['email'])
        username=login_session['username']
    antibodies=session.query(Antibody).order_by(Antibody.name).all()
    lots=session.query(AntibodyLot).all()
    lotdict={}
    for x in range(1,session.query(Antibody).count()+1):
        lotdict[x]=session.query(AntibodyLot).filter(AntibodyLot.antibody_id==x).order_by(AntibodyLot.date).all()
    return render_template('antibody.html', title='Antibody', antibodies=antibodies, lotdict=lotdict, lots=lots, userID=userID, username=username)

@app.route('/<dbtype>/img/<int:item_id>/')
def get_picture_url(dbtype, item_id):
    item=session.query(eval(dbtype.capitalize())).filter_by(id=item_id).one()
    with store_context(fs_store):
        try:
            picture_url = item.picture.locate()
        except IOError:
            print "No picture found for lot# %s" % str(item_id)
            picture_url=''
    return render_template('img.html',item=item, picture_url=picture_url, dbtype=dbtype)

@app.route('/cytotoxin/')
def cytotoxin():
    userID, username = None, None
    if 'username' in login_session:
        userID=getUserID(login_session['email'])
        username=login_session['username']
    cytotoxins=session.query(Cytotoxin).order_by(Cytotoxin.name).all()
    lots=session.query(CytotoxinLot).all()
    lotdict={}
    for x in range(1,session.query(Cytotoxin).count()+1):
        lotdict[x]=session.query(CytotoxinLot).filter(CytotoxinLot.cytotoxin_id==x).order_by(CytotoxinLot.date).all()
    return render_template('cytotoxin.html', title='Cytotoxin', cytotoxins=cytotoxins, lotdict=lotdict, lots=lots, userID=userID, username=username)

@app.route('/adc/')
def adc():
    userID, username = None, None
    if 'username' in login_session:
        userID=getUserID(login_session['email'])
        username=login_session['username']
    adcs=session.query(Adc).order_by(Adc.name).all()
    lots=session.query(AdcLot).all()
    lotdict={}
    for x in range(1,session.query(Adc).count()+1):
        lotdict[x]=session.query(AdcLot).filter(AdcLot.adc_id==x).order_by(AdcLot.date).all()
    return render_template('adc.html', title='ADC', adcs=adcs, lotdict=lotdict, lots=lots, userID=userID, username=username)

@app.route('/<dbtype>/create', methods=['GET','POST'])
def createType(dbtype):
    table=Table(dbtype, meta, autoload=True, autoload_with=engine)
    if request.method == 'POST':
        if dbtype == 'antibody':
            new=eval(dbtype.capitalize())(name=request.form['name'], weight=request.form['weight'], target=request.form['target'])
        elif dbtype == 'cytotoxin':
            new=eval(dbtype.capitalize())(name=request.form['name'], weight=request.form['weight'], drugClass=request.form['drugClass'])
        else:
            new=eval(dbtype.capitalize())(name=request.form['name'], chemistry=request.form['chemistry'])
        session.add(new)
        session.commit()
        image=request.files['picture']
        if image and allowed_file(image.filename):
            with store_context(fs_store):
                new.picture.from_file(image)
        flash('%s Created' % dbtype.capitalize())
        return redirect(url_for(dbtype))
    else:
        return render_template('create-type.html', columns=table.columns, dbtype=dbtype)

@app.route('/<dbtype>/<int:item_id>/create/', methods=['GET','POST'])
def createTypeLot(dbtype, item_id):
    table=Table('%s_lot' %dbtype, meta, autoload=True, autoload_with=engine)
    maxablot=session.query(AntibodyLot).order_by(desc(AntibodyLot.id)).first().id
    maxtoxinlot=session.query(CytotoxinLot).order_by(desc(CytotoxinLot.id)).first().id
    if request.method == 'POST':
        if dbtype == 'antibody':
            new=AntibodyLot(date=datetime.datetime.strptime(request.form['date'].replace('-',' '), '%Y %m %d'), aggregate=request.form['aggregate'], endotoxin=request.form['endotoxin'], concentration=request.form['concentration'], vialVolume=request.form['vialVolume'], vialNumber=request.form['vialNumber'], antibody_id=item_id)
        elif dbtype == 'cytotoxin':
            new=CytotoxinLot(date=datetime.datetime.strptime(request.form['date'].replace('-',' '), '%Y %m %d'), purity=request.form['purity'], concentration=request.form['concentration'], vialVolume=request.form['vialVolume'], vialNumber=request.form['vialNumber'], cytotoxin_id=item_id)
        else:
            new=AdcLot(date=datetime.datetime.strptime(request.form['date'].replace('-',' '), '%Y %m %d'), aggregate=request.form['aggregate'], endotoxin=request.form['endotoxin'], concentration=request.form['concentration'], vialVolume=request.form['vialVolume'], vialNumber=request.form['vialNumber'], antibodylot_id=request.form['antibodylot_id'], cytotoxinlot_id=request.form['cytotoxinlot_id'], adc_id=item_id)
        session.add(new)
        session.commit()
        flash('%s Lot Created' %dbtype.capitalize())
        return redirect(url_for(dbtype))
    else:
        return render_template('create-type-lot.html', dbtype=dbtype, columns=table.columns, item_id=item_id, maxablot=maxablot, maxtoxinlot=maxtoxinlot)

@app.route('/<dbtype>/<int:item_id>/edit', methods=['GET','POST'])
def editType(dbtype, item_id):
    table=Table(dbtype, meta, autoload=True, autoload_with=engine)
    editedItem = session.query(eval(dbtype.capitalize())).filter_by(id=item_id).one()
    if request.method == 'POST':
        image=request.files['picture']
        if image and allowed_file(image.filename):
            with store_context(fs_store):
                editedItem.picture.from_file(image)
        for column in table.columns:
            if column.name == 'id':
                pass
            else:
                setattr(editedItem, column.name, request.form[column.name])
        session.add(editedItem)
        session.commit()
        flash('%s Edited' % dbtype.capitalize())
        return redirect(url_for(dbtype))
    else:
        return render_template('edit-type.html', dbtype=dbtype, columns=table.columns, item_id=item_id, editedItem=editedItem)

@app.route('/<dbtype>/lot/<int:item_id>/edit', methods=['GET','POST'])
def editTypeLot(dbtype, item_id):
    table=Table('%s_lot' % dbtype, meta, autoload=True, autoload_with=engine)
    maxablot=session.query(AntibodyLot).order_by(desc(AntibodyLot.id)).first().id
    maxtoxinlot=session.query(CytotoxinLot).order_by(desc(CytotoxinLot.id)).first().id
    editedItem = session.query(eval(dbtype.capitalize()+'Lot')).filter_by(id=item_id).one()
    if request.method == 'POST':
        editedItem.date=datetime.datetime.strptime(request.form['date'].replace('-',' '), '%Y %m %d')
        for column in table.columns:
            print column.name
            if column.name in ('id', 'date', 'antibody_id', 'cytotoxin_id', 'adc_id'):
                pass
            else:
                setattr(editedItem, column.name, request.form[column.name])
        session.add(editedItem)
        session.commit()
        flash('%s Lot Edited'% dbtype.capitalize())
        return redirect(url_for(dbtype))
    else:
        return render_template('edit-type-lot.html', dbtype=dbtype, columns=table.columns, item_id=item_id, editedItem=editedItem, maxablot=maxablot, maxtoxinlot=maxtoxinlot)

@app.route('/<dbtype>/<int:item_id>/delete/', methods=['GET','POST'])
def delete(dbtype, item_id):
    deleteItem=session.query(eval(dbtype[0].upper()+dbtype[1:])).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        if dbtype[-3:].lower() == 'lot':
            flash('%s Lot Deleted' % dbtype[:-3].capitalize())
            return redirect(url_for(dbtype[:-3]))
        else:
            flash('%s  Deleted' % dbtype.capitalize())
            return redirect(url_for(dbtype))
    else:
        pass

@app.before_request
def start_implicit_store_context():
    push_store_context(fs_store)

@app.teardown_request
def stop_implicit_store_context(exception=None):
    pop_store_context()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def attach_picture(table, item_id, location):
    try:
        item=session.query(table).filter_by(id=item_id).one()
        with store_context(fs_store):
            with open(location,'rb') as f:
                item.picture.from_file(f)
                session.commit()
    except Exception:
        session.rollback()
        raise

def attach_picture_url(table, item_id, location):
    try:
        item=session.query(table).filter_by(id=item_id).one()
        with store_context(fs_store):
            item.picture.from_file(urlopen(location))
            session.commit()
    except Exception:
        session.rollback()
        raise

def delete_picture(table, item_id):
    item=session.query(table).filter_by(id=item_id).one()
    fs_store.delete(item.picture.original)
    session.commit()

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
