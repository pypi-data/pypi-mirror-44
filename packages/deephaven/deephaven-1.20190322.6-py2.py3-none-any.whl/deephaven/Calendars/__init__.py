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
        __java_type__ = jpy.get_type("com.illumon.util.calendar.Calendars")


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
def calendar(*args):
    return __java_type__.calendar(*args)


@passThrough
def calendarNames():
    return list(__java_type__.calendarNames())


@passThrough
def getDefaultName():
    return __java_type__.getDefaultName()
