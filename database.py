"""Execute all the quries on the main mysql database"""

# %%
import os
from sqlalchemy import create_engine


# %%
class DataBase:
    """Execute all the quries on the main mysql database"""

    __DB = os.environ['MYSQL_DB']
    __PORT = os.environ['MYSQL_PORT']
    __HOST = os.environ['MYSQL_HOST']
    __USERNAME = os.environ['MYSQL_USERNAME']
    __PASSWORD = os.environ['MYSQL_PASSWORD']

    @classmethod
    def update(cls, statement, dataframe):
        """Execute Insert or Update SQL statement on the database"""

        engine = create_engine('mysql://{}:{}@{}/{}'.format(
            cls.__USERNAME, cls.__PASSWORD, cls.__HOST, cls.__DB))

        connection = engine.connect()
        with connection.begin() as transaction:
            try:
                for row in dataframe.itertuples():
                    # print(statement.format(emi_master=row.emi_master))
                    connection.execute(statement, **row._asdict())
            except Exception as e:
                print(e)
                transaction.rollback()
                #raise
