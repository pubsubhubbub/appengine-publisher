#
# Copyright 2007 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Simple publisher example that pings the hub after publishing."""

import logging
import os
import urllib

import jinja2
import webapp2

from google.appengine.api import urlfetch
from google.appengine.ext import db


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Message(db.Model):
  """A message to publish."""
  title = db.TextProperty(default='')
  content = db.TextProperty(default='')
  when = db.DateTimeProperty(auto_now_add=True)

  def get_zulu_time(self):
    return self.when.strftime('%Y-%m-%dT%H:%M:%SZ')


class MainHandler(webapp2.RequestHandler):
  """Allows users to publish new entries."""

  def get(self):
    context = dict(messages=Message.gql('ORDER BY when DESC').fetch(20))
    template = JINJA_ENVIRONMENT.get_template('input.html')
    self.response.out.write(template.render(context))

  def post(self):
    hub_url = self.request.get('hub')
    message = Message(title=self.request.get('title'),
                      content=self.request.get('content'))
    message.put()

    headers = {'content-type': 'application/x-www-form-urlencoded'}
    post_params = {
        'hub.mode': 'publish',
        'hub.url': self.request.host_url + '/feed'
    }
    payload = urllib.urlencode(post_params)
    try:
      response = urlfetch.fetch(hub_url, method='POST', headers=headers,
                                payload=payload)
    except urlfetch.Error:
      logging.exception('Failed to deliver publishing message to %s', hub_url)
    else:
      logging.info('URL fetch status_code=%d, content="%s"',
                   response.status_code, response.content)
    self.redirect('/')


class FeedHandler(webapp2.RequestHandler):
  """Renders an Atom feed of published entries."""

  def get(self):
    messages = Message.gql('ORDER BY when DESC').fetch(20)
    context = {
        'messages': messages,
        'source': self.request.host_url + '/feed',
    }
    if messages:
      context['first_message'] = messages[0]
    self.response.headers['content-type'] = 'application/xml'
    template = JINJA_ENVIRONMENT.get_template('atom.xml')
    self.response.out.write(template.render(context))


app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/feed', FeedHandler)],
                              debug=True)
