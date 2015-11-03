from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_imageattach.stores.fs import FileSystemStore
from sqlalchemy_imageattach.context import store_context
from database_setup import Base, Antibody, Cytotoxin, AntibodyImg, AntibodyLot, CytotoxinImg, CytotoxinLot, ADC, ADCLot
import datetime
import os
from werkzeug.contrib.atom import AtomFeed

app = Flask(__name__)

fs_store = FileSystemStore(
    path='static/images/',
    base_url='http://images.yourapp.com/'
)

engine = create_engine('sqlite:///biologicscatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# def make_external(url):
#     return urljoin(request.url_root, url)

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

@app.route('/antibody')
def antibodyMenu():
    antibodies=session.query(Antibody).order_by(Antibody.name).all()
    lots=session.query(AntibodyLot).all()
    lotdict={}
    for x in range(1,session.query(Antibody).count()+1):
        lotdict[x]=session.query(AntibodyLot).filter(AntibodyLot.antibody_id==x).order_by(AntibodyLot.date).all()
    return render_template('antibody.html', antibodies=antibodies, lotdict=lotdict, lots=lots)

@app.route('/cytotoxin')
def cytotoxinMenu():
    return render_template('cytotoxin.html')

@app.route('/ADC')
def adcMenu():
    return render_template('adc.html')

@app.route('/create', methods=['GET','POST'])
def createAb():
    if request.method == 'POST':
        new=Antibody(name=request.form['name'], weight=request.form['weight'], target=request.form['target'])
        session.add(new)
        session.commit()
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

def get_picture_url(table, item_id):
    item=session.query(table).filter_by(id=item_id).one()
    with store_context(fs_store):
        picture_url = item.picture.locate()
    return picture_url

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
