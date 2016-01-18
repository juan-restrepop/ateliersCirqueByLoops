__author__ = 'Loops'

## Imports
import os
import webapp2
import jinja2

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
        self.write('Bonjour les circassiens!')

class NewCourse(CircusAppHandler):
    def get(self):
        self.write("Cette page permettra d'ajouter un nouveau stage a la base de donnees")

class NewStudent(CircusAppHandler):
    def get(self):
        self.write("Cette page permettra d'ajouter un nouveau 'eleve' a la base de donnees")



### And the handler of everything
app = webapp2.WSGIApplication([('/', MainPage),
                                ('/ajouter-stage', NewCourse),
                                ('/ajouter-eleve', NewStudent)
                             ],
                              debug=True)