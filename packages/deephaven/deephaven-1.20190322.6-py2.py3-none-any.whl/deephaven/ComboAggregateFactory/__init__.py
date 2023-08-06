#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

##############################################################################
# This code is auto generated. DO NOT EDIT FILE!
# Run generatePythonIntegrationStaticMethods or 
# "./gradlew :Generators:generatePythonIntegrationStaticMethods" to generate
##############################################################################


import jpy
import functools


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
        __java_type__ = jpy.get_type("com.illumon.iris.db.v2.by.ComboAggregateFactory")


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


# Define all of our functionality, if currently possible
try:
    defineSymbols()
except Exception as e:
    pass


@passThrough
def Agg(*args):
    return __java_type__.Agg(*args)


@passThrough
def AggAbsSum(*matchPairs):
    return __java_type__.AggAbsSum(*matchPairs)


@passThrough
def AggArray(*matchPairs):
    return __java_type__.AggArray(*matchPairs)


@passThrough
def AggAvg(*matchPairs):
    return __java_type__.AggAvg(*matchPairs)


@passThrough
def AggCombo(*aggregations):
    return __java_type__.AggCombo(*aggregations)


@passThrough
def AggCount(resultColumn):
    return __java_type__.AggCount(resultColumn)


@passThrough
def AggFirst(*matchPairs):
    return __java_type__.AggFirst(*matchPairs)


@passThrough
def AggFormula(formula, formulaParam, *matchPairs):
    return __java_type__.AggFormula(formula, formulaParam, *matchPairs)


@passThrough
def AggLast(*matchPairs):
    return __java_type__.AggLast(*matchPairs)


@passThrough
def AggMax(*matchPairs):
    return __java_type__.AggMax(*matchPairs)


@passThrough
def AggMed(*matchPairs):
    return __java_type__.AggMed(*matchPairs)


@passThrough
def AggMin(*matchPairs):
    return __java_type__.AggMin(*matchPairs)


@passThrough
def AggPct(*args):
    return __java_type__.AggPct(*args)


@passThrough
def AggStd(*matchPairs):
    return __java_type__.AggStd(*matchPairs)


@passThrough
def AggSum(*matchPairs):
    return __java_type__.AggSum(*matchPairs)


@passThrough
def AggVar(*matchPairs):
    return __java_type__.AggVar(*matchPairs)


@passThrough
def AggWAvg(weight, *matchPairs):
    return __java_type__.AggWAvg(weight, *matchPairs)
