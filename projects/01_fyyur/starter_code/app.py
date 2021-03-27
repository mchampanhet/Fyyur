#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from datetime import datetime


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String)
    image_link = db.Column(db.String)
    facebook_link = db.Column(db.String)
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='venue', lazy=True)


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='artist', lazy=True)


class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  venue_name = db.Column(db.String(120), nullable=False)
  venue_image_link = db.Column(db.String(500))
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  artist_name = db.Column(db.String(120), nullable=False)
  artist_image_link = db.Column(db.String(500))
  start_time = db.Column(db.DateTime, nullable=False)

conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])
cursor = conn.cursor()
cursor.execute('select count(*) as count from pg_tables where tablename in (\'Venue\', \'Show\', \'Artist\')')
row = cursor.fetchone()
print(row[0])
if row[0] == 3:
  cursor.execute('select count(a.id) as count from (select id from "Artist" b union select id from "Show" c union select id from "Venue" d) a')
  row = cursor.fetchone()
  if row[0] == 0:

    venue1 = Venue(
      name='The Musical Hop',
      genres=['Jazz','Reggae','Swing','Classical','Folk'],
      address='1015 Folsom Street',
      city='San Francisco',
      state='CA',
      phone='123-123-1234',
      website='https://www.themusicalhop.com',
      facebook_link='https://www.facebook.com/TheMusicalHop',
      seeking_talent=True,
      seeking_description='We are on the lookout for a local artist to play every two weeks. Please call us.',
      image_link='https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60'
    )
    venue2 = Venue(
      name='The Dueling Pianos Bar',
      genres=['Classical','R&B','Hip-Hop'],
      address='336 Delancey Street',
      city='New York',
      state='NY',
      phone='914-003-1132',
      website='https://www.theduelingpianos.com',
      facebook_link='https://www.facebook.com/theduelingpianos',
      seeking_talent=False,
      image_link='https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80'
    )
    venue3 = Venue(
      name='Park Square Live Music & Coffee',
      genres=['Rock n Roll','Jazz','Classical','Folk'],
      address='34 Whiskey Moore Ave',
      city='San Francisco',
      state='CA',
      phone='415-000-1234',
      website='https://www.parksquarelivemusicandcoffee.com',
      facebook_link='https://www.facebook.com/ParkSquareLiveMusicAndCoffee',
      seeking_talent=False,
      image_link='https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80'
    )
    artist1 = Artist(
      name='Guns n Petals',
      genres=['Rock n Roll'],
      city='San Francisco',
      state='CA',
      phone='326-123-5000',
      website='https://www.gunsnpetalsband.com',
      facebook_link='https://www.facebook.com/GunsNPetals',
      seeking_venue=True,
      seeking_description='Looking for shows to perform at in the San Francisco Bay Area!',
      image_link='https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80'
    )
    artist2 = Artist(
      name='Matt Quevedo',
      genres=['Jazz'],
      city='New York',
      state='NY',
      phone='300-400-5000',
      facebook_link='https://www.facebook.com/mattquevedo923251523',
      seeking_venue=False,
      image_link='https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80'
    )
    artist3 = Artist(
      name='The Wild Sax Band',
      genres=['Jazz','Classical'],
      city='San Francisco',
      state='CA',
      phone='432-325-5432',
      seeking_venue=False,
      image_link='https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80'
    )
    show1 = Show(
      venue_id=1,
      venue_name='The Musical Hop',
      venue_image_link='https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
      artist_id=1,
      artist_name='Guns N Petals',
      artist_image_link='https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',
      start_time='2019-05-21T21:30:00.000Z'
    )
    show2 = Show(
      venue_id=3,
      venue_name='Park Square Live Music & Coffee',
      venue_image_link='https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
      artist_id=2,
      artist_name='Matt Quevedo',
      artist_image_link='https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80',
      start_time='2019-06-15T23:00:00.000Z'
    )
    show3 = Show(
      venue_id=3,
      venue_name='Park Square Live Music & Coffee',
      venue_image_link='https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
      artist_id=3,
      artist_name='The Wild Sax Band',
      artist_image_link='https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
      start_time='2035-04-01T20:00:00.000Z'
    )
    show4 = Show(
      venue_id=3,
      venue_name='Park Square Live Music & Coffee',
      venue_image_link='https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
      artist_id=3,
      artist_name='The Wild Sax Band',
      artist_image_link='https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
      start_time='2035-04-08T20:00:00.000Z'
    )
    show5 = Show(
      venue_id=3,
      venue_name='Park Square Live Music & Coffee',
      venue_image_link='https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
      artist_id=3,
      artist_name='The Wild Sax Band',
      artist_image_link='https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
      start_time='2035-04-15T20:00:00.000Z'
    )
    db.session.add(venue1)
    db.session.add(venue2)
    db.session.add(venue3)
    db.session.add(artist1)
    db.session.add(artist2)
    db.session.add(artist3)
    db.session.add(show1)
    db.session.add(show2)
    db.session.add(show3)
    db.session.add(show4)
    db.session.add(show5)
    db.session.commit()


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = datetime.now()
  if type(value) is not datetime:
    date = dateutil.parser.parse(value)
  else:
    date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  venues_data = Venue.query.order_by(Venue.city).all()
  data = {}
  for venue in venues_data:
    if venue.city + venue.state not in data:
      data[venue.city + venue.state] = {
        'city':venue.city,
        'state':venue.state,
        'venues': list(filter(lambda v: v.city == venue.city and v.state == venue.state, venues_data))
      }

      for subvenue in data[venue.city + venue.state]['venues']:
        subvenue.num_upcoming_shows = db.session.query(Show).filter(Show.venue_id == subvenue.id, Show.start_time > datetime.now()).count()
  return render_template('pages/venues.html', areas=data.values());

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  data = Venue.query.get(venue_id)
  data.upcoming_shows = db.session.query(Show).filter(Show.venue_id == venue_id, Show.start_time > datetime.now())
  data.upcoming_shows_count = data.upcoming_shows.count()
  data.past_shows = db.session.query(Show).filter(Show.venue_id == venue_id, Show.start_time < datetime.now())
  data.past_shows_count = data.past_shows.count()
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.', 'error')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.order_by(Artist.name).all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  data = Artist.query.get(artist_id)
  data.upcoming_shows = db.session.query(Show).filter(Show.artist_id == artist_id, Show.start_time > datetime.now())
  data.upcoming_shows_count = data.upcoming_shows.count()
  data.past_shows = db.session.query(Show).filter(Show.artist_id == artist_id, Show.start_time < datetime.now())
  data.past_shows_count = data.past_shows.count()
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm(obj=artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  data = Show.query.order_by(Show.start_time.desc()).all()
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
