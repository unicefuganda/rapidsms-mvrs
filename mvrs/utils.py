'''
Created on Jul 12, 2012

@author: asseym
'''
from django.core.exceptions import ValidationError
import re
from django.conf import settings
from rapidsms_xforms.models import XFormField

def dictinvert(dict):
    inv = {}
    for k, v in dict.iteritems():
        inv[v]=k
    return inv



def get_summary_dict(session, ussd_menu_dict):
    results = {}
    action = ussd_menu_dict['ACTION']
    pin = None
    keys=dictinvert(ussd_menu_dict)
    for nav in session.navigations.all():
        if nav.screen.downcast().slug in settings.PIN_SLUGS:
            pin = nav.response
        else:
            if keys.has_key(nav.screen.downcast().slug):
                results[keys.get(nav.screen.downcast().slug)] = nav.response
    results['SESSION'] = session.transaction_id
    results['MSISDN'] = session.connection.identity
    results['PIN'] = pin
    results['ACTION'] = action
    return results

def get_session_data_turples(session, ussd_menu_dict, action):
    
    results = ussd_menu_dict
    pin = None
    keys=dictinvert(ussd_menu_dict)
    for nav in session.navigations.all():
        val = settings.TRANSLATION_DICT.get(nav.screen.downcast().slug,None)
        if val in ["death_summary","birth_summary"]:
            pin = nav.screen.downcast().slug
        if val:
            results[keys.get(nav.screen.downcast().slug)] = nav.response
    results['SESSION'] = 1123
    results['MSISDN'] = session.connection.identity
    results['PIN'] = pin
    results['ACTION'] = action
    
    return results.items()


def get_summary(session):
    summary = ""
    for nav in session.navigations.all():
        val = settings.TRANSLATION_DICT.get(nav.screen.downcast().slug,None)
        if val:
            summary += "%s %s " % (val, nav.response)
    return summary


def get_dictionary_for_session(session):
    def _all_match(session, positions):
        for position in range(len(positions)):
            if not session.navigations.order_by('date')[position].response== str(positions[position]):
                return False
        return True
    for dict in [getattr(settings,d) for d in dir(settings) if d.startswith('UTL_')]:
        if _all_match(session,dict['positions']):
            return dict
    raise Exception('Dictionary for this session cannot be found in session %s' %session.id)

def _parse_pin(command,value): return value

def _parse_name(command,value):
    names,name_list = value.split(" "),[]
    if value.trim() == "0":
        return value
    if len(names) == 2:
        for name in names:
            name = name.trim().lower().capitalize()
            if not re.match(r'^([a-zA-Z]+)$',name):
                raise ValidationError('Both names should be valid names')
            name_list.append(name)
        return " ".join(name_list)
    raise ValidationError('Two names are required')

def register_custom_field_types():
    XFormField.register_field_type('pin', 'Pin', _parse_pin,xforms_type='string', db_type=XFormField.TYPE_INT)
    XFormField.register_field_type('name_val', 'Name',_parse_name)

