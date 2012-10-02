from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from rapidsms_xforms.models import XFormField, XForm
from ussd.models import Menu, Field, StubScreen

class Creator(object):
    def __init__(self):
        self.root_menu = Menu.objects.create(label='Root Menu',slug='ussd_root',order=1)
        self.edit_info = Menu.objects.create(label='Edit Record',slug = 'edit_record',order=3, parent=self.root_menu)
        self.user_management = Menu.objects.create(label='User Management', slug="user_management",parent=self.root_menu, order=4)

        xform = XForm.objects.create(keyword='test', name='test xform', response='thanks for testing', owner=User.objects.get(username='kenneth'), site=Site.objects.get_current())


        self.thank_msg = StubScreen.objects.create(slug="thank_msg", text='Thank you for recording a new birth! You will  receive a confirmation message with the summary of the record and the registration number')
        field10 = XFormField.objects.create(xform=xform, name='birth_summary', field_type=XFormField.TYPE_INT, command='e', question='Enter Pin to comfirm or 0 to cancel', order=1)
        self.summary = Field.objects.create(slug="birth_summary",
            field = field10,
            question_text=field10.question,
            label= 'Birth Summary',
            order = 0,
            next = self.thank_msg)
        field9 = XFormField.objects.create(xform=xform, name='father_nationality', field_type=XFormField.TYPE_TEXT, command='e1', question='Select father\'s nationality:\n1. Uganda\n2. Kenya\n3. Tanzania\n4. Rwanda\nOthers (Type in the country manually)', order=1)
        self.father_nationality = Field.objects.create(slug="father_nationality",
            field = field9,
            question_text=field9.question,
            label= 'Father\'s Nationality',
            order = 0,
            next = self.summary)
        field8 = XFormField.objects.create(xform=xform, name='father_name', field_type=XFormField.TYPE_TEXT, command='e2', question='Enter father\'s names:', order=1)
        self.father_name = Field.objects.create(slug="father_name",
            field = field8,
            question_text=field8.question,
            label= 'Father\'s Name',
            order = 0,
            next = self.father_nationality)
        field7 = XFormField.objects.create(xform=xform, name='mother_nationality', field_type=XFormField.TYPE_TEXT, command='e3', question='Select mother\'s nationality:\n1. Uganda\n2. Kenya\n3. Tanzania\n4. Rwanda\nOthers (Type in the country manually)', order=1)
        self.mother_nationality = Field.objects.create(slug="mother_nationality",
            field = field7,
            question_text=field7.question,
            label= 'Mother\'s Nationality',
            order = 0,
            next = self.father_name)
        field6 = XFormField.objects.create(xform=xform, name='mother_name', field_type=XFormField.TYPE_TEXT, command='e4', question='Enter mother\'s names:', order=1)
        self.mother_name = Field.objects.create(slug="mother_name",
            field = field6,
            question_text=field6.question,
            label= 'Mother\'s name',
            order = 0,
            next = self.mother_nationality)
        field5 = XFormField.objects.create(xform=xform, name='child_sex', field_type=XFormField.TYPE_INT, command='e5', question='Select the sex of the child:\n 1. Male\n 2. Female', order=1)
        self.sex = Field.objects.create(slug="child_sex",
            field = field5,
            question_text=field5.question,
            label= 'Child\'s Sex',
            order = 0,
            next = self.mother_name)
        field4 = XFormField.objects.create(xform=xform, name='birth_date', field_type=XFormField.TYPE_INT, command='e6', question='Enter date of birth:\n1. Today\n2. Yesterday\nOther (Enter manually in the format ddmmyyyy) ', order=1)
        self.date_of_birth = Field.objects.create(slug="birth_date",
            field = field4,
            question_text=field4.question,
            label= 'Date of Birth',
            order = 0,
            next = self.sex)
        field3 = XFormField.objects.create(xform=xform, name='other_name', field_type=XFormField.TYPE_TEXT, command='e7', question='Enter child\'s other name(s):', order=1)
        self.first_name = Field.objects.create(slug="other_name",
            field = field3,
            question_text=field3.question,
            label= 'Child Name',
            order = 0,
            next = self.date_of_birth)

        #        This is where the birth menu stops.
        #        This is where death menu starts
        self.death_msg = StubScreen.objects.create(slug="death_thank_you", text='Thank you for recording a new death. Please inform relatives to present themselves at the Registrars office to complete the process')
        field21 = XFormField.objects.create(xform=xform, name='death_summary', field_type=XFormField.TYPE_INT, command='e8', question='Enter Pin to comfirm or 0 to cancel', order=1)
        self.summary_death = Field.objects.create(slug="death_summary",
            field = field21,
            question_text=field21.question,
            label= 'Death Summary',
            order = 0,
            next = self.death_msg)

        field19 = XFormField.objects.create(xform=xform, name='death_reporter_capacity', field_type=XFormField.TYPE_TEXT, command='e9', question='Capacity:\n1.Relative present at Death\n2.Other Relative\n3.Person present at death\n4.House occupant at location\n5.Person with knowledge\n6. Person finding  body', order=1)
        self.death_reporter_capacity = Field.objects.create(slug="death_reporter_capacity",
            field = field19,
            question_text=field19.question,
            label= 'Declarant Capacity',
            order = 0,
            next = self.summary_death)

        field18 = XFormField.objects.create(xform=xform, name='death_reporter_phone', field_type=XFormField.TYPE_TEXT, command='e10', question='Declarant\'s Phone Number:', order=1)
        self.deceased_reporter_phone = Field.objects.create(slug="death_reporter_phone",
            field = field18,
            question_text=field18.question,
            label= 'Declarant Phone Number',
            order = 0,
            next = self.death_reporter_capacity)

        field17 = XFormField.objects.create(xform=xform, name='death_reporter', field_type=XFormField.TYPE_TEXT, command='e11', question='Names of Declarant:', order=1)
        self.deceased_reporter = Field.objects.create(slug="death_reporter",
            field=field17,
            question_text=field17.question,
            label= 'Declarant Name',
            order = 0,
            next = self.deceased_reporter_phone)

        field16 = XFormField.objects.create(xform=xform, name='death_date', field_type=XFormField.TYPE_INT, command='e12', question='Date of death (ddmmyyyy):', order=1)
        self.deceased_date = Field.objects.create(slug="death_date",
            field=field16,
            question_text=field16.question,
            label= 'Deceased Date',
            order = 0,
            next = self.deceased_reporter)

        field15 = XFormField.objects.create(xform=xform, name='death_sex', field_type=XFormField.TYPE_INT, command='e13', question='Sex of the deceased:\n1. Male\n2. Female', order=1)
        self.deceased_sex = Field.objects.create(slug="death_sex",
            field=field15,
            question_text=field15.question,
            label= 'Deceased Sex',
            order = 0,
            next = self.deceased_date)

        field14 = XFormField.objects.create(xform=xform, name='death_age', field_type=XFormField.TYPE_INT, command='e14', question='Age of the deceased:', order=1)
        self.deceased_age = Field.objects.create(slug="death_age",
            field=field14,
            question_text=field14.question,
            label= 'Deceased Age',
            order = 0,
            next = self.deceased_sex)

        #       This is where the death menu stops

        field1 = XFormField.objects.create(xform=xform, name='child_first_name', field_type=XFormField.TYPE_TEXT, command='e15', question='Enter child\'s first name:', order=0)
        self.notify_birth = Field.objects.create(slug="child_first_name",
            field=field1,
            question_text=field1.question,
            parent=self.root_menu,
            label= 'Notify Birth',
            order = 1,
            next = self.first_name)
        field2 = XFormField.objects.create(xform=xform, name='death_name', field_type=XFormField.TYPE_TEXT, command='e16', question='Enter names of the Deceased:', order=1)
        self.notify_death = Field.objects.create(slug="death_name",
            field = field2,
            question_text = field2.question,
            parent=self.root_menu,
            label = 'Notify Death',
            order = 2,
            next = self.deceased_age)


        efield9 = XFormField.objects.create(xform=xform, name='e_thank_you', field_type=XFormField.TYPE_TEXT, command='u1', question='Thank you', order=1)
        thank_you = Field.objects.create(slug="e_thank_you",
            field = efield9,
            question_text=efield9.question,
            label= 'thank you',
            order = 0,
            next = StubScreen())

        efield8 = XFormField.objects.create(xform=xform, name='e_confirm', field_type=XFormField.TYPE_TEXT, command='u2', question='Enter  PIN to confirm or "0" to cancel', order=1)
        confirm = Field.objects.create(slug="e_confirm",
            field = efield8,
            question_text=efield8.question,
            label= 'Confirm',
            order = 0,
            next = thank_you)

        efield7 = XFormField.objects.create(xform=xform, name='e_parish_or_ward', field_type=XFormField.TYPE_TEXT, command='u3', question='Enter User\'s parish or ward:', order=1)
        parish = Field.objects.create(slug="e_parish_or_ward",
            field = efield7,
            question_text=efield7.question,
            label= 'Parish or Ward',
            order = 0,
            next = confirm)

        efield6 = XFormField.objects.create(xform=xform, name='e_phone', field_type=XFormField.TYPE_TEXT, command='u4', question='Enter user\'s phone number:', order=1)
        phone = Field.objects.create(slug="e_phone",
            field = efield6,
            question_text=efield6.question,
            label= 'Phone Number',
            order = 0,
            next = parish)

        efield5 = XFormField.objects.create(xform=xform, name='e_birth_date', field_type=XFormField.TYPE_TEXT, command='u5', question='Enter User\'s Date of Birth (ddmmyyyy):', order=1)
        birth_date = Field.objects.create(slug="e_birth_date",
            field = efield5,
            question_text=efield5.question,
            label= 'Birth Date',
            order = 0,
            next = phone)

        efield4 = XFormField.objects.create(xform=xform, name='e_gender', field_type=XFormField.TYPE_INT, command='u6', question='Enter User\'s sex:\n1. Male\n2. Female', order=1)
        gender = Field.objects.create(slug="e_gender",
            field = efield4,
            question_text=efield4.question,
            label= 'Gender',
            order = 0,
            next = birth_date)

        efield3 = XFormField.objects.create(xform=xform, name='e_other_name', field_type=XFormField.TYPE_TEXT, command='u7', question='Enter User\'s other names:', order=1)
        other_name = Field.objects.create(slug="e_other_name",
            field = efield3,
            question_text=efield3.question,
            label= 'Other Names',
            order = 0,
            next = gender)

        efield1 = XFormField.objects.create(xform=xform, name='create_user', field_type=XFormField.TYPE_TEXT, command='u8', question='Enter User\'s Surname:', order=1)
        create_user = Field.objects.create(slug="create_user",
            field = efield1,
            question_text=efield1.question,
            label= 'Create User',
            order = 1,
            parent = self.user_management,
            next = other_name)

        self.resume = StubScreen.objects.create(slug='resume',label='Resume Previous', parent=self.root_menu,order=5, terminal=False)



def addModifyPinMenu():
    xform = XForm.objects.get(keyword='test')
    efield9 = XFormField.objects.create(xform=xform, name='pin_confirm', field_type=XFormField.TYPE_TEXT, command='m5', question='You will receive a message to confirm the change of your PIN. Protect your PIN. Keep it secret. Do not share it.', order=1)
    end = Field.objects.create(slug="pin_confirm",
        field = efield9,
        question_text=efield9.question,
        label= 'pin End',
        order = 0,
        next = StubScreen())
    efield4 = XFormField.objects.create(xform=xform, name='new_pin_again', field_type=XFormField.TYPE_TEXT, command='m3', question='Re-enter new PIN:', order=1)
    new_pin_again = Field.objects.create(slug="new_pin_again",
        field = efield4,
        question_text=efield4.question,
        label= 'New Pin Again',
        order = 0,
        next = end)

    efield3 = XFormField.objects.create(xform=xform, name='new_pin', field_type=XFormField.TYPE_TEXT, command='m1', question='Enter new PIN:', order=1)
    new_pin = Field.objects.create(slug="new_pin",
        field = efield3,
        question_text=efield3.question,
        label= 'New Pin',
        order = 0,
        next = new_pin_again)

    efield2 = XFormField.objects.create(xform=xform, name='edit_user', field_type=XFormField.TYPE_TEXT, command='m2', question='Enter old PIN:', order=1)
    edit_user = Field.objects.get(slug='modify_pin')
    edit_user.field = efield2
    edit_user.next = new_pin
    edit_user.save()


def changeMainMenu():
    root_menu = Menu.objects.get(slug='ussd_root')
    user_management = Menu.objects.get(slug="user_management")
    user_management.order = 5
    user_management.save()
    resume = StubScreen.objects.get(slug='resume')
    resume.order = 6
    resume.save()
    validation = Menu.objects.create(label='Validation', slug="validation",parent=root_menu, order=4)

def addViewRecordIntoValidation():
    xform = XForm.objects.get(keyword='test')
    validation = Menu.objects.get(slug="validation")
    field1 = XFormField.objects.create(xform=xform, name='val_thank_you', field_type=XFormField.TYPE_TEXT, command='v3', question='Thank you. You will receive a message with a summary of this record.', order=1)
    val_thank_you = Field.objects.create(slug="val_thank_you",
        field = field1,
        question_text=field1.question,
        label= 'Thank you',
        order = 1,
        next = StubScreen())
    field = XFormField.objects.create(xform=xform, name='val_pin', field_type=XFormField.TYPE_TEXT, command='v2', question='View Record\n\nEnter  PIN to confirm or "0" to cancel', order=1)
    val_pin = Field.objects.create(slug="val_pin",
        field = field,
        question_text=field.question,
        label= 'View Record',
        order = 1,
        next = val_thank_you)
    field3 = XFormField.objects.create(xform=xform, name='view_record', field_type=XFormField.TYPE_TEXT, command='v1', question='Enter reference number:', order=1)
    view_record = Field.objects.create(slug="view_record",
        field = field3,
        question_text=field3.question,
        label= 'View Record',
        order = 1,
        parent = validation,
        next = val_pin)

def addValidateIntoValidation():
    xform = XForm.objects.get(keyword='test')
    validation = Menu.objects.get(slug="validation")
    field1 = XFormField.objects.create(xform=xform, name='validate_thank_you', field_type=XFormField.TYPE_TEXT, command='v7', question='Thank you for validating this record. You will receive a confirmation message.', order=1)
    val_thank_you = Field.objects.create(slug="validate_thank_you",
        field = field1,
        question_text=field1.question,
        label= 'Thank you',
        order = 1,
        next = StubScreen())
    field = XFormField.objects.create(xform=xform, name='validate_pin', field_type=XFormField.TYPE_TEXT, command='v6', question='Validate Record\n\nEnter  PIN to confirm or "0" to cancel', order=1)
    val_pin = Field.objects.create(slug="validate_pin",
        field = field,
        question_text=field.question,
        label= 'Validate Pin',
        order = 1,
        next = val_thank_you)
    field1 = XFormField.objects.create(xform=xform, name='reenter', field_type=XFormField.TYPE_TEXT, command='v5', question='Re-enter reference number:', order=1)
    renter = Field.objects.create(slug="reenter",
        field = field1,
        question_text=field1.question,
        label= 'Re-enter Validate Pin',
        order = 0,
        next = val_pin)
    field3 = XFormField.objects.create(xform=xform, name='validate_record', field_type=XFormField.TYPE_TEXT, command='v4', question='Enter reference number:', order=1)
    validate_record = Field.objects.create(slug="validate_record",
        field = field3,
        question_text=field3.question,
        label= 'Validate',
        order = 2,
        parent = validation,
        next = renter)

def addDeleteIntoValidation():
    xform = XForm.objects.get(keyword='test')
    validation = Menu.objects.get(slug="validation")
    field1 = XFormField.objects.create(xform=xform, name='delete_thank_you', field_type=XFormField.TYPE_TEXT, command='d3', question='Thank you for updating the civil registry! You will receive a confirmation message.', order=1)
    val_thank_you = Field.objects.create(slug="delete_thank_you",
        field = field1,
        question_text=field1.question,
        label= 'Thank you',
        order = 1,
        next = StubScreen())
    field = XFormField.objects.create(xform=xform, name='delete_pin', field_type=XFormField.TYPE_TEXT, command='d2', question='Delete Record\n\nEnter  PIN to confirm or "0" to cancel', order=1)
    delete_pin = Field.objects.create(slug="delete_pin",
        field = field,
        question_text=field.question,
        label= 'Delete Pin',
        order = 1,
        next = val_thank_you)
    field1 = XFormField.objects.create(xform=xform, name='del_reenter', field_type=XFormField.TYPE_TEXT, command='d1', question='Re-enter reference number:', order=1)
    renter = Field.objects.create(slug="del_reenter",
        field = field1,
        question_text=field1.question,
        label= 'Re-enter Validate Pin',
        order = 0,
        next = delete_pin)
    field3 = XFormField.objects.create(xform=xform, name='delete_record', field_type=XFormField.TYPE_TEXT, command='d', question='Enter reference number:', order=1)
    delete_record = Field.objects.create(slug="delete_record",
        field = field3,
        question_text=field3.question,
        label= 'Delete',
        order = 3,
        parent = validation,
        next = renter)