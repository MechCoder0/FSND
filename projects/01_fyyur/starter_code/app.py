#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from datetime import datetime
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app,db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String)
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    shows = db.relationship('Show', backref='venue')

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    website = db.Column(db.String)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    shows = db.relationship('Show', backref='artist', lazy=True)

class Show(db.Model):
    __tablename__ = 'Shows'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.String)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

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
  data = []
  areas = Venue.query.distinct('city','state').all()
  for area in areas:
    venues = Venue.query.filter(Venue.city==area.city, Venue.state == area.state).all()
    record = {
      'city': area.city,
      'state': area.state,
      'venues': venues
    }
    data.append(record)
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')
  look_for = '%{0}%'.format(search_term)
  items = Venue.query.filter(Venue.name.ilike(look_for)).all()
  response={
    'count': len(items),
    'data': items
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  data = Venue.query.get(venue_id)
  data.genres = data.genres.split(",")
  data = sep_shows(data, get_show_artist_ob)
  return render_template('pages/show_venue.html', venue=data)

def get_show_artist_ob(show):
  return {
        'start_time': show.start_time,
        'artist_image_link': show.artist.image_link,
        'artist_name': show.artist.name,
        'artist_id': show.artist_id
      }

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:
    # on successful db insert, flash success
    db.session.add(create_venue_from_form(request.form))
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  
  return render_template('pages/home.html')

"""
  Creates and returns a venue object based on the 
  information in the passed form. 
"""
def create_venue_from_form(form):
  new_venue = Venue()
  new_venue.name = form['name']
  new_venue.city = form['city']
  new_venue.state = form['state']
  new_venue.address = form['address']
  new_venue.phone = form['phone']
  new_venue.genres = form.getlist('genres')
  new_venue.facebook_link = form['facebook_link']
  new_venue.image_link = form['image_link']
  new_venue.website = form['website']
  return new_venue

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('index'))

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button deletes it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  return render_template('pages/artists.html', artists=Artist.query.all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  look_for = '%{0}%'.format(search_term)
  items = Artist.query.filter(Artist.name.ilike(look_for)).all()
  response={
    'count': len(items),
    'data': items
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  data = get_form_object_for_artists(Artist.query.get(artist_id))
  return render_template('pages/show_artist.html', artist=data)

def get_form_object_for_artists(data):
  data.genres = data.genres.split(",")
  data = sep_shows(data, get_show_venue_ob)
  return data

  """
    seperate shows into past and future.
    Also adds the counts for past and future.
    You must pass the function which returns the 
    object to append to the upcoming shows.
  """
def sep_shows(data, get_ob_function):
  now = datetime.now()
  data.upcoming_shows = []
  data.past_shows = []
  
  for show in data.shows:
    if(datetime.strptime(show.start_time,"%Y-%m-%d %H:%M:%S") > now):
      data.upcoming_shows.append(get_ob_function(show))
    else:
      data.past_shows.append(get_ob_function(show))
  data.upcoming_shows_count = len(data.upcoming_shows)
  data.past_shows_count = len(data.past_shows)
  return data

"""
  populates an object with shows data. 
"""
def get_show_venue_ob(show):
  return {
        'start_time': show.start_time,
        'venue_image_link': show.venue.image_link,
        'venue_name': show.venue.name,
        'venue_id': show.venue_id
      }

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # TODO: populate form with fields from artist with ID <artist_id>
  artist=Artist.query.get(artist_id)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  # TODO: populate form with values from venue with ID <venue_id>
  venue=Venue.query.get(venue_id)
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
  try:
    # on successful db insert, flash success
    db.session.add(create_artist_from_form(request.form))
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()

  return render_template('pages/home.html')

"""
  Creates and returns the artist object 
  using the values in the passed form
"""
def create_artist_from_form(form):
  new_artist = Artist()
  new_artist.name = form['name']
  new_artist.city = form['city']
  new_artist.state = form['state']
  new_artist.phone = form['phone']
  new_artist.genres = form['genres']
  new_artist.facebook_link = form['facebook_link']
  new_artist.image_link = form['image_link']
  new_artist.website = form['website']
  return new_artist

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  data = []
  shows=Show.query.all()
  for show in shows:
    data.append({
      'artist_image_link': show.artist.image_link,
      'start_time': show.start_time,
      'artist_name': show.artist.name,
      'venue_name': show.venue.name,
      'venue_id': show.venue_id,
      'artist_id': show.artist_id
    })
  
  # data = Show.query.join(Venue, Show.venue_id == Venue.id).join(Artist, Artist.id == Show.artist_id).all()
  return render_template('pages/shows.html', shows=data) 

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  try:
    # on successful db insert, flash success
    db.session.add(create_show_from_form(request.form))
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

def create_show_from_form(form):
  new_show = Show()
  new_show.artist_id = form['artist_id']
  new_show.venue_id = form['venue_id']
  new_show.start_time = form['start_time']
  return new_show

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
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
