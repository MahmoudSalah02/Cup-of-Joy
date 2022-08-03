from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from controllers.employees import read_all
from models.models import Employee
import unittest
from unittest.mock import patch


class MyTest(unittest.TestCase):
    def setUp(self):
        self.session = UnifiedAlchemyMagicMock()
        self.session.add(Employee(name='One', contact_number=1))
        self.session.add(Employee(name='Two', contact_number=2))
        self.session.add(Employee(name='Three', contact_number=3))
        self.session.commit()

    def test_count(self):
        assert len(self.session.query(Employee).all()) == 3

    def tearDown(self):
        pass

    # def test_session(self):
    #     with patch('init_db.get_session') as mock:
    #         assert len(self.session.query(Employee).all()) == 3
    #         instance = mock.return_value
    #         instance.method.return_value = self.session
    #         read_all()

    @patch('init_db.get_session')
    def test_read_all(self, mock_get_session):
        mock_get_session.return_value = self.session
        read_all()


if __name__ == '__main__':
    unittest.main()
