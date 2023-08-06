import os
import pandas as pd
import pandas_profiling
import logging
import itertools

from sqlalchemy import create_engine
from base64 import b64decode

# importante para el tema de acentos y codificación
os.environ['NLS_LANG'] = 'SPANISH_SPAIN.WE8ISO8859P15'


class Zone(object):

    def __init__(self, schemaName):
        self.__con = None
        self.__schema = schemaName
        self.__logger = logging.getLogger(__name__)

    def __connect(self):
        if self.__con is not None:
            return
        user = os.getenv('DB_USER')
        if user is None or user == '':
            user = self.__schema
        password = os.getenv('DB_PASS')
        if password is None or password == '':
            raise ImportError('The DB_PASS has not been defined as an environment variable')
        password = b64decode(password).decode('utf-8')
        url = os.getenv('DB_URL')
        if url is None or url == '':
            url = '(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=mtcldb-scan.mutuatfe.local)(PORT=1521))(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=DESA)))'

        self.__logger.debug(f'Connecting to "{url}" with user "{user}" and using schema "{self.__schema}" ')

        if "DESCRIPTION" in url:  # conexión vía SERVICE
            self.__engine = create_engine('oracle+cx_oracle://{0}:{1}@{2}'.format(user, password, url))
        else:  # conexíon vía SID
            self.__engine = create_engine('oracle://{0}:{1}@{2}'.format(user, password, url))

        self.__con = self.__engine.connect()

    @property
    def df_names(self):
        """
        Property read_only that contains logical names of the persisted dataframes
        :return: logical names of persisted dataframe from specific datazone
        """
        self.__connect()
        names = self.__con.execute(f"SELECT lower(OBJECT_NAME) FROM USER_OBJECTS WHERE OBJECT_TYPE IN ('TABLE', 'VIEW')").fetchall()
        return tuple(itertools.chain.from_iterable(names))
        #return self.__engine.table_names(self.__schema, self.__con)
        
    def load_df(self, name):
        """
        Load a dataframe from persisted logical dataframe name. This name equals tablename or viewname-
        :param name: logical name used to persist the dataframe (table name or view name).
        :return: pandas dataframe load in memory
        """
        self.__connect()
        return pd.read_sql_table(name, self.__con, schema=self.__schema)

    
    def load_df_sql(self, query):
        """
        Load a dataframe from SQL sentence
        :param query: SQL BD query
        :return: Panda dataframe
        """
        self.__connect()
        return pd.read_sql(query, self.__con)
    
    def save_df(self, df, name, if_exists='replace'):
        """
        Save a dataframe (persists) in a database table. Doesn't work with view.
        :param df: dataframe load in memory
        :param name:  dataframe persisted logical name (table name).
        :param if_exists: {‘fail’, ‘replace’, ‘append’}
            Indicates the collision policy (default 'replace')
        :return: None
        """
        self.__connect()
        df.to_sql(name, self.__con, schema=self.__schema, if_exists=if_exists)
        
    def generate_profile(self, df):
        """
        Generate a profile from dataframe
        :param df: dataframe load in memory
        :return: profile report in html format
        """
        return pandas_profiling.ProfileReport(df)
    
    def save_profile_to_file(self, pathFile, df=None, profile=None):
        """
        Save a profile in a file from datatframe
        :param pathFile: path of the file
        :param df: dataframe load in memory
        :param profile:  profile load in memory
        :return: None
        """
        if df is None and profile is None:
            raise ValueError('One parameter is missing, df or profile parameter is required')
        if df is not None:
            profile = pandas_profiling.ProfileReport(df)
        profile.to_file(outputfile=pathFile)