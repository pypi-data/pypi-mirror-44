"""
ticDat module for reading and writing data modules in ticDat format.
ticDat is a simple, easy-to-read format for tabular data. It is partly inspired by csv.DictReader
and csv.DictWriter.  When primary keys are specified, each table is a dictionary of dictionaries.
Otherwise, each table is an enumerable of dictionaries (as in DictReader/DictWriter). When foreign keys are
specified, they are used to create links between the "row dictionaries" of the parent table to the matching
"row dictionaries" of the child objects.
Although ticDat was specifically designed with Mixed Integer Programming data sets in mind, it can be used for
rapidly developing a wide variety of mathematical engines. It facilitates creating one definition of your
input data schema and one solve module, and reusing this same code, unchanged, on data from different
sources. This "separation of model from data" enables a user to move easily from toy, hard coded data to
larger, more realistic data sets.
The ticDat library is distributed under the BSD2 open source license.
"""

from ticdat.ticdatfactory import TicDatFactory, freeze_me
from ticdat.utils import Sloc, LogFile, Progress, Slicer, \
                         find_denormalized_sub_table_failures, standard_main, \
                         gurobi_env, ampl_format, verify
from ticdat.opl import opl_run, create_opl_mod_text, create_opl_mod_output_text
from ticdat.lingo import lingo_run
from ticdat.model import Model
from ticdat.pandatfactory import PanDatFactory
__version__ = '0.2.18'
__all__ = ["TicDatFactory", "PanDatFactory", "freeze_me", "LogFile", "Sloc", "Slicer", "Progress", "standard_main",
           "Model", "opl_run", "create_opl_mod_text", "create_opl_mod_output_text", "lingo_run", "ampl_format",
           "gurobi_env", "verify"]
