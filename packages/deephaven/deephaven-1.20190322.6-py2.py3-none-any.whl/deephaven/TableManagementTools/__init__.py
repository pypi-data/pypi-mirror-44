#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

##############################################################################
#               This code is auto generated. DO NOT EDIT FILE!
# Run generatePythonIntegrationStaticMethods or
# "./gradlew :Generators:generatePythonIntegrationStaticMethods" to generate
##############################################################################


import sys
import jpy
import functools
from ..conversion_utils import _isJavaType, _isStr

__java_type__ = None  # None until the first defineSymbols() call
__java_file_type__ = None
__iris_config__ = None


def defineSymbols():
    """
    Defines appropriate java symbol, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global __java_type__, __java_file_type__, __iris_config__
    if __java_type__ is None:
        # This will raise an exception if the desired object is not the classpath
        __java_type__ = jpy.get_type("com.illumon.iris.db.tables.utils.TableManagementTools")
        __java_file_type__ = jpy.get_type("java.io.File")
        __iris_config__ = jpy.get_type("com.fishlib.configuration.Configuration")


# every module method should be decorated with @passThrough
def passThrough(func):
    """
    For decoration of module methods, to define necessary symbols at runtime

    :param func: the method to be decorated
    :return: the decorated version of the method
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        defineSymbols()
        return func(*args, **kwargs)
    return wrapper


@passThrough
def getFileObject(input):
    """
    Helper function for easily creating a java file object from a path string
    :param input: path string, or list of path strings
    :return: java File object, or java array of File objects
    """

    if _isJavaType(input):
        return input
    elif _isStr(input):
        return __java_file_type__(input)
    elif isinstance(input, list):
        # NB: map() returns an iterator in python 3, so list comprehension is appropriate here
        return jpy.array("java.io.File", [__java_file_type__(el) for el in input])
    else:
        raise ValueError("Method accepts only a java type, string, or list of strings as input. Got {}".format(type(input)))


@passThrough
def getWorkspaceRoot():
    """
    Helper function for extracting the root directory for the workspace configuration
    """

    return __iris_config__.getInstance().getWorkspacePath()


# Define all of our functionality, if currently possible
try:
    defineSymbols()
except Exception as e:
    pass


@passThrough
def addColumns(*args):
    return __java_type__.addColumns(args[0], getFileObject(args[1]), *args[2:])


@passThrough
def addGroupingMetadata(*args):
    if len(args) == 1:
        return __java_type__.addGroupingMetadata(getFileObject(args[0]))
    else:
        return __java_type__.addGroupingMetadata(getFileObject(args[0]), *args[1:])


@passThrough
def appendToTable(tableToAppend, destDir):
    return __java_type__.appendToTable(tableToAppend, destDir)


@passThrough
def appendToTables(definitionToAppend, tablesToAppend, destinationDirectoryNames):
    return __java_type__.appendToTables(definitionToAppend, tablesToAppend, destinationDirectoryNames)


@passThrough
def deleteTable(path):
    return __java_type__.deleteTable(getFileObject(path))


@passThrough
def dropColumns(*args):
    return __java_type__.dropColumns(args[0], getFileObject(args[1]), *args[2:])


@passThrough
def flushColumnData():
    return __java_type__.flushColumnData()


@passThrough
def getAllDbDirs(tableName, rootDir, levelsDepth):
    return [el.getAbsolutePath() for el in __java_type__.getAllDbDirs(tableName, getFileObject(rootDir), levelsDepth).toArray()]


@passThrough
def readTable(*args):
    if len(args) == 1:
        return __java_type__.readTable(getFileObject(args[0]))
    else:
        return __java_type__.readTable(getFileObject(args[0]), *args[1:])


@passThrough
def renameColumns(*args):
    return __java_type__.renameColumns(args[0], getFileObject(args[1]), *args[2:])


@passThrough
def updateColumns(currentDefinition, rootDir, levels, *updates):
    return __java_type__.updateColumns(currentDefinition, getFileObject(rootDir), levels, *updates)


@passThrough
def writeColumn(sourceTable, destinationTable, pendingCount, columnDefinition, currentMapping, currentSize):
    return __java_type__.writeColumn(sourceTable, destinationTable, pendingCount, columnDefinition, currentMapping, currentSize)


@passThrough
def writeTable(*args):
    return __java_type__.writeTable(*args)


@passThrough
def writeTables(sources, tableDefinition, destinations):
    return __java_type__.writeTables(sources, tableDefinition, getFileObject(destinations))
