Appendix
========


.. _appendix_typed_text:

Input typed values as text
--------------------------

Some nodes will allow you to input text to use to produce a typed value - which
could depend, for example, on the type of columns used in the operation.  The
text needs to use a format that is understood by the functions for reading the
type used.

If the type is text, any input will do, but for other types see the following
examples:

    :bool: True, False, true, false, 1, 0
    :integer: 0, 1, 2, ...
    :float: 0, 0.0, 1, 1.1, ...
    :text: Anything goes here!
    :datetime: 1970-01-01T00:00:00.000000,
               1970-01-01 00:00:00.000000,
               1970-01-01 00:00:00.00,
               1970-01-01
    :timedelta: 1 days,
                2 d,
                44.333 seconds,
                2 days 2 h 44 seconds,
    :complex:  1.1 + 2j
