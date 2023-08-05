#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Thibault TUBIANA"
__version__  = "GUI 1.0.2"
__license__ = "GNU GPLv3"
__date__ = "2018/02"

"""
This module is the Graphical User Interface (GUI) of TTclust. Keep this module
in the same directory of ttclust.py. 
"""
import matplotlib as mpl
mpl.use('WXAgg')
from gooey import Gooey, GooeyParser
import ttclust
import os,sys
import subprocess

#nonbuffered_stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
#sys.stdout = nonbuffered_stdout
LOGFILE=""

def which(pgm):
    """
    DESCRIPTION : replace shutil.which which is not implemented in Python <3.3
    from : https://stackoverflow.com/a/9877856/1928090
    Args:
        pgm (string): programme name
    return :
        p (string): programme path
    """
    path=os.getenv('PATH')
    for p in path.split(os.path.pathsep):
        p=os.path.join(p,pgm)
        if os.path.exists(p) and os.access(p,os.X_OK):
            return p

@Gooey(required_cols=1,tabbed_groups=True)
def parseArg():
    parser=GooeyParser(description="This program was developped in order to clusterize molecular dynamic trajectories")


    
    files = parser.add_argument_group("File")
    files.add_argument("Trajectory File",
                       help="Trajectory file (xtc/trr/dcd/nc/pdb..)",
                       widget="FileChooser")
    files.add_argument("Topology File", help="Topology file (pdb/prmtop..)", widget="FileChooser")
    files.add_argument("-l","--Log File", help="Logfile", widget="FileSaver", default="clustering.log")
    


    selection = parser.add_argument_group("Selection")
    selection.add_argument('-st','--Trajectory Selection', help="selection syntax for trajectory extraction.", default="all")
    selection.add_argument('-sa','--Alignement Selection', help="selection syntax for alignement. use 'none' to remove alignement", default="backbone")
    selection.add_argument('-sr','--Selection for RMSD Calculation', help="selection syntax for RMSD (used for clustering).",  default="backbone")

    #Clustering arguments
    clustering = parser.add_argument_group("Clustering")
    clustering.add_argument('-m','--Clustering Method', help="method for clustering", default="ward", choices=["ward",
                                                                                                              "single ",
                                                                                                              "complete",
                                                                                                              "average",
                                                                                                              "weighted",
                                                                                                              "centroid",
                                                                                                              "median"])

    
    clustering_cutoff = clustering.add_mutually_exclusive_group(required=True,
                                                                gooey_options={'initial_selection': 0}
                                                                )
    clustering_cutoff.add_argument("-aa", "--Auto Clustering",
                                   action="store_true",
                                   help="Autoclustering with the Elbow method",
                                   default=True)
    clustering_cutoff.add_argument("-gs","--Graphical Selection",
                                   action="store_true",
                                   help="Clic on the dendrogram to clusterize")
    clustering_cutoff.add_argument('-ng', "--Number of clustering Group",
                                   help="Number of group wanted",
                                   default=None)
    clustering_cutoff.add_argument('-cc',"--Dendrogramme Clustering Cutoff",
                                   help="cutoff for clusterization from hierarchical clusturing with Scipy", 
                                   default=None)

    


    args = vars(parser.parse_args())
    #args = vars(parser.parse_args())


    if args["Auto Clustering"] == True:
        args["Dendrogramme Clustering Cutoff"] = None
        args["Number of clustering Group"] = "auto"
    return(args)



def rename_args_keys(args):
    """
    DESCRIPTION
    Rename dictionnary keys to have the same names than TTCLUST main program)
        Arg : args (dictionnary of arguments)
        return : renamed_args (renamed dictionnary of arguments)
    """
    renamed_args={"traj":args["Trajectory File"],
                  "top":args["Topology File"],
                  "logfile":args["Log File"],
                  "select_traj":args["Trajectory Selection"],
                  "select_alignement":args["Alignement Selection"],
                  "select_rmsd":args["Selection for RMSD Calculation"],
                  "method":args["Clustering Method"],
                  "cutoff":args["Dendrogramme Clustering Cutoff"],
                  "ngroup":args["Number of clustering Group"],
                  "interactive":"N",}
    return renamed_args


def main():
    os.chdir("D:\\CLOUDS\\GoogleDrive\\WORK\\Perso\\DEV\\ttclust\\examples")
    if (sys.platform == 'darwin' and
        ('| packaged by conda-forge |' in sys.version or
         '|Anaconda' in sys.version)):

        # On macOS with Anaconda, GUI applications need to be run using
        # `pythonw`. Since we have no way to determine whether this is currently
        # the case, we run this script again -- ensuring we're definitely using
        # pythonw.
        
        if 'pythonw' not in sys.executable:
            sys.executable = which("pythonw")
            subprocess.Popen([sys.executable, __file__])
            sys.exit()
    
    """Execute TTclust with the GUI"""
    print("\n********************************************************")
    print("*****************  TTCLUST {} *********************".format(\
              __version__))
    print("********************************************************\n")
    #We get all arguments
    args=parseArg()
    args=rename_args_keys(args)

    #add ".log" if the logfile doesn't have extension
    if os.path.splitext(args["logfile"])[1] == "":
        args["logfile"] = args["logfile"]+".log"

    #create a folder based on the logfile name and write everything inside
    logname = os.path.splitext(args["logfile"])[0]
    args["logname"] = logname
    if not os.path.exists(logname):
        os.makedirs(logname)
    elif not os.path.isdir(logname): #If a file exist with the same foldername
        os.rename(logname,logname+".bak")
        print("NOTE : A file with the same folder name was found and rename "
              "into {}.bak".format(logname))
        os.makedirs(logname)

    filename = args["logfile"].split(os.sep)[-1]
    LOGFILE=open("{0}/{1}".format(logname,filename),"w")
    ttclust.define_LOGFILE(LOGFILE)
    ttclust.Cluster_analysis_call(args)
    LOGFILE.close()



if __name__ == '__main__':
    main()
    
