import unittest
from sqlalchemy import create_engine, MetaData, Column, Table, Integer, String
import os
import shutil


class TestExtractFunctions(unittest.TestCase):
    """
    Test the extract functions
    """
    TMP_DIR = "/tmp/abathur_unittest"
    DB_NAME = "testdb.db"

    def setUp(self):
        print "calling setUp"
        tmp_dir = self.__class__.TMP_DIR
        db_name = self.__class__.DB_NAME
        # Setup the tmp dir and a small database for testing
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        os.makedirs(tmp_dir)

        db_conn_str = "sqlite:///{tmp_dir}/{db_name}".format(
            tmp_dir=tmp_dir, db_name=db_name)
        engine = create_engine(db_conn_str)
        metadata = MetaData()

        # Test tables
        user = Table(
            'user', metadata,
            Column('user_id', Integer, primary_key=True),
            Column('user_name', String(16), nullable=False),
            Column('email_address', String(60))
        )

        user.create(engine)

        conn = engine.connect()

        conn.execute(user.insert(), [
            {"user_id": 1, "user_name": "Kevin", "email_address":
                "kevin@testmail.com"},
            {"user_id": 2, "user_name": "Lucy", "email_address":
                "lucy@testmail.com"},
            {"user_id": 3, "user_name": "Matt", "email_address":
                "matt@testmail.com"},
            {"user_id": 4, "user_name": "Ryan", "email_address":
                "ryan@testmail.com"},
        ])

    def tearDown(self):
        print "Calling tearDown"
        tmp_dir = self.__class__.TMP_DIR
        shutil.rmtree(tmp_dir)

    def test_setup(self):
        tmp_dir = self.__class__.TMP_DIR
        db_name = self.__class__.DB_NAME

        db_conn_str = "sqlite:///{tmp_dir}/{db_name}".format(
            tmp_dir=tmp_dir, db_name=db_name)
        engine = create_engine(db_conn_str)
        conn = engine.connect()
        result = conn.execute("select count(*) from user")
        self.assertEqual(result.fetchone()[0], 3)
        result.close()


if __name__ == "__main__":
    unittest.main()
