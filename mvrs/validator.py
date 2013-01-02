from datetime import datetime
from django.core.exceptions import ValidationError
from rapidsms_xforms.models import XFormField
import re

def _parse_pin(command,value): return value


def _parse_name(command,value):
    names,name_list = value.split(" "),[]
    if value.strip() == "0":return value
    if len(names) > 1:
        for name in names:
            name = name.strip().lower().capitalize()
            if not re.match(r'^([a-zA-Z]+)$',name) or len(name) < 2:raise ValidationError('All names should be valid names')
            name_list.append(name)
        return " ".join(name_list)
    raise ValidationError('At least two names are required, (%d) given'%len(names))

def _parse_name_single(command,value):
    name = value.strip().lower().capitalize()
    if name =="0":return name
    if not re.match(r'^([a-zA-Z]+)$',name) or len(name)<2:raise ValidationError('The name looks invalid or too short (Should be 1 name)')
    return value


def _parse_date(command,value):
    if not re.match(r'^([0-9]{8})$',value): raise ValidationError('Invalid date. Date should look like - 02091990')
    try:datetime(int(value[4:8]),int(value[2:4]),int(value[0:2]))
    except ValueError, e:raise ValidationError(str(e))
    return value

def _parse_child_date_of_birth(command,value):
    if value in ["1","2"]: return value
    if not re.match(r'^([0-9]{8})$',value): raise ValidationError('Invalid date. Date should look like - 02091990')
    try:datetime(int(value[4:8]),int(value[2:4]),int(value[0:2]))
    except ValueError, e:raise ValidationError(str(e))
    return value

def register_custom_field_types():
    XFormField.register_field_type('pin', 'Pin', _parse_pin,xforms_type='string', db_type=XFormField.TYPE_INT)
    XFormField.register_field_type('name_val', 'Name',_parse_name)
    XFormField.register_field_type('date_val','Date',_parse_date)
    XFormField.register_field_type('date_c','CDate',_parse_child_date_of_birth)
    XFormField.register_field_type('sex_val','Sex',_parse_pin, db_type=XFormField.TYPE_INT)
    XFormField.register_field_type('nat_val','Nationality',_parse_pin, db_type=XFormField.TYPE_INT)
    XFormField.register_field_type('name_sal','SName',_parse_name_single)