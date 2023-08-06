#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

import jpy
import sys
import logging
import random

from .java_to_python import tableToDataFrame
from .python_to_java import dataFrameToTable


class DeephavenDb(object):
    """
    IllumonDb session
    """

    def __init__(self):
        """
        Constructs a new Iris session
        """

        DbGroovySession = jpy.get_type('com.illumon.integrations.common.IrisIntegrationGroovySession')
        self.session = DbGroovySession("Python Session", True)

    def reconnect(self):
        """
        Disconnects/shuts down the current session, and establishes a new session

        .. warning:: The current Iris state will be lost
        """

        DbGroovySession = jpy.get_type('com.illumon.integrations.common.IrisIntegrationGroovySession')
        self.session.getDb().shutdown()
        self.session = DbGroovySession("Python Session", True)

    def db(self):
        """
        Gets the Iris database object
        """

        return self.session.getDb()

    def execute(self, groovy):
        """
        Executes Iris groovy code from a snippet/string

        :param groovy: groovy code
        """

        self.session.execute(groovy)

    def executeFile(self, file):
        """
        Executes Iris groovy code from a file

        :param file: the file
        """

        self.session.executeFile(file)

    def get(self, variable):
        """
        Gets a variable from the groovy session

        :param variable: variable name
        :return: the value
        """

        return self.session.getVariable(variable)  # TODO: should we convert anything?

    def __getitem__(self, variable):
        """
        Gets a variable from the groovy session.

        :param variable: the variable name
        :return: the value
        """

        return self.get(variable)

    def getDf(self, variable):
        """
        Gets a Table as a :class:`pandas.DataFrame` from the console session

        :param variable: the variable (table) name
        :return: :class:`pandas.DataFrame` instance representing Table specified by `variable`
        """

        return tableToDataFrame(t)

    def pushDf(self, name, df):
        """
        Pushes a :class:`pandas.DataFrame` to the Iris groovy session as a Table

        :param name: the destination variable name in the groovy session
        :param df: :class:`pandas.DataFrame` instance
        """

        logging.info("Dataframe {} push...".format(name))
        t = dataFrameToTable(df)
        self.session.publishTable(name, t)
        logging.info("...Dataframe {} push done.".format(name))
