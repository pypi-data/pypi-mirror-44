"""Tools for managing archives

This package provides tools for managing archives.  An archive in
terms of this package is a (compressed) tar archive file with some
embedded metadata on the included files.  This metadata include the
name, file stats, and checksums of the file.

The package provides a command line tool to enable the following
tasks:

+ Create an archive, takes a list of files to include in the archive
  as input.

+ Check the integrity and consistency of an archive.

+ List the contents of the archive.

+ Display details on a file in an archive.

+ Given a list of files as input, list those files that are either not
  in the archive or where the file in the archive differs.

All tasks providing information on an archive take this information
from the embedded metadata.  Retrieving this metadata does not require
reading through the compressed tar archive.
"""

__version__ = "0.1"

from archive.archive import Archive
from archive.exception import *

