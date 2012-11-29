#   Hook Name: ping-url
#   Arguments: URL
# Description: Used to GET a url. Useful for nofiying services such as CI, etc.
#  Suggestion: Run on last_commit as a post-preceive hook
#      Author: Jesper Thomschutz (jesper@jespersaur.com)

import sys
import urllib2

sys.path.append('..')
from libhookkit import HookScript


class ping_url(HookScript):

    def run(self, old_sha1, new_sha1, ref):
        success = True

        try:
            connection = urllib2.urlopen(self.args)
            if connection.getcode() != 200:
                success = False
            connection.close()
        except urllib2.HTTPError, e:
            print "There was an error trying to ping the url:" + self.args
            print "Error:"
            print e
            success = False

        return success
