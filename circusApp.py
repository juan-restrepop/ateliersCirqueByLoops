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
        self.render('front.html')

class NewCourse(CircusAppHandler):
    def get(self):
        self.render('nouveau_stage.html')

class NewStudent(CircusAppHandler):
    def get(self):
        self.render('nouveau_eleve.html')



### And the handler of everything
app = webapp2.WSGIApplication([('/', MainPage),
                                ('/ajouter-stage', NewCourse),
                                ('/ajouter-eleve', NewStudent)
                             ],
                              debug=True)