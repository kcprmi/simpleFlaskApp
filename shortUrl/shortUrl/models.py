from shortUrl import db

class Link(db.Model):

    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(2000), unique=True)
    short_url = db.Column(db.String(5))
    domain = db.Column(db.String(64))
    entries = db.Column(db.Integer, default = 0)

    def __init__(self, long_url, short_url, domain, entries):
        self.long_url = long_url
        self.short_url = short_url
        self.domain = domain
        self.entries = entries 

    def __repr__(self):
        return f"{self.id}, {self.long_url}, {self.short_url}, {self.domain}, {self.entries}" 