#!/usr/bin/env python
import logging
from urllib2 import Request, urlopen, URLError

from django.core.mail import send_mail
from django.core.management.base import NoArgsCommand

__author__ = 'Saimon Rai'
__copyright__ = 'Copyright 2014 Poolsidelabs Inc.'

logger = logging.getLogger(__name__)
SCHEDULE_URL = 'http://nea.org.np/images/supportive_docs/8619loadshedding.pdf'
CACHED_ETAG = '"9e0290-1a4ec-4f1c7214a87f9"'  # Make sure that the quotes are contained.


class Command(NoArgsCommand):
    """
    Sends an email if new schedule is available.
    """
    def handle_noargs(self, **options):
        msg = None

        req = Request("http://nea.org.np/loadshedding.html")
        try:
            response = urlopen(req, timeout=60)  # set the timeout to 60 seconds
            has_changed = SCHEDULE_URL not in response.read()
            if has_changed:
                msg = "Schedule has most likely changed. '" + SCHEDULE_URL + "' is not found in the webpage."
        except URLError as e:
            if hasattr(e, 'reason'):
                msg = 'Failed to reach server. reason: %s' % e.reason
            elif hasattr(e, 'code'):
                msg = 'The server could not fulfill the request. error_code: %d' % e.code

        if msg:
            msg += " Website: http://nea.org.np/loadshedding.html"
            logger.info(msg + " Notifying via email...")
            send_mail('Load Shedding Schedule (' + msg + ')', msg, 'saimonrai@gmail.com',
                      ['saimonrai@gmail.com'], fail_silently=False)
        else:
            logger.info("New schedule not available.")



#        msg = None
#
#        req = Request(SCHEDULE_URL)
#        try:
#            response = urlopen(req)
#            etag = response.headers.getheader('ETag')
#            logger.info("ETag received: %s, cached: %s", etag, CACHED_ETAG)
#
#            if not etag:
#                msg = "Server responded with ETag header not present."
#            elif etag != CACHED_ETAG:
#                msg = "ETag mismatch! Received: %s, Cached: %s" % (etag, CACHED_ETAG)
#
#        except URLError as e:
#            if hasattr(e, 'reason'):
#                msg = 'Failed to reach server. reason: %s' % e.reason
#            elif hasattr(e, 'code'):
#                msg = 'The server could not fulfill the request. error_code: %d' % e.code
#
#        if not msg:
#            logger.info("New schedule not available.")
#        else:
#            logger.info("New schedule available OR the server is not responding. Notifying via email...")
#            msg = msg + ", url: " + SCHEDULE_URL
#            send_mail('Load Shedding Schedule', msg, 'saimonrai@gmail.com',
#                ['saimonrai@gmail.com'], fail_silently=False)



