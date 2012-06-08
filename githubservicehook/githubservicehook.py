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
        import pdb; pdb.set_trace()
        if (request.path_info.rstrip('/') == ('/github/%s' % str(self.token))
            and request.method == 'POST'):
            request.form_token = None
            return True
        else:
            return False

    def process_request(self, request):
        data = request.args.get('payload')
        if data:
            jsondata = json.loads(data)
            for commit in jsondata['commits']:
                self.process_commit(commit)
        return 'Thanks!'

    def process_commit(self, commit):
        '''Process a new git commit.'''

        # Get the git commit message.
        msg = '''{author} [{url} {id}]

{message}'''.format(
                author=commit['author']['name'],
                url=commit['url'],
                id=commit['id'],
                message=commit['message'])

        # Find all the #123 strings in the commit message.
        ticket_re = re.compile('#[0-9]*')
        ticket_numbers = ticket_re.findall(msg)

        # Turn the ticket numbers into ints.
        ticket_numbers = [int(ticket_number[1:]) for ticket_number in
                ticket_numbers]

        for ticket_number in ticket_numbers:
            try:
                db = self.env.get_db_cnx()
                ticket = Ticket(self.env, int(ticket_number), db)
                ticket.save_changes('GitHubServiceHook', msg)
                db.commit()
            except ResourceNotFound, e:
                continue

