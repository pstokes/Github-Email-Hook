#!/usr/bin/env python
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import mail
from django.utils import simplejson as json

import datetime
import iso8601

class MainHandler(webapp.RequestHandler):
    
    def post(self):
        data = json.loads(self.request.get('payload'))
        repo = '<a href="' + data['repository']['url'] + '">' + data['repository']['name'] + '</a>'
        repoDesc = data['repository']['description']
        branch = data['ref']
        
        email =  "<b>Repository: </b>" + data['repository']['name'] + "<br/>"
        email += "<b>Branch: </b>" + branch + "<br/>"
        email += "<b>Home: </b>" + repo
        
        for commit in data['commits']:
            time = iso8601.parse_date(commit['timestamp'])
            
            email += "<br/><br/><b>Commit: </b> " + '<a href="' + commit['url'] + '">' + commit['id'] + '</a><br/>'
            email += "<b>Author: </b>" + commit['author']['name'] + " (" + commit['author']['email'] + ")<br/>"
            email += "<b>Date: </b>" + time.strftime('%B %d, %Y %I:%M%p') + "<br/><br/>"
            
            email += "<b>Message: </b><i>" + commit['message'] + "</i><br/><br/>"
            
            ## MODIFIED FILES
            if len(commit['modified']) > 0:
                email +="<b><u>Modified Files</u></b><br/>"
              
                for modified in commit['modified']:
                    email += "&nbsp;&nbsp;" + modified + "<br/>"
            
            ## ADDED FILES
            if len(commit['added']) > 0:
                email +="<b><u>Added Files</u></b><br/>"
              
                for added in commit['added']:
                    email += "&nbsp;&nbsp;" + added + "<br/>"

            ## REMOVED FILES
            if len(commit['removed']) > 0:
                email +="<b><u>Removed Files</u></b><br/>"
              
                for removed in commit['removed']:
                    email += "&nbsp;&nbsp;" + removed + "<br/>"
            
            email += "<br/>----------------------"
        
        email += '<br/><img src="http://d2ztt7pe7ibsob.cloudfront.net/pushit.jpg" alt="Push it REAL Good"/>'
        
        ## ASSIGN THE FROM ADDRESS
        fromAddress = ""
        
        ## SEND THE EMAIL
        mail.send_mail(sender=fromAddress,
              to=self.request.get('sendto'),
              subject=data['repository']['name'] + " Push on " + branch,
              body=email,html=email)


def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
