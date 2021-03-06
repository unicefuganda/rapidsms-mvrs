from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.client import Client
from django.conf import settings
import urllib2
import urllib
import datetime
import logging

logger = logging.getLogger(__name__)

class ViewTest(TestCase):

    def setUp(self):
        self.transactionId = '123344'
        self.transactionTime = datetime.datetime.now().strftime('%Y%m%dT%H:%M:%S')
        self.msisdn = '256776520831'
        self.ussdServiceCode = '130'
        self.ussdRequestString = ''
        self.response = False

    def sendRequest(self, transactionId = None, transactionTime = None, msisdn = None, ussdServiceCode = None, ussdRequestString = None, response = None ):
        client = Client()
        transactionId = self.transactionId if transactionId is None else transactionId
        transactionTime = self.transactionTime if transactionTime is None else transactionTime
        msisdn = self.msisdn if msisdn is None else msisdn
        ussdServiceCode = self.ussdServiceCode if ussdServiceCode is None else ussdServiceCode
        ussdRequestString = self.ussdRequestString if ussdRequestString is None else ussdRequestString
        response = self.response if response is None else response

        return client.post('/ussd/', {'transactionId': transactionId,
                                      'transactionTime': transactionTime,
                                      'msisdn': msisdn,
                                      'ussdServiceCode': ussdServiceCode,
                                      'ussdRequestString': ussdRequestString,
                                      'response': response
                                    })

    def testUSSDRequest(self):
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")

    def testUTLDataPost(self):
        data_structure = settings.UTL_BIRTH_DICT
        keys = dict([[v,k] for k,v in data_structure.items()])
        action = 'NEWBIRTH'
        post_data = {
            "NMNAT":"1",
            "NFNAT":"1",
            "NMOT":"test mother name",
            "NFAT":"test father name",
            "NSEX":"1",
            "NDATE":"11092012",
            "NNAME":"test child name",
            "NLNAME":"other child name",
            "PIN":"9045",
            "MSISDN":"256776520831",
            "ACTION":action,
            "SESSION":"1123",
        }
        result = urllib2.urlopen('http://www.mobilevrs.co.ug/ussd/notify.php?%s' % urllib.urlencode(post_data))
        self.assertEquals(result.getcode(), 200)

    def testBirthNotify(self):
        logger.info("\n\n Testing Birth Notify....\n\n")
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter child's Name\nor\nEnter '0' if not available :&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'first',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter child's Surname:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'other',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter date of birth:\n1. Today\n2. Yesterday\nOther (Enter manually in the format ddmmyyyy) &action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Select the sex of the child:\n 1. Male\n 2. Female&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter Mother's Name and Surname:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'name mother',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Select mother's nationality:\n1. Uganda\n2. Kenya\n3. Tanzania\n4. Rwanda\n5. Burundi\n6. South Sudan\n7. DR Congo\nOthers (Type in the country manually)&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter father's Name and Surname\nor\nEnter '0' if not available:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'the father',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Select father's nationality:\n1. Uganda\n2. Kenya\n3. Tanzania\n4. Rwanda\n5. Burundi\n6. South Sudan\n7. DR Congo\nOthers (Type in the country manually)&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter Pin to confirm or \"0\" to cancel&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '9045',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=This phone 256776520831 is not registered on Mobile VRS&action=end')

    def testBirthNotifyCorrected(self):
        logger.info("\n\n Testing Birth Notify....\n\n")
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter child's Name\nor\nEnter '0' if not available :&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'first1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=All names should be valid names\nEnter child's Name\nor\nEnter '0' if not available :&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'first',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter child's Surname:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'other\' J-ohn',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter date of birth:\n1. Today\n2. Yesterday\nOther (Enter manually in the format ddmmyyyy) &action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Select the sex of the child:\n 1. Male\n 2. Female&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter Mother's Name and Surname:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'name mother',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Select mother's nationality:\n1. Uganda\n2. Kenya\n3. Tanzania\n4. Rwanda\n5. Burundi\n6. South Sudan\n7. DR Congo\nOthers (Type in the country manually)&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter father's Name and Surname\nor\nEnter '0' if not available:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'the father',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Select father's nationality:\n1. Uganda\n2. Kenya\n3. Tanzania\n4. Rwanda\n5. Burundi\n6. South Sudan\n7. DR Congo\nOthers (Type in the country manually)&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter Pin to confirm or \"0\" to cancel&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '9045',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=This phone 256776520831 is not registered on Mobile VRS&action=end')

    def testBirthNotifyCancel(self):
        logger.info("\n\n Testing Birth Notify....\n\n")
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter child's Name\nor\nEnter '0' if not available :&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'first',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter child's Surname:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'other',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter date of birth:\n1. Today\n2. Yesterday\nOther (Enter manually in the format ddmmyyyy) &action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Select the sex of the child:\n 1. Male\n 2. Female&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter Mother's Name and Surname:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'the mother',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Select mother's nationality:\n1. Uganda\n2. Kenya\n3. Tanzania\n4. Rwanda\n5. Burundi\n6. South Sudan\n7. DR Congo\nOthers (Type in the country manually)&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'Patricia Something',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter father's Name and Surname\nor\nEnter '0' if not available:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'the father',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Select father's nationality:\n1. Uganda\n2. Kenya\n3. Tanzania\n4. Rwanda\n5. Burundi\n6. South Sudan\n7. DR Congo\nOthers (Type in the country manually)&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter Pin to confirm or \"0\" to cancel&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '0',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=The information was not recorded. Please start again.&action=end')

    def testBirthNotifyResume(self):
        logger.info("\n\nTesting Birth Resume Notify \n\n")
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter child's Name\nor\nEnter '0' if not available :&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'first',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter child's Surname:&action=request")
        response = self.sendRequest(transactionId = '34455',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'Chld',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request')
        response = self.sendRequest(transactionId = '34455',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '6',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter child's Surname:&action=request")

    def testDeathNotify(self):
        logger.info("\n\nTesting Death Notify\n\n")
        response = self.sendRequest(transactionId = '123345',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '',
            response = True
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = '123345',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Name and Surname of Deceased:&action=request")
        response = self.sendRequest(transactionId = '123345',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'my first dead guy',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Age of the deceased:&action=request")
        response = self.sendRequest(transactionId = '123345',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '42',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Sex of the deceased:\n1. Male\n2. Female&action=request')
        response = self.sendRequest(transactionId = '123345',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Date of death (ddmmyyyy):&action=request')
        response = self.sendRequest(transactionId = '123345',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '18072012',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Name and Surname of Declarant:&action=request")
        response = self.sendRequest(transactionId = '123345',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'some woman',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Declarant's Phone Number:&action=request")
        response = self.sendRequest(transactionId = '123345',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '256782998903',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Capacity:\n1.Relative present at Death\n2.Other Relative\n3.Person present at death\n4.House occupant at location\n5.Person with knowledge\n6. Person finding  body&action=request")
        response = self.sendRequest(transactionId = '123345',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter Pin to confirm or \"0\" to cancel&action=request")
        response = self.sendRequest(transactionId = '123345',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '9045',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=This phone 256776520831 is not registered on Mobile VRS&action=end')

    def testResumeDeathNotify(self):
        logger.info("\n\nTesting Death Notify Resume\n\n")
        response = self.sendRequest(transactionId = '123346',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '',
            response = True
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = '123346',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Name and Surname of Deceased:&action=request")
        response = self.sendRequest(transactionId = '123346',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'my first dead guy',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Age of the deceased:&action=request")
        response = self.sendRequest(transactionId = '123347',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = '123347',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '6',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Age of the deceased:&action=request")

    def testResumeDeathNotifyAccuracy(self):
        logger.info("\n\nTesting Death Notify Accuraccy\n\n")
        response = self.sendRequest(transactionId = '123346',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '',
            response = True
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = '123346',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Name and Surname of Deceased:&action=request")
        response = self.sendRequest(transactionId = '123346',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'Yon Dead',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Age of the deceased:&action=request")
        response = self.sendRequest(transactionId = '123347',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = '123347',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '6',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Age of the deceased:&action=request")
        response = self.sendRequest(transactionId = '123347',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '45',
            response = True
        )
        self.assertEqual(urllib2.unquote(response.content), "responseString=Sex of the deceased:\n1. Male\n2. Female&action=request")
        response = self.sendRequest(transactionId = '123347',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEqual(urllib2.unquote(response.content), "responseString=Date of death (ddmmyyyy):&action=request")
        response = self.sendRequest(transactionId = '123347',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '12122011',
            response = True
        )
        self.assertEqual(urllib2.unquote(response.content), "responseString=Name and Surname of Declarant:&action=request")
        response = self.sendRequest(transactionId = '123347',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'Osama Bin Laden',
            response = True
        )
        self.assertEqual(urllib2.unquote(response.content), "responseString=Declarant's Phone Number:&action=request")
        response = self.sendRequest(transactionId = '123347',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '63773737737',
            response = True
        )
        self.assertEqual(urllib2.unquote(response.content), "responseString=Capacity:\n1.Relative present at Death\n2.Other Relative\n3.Person present at death\n4.House occupant at location\n5.Person with knowledge\n6. Person finding  body&action=request")
        response = self.sendRequest(transactionId = '123347',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = False
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter Pin to confirm or "0" to cancel&action=request')
        response = self.sendRequest(transactionId = '123347',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '9045',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=This phone 256776520831 is not registered on Mobile VRS&action=end')

    def testUserManagementUserCreation(self):
        logger.info("\n\nTesting User Management User Creation\n\n")
        self.transactionId = '50012'
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '5',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Create User\n2. Modify Pin\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter User's name:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString ="user",
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter User's surname:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'Other',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter User's sex:\n1. Male\n2. Female&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter User's Date of Birth (ddmmyyyy):&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '12121999',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter user's phone number:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '078942422424',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Capacity:\n1. Notifier\n2. Registrar&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'kampala',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter User's parish or ward:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter  PIN to confirm or "0" to cancel&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '9045',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=This phone 256776520831 is not registered on Mobile VRS&action=end")

    def testUserManagementUserCreationResume(self):
        logger.info("\n\nTesting User Management User Creation\n\n")
        self.transactionId = '50012'
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '5',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Create User\n2. Modify Pin\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter User's name:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString ="User",
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter User's surname:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'Other',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter User's sex:\n1. Male\n2. Female&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter User's Date of Birth (ddmmyyyy):&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '12121999',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter user's phone number:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '078942422424',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Capacity:\n1. Notifier\n2. Registrar&action=request")
        response = self.sendRequest(transactionId = "1233444",
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'kampala',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = '1233444',
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '6',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Capacity:\n1. Notifier\n2. Registrar&action=request")


    def testModifyPin(self):
        logger.info("\n\nTesting User management modify Pin\n\n")
        self.transactionId = '534545'
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '5',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Create User\n2. Modify Pin\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter old PIN:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '9045',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter new PIN:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2325',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Re-enter new PIN:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2325',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=This phone 256776520831 is not registered on Mobile VRS&action=end")

    def testValidateViewRecord(self):
        logger.info("\n\nTesting Validate View Record\n\n")
        self.transactionId = '534545'
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '4',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. View Record\n2. Validate\n3. Delete\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=View Record\n\nEnter  PIN to confirm or "0" to cancel&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '9045',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=This phone 256776520831 is not registered on Mobile VRS&action=end')


    def testValidateViewRecordCancel(self):
        logger.info("\n\nTesting Validate View Record\n\n")
        self.transactionId = '534545'
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '4',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. View Record\n2. Validate\n3. Delete\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=View Record\n\nEnter  PIN to confirm or "0" to cancel&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '0',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Your request was not submitted. Please start again.&action=end')


    def testValidateValidateRecord(self):
        logger.info("\n\nTesting Validate View Record\n\n")
        self.transactionId = '534545'
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '4',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. View Record\n2. Validate\n3. Delete\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1232',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Re-enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1232',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Validate Record\n\nEnter  PIN to confirm or "0" to cancel&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '9045',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=This phone 256776520831 is not registered on Mobile VRS&action=end')

    def testValidateValidateRecordCancel(self):
        logger.info("\n\nTesting Validate View Record\n\n")
        self.transactionId = '534545'
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '4',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. View Record\n2. Validate\n3. Delete\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1232',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Re-enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1232',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Validate Record\n\nEnter  PIN to confirm or "0" to cancel&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '0',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Your request was not submitted. Please start again.&action=end')

    def testDeleteValidateRecord(self):
        logger.info("\n\nTesting Validate View Record\n\n")
        self.transactionId = '534545'
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '4',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. View Record\n2. Validate\n3. Delete\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1232',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Re-enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1232',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Delete Record\n\nEnter  PIN to confirm or "0" to cancel&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '9045',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=This phone 256776520831 is not registered on Mobile VRS&action=end')


    def testDeleteValidateRecordCancel(self):
        logger.info("\n\nTesting Validate View Record\n\n")
        self.transactionId = '534545'
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '4',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. View Record\n2. Validate\n3. Delete\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1232',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Re-enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1232',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Delete Record\n\nEnter  PIN to confirm or "0" to cancel&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '0',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Your request was not submitted. Please start again.&action=end')

    def testEditChildFirstName(self):
        logger.info("\n\n Testing Edit Child First Name....\n\n")
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Edit Birth Record\n2. Edit Death Record\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Child's details\n2. Mother's details\n3. Father's details\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Child's Name\n2. Child's Surname\n3. DoB\n4. Child's Sex\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1231',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter child's Name&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'Childa',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Change Child\'s Name\n\nEnter  PIN to confirm or \"0\" to cancel&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '9045',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=This phone 256776520831 is not registered on Mobile VRS&action=end")

    def testEditChildOtherName(self):
        logger.info("\n\n Testing Edit Child First Name....\n\n")
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Edit Birth Record\n2. Edit Death Record\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Child's details\n2. Mother's details\n3. Father's details\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Child's Name\n2. Child's Surname\n3. DoB\n4. Child's Sex\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1231',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter child's Surname&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'Childa',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Change Child\'s Surname\n\nEnter  PIN to confirm or \"0\" to cancel&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '9045',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=This phone 256776520831 is not registered on Mobile VRS&action=end")


    def testEditChildDoB(self):
        logger.info("\n\n Testing Edit Child First Name....\n\n")
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Edit Birth Record\n2. Edit Death Record\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Child's details\n2. Mother's details\n3. Father's details\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Child's Name\n2. Child's Surname\n3. DoB\n4. Child's Sex\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1231',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter date of birth:\n1. Today\n2. Yesterday\nOther (Enter manually in the format ddmmyyyy)&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '12112011',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Change Date of birth\n\nEnter  PIN to confirm or \"0\" to cancel&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '9045',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=This phone 256776520831 is not registered on Mobile VRS&action=end")

    def testEditChildSex(self):
        logger.info("\n\n Testing Edit Child First Name....\n\n")
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Edit Birth Record\n2. Edit Death Record\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Child's details\n2. Mother's details\n3. Father's details\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Child's Name\n2. Child's Surname\n3. DoB\n4. Child's Sex\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '4',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1231',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter Child\'s Sex:\n1. Male\n2. Female&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '12112011',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Change Child's Sex \n\nEnter  PIN to confirm or \"0\" to cancel&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '9045',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=This phone 256776520831 is not registered on Mobile VRS&action=end")


    def testEditMotherName(self):
        logger.info("\n\n Testing Edit Child First Name....\n\n")
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Edit Birth Record\n2. Edit Death Record\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Child's details\n2. Mother's details\n3. Father's details\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Mother's Names\n2. Mother's Nationality\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1231',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter mother's Name and Surname:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'Mama Fina',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Change Mother\'s Name and Surname\n\nEnter  PIN to confirm or \"0\" to cancel&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '9045',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=This phone 256776520831 is not registered on Mobile VRS&action=end")

    def testEditMotherNatioanality(self):
        logger.info("\n\n Testing Edit Child First Name....\n\n")
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Edit Birth Record\n2. Edit Death Record\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Child's details\n2. Mother's details\n3. Father's details\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Mother's Names\n2. Mother's Nationality\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1231',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter mother's nationality:\n1. Uganda\n2. Kenya\n3. Tanzania\n4. Rwanda\n5. Burundi\n6. South Sudan\n7. DR Congo\nOthers (Type in the country manually)&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'Mama',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Change Mother\'s nationality\n\nEnter  PIN to confirm or \"0\" to cancel&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '9045',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=This phone 256776520831 is not registered on Mobile VRS&action=end")

    def testEditFatherName(self):
        logger.info("\n\n Testing Edit Child First Name....\n\n")
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Edit Birth Record\n2. Edit Death Record\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Child's details\n2. Mother's details\n3. Father's details\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Father's Names\n2. Father's Nationality\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1231',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter father's Name and Surname:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'Mama Fina',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Change father\'s Name and Surname\n\nEnter  PIN to confirm or \"0\" to cancel&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '9045',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=This phone 256776520831 is not registered on Mobile VRS&action=end")

    def testEditFatherNationality(self):
        logger.info("\n\n Testing Edit Child First Name....\n\n")
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Edit Birth Record\n2. Edit Death Record\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Child's details\n2. Mother's details\n3. Father's details\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Father's Names\n2. Father's Nationality\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1231',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter father\'s nationality:\n1. Uganda\n2. Kenya\n3. Tanzania\n4. Rwanda\n5. Burundi\n6. South Sudan\n7. DR Congo\nOthers (Type in the country manually)&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'Mama',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Change Father\'s nationality\n\nEnter  PIN to confirm or \"0\" to cancel&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '9045',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=This phone 256776520831 is not registered on Mobile VRS&action=end")

    def testEditDeceasedName(self):
        logger.info("\n\n Testing Edit Child First Name....\n\n")
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Edit Birth Record\n2. Edit Death Record\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Deceased's details\n2. Declarant's details\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Deceased's names\n2. Age\n3. Sex\n4. Date of Death\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1231',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter deceased's Name and Surname&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'Mama Fina',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Change deceased\'s Name and Surname\n\nEnter  PIN to confirm or \"0\" to cancel&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '9045',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=This phone 256776520831 is not registered on Mobile VRS&action=end")

    def testEditDeceasedAge(self):
        logger.info("\n\n Testing Edit Child First Name....\n\n")
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Edit Birth Record\n2. Edit Death Record\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Deceased's details\n2. Declarant's details\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Deceased's names\n2. Age\n3. Sex\n4. Date of Death\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1231',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Age of the deceased:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'Mama',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Change Deceased\'s age\n\nEnter  PIN to confirm or \"0\" to cancel&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '9045',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=This phone 256776520831 is not registered on Mobile VRS&action=end")


    def testEditDeceasedSex(self):
        logger.info("\n\n Testing Edit Child First Name....\n\n")
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Edit Birth Record\n2. Edit Death Record\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Deceased's details\n2. Declarant's details\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Deceased's names\n2. Age\n3. Sex\n4. Date of Death\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1231',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Sex of the deceased:\n1. Male\n2. Female&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Change Deceased's Sex\n\nEnter  PIN to confirm or \"0\" to cancel&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '9045',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=This phone 256776520831 is not registered on Mobile VRS&action=end")


    def testEditDeceasedDod(self):
        logger.info("\n\n Testing Edit Child First Name....\n\n")
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Edit Birth Record\n2. Edit Death Record\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Deceased's details\n2. Declarant's details\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Deceased's names\n2. Age\n3. Sex\n4. Date of Death\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '4',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1231',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Date of death (ddmmyyyy):&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '13022012',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Change Deceased's Date of death\n\nEnter  PIN to confirm or \"0\" to cancel&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '9045',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=This phone 256776520831 is not registered on Mobile VRS&action=end")


    def testEditDeclarantName(self):
        logger.info("\n\n Testing Edit Child First Name....\n\n")
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Edit Birth Record\n2. Edit Death Record\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Deceased's details\n2. Declarant's details\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Names of Declarant\n2. Declarant's Phone Number\n3. Declarant's Capacity\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1231',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=declarant's Name and Surname:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = 'dskd huty',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Change declarant\'s Name and Surname\n\nEnter  PIN to confirm or \"0\" to cancel&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '9045',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=This phone 256776520831 is not registered on Mobile VRS&action=end")


    def testEditDeclarantPhone(self):
        logger.info("\n\n Testing Edit Child First Name....\n\n")
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Edit Birth Record\n2. Edit Death Record\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Deceased's details\n2. Declarant's details\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Names of Declarant\n2. Declarant's Phone Number\n3. Declarant's Capacity\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1231',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Declarant's Phone Number:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Change Declarant's phone number\n\nEnter  PIN to confirm or \"0\" to cancel&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '9045',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=This phone 256776520831 is not registered on Mobile VRS&action=end")


    def testEditDeclarantPhoneCancel(self):
        logger.info("\n\n Testing Edit Child First Name....\n\n")
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Edit Birth Record\n2. Edit Death Record\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Deceased's details\n2. Declarant's details\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Names of Declarant\n2. Declarant's Phone Number\n3. Declarant's Capacity\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1231',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Declarant's Phone Number:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Change Declarant's phone number\n\nEnter  PIN to confirm or \"0\" to cancel&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '0',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=The information was not updated. Please start again.&action=end")


    def testEditDeclarantCapacity(self):
        logger.info("\n\n Testing DeclarantCapacity....\n\n")
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Edit Birth Record\n2. Edit Death Record\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Deceased's details\n2. Declarant's details\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Names of Declarant\n2. Declarant's Phone Number\n3. Declarant's Capacity\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1231',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Capacity:\n1. Relative present at Death\n2. Other Relative\n3. Person present at death\n4. Household member\n5. Person with knowledge of death\n6. Person finding the body&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Change Declarant\'s Capacity \n\nEnter  PIN to confirm or \"0\" to cancel&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '9045',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=This phone 256776520831 is not registered on Mobile VRS&action=end")

    def testEditDeclarantCapacityCancel(self):
        logger.info("\n\n Testing DeclarantCapacity....\n\n")
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Edit Birth Record\n2. Edit Death Record\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Deceased's details\n2. Declarant's details\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '2',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Names of Declarant\n2. Declarant's Phone Number\n3. Declarant's Capacity\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '3',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1231',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Capacity:\n1. Relative present at Death\n2. Other Relative\n3. Person present at death\n4. Household member\n5. Person with knowledge of death\n6. Person finding the body&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '1',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Change Declarant\'s Capacity \n\nEnter  PIN to confirm or \"0\" to cancel&action=request")
        response = self.sendRequest(transactionId = self.transactionId,
            transactionTime = self.transactionTime,
            msisdn = self.msisdn,
            ussdServiceCode = self.msisdn,
            ussdRequestString = '0',
            response = True
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=The information was not updated. Please start again.&action=end")


#class ParseFuncTest(TestCase):
#    def setUp(self):
#        c = self.client
#
#    def testParseName(self):
#        self.assertEqual("Kenneth Matovu",_parse_name('',"kenneth matovu"))
#        #self.assertRaises(ValidationError,_parse_name('','Kenneth1w Matovu'))
#        self.assertRaises(ValidationError,_parse_name("",'Kenneth'))