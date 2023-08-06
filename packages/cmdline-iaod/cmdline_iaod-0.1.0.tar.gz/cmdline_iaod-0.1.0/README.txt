This package takes a whole-genome sequence file and an annotation file (a GTF or
GFF3 file in most cases) and uses them to create an SQLite database of
intron annotation information. This package uniquely annotates intron class for
every intron annotated in the annotation file, so it can be used to identify
all U12-dependent introns in any genome with annotated introns.

There is also a script called "search_functions.py" that allows one to execute
various queries against the SQLite database without needing to write any SQL.
For more details about executing queries, run the script with no arguments.
