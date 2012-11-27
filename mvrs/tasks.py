from django.conf import settings
from utils import get_summary_dict, get_dictionary_for_session
import urllib2, urllib
import logging
from celery.task import Task
#noinspection PyUnresolvedReferences
from celery.registry import tasks

logger = logging.getLogger(__name__)

def forward_to_utl(session,**kwargs):
    try:
        logger.info("forwarding to utl...")
        collected_data = get_summary_dict(session, get_dictionary_for_session(session))
        result = urllib2.urlopen('%s?%s' % (settings.FORWARD_URL,urllib.urlencode(collected_data)))
        logger.info('Submitting to UTL: %s' % result.url)
        result_info = result.read().strip() if result.getcode() == 200 else 'Bad Status (%d) from UTL'%result.getcode()
        logger.info('UTL Replied: %s' % result_info)
        return str(result_info)
    except Exception,e:
        logger.error(e)
        return "Something went wrong at UTL"

class ForwardToTel(Task):
    def run(self,session,**kwargs):
        try:
            logger.info("forwarding to utl...")
            collected_data = get_summary_dict(session, get_dictionary_for_session(session))
            result = urllib2.urlopen('%s?%s' % (kwargs.get('forward_url'),urllib.urlencode(collected_data)))
            logger.info('Submitting to UTL: %s' % result.url)
            logger.info('UTL Replied: %s' % result.read().strip())
        except Exception,e:
            logger.error(e)

tasks.register(ForwardToTel)
