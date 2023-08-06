#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

############################################################################
#               This code is auto generated. DO NOT EDIT FILE!
# Run generatePythonIntegrationStaticMethods or
# "./gradlew :Generators:generatePythonIntegrationStaticMethods" to generate
#############################################################################


import jpy
import logging
import sys
import functools
import numpy
import pandas
from datetime import datetime, date

from ..conversion_utils import _isJavaType, _isStr, makeJavaArray, _parseJavaArrayType, _basicArrayTypes, \
    _boxedArrayTypes, _nullValues, NULL_CHAR


__java_type__ = None  # None until the first defineSymbols() call


def defineSymbols():
    """
    Defines appropriate java symbol, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global __java_type__
    if __java_type__ is None:
        # This will raise an exception if the desired object is not the classpath
        __java_type__ = jpy.get_type("com.illumon.iris.db.tables.utils.TableTools")


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


def _makeJavaList(arr):
    # convert from java array to java Collection, for call signature purpose
    return jpy.get_type('java.util.Arrays').asList(arr)


def _custom_newTable(*args):
    # should only be called via newTable method below
    if (len(args) in [2, 3]) and (isinstance(args[0], int) or isinstance(args[0], float)):
        rows = int(args[0])

        if isinstance(args[1], dict):
            # desired args = (long, map<String, ColumnSource>)
            pydict = args[1]
            java_map = jpy.get_type("java.util.HashMap")()
            for key in pydict:
                java_map.put(key, pydict[key])
            return __java_type__.newTable(rows, java_map)
        elif (len(args) == 3) and isinstance(args[1], list) and isinstance(args[2], list):
            # desired args = (long, List<String>, List<ColumnSource>)
            names = _makeJavaList(args[1])
            sources = _makeJavaList(args[2])
            return __java_type__.newTable(rows, names, sources)

    return __java_type__.newTable(*args)


def _custom_colSource(*args):
    # should only be called from colSource() below
    if len(args) < 1:
        # pass it straight through
        return __java_type__.colSource(*args)
    elif len(args) == 1:
        if isinstance(args[0], int) or isinstance(args[0], float) or isinstance(args[0], bool) or \
                isinstance(args[0], datetime) or isinstance(args[0], date) or _isStr(args[0]):
            return _custom_colSource(numpy.asarray(args))
        elif isinstance(args[0], numpy.ndarray) or isinstance(args[0], pandas.Series) \
                or isinstance(args[0], pandas.Categorical):
            arr = makeJavaArray(args[0], 'unknown')  # check if this is one of the basic primitive types...
            if arr is None:
                raise ValueError("Unable to parse input arguments to viable java array")

            dimension, basic_type = _parseJavaArrayType(arr)

            if dimension == 0:  # this is an empty array
                return __java_type__.colSource()  # TODO: this is not valid
            elif dimension == 1 and basic_type == 'java.lang.String':
                # fetching a java.lang.String into python converts it to python str, so...
                return __java_type__.colSource(jpy.get_type(basic_type)().getClass(), _makeJavaList(arr))
            elif dimension == 1 and basic_type == 'java.lang.Boolean':
                # fetching a java.lang.Boolean into python converts it to python bool, so...
                return __java_type__.colSource(jpy.get_type(basic_type)(True).getClass(), _makeJavaList(arr))
            elif dimension > 1 or basic_type not in _basicArrayTypes:
                # we have to turn arr into a collection
                return __java_type__.colSource(arr[0].getClass(), _makeJavaList(arr))
            else:
                # it's a one-dimensional primitive type - so straight through
                return __java_type__.colSource(arr)
        elif isinstance(args[0], list) or isinstance(args[0], tuple):
            if len(args[0]) < 1:
                return __java_type__.colSource()
            # naively try to turn it into a numpy array and send it through
            return _custom_colSource(numpy.asarray(args[0]))
        elif _isJavaType(args[0]):
            return __java_type__.colSource(*args)
    else:
        if isinstance(args[0], int) or isinstance(args[0], float):
            # naively try to turn it into a numpy array and send it through
            return _custom_colSource(numpy.asarray(args))
        elif _isJavaType(args[0]):
            # push it straight through
            return __java_type__.colSource(*args)
        else:
            # naively try to turn it into a numpy array and send it through
            return _custom_colSource(numpy.asarray(args))
    # push it straight through
    return __java_type__.colSource(*args)


def _custom_objColSource(*args):
    # should only be called from objColSource() below
    if len(args) < 1 or _isJavaType(args[0]):
        # pass it straight through
        return __java_type__.objColSource(*args)
    elif len(args) == 1:
        if isinstance(args[0], numpy.ndarray) or isinstance(args[0], pandas.Series) \
                or isinstance(args[0], pandas.Categorical):
            arr = makeJavaArray(args[0], 'unknown')  # check if this is one of the basic primitive types...
            if arr is None:
                raise ValueError("Unable to parse input arguments to viable java array")

            dimension, basic_type = _parseJavaArrayType(arr)
            if dimension == 0:  # this is an empty array
                return __java_type__.objColSource()  # TODO: what would I do here? does this raise an NPE?
            else:
                return __java_type__.objColSource(arr)
        elif isinstance(args[0], list) or isinstance(args[0], tuple):
            if len(args[0]) < 1:
                __java_type__.objColSource([])
            # naively try to turn it into a numpy array and send it through
            return _custom_objColSource(numpy.asarray(args[0]))
    # pass it straight through in any other circumstance
    return __java_type__.objColSource(*args)


def _custom_col(name, *data):
    # should only be called from col() below
    if len(data) < 1:
        raise ValueError("No data provided")
    if len(data) == 1:
        if isinstance(data[0], int) or isinstance(data[0], float) or isinstance(data[0], bool) or \
                isinstance(data[0], datetime) or isinstance(data[0], date):
            return _custom_col(name, numpy.asarray(data))
        elif _isJavaType(data[0]):
            return __java_type__.col(name, data[0])
        elif _isStr(data[0]):
            return __java_type__.col(name, jpy.array('java.lang.String', data))
        elif isinstance(data[0], numpy.ndarray) or isinstance(data[0], pandas.Series) \
                or isinstance(data[0], pandas.Categorical):
            arr = makeJavaArray(data[0], name)
            dimension, basic_type = _parseJavaArrayType(arr)
            if dimension == 0:  # this is an empty array
                return __java_type__.col(name, [])
            if dimension == 1 and basic_type in _boxedArrayTypes:
                # it's supposed to be boxed. This is silly.
                return __java_type__.col(name, jpy.array(_boxedArrayTypes[basic_type], arr))
            return __java_type__.col(name, arr)
        elif isinstance(data[0], list) or isinstance(data[0], tuple):
            if len(data[0]) < 1:
                return __java_type__.col(name, [])
            # naively try to turn it into a numpy array and send it through
            return _custom_col(name, numpy.asarray(data[0]))
        else:
            raise ValueError("Encountered unexpected type {}".format(type(data[0])))
    else:
        if isinstance(data[0], int) or isinstance(data[0], float):
            # naively try to turn it into a numpy array and send it through
            return _custom_col(name, numpy.asarray(data))
        elif _isJavaType(data[0]):
            # push it straight through
            return __java_type__.col(name, *data)
        else:
            # naively try to turn it into a numpy array and send it through
            return _custom_col(name, numpy.asarray(data))


def _custom_charCol(name, *data):
    def makeElementChar(el):
        if el is None:
            return NULL_CHAR
        if isinstance(el, int):
            return el
        if _isStr(el):
            if len(el) < 1:
                return NULL_CHAR
            return ord(el[0])
        try:
            return int(el)
        except ValueError:
            return NULL_CHAR

    # should only be called from charCol() below
    if len(data) < 1:
        raise ValueError("No data provided")
    if len(data) == 1:
        if _isJavaType(data[0]):
            return __java_type__.charCol(name, data[0])
        elif _isStr(data[0]):
            return __java_type__.charCol(name, [ord(char) for char in data[0]])  # NB: map returns an iterable in py3
        elif isinstance(data[0], numpy.ndarray):
            if data[0].dtype == numpy.uint16:
                return __java_type__.charCol(name, jpy.array('char', data[0]))
            elif data[0].dtype in [numpy.int8, numpy.uint8, numpy.int16, numpy.int32, numpy.uint32, numpy.int64, numpy.uint64]:
                # not entirely sure that this is necessary
                return __java_type__.charCol(name, jpy.array('char', data[0].astype(numpy.uint16)))
            elif data[0].dtype == numpy.dtype('U1') and data[0].dtype.name in ['unicode32', 'str32', 'string32', 'bytes32']:
                junk = numpy.copy(data[0])
                junk.dtype = numpy.uint32
                return __java_type__.charCol(name, jpy.array('char', junk.astype(numpy.uint16)))
            elif data[0].dtype == numpy.dtype('S1') and data[0].dtype.name in ['str8', 'string8', 'bytes8']:
                junk = numpy.copy(data[0])
                junk.dtype = numpy.uint8
                return __java_type__.charCol(name, jpy.array('char', junk.astype(numpy.uint16)))
            elif data[0].dtype == numpy.object:
                # do our best
                return __java_type__.charCol(name, jpy.array('char', numpy.array([makeElementChar(el) for el in data[0]], dtype=numpy.uint16)))
            else:
                raise ValueError("Input was an ndarray, expected integer dtype or "
                                 "one character string dtype, and got {}".format(data[0].dtype))
        elif isinstance(data[0], pandas.Series):
            return _custom_charCol(name, data[0].values)
        elif hasattr(data[0], '__iter__'):
            # naively turn it into a numpy array, and see what happens
            try:
                return _custom_charCol(name, numpy.asarray(data[0]))
            except Exception as e:
                logging.error("Attempted converting charCol() input to numpy array and failed.")
                raise e
    else:
        # naively turn it into a numpy array, and see what happens
        try:
            narr = numpy.asarray(data)
            return _custom_charCol(name, narr)
        except Exception as e:
            logging.error("Attempted converting charCol() input to numpy array and failed.")
            raise e


_intTypes = (numpy.int8, numpy.int16, numpy.int32, numpy.int64, numpy.uint8, numpy.uint16, numpy.uint32, numpy.uint64)
_floatTypes = (numpy.float32, numpy.float64)
_intTypeMapping = {
    'byte': [numpy.int8, numpy.uint8], 'short': [numpy.int16, numpy.uint16],
    'int': [numpy.int32, numpy.uint32], 'long': [numpy.int64, numpy.uint64]
}
_floatTypeMapping = {'float': numpy.float32, 'double': numpy.float64}


def _handleIntTypeColumn(typ, func, name, *data):
    if len(data) < 1:
        raise ValueError("No data provided")
    if len(data) == 1 and isinstance(data[0], numpy.ndarray):
        if data[0].dtype in _intTypeMapping[typ]:
            return func(name, jpy.array(typ, data[0]))
        elif data[0].dtype in _intTypes:
            return func(name, jpy.array(typ, data[0].astype(_intTypeMapping[typ][0])))
        elif data[0].dtype in _floatTypes:
            boolc = numpy.isnan(data[0])
            junk = data[0].astype(_intTypeMapping[typ][0])
            junk[boolc] = _nullValues[typ]
            return func(name, jpy.array(typ, junk))
        else:
            raise ValueError("Incompatible numpy dtype ({}) for {} array".format(data[0].dtype, typ))
    elif len(data) == 1 and isinstance(data[0], pandas.Series):
        return _handleIntTypeColumn(typ, func, name, data[0].values)
    else:
        return func(name, *data)


def _handleFloatTypeColumn(typ, func, name, *data):
    if len(data) < 1:
        raise ValueError("No data provided")
    if len(data) == 1 and isinstance(data[0], numpy.ndarray):
        if data[0].dtype == _floatTypeMapping[typ]:
            junk = data[0].copy()
            junk[numpy.isnan(junk)] = _nullValues[typ]
            return func(name, jpy.array(typ, data[0]))
        elif data[0].dtype in _floatTypes:
            junk = data[0].astype(typ)
            junk[numpy.isnan(junk)] = _nullValues[typ]
            return func(name, jpy.array(typ, junk))
        elif data[0].dtype in _intTypes:
            return func(name, jpy.array(typ, data[0].astype(_floatTypeMapping[typ])))
        else:
            raise ValueError("Incompatible numpy dtype ({}) for {} array".format(data[0].dtype, typ))
    elif len(data) == 1 and isinstance(data[0], pandas.Series):
        return _handleFloatTypeColumn(typ, func, name, data[0].values)
    else:
        return func(name, *data)


def _custom_byteCol(name, *data):
    # should only be called from byteCol() below
    return _handleIntTypeColumn('byte', __java_type__.byteCol, name, *data)


def _custom_shortCol(name, *data):
    # should only be called from shortCol() below
    return _handleIntTypeColumn('short', __java_type__.shortCol, name, *data)


def _custom_intCol(name, *data):
    # should only be called from intCol() below
    return _handleIntTypeColumn('int', __java_type__.intCol, name, *data)


def _custom_longCol(name, *data):
    # should only be called from longCol() below
    return _handleIntTypeColumn('long', __java_type__.longCol, name, *data)


def _custom_floatCol(name, *data):
    # should only be called from floatCol() below
    return _handleFloatTypeColumn('float', __java_type__.floatCol, name, *data)


def _custom_doubleCol(name, *data):
    # should only be called from doubleCol() below
    return _handleFloatTypeColumn('double', __java_type__.doubleCol, name, *data)


# Define all of our functionality, if currently possible
try:
    defineSymbols()
except Exception as e:
    pass


@passThrough
def base64Fingerprint(source):
    return __java_type__.base64Fingerprint(source)


@passThrough
def byteCol(name, *data):
    return _custom_byteCol(name, *data)


@passThrough
def charCol(name, *data):
    return _custom_charCol(name, *data)


@passThrough
def col(name, *data):
    return _custom_col(name, *data)


@passThrough
def colSource(*args):
    return _custom_colSource(*args)


@passThrough
def computeFingerprint(source):
    return __java_type__.computeFingerprint(source)


@passThrough
def diff(*args):
    return __java_type__.diff(*args)


@passThrough
def doubleCol(name, *data):
    return _custom_doubleCol(name, *data)


@passThrough
def emptyTable(*args):
    return __java_type__.emptyTable(*args)


@passThrough
def floatCol(name, *data):
    return _custom_floatCol(name, *data)


@passThrough
def getKey(groupByColumnSources, row):
    return __java_type__.getKey(groupByColumnSources, row)


@passThrough
def getPrevKey(groupByColumnSources, row):
    return __java_type__.getPrevKey(groupByColumnSources, row)


@passThrough
def html(source):
    return __java_type__.html(source)


@passThrough
def intCol(name, *data):
    return _custom_intCol(name, *data)


@passThrough
def longCol(name, *data):
    return _custom_longCol(name, *data)


@passThrough
def merge(*args):
    return __java_type__.merge(*args)


@passThrough
def mergeSorted(*args):
    return __java_type__.mergeSorted(*args)


@passThrough
def newTable(*args):
    return _custom_newTable(*args)


@passThrough
def objColSource(*values):
    return _custom_objColSource(*values)


@passThrough
def readBin(*args):
    return __java_type__.readBin(*args)


@passThrough
def readCsv(*args):
    return __java_type__.readCsv(*args)


@passThrough
def readHeaderlessCsv(*args):
    return __java_type__.readHeaderlessCsv(*args)


@passThrough
def roundDecimalColumns(*args):
    return __java_type__.roundDecimalColumns(*args)


@passThrough
def roundDecimalColumnsExcept(table, *columnsNotToRound):
    return __java_type__.roundDecimalColumnsExcept(table, *columnsNotToRound)


@passThrough
def shortCol(name, *data):
    return _custom_shortCol(name, *data)


@passThrough
def show(*args):
    return __java_type__.show(*args)


@passThrough
def showCommaDelimited(*args):
    return __java_type__.showCommaDelimited(*args)


@passThrough
def showWithIndex(*args):
    return __java_type__.showWithIndex(*args)


@passThrough
def string(*args):
    return __java_type__.string(*args)


@passThrough
def writeCsv(*args):
    return __java_type__.writeCsv(*args)
