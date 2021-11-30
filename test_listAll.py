import unittest
from zendesk import ListAll, ListSpecific,ParseAllJson, totTickets
from variablesForTest import *

from unittest import mock
from unittest.mock import patch
import io

class test_Tickets(unittest.TestCase):

    # This tests the List specific method to make sure we are getting the right ticket
    def test_listAll(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            ListSpecific('1')
        assert str(fake_stdout.getvalue()) == str(specificTicket)
    
    # This tests the count total method and the API request for it
    def test_count(self):
        assert totTickets() == totTicketCount
        

if __name__ == '__main__':
    unittest.main()



