from flask import Flask, Blueprint, redirect, render_template, request 
from shortUrl import db
from shortUrl.models import Link
from shortUrl.forms import UrlForm
from sqlalchemy import func
from urllib.parse import urlparse

import string
import random

# Generate short URL string
def generate_short_url():
    # Characters allowed in URL's
    characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd',
                'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7',
                '8', '9', '-', '_', '.', '!', '~', '*', "'"]
    short_url = ''.join(random.choice(characters) for i in range(5))
    return short_url

# Get domain from long_url
def get_domain(x):
    f = urlparse(x)
    return f[1]

#Blueprint
main = Blueprint('main',__name__)

# index view
@main.route('/', methods = ['GET', 'POST'])
def index():
    
    form = UrlForm()
    # Handle the form submission
    if form.validate_on_submit():
        # Get the host domain of the current request
        current_domain = request.host
        long_url = form.long_url.data
        links = Link.query.all()
        # Prepare a list of existing long URLs to check for duplicates
        list_long_urls = [link.long_url for link in links]
        
        # If the submitted long URL already exists, get the corresponding short URL
        if long_url in list_long_urls:
            record = Link.query.filter_by(long_url = long_url).first()
            short_url = record.short_url
         
        else:
             # Prepare a list of existing short URLs to avoid collisions
            list_short_urls = [link.short_url for link in links]
            short_url = generate_short_url()   
             # Keep generating a new short URL until it is unique
            while short_url in list_short_urls:
                short_url = generate_short_url()   
            
            # Get the domain from the long URL
            domain = get_domain(long_url)
            entries = 0
            # Create a new link record
            new_link = Link(long_url, short_url, domain, entries)
            # Add the new link to the database and commit
            db.session.add(new_link)
            db.session.commit()
        
         # Show the result to the user with the generated short URL
        return render_template('result.html', long_url = long_url, short_url = short_url, current_domain=current_domain)
    
    # Render the index page with the URL form
    return render_template('index.html', form = form)

# Route to display statistics about domain and their link entries
@main.route('/list')
def list_rep():
    list_of_domains = db.session.query(Link.domain, func.sum(Link.entries)).group_by(Link.domain).all()
    return render_template('list.html', list_of_domains = list_of_domains)

# Route to handle redirection from a short URL to the original long URL
@main.route('/<short_url>')
def redirect_to_original(short_url):
    record = Link.query.filter_by(short_url = short_url).first()
    long_url = record.long_url
    
    # If a record is found, increment the number of entries and redirect to the long URL
    if long_url:
        record = Link.query.filter_by(long_url = long_url).first()
        e = record.entries
        record.entries = e + 1
        db.session.add(record)
        db.session.commit()
        try:
            return redirect(long_url)
        except:
            return render_template('404.html')

@main.errorhandler(500)
def page_not_found(error):
    return render_template('500.html'), 500

@main.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
    
