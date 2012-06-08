import json
import re
from trac.core import *
from trac.config import Option
from trac.web import IRequestHandler
from trac.ticket import Ticket
from trac.resource import ResourceNotFound

class GitHubServiceHookPlugin(Component):
    implements(IRequestHandler)

    token = Option('githubservicehook', 'token', '')

    def match_request(self, request):
        self.env.log.debug(
            "match_request: {method} -> {path}".format(
            method=request.method, path=request.path_info))
        if (request.path_info.rstrip('/') == ('/github/%s' % str(self.token))
            and request.method == 'POST'):
            request.form_token = None
            self.env.log.debug('accepted request')
            return True
        else:
            self.env.log.debug('refused request')
            return False

    def process_request(self, request):
        self.env.log.debug(
            "process_request: {method} -> {path}".format(
            method=request.method, path=request.path_info))
        data = request.args.get('payload')
        if data:
            jsondata = json.loads(data)
            self.env.log.debug('got json')
            for commit in jsondata['commits']:
                self.process_commit(commit)
        content = "Thanks!"
        request.send_response(200)
        request.send_header('Content-Type', 'text/plain')
        request.send_header('Content-Length', len(content))
        request.end_headers()
        request.write(content)

    def process_commit(self, commit):
        '''Process a new git commit.'''
        self.env.log.debug('process_commit: {commit}'.format(commit=commit))

        # Get the git commit message.
        msg = '''{author} [{url} {id}]

{{{{{{
{message}
}}}}}}
'''.format(author=commit['author']['name'],
           url=commit['url'],
           id=commit['id'],
           message=commit['message'])

        # Find all the #123 strings in the commit message.
        ticket_re = re.compile('#[0-9]*')
        ticket_numbers = ticket_re.findall(msg)

        # Turn the ticket numbers into ints.
        ticket_numbers = set([int(ticket_number[1:]) for ticket_number in
                ticket_numbers])

        for ticket_number in ticket_numbers:
            self.env.log.debug(
                'Found ticket number: {n}'.format(n=str(ticket_number)))
            try:
                db = self.env.get_db_cnx()
                ticket = Ticket(self.env, int(ticket_number), db)
                ticket.save_changes('GitHubServiceHook', msg)
                db.commit()
                self.env.log.debug('Comment added')
            except ResourceNotFound, e:
                self.env.log.debug(
                    'Ticket not found: {n}'.format(n=str(ticket_number)))
                continue
