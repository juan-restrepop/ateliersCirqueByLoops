__author__ = 'Loops'

## Imports
import os
import webapp2
import jinja2
import re

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

## Basic template rendering ##
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

## The Basic web page handler class ##
class CircusAppHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

## The main page ##
class MainPage(CircusAppHandler):
    def get(self):
        self.render('front.html')

## New course page ##
class NewCourse(CircusAppHandler):
    def get(self):
        self.render('nouveau_stage.html')

## New student page ##
# Regular expression to check inputs #
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

TEL_RE = re.compile(r"^[0-9_-]{10}$")
def valid_telephone(telephone):
    return not telephone or TEL_RE.match(telephone)


class NewStudent(CircusAppHandler):
    def get(self):
        self.render('nouveau_eleve.html')

    def post(self):
        have_error = False
        self.nom = self.request.get('nom')
        self.prenom = self.request.get('prenom')
        self.age = self.request.get('age')
        self.sexe = self.request.get('sexe')
        self.email = self.request.get('email')
        self.telephone = self.request.get('telephone')
        self.location = self.request.get('location')

        params = dict(nom = self.nom,
                      prenom = self.prenom,
                      age = self.age,
                      email=self.email,
                      telephone=self.telephone)

        if not self.nom :
            params['error_nom'] = "Un nom siouple"
            have_error = True

        if not self.prenom:
            params['error_prenom'] = "Un prenom siouple"
            have_error = True

        if not self.age:
            params['error_age'] = "L' age siouple"
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "Email invalide"
            have_error = True

        if not valid_telephone(self.telephone):
            params['error_telephone'] = "Telephone invalable"
            have_error = True

        if have_error:
            self.render('nouveau_eleve.html', **params)
        else:
            self.done()

    def done(self):
        raise NotImplementedError

class NewStudentRegistration(NewStudent):
    def done(self):
        self.redirect('ajouter-eleve/bienvenue?nom=' + self.nom + '&prenom=' + self.prenom)


class Bienvenue(CircusAppHandler):
    def get(self):
        nom = self.request.get('nom')
        prenom = self.request.get('prenom')

        self.render('bienvenue.html', nom = nom, prenom = prenom)

### And the handler of everything
app = webapp2.WSGIApplication([('/', MainPage),
                                ('/ajouter-stage', NewCourse),
                                ('/ajouter-eleve', NewStudentRegistration),
                                ('ajouter-eleve/bienvenue', Bienvenue)
                             ],
                              debug=True)