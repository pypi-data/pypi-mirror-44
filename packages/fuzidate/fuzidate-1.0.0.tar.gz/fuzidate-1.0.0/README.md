# Introduction

Fuzidate is a type used to represent information where the precise date may or
may not be known. While similar to a date range (defined as a tuple containing
a low date and a high date), it encodes information about at what level of
precision a date is not known.

# Background

This datatype was originally developed in cooperation with HRDAG
(http://hrdag.org) for helping to analyze information where deponents of events
were imprecise about when they occurred. So for example, when recalling events
people often are unable to recall them with great precision. Someone when
someone describes a specific event as happening "a month before harvest in
2011", it is not possible to pinpoint it to a specific date. However, given
some contextual information (ie, harvest usually occurs between September and
November) it is possible to construct an estimation of the range around the
event. In this case, if a month before harvest can be roughly be any time
between August and October. This date can be described as a date range as
between 2011-08-01 and 2011-09-31. However, the fact that it is precise to
the level of a month as opposed to a range of days is itself useful
information. This date range can be represented as a starting month plus the
number of additional possible months. In this case, it is represented as
2011-08+1. That is "July 2011 plus one month".

Originally this kind of date representation was referred to as a "flexidate",
however, in the Python world, that package name has already been defined.
Therefore, this package is being named "fuzidate". It contains only one "z"
in order to respect the limited typing capacity experienced by certain founding
HRDAG members. It uses "i" because once you get rid of the "z" it looks better
that way.

# Representation

It is most convenient to represent a fuzidate using two postive integer values.
The first integer encodes the root date with the unknown bits missing. The
second value is referred to as the "offset" describes the range of values
from the root date that the last possible value should be determined. The
offset represents the number of days, months or years depending no the
precision of the fuzidate. If a fuzidate is known at the day level, the offset
represents a count of days. If fuzidate is known at the month level, the offset
represents a count of months. If fuzidate is known at the year level, the
offset represents a count of years.

When represented visually, the integer value of the date is seen as:

`yyyymmdd`

This can be calculated by the formula (y * 10000) + (m * 100) + d. Since months
days and years (sorry 0AD and all BC years) can be represented by a values
\>= 1 unknown values are represented by 0. So, for example if a person
remembers that an event happened in August 1914, the root date can be
represented as `19140800`.

# Invalid fuzidates

By default, the library does not permit the construction of invalid fuzidates.
When an invalid construction is normally attempted the library will raise
`InvalidFuzidateError'.

A fuzidate is invalid when:
* The year is \< 0.
* The year is \> 9999 (this is determined by the built in Python `date` class)
* The high bound of the range created by the offset is beyond
`datetime.date.max`.
* Contains invalid days for specified months. For example 1914-10-31 is valid
but 1914-09-31 is not.
* Contains invalid months (months \> 12)
* Contains precise information in lower order values than higher ones. For
example, a flexidate 1914-00-28 is invalid because it has a precise day
even though the month is unknown.
* Offset must be \>= 0.

However, it is possible to explicitly override this behavior with the
`validate` parameter on most construction functions.

This library allows for representation of invalid fuzidatesm because often
data are not entered correctly when read from other sources and may need to
undergo some cleaning steps (or elimination, depending on circumstances). This
library allows for the preservation of these dates where possible. So, for
example, if a date has a month of "17" instead of "7" it is possible to
construct a fuzidate as such. However, when checked for validity before
certain operations, this will cause an error.

Many operations for fuzidate cause a validity check. These checks will raise
`InvalidFuzidateError` when they fail.

# Fuzidate parsing

The basic parsing operation is `Fuzidate.parse(s: str)`. The generalized
format of this parser is:

`<year>-<month>-<day>+<offset>`

For example: `1914-07-00+2`

The offset is optional. A missing offset is treated as offset == 0.

Days and months may also be left off. Those missing values are treated as 0
(unknown). So for example: `1914-07+2` is the same as `1914-07-00+2`.

The padding around months and days is optional. `1914-7-0+2` parses.

The unknown date is represented as `0`.

# Order

Fuzidates are fully ordered. Less precise dates are ordered before more
precise values. So, `1914-07` \< `1914-07-28`. Shorter ranges are ordered
before greater ranges. So `1914-07+2` \< `1914-07+3`.

# Usage

## Construction

Fuzidates are create in a few ways. In general, avoid using the constructor.

To create a fuzidate from integers: `Fuzidate.from_int(19140700, 2)`

To create a fuzidate from its component parts:
`Fuzidate.compose(1914, 07, offset=2)`

To create a fuzidate from a Python date:
`Fuzidate.from_date(date(1914, 8, 28))`

To create a fuzidate from a string: `Fuzidate.parse('1914-7+2')`

There are also aliases for these construction methods in the `fuzidate`
module itself.  So `fuzidate.parse('1914-7')` is the same as
`fuzidate.Fuzidate.parse('1914-7')`.

## Range

A Python `date` range can be constructed from a valid fuzidate using:
`fzd.range`. It returns a tuple (low, high) of type (date, date).

It is also possible to extract the low value and high value individually
as `fzd.low` and `fzd.high` respectively. For example, using fuzidate
`Fuzidate.compose(1914, 7, offset=2)`:
* `fzd.low` becomes `date(1914, 7, 1)`.
* `fzd.high` becomes `date(1914, 9, 30)`.

