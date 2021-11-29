import unittest
from zendesk import ListAll,ParseAllJson
from variablesForTest import *

from unittest import mock
from unittest.mock import patch
import io

class test_list(unittest.TestCase):
    def test_listAll(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            ListAll()
        assert str(fake_stdout.getvalue()) == str(allTickets)


if __name__ == '__main__':
    unittest.main()



