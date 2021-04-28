import os
import time
import pandas as pd
import sqlalchemy as sa
from dotenv import load_dotenv
load_dotenv()


class MySQLpy:
    '''
    MySQL database control
    
    :Authors:
        Leandro Furlam Turi <leandrofturi@gmail.com>
    '''

    __engine     = None
    __metadata   = None
    __user       = None
    __pswd       = None
    __host       = None
    __port       = None
    __database   = None
    __connection = None


    def __init__(self, database):
        '''
        __init__ Class constructor.
        It is necessary to define database access parameters in enviroment file.

        Args:
            database (text object): database name.
        '''

        self.__user = os.getenv('MYSQL_USERNAME')
        self.__pswd = os.getenv('MYSQL_PASSWORD')
        self.__host = os.getenv('MYSQL_HOST')
        self.__port = os.getenv('MYSQL_PORT')
        self.__database = database

        if database is None:
            self.__engine = sa.create_engine('mysql://{0}:{1}@{2}:{3}'.format(
                self.__user, self.__pswd, self.__host, self.__port))
        else:
            self.__engine = sa.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(
                self.__user, self.__pswd, self.__host, self.__port, database))
            self.__metadata = sa.MetaData(bind=self.__engine)


    def __open(self):
        '''
        __open Open a connection.
        '''

        try:
            self.__connection = self.__engine.connect()
        except sa.exc.SQLAlchemyError as e:
            print(e.args)


    def __close(self):
        '''
        __close Close a connection.
        '''

        self.__connection.close()


    def test_connection(self):
        '''
        test_connection Test connection
        '''

        try:
            self.__connection = self.__engine.connect()
        except:
            print("Can't connect!")
        else:
            print("Connect!")
            self.__connection.close()


    def show_databases(self):
        '''
        show_databases Show all databases names

        Returns:
            [List]: List of databases
        '''

        db = None
        try:
            db = sa.inspect(self.__engine).get_schema_names()
        except sa.exc.SQLAlchemyError as e:
            print(e.args)
        return db


    def table(self, table_name):
        '''
        table Take the representation of a table in a database.
        Can be used to create a sqlalchemy selectable.

        Args:
            table_name (text object): table name.

        Returns:
            sqlalchemy Table object: Representation of a table in database.
        '''

        if self.__metadata is None:
            return None

        tb = None
        try:
            tb = sa.Table(table_name, self.__metadata, autoload=True)
        except sa.exc.SQLAlchemyError as e:
            print(e.args)
        return tb


    def show_tables(self):
        '''
        show_tablenames Show all table names

        Returns:
            [List]: List of table names
        '''

        tb = None
        try:
            tb = sa.inspect(self.__engine).get_table_names()
        except sa.exc.SQLAlchemyError as e:
            print(e.args)
        return tb


    def read_sql(self, sql, chunksize=None):
        '''
        read_sql Read data from sql query.

        Args:
            sql (SQLAlchemy Selectable (select or text object)): SQL query to be executed. Saw https://docs.sqlalchemy.org/en/13/core/selectable.html for more information.
            chunksize (None or int, optional): If specified, return an iterator where chunksize is the number of rows to include in each chunk. Defaults to None.

        Returns:
            DataFrame or Iterator[DataFrame]: DataFrame corresponding to the result set of the query string.
        '''

        df = None
        self.__open()
        try:
            df = pd.read_sql_query(sql, self.__connection, chunksize=chunksize)
        except sa.exc.SQLAlchemyError as e:
            print(e.args)
        finally:
            self.__close()
            return df


    def pandas_2mysql(self, df, table_name, if_exists='fail'):
        '''
        read_sql Read data from sql query.

        Args:
            df (DataFrame): DataFrame to be inserted.
            table_name (text object): Name of table in database to be inserted.
            if_exists (text object): How to behave if the table already exists. fail: Raise a ValueError. replace: Drop the table before inserting new values. append: Insert new values to the existing table, Defaults to fail.
        '''
        
        df.columns = df.columns.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        df.columns = df.columns.str.replace(' ', '_').str.replace(r'[^\w]', '').str.lower()
        
        self.__open()
        try:
            df.to_sql(name=table_name, con=self.__connection, if_exists=if_exists)
        except sa.exc.SQLAlchemyError as e:
            print(e.args)
        else:
            print('Done!')
        finally:
            self.__close()


    def xlsx_2mysql(self, table_name, path_xlsx, sheet_name=None, if_exists='fail', engine=None):
        '''
        xlsx_2mysql Create or append an table by xlsx file.
        If the table exists, it will be appended.
        The file is readed by xlrd engine.
        Note that if there are column names with non-alphanumeric characters, they will be removed, as well as accents.
        Spaces will be replaced by underline.
        Note if table already exists, it will be appended in the exists columns.
        If there are extra columns in your dataframe then you need to manually add that column to the database table.

        Args:
            table_name (text object): Name of table in database to be inserted.
            path_xlsx (text object): Path to xlsx file.
            sheet_name (text object or None, optional): Sheet name to be loaded in xlsx file. If there is only one sheet, None can be used to load this single sheet. Defaults to None.
            if_exists (text object): How to behave if the table already exists. fail: Raise a ValueError. replace: Drop the table before inserting new values. append: Insert new values to the existing table, Defaults to fail.
            engine (text object or None, optional): If io is not a buffer or path, this must be set to identify io. Supported engines: xlrd, openpyxl, odf, pyxlsb. Engine compatibility : xlrd supports old-style Excel files (.xls); openpyxl supports newer Excel file formats; odf supports OpenDocument file formats (.odf, .ods, .odt); pyxlsb supports Binary Excel files. Defaults to None.
        '''

        print('Loading data ...')
        tic = time.perf_counter()
        df = pd.read_excel(path_xlsx, sheet_name=sheet_name, engine=engine)
        if sheet_name is None:
            df = next(iter(df.values()))
        df.columns = df.columns.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        df.columns = df.columns.str.replace(' ', '_').str.replace(r'[^\w]', '').str.lower()
        df["FILENAME"] = path_xlsx.split('/')[-1]

        for c in df.select_dtypes(include='object').columns:
            df[c] = df[c].str.encode('utf-8')

        toc = time.perf_counter()
        print('Elapsed time is ' + time.strftime('%H:%M:%S', time.gmtime(toc - tic)))

        self.__open()
        try:
            df.to_sql(name=table_name, con=self.__connection, if_exists=if_exists)
        except sa.exc.SQLAlchemyError as e:
            print(e.args)
        else:
            print('Done!')
        finally:
            self.__close()


    def execute(self, stmt):
        '''
        execute Execute a SQL query.

        Args:
            stmt (text object): SQL query.
        '''

        result = None
        self.__open()
        try:
            result = self.__connection.execute(stmt)
        except sa.exc.SQLAlchemyError as e:
            print(e.args)
        else:
            print("Done!")
        finally:
            self.__close()
        return result
