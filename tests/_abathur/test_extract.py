import unittest
from sqlalchemy import (
    create_engine, MetaData, Column, Table, Integer, String, ForeignKey)
import os
import shutil
import sys
import filecmp

# A hack to find _abathur package, needs to be changed properly
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from _abathur.extract import Extractor


class TestExtractFunctions(unittest.TestCase):
    """
    Test the extract functions
    """
    TMP_DIR = "/tmp/abathur_unittest"
    DB_NAME = "testdb.db"

    def setUp(self):
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
        conn = engine.connect()

        # User table
        user = Table(
            'user', metadata,
            Column('user_id', Integer, primary_key=True),
            Column('user_name', String(16), nullable=False),
            Column('email_address', String(60)),
            Column('active', Integer, nullable=False)
        )
        user.create(engine)
        conn.execute(user.insert(), [
            {"user_id": 1, "user_name": "Kevin", "email_address":
                "kevin@testmail.com", "active": 1},
            {"user_id": 2, "user_name": "Lucy", "email_address":
                "lucy@testmail.com", "active": 1},
            {"user_id": 3, "user_name": "Matt", "email_address":
                "matt@testmail.com", "active": 1},
            {"user_id": 4, "user_name": "Ryan", "email_address":
                "ryan@testmail.com", "active": 1},
            {"user_id": 5, "user_name": "Ben", "email_address":
                "ben@testmail.com", "active": 0},
        ])

        # Follow table
        follow = Table(
            'follow', metadata,
            Column(
                'user_id', Integer, ForeignKey("user.user_id"),
                nullable=False, primary_key=True),
            Column(
                'follow_user_id', Integer, ForeignKey("user.user_id"),
                nullable=False, primary_key=True)
        )
        follow.create(engine)
        conn.execute(follow.insert(), [
            {"user_id": 2, "follow_user_id": 1},
            {"user_id": 3, "follow_user_id": 1},
            {"user_id": 4, "follow_user_id": 1},
            {"user_id": 1, "follow_user_id": 2},
            {"user_id": 3, "follow_user_id": 2},
            {"user_id": 1, "follow_user_id": 3},
            {"user_id": 1, "follow_user_id": 5},
            {"user_id": 2, "follow_user_id": 5},
            {"user_id": 5, "follow_user_id": 1},
        ])

    def tearDown(self):
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
        self.assertEqual(result.fetchone()[0], 5)
        result.close()

        result = conn.execute("select count(*) from follow")
        self.assertEqual(result.fetchone()[0], 9)
        result.close()

    def test_extractor_query_param(self):
        """
        Testing the Extractor with query_param = True
        """
        tmp_dir = self.__class__.TMP_DIR
        db_name = self.__class__.DB_NAME

        db_conn_str = "sqlite:///{tmp_dir}/{db_name}".format(
            tmp_dir=tmp_dir, db_name=db_name)

        test_dir_name = os.path.dirname(__file__)
        test_param_query_filename = os.path.join(
            test_dir_name, "data/test_param_query_file.sql")
        test_query_filename = os.path.join(
            test_dir_name, "data/test_query_file.json")
        output_filename = os.path.join(tmp_dir, "test_output.csv")
        extractor = Extractor(
            db_conn_str, test_param_query_filename, test_query_filename,
            output_filename, True)
        extractor.perform_extraction()

        sample_output_filename = os.path.join(
            test_dir_name, "data/sample_test_output.csv")

        self.assertTrue(filecmp.cmp(output_filename, sample_output_filename))

    def test_extractor_no_query_param(self):
        """
        Test the Extractor with query_param = False
        """
        tmp_dir = self.__class__.TMP_DIR
        db_name = self.__class__.DB_NAME

        db_conn_str = "sqlite:///{tmp_dir}/{db_name}".format(
            tmp_dir=tmp_dir, db_name=db_name)

        test_dir_name = os.path.dirname(__file__)
        test_param_query_filename = os.path.join(
            test_dir_name, "data/test_param_file.csv")
        test_query_filename = os.path.join(
            test_dir_name, "data/test_query_file.json")
        output_filename = os.path.join(tmp_dir, "test_output.csv")
        extractor = Extractor(
            db_conn_str, test_param_query_filename, test_query_filename,
            output_filename, False)
        extractor.perform_extraction()

        sample_output_filename = os.path.join(
            test_dir_name, "data/sample_test_output.csv")

        self.assertTrue(filecmp.cmp(output_filename, sample_output_filename))


if __name__ == "__main__":
    unittest.main()
