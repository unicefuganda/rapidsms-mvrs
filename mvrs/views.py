from rapidsms_uganda_ussd.ussd.forms import YoForm
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import urllib
from ussd.models import *
from django.conf import settings
from tasks import forward_to_utl
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

def ussd_menu(req, input_form=YoForm, output_template='ussd/yo.txt'):
    form = input_form(req.REQUEST)
    if form and form.is_valid():
        session = form.cleaned_data['transactionId']
        request_string = form.cleaned_data['ussdRequestString']
        if request_string:
            logger.info('They Answered: %s' % request_string)
        #start caching for navigations>3
        if session.navigations.count()>=2:
            if not session.connection.identity in cache:
                sess= {'pk': session.pk, 'transaction_id': session.transaction_id}
                cache.set(session.connection.identity, sess, 1800)

        #submit input and advance to the next screen
        response_screen = session.advance_progress(request_string)
        if isinstance(response_screen,Menu):
            last_nav = Navigation.objects.order_by('-date').filter(session=session)[0]
            logger.info('We asked: %s' % last_nav.screen.downcast())
        else:
            question = response_screen.question if isinstance(response_screen,Question) else response_screen.label
            logger.info('We asked: %s' % question)

        #if we have already progressed to the last screen, the user must have put in a pin or cancelled, lets forward to UTL
        if response_screen.slug in settings.END_SCREENS:
            cache.delete(session.connection.identity)
            logger.info('Preparing to submit this data...')
            if request_string == '0':
                if response_screen.slug in ["delete_thank_you","validate_thank_you","val_thank_you"]:
                    response_screen = "Your request was not submitted. Please start again."
                elif response_screen.slug == "new_name_thank":
                    response_screen = "The information was not updated. Please start again."
                else:
                    response_screen = 'The information was not recorded. Please start again.'

                logger.info("Submission canceled by user... ")
            else:
                forward_to_utl(session)

            return render_to_response(output_template, {
                        'response_content':urllib.quote(str(response_screen)),
                        'action':'end',
                        }, context_instance=RequestContext(req))



        #is this a terminal screen or not?
        action = 'end' if response_screen.is_terminal() else 'request'

        #Determine if a resume option has been selected and serve the last dropped session    
        label = response_screen if type(response_screen) == unicode or type(response_screen) == str else response_screen.label
        if label == getattr(settings,'ROOT_MENU_DICT',None).get('resume'):
            if session.connection.identity in cache:
                ses=cache.get(session.connection.identity)
                prev_session=Session.objects.get(pk=ses.get('pk'))
                response_screen=prev_session.navigations.latest('date').text
                prev_session.transaction_id=session.transaction_id
                prev_session.save()
                session.delete()
                logger.info('Resumed Broken Session: %s' % prev_session.transaction_id)
            else:
                response_screen="You Have No Resumable Sessions"
                action = 'end'

        #TODO: handle skips
        return render_to_response(output_template, {
            'response_content':urllib.quote(str(response_screen)),
            'action':action,
            }, context_instance=RequestContext(req))

    logging.info('Status is 404...')
    return HttpResponse(status=404)

