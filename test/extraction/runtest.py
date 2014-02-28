import unittest
from sqlalchemy import create_engine, MetaData, Column, Table, Integer, String
import os


class TestExtractFunctions(unittest.TestCase):
    """
    Test the extract functions
    """

    def setUp(self):
        # Setup a small database for testing
        tmp_dir = "/tmp/abathur"
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        db_conn_str = "sqlite:///{tmp_dir}/testdb.db".format(tmp_dir=tmp_dir)
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


if __name__ == "__main__":
    unittest.main()
