
# Choochoo (ch2)

An **open**, **hackable** and **free** training diary.

Please see the [full
documentation](https://andrewcooke.github.io/choochoo/).  This page
contains only:

* [Technical Overview](#technical-overview)
* [Latest Changes](#latest-changes)

![](docs/graphic-summary.png)

![](docs/graphic-similarity.png)

## Technical Overview

All data are stored in an SQLite database (SQLAlchemy ORM interface).
The schema separates "statistics" (named time series data) from the
source (which might be direct entry, read from a FIT file, or
calculated from pre-existing values).

The "diary" view, where the user enters data, is itself generated from
the database.  So the fields displayed (and the statistics collected)
can be customized.  This configuration can include "schedules" which
control when information is displayed (eg: weekdays only; every other
day; second Sunday in the month).

The combination of customizable diary fields and scheduling allows
training plans to be entered and displayed.

Customization (fields, training plans, etc) must be done via Python or
SQL.  There is no graphical user interface for configuration.  This
presents a steep learning curve but is ultimately very flexible -
"any" training plan can be accommodated.  Python code for generating
example plans is included (see package `ch2.config.plan`).

Data are processed via "pipelines".  These are Python classes whose
class names are also configured in the database.  Existing pipelines
calculate statistics from FIT file data, recognise segments from GPS
endpoints, and generate summaries (eg monthly averages).

A Python interface allows data to be extracted as DataFrames for
analysis in Jupyter workbooks (or dumping to stdout).  So general
Python data science tools (Pandas, Numpy, etc) can be used to analyze
the data.  Example workbooks are included in the source.

The data are stored in an "open" format, directly accessible by third
party tools, and easily backed-up (eg by copying the database file).
When the database format changes scripts are provided to migrate
existing data (see package `ch2.migraine`).  Data extracted from FIT
files are *not* migrated - they must be re-imported.

Support libraries include FIT file parsing, spatial R-Trees, and
reading elevation data from SRTM files.

Currently the program is single-user (ie the data in the database are
not grouped by user).  Multiple users can co-exist using separate
database files.

*Choochoo collects and organizes time-series data using
athlete-appropriate interfaces.  It facilitates calculations of
derived statistics and extraction of data for further analysis using
Python's rich data science tools.  Both data and code are open and
extensible.*

## Latest Changes

### v0.18.0

Major rewrite to import pipelines.  Now use multiple processes where
possible.  Rebuild time for my data, on my machine, cut in half (and
now including power calculations).  Experimented with power
calculations, but "advanced" approach, fitting for wind direction and
speed, didn't give good results (and was slow, hence the rewrite).
Migrate existing databases using `migraine/sqlp2sqlq.sh` (edit the
file, run, and then reload data from FIT files).

### v0.17.0

Added `timestamp` to database which improves / extends logic to avoid
un-needed work re-calcualting statistics.  Migrate existing databases
using `migraine/sqlo2sqlp.sh` (edit the file, run, and then reload
data from FIT files).

### v0.16.0

Diary plots are generated via Jupyter (running an embedded Jupyter
server, generating a notebook, and pushing it to the browser) rather
than Bokeh.  This works round some Bokeh server bugs and serves as a
nice intro to Jupyter.  Cleaned up a lot of the plotting code, too.

### v0.15.0

Modified database schema (`serial` in statistic_journal which makes
time-series logic simpler).  Migrate existing databases using
`migraine/sqln2sqlo.sh` (you will then need to reload data from FIT
files).

### v0.14.0

Zoom in summary plots (embedded Bokeh server while diary is used).

### v0.13.0

Automatic addition of
[elevation](https://andrewcooke.github.io/choochoo/elevation) and
detection of [climbs](https://andrewcooke.github.io/choochoo/docs).

### v0.12.0

Extend `ch2 fix-fit` functionality (can scan a directory and print
file names of god or bad files).  Required a change in parameters -
now you must explicitly add `--fix-header` and `--fix-checksum` if you
want to do that.

### v0.11.0

Parsing of "accumulated" fields in FIT files plus a bunch more fixes
thanks to test data from python-fitparse.

### v0.10.0

Contains a tool to [fix corrupt FIT
files](https://andrewcooke.github.io/choochoo/fix-fit).

### v0.9.0

Choochoo has a [GUI](https://andrewcooke.github.io/choochoo/summary)!!!

### v0.8.0

[Nearby activities](https://andrewcooke.github.io/choochoo/nearby) and
simplified / improved data access in Jupyter.

### v0.7.0

[Segments](https://andrewcooke.github.io/choochoo/segments).

### v0.6.0

Impulse calculations.  Faster importing and statistics.  See [Scaled
Heart Rate Impulse -
SHRIMP](https://andrewcooke.github.io/choochoo/impulse)

### v0.5.0

More readable database (using text instead of opaque numerical hashes
in a couple of places).  Faster database loading of activity and
monitor data.  Time is now directly present in the statistic journal
table, along with all activity and monitor data (no separate data
tables).  This enables TSS calculation (next version).

### v0.4.0

Tidied lots of rough corners, improved docs, added examples, download
from Garmin Connect.  This could probably be used by 3rd parties.

### v0.3.0

Diary now uses dates (rather than datetimes) and is timezone aware
(Previously all times were UTC datetimes; now data related to the
diary - like statistics calculated on daily intervals - use the date
and the local timezone to convert to time.  So, for example, stats
based on monitor data are from your local "day" (midnight to
midnight)).

Monitor data from FIT files can be imported.

### v0.2.0

Major rewrite to generalize the database schema.  Moved a lot of
configuration into the database.  Now much more flexible, but less
interactive.
