from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from werkzeug import secure_filename
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_imageattach.stores.fs import FileSystemStore
from sqlalchemy_imageattach.context import store_context, push_store_context, pop_store_context
from database_setup import Base, Antibody, Cytotoxin, AntibodyImg, AntibodyLot, CytotoxinImg, CytotoxinLot, ADC, ADCLot
import datetime
import os
from werkzeug import secure_filename
from werkzeug.contrib.atom import AtomFeed

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

fs_store = FileSystemStore(
    path='static/images/',
    base_url='http://localhost:5000/static/images/')

engine = create_engine('sqlite:///biologicscatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

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
def mainMenu():
    return render_template('home.html')

@app.route('/antibody/')
def antibodyMenu():
    antibodies=session.query(Antibody).order_by(Antibody.name).all()
    lots=session.query(AntibodyLot).all()
    lotdict={}
    for x in range(1,session.query(Antibody).count()+1):
        lotdict[x]=session.query(AntibodyLot).filter(AntibodyLot.antibody_id==x).order_by(AntibodyLot.date).all()
    return render_template('antibody.html', antibodies=antibodies, lotdict=lotdict, lots=lots)

@app.route('/<table>/img/<int:item_id>/')
def get_picture_url(item_id, table):
    item=session.query(eval(table.capitalize())).filter_by(id=item_id).one()
    with store_context(fs_store):
        try:
            picture_url = item.picture.locate()
        except IOError:
            print "No picture found for lot# %s" % str(item_id)
            picture_url=''
    return render_template('img.html',item=item, picture_url=picture_url)

@app.route('/cytotoxin/')
def cytotoxinMenu():
    return render_template('cytotoxin.html')

@app.route('/ADC/')
def adcMenu():
    return render_template('adc.html')

@app.route('/create', methods=['GET','POST'])
def createAb():
    if request.method == 'POST':
        new=Antibody(name=request.form['name'], weight=request.form['weight'], target=request.form['target'])
        session.add(new)
        session.commit()
        image=request.files['picture']
        if image and allowed_file(image.filename):
            with store_context(fs_store):
                new.picture.from_file(image)
        flash('Antibody Created')
        return redirect(url_for('antibodyMenu'))
    else:
        return render_template('create-Ab.html')

@app.route('/create/<int:item_id>/', methods=['GET','POST'])
def createAbLot(item_id):
    if request.method == 'POST':
        new=AntibodyLot(date=datetime.datetime.strptime(request.form['date'].replace('-',' '), '%Y %m %d'), aggregate=request.form['aggregate'], endotoxin=request.form['endotoxin'], concentration=request.form['concentration'], vialVolume=request.form['vialVolume'], vialNumber=request.form['vialNumber'], antibody_id=item_id)
        session.add(new)
        session.commit()
        flash('Antibody Lot Created')
        return redirect(url_for('antibodyMenu'))
    else:
        return render_template('create-ab-lot.html',item_id=item_id)

@app.route('/editAb/<int:item_id>/', methods=['GET','POST'])
def editAb(item_id):
    editedItem = session.query(Antibody).filter_by(id=item_id).one()
    if request.method == 'POST':
        image=request.files['picture']
        if image and allowed_file(image.filename):
            with store_context(fs_store):
                editedItem.picture.from_file(image)
        editedItem.name=request.form['name']
        editedItem.weight=request.form['weight']
        editedItem.target=request.form['target']
        session.add(editedItem)
        session.commit()
        flash('Antibody Edited')
        return redirect(url_for('antibodyMenu'))
    else:
        return render_template('edit-ab.html', item_id=item_id, editedItem=editedItem)

@app.route('/editAbLot/<int:item_id>/', methods=['GET','POST'])
def editAbLot(item_id):
    editedItem = session.query(AntibodyLot).filter_by(id=item_id).one()
    if request.method == 'POST':
        editedItem.date=datetime.datetime.strptime(request.form['date'].replace('-',' '), '%Y %m %d')
        editedItem.aggregate=request.form['aggregate']
        editedItem.endotoxin=request.form['endotoxin']
        editedItem.concentration=request.form['concentration']
        editedItem.vialVolume=request.form['vialVolume']
        editedItem.vialNumber=request.form['vialNumber']
        session.add(editedItem)
        session.commit()
        flash('Antibody Lot Edited')
        return redirect(url_for('antibodyMenu'))
    else:
        return render_template('edit-ab-lot.html',item_id=item_id, editedItem=editedItem)

@app.route('/delete/<dbtype>/<int:item_id>/', methods=['GET','POST'])
def delete(dbtype, item_id):
    deleteItem=session.query(eval(dbtype)).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        flash('Item Deleted')
        return redirect(url_for('antibodyMenu'))
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

def delete_picture(table, item_id):
    item=session.query(table).filter_by(id=item_id).one()
    fs_store.delete(item.picture.original)
    session.commit()

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
