r"""

Description
^^^^^^^^^^^
GET a specific webpage. Useful for notifying web services of a git push.

Arguments
^^^^^^^^^
<*URL*>

* **Example**: ``http://jenkins.company.com/git/notifyCommit?url=git/foo.git``
    * Grab the Jenkins URL for new git push notifications.

Suggestion
^^^^^^^^^^
Run on last_commit as a post-receive hook.

"""

import sys
import urllib2

sys.path.append('..')
from libhookkit import HookScript


class ping_url(HookScript):

    def run(self, _old_sha1, _new_sha1, _ref):
        success = True

        try:
            connection = urllib2.urlopen(self.args)
            if connection.getcode() != 200:
                success = False
            connection.close()
        except urllib2.HTTPError, exception:
            print "There was an error trying to ping the url:" + self.args
            print "Error:"
            print exception
            success = False

        return success
