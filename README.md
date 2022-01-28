# gaussMiner
gaussian log file scraper for database creation

Usage:

This code was written in python 3

Usage: python python gaussMiner '<pattern>' flags
 
e.g. <pattern> = *.log  ...Must put glob pattern in quotes to avoid the shell from expanding the wildcards etc.  Python will do that later when I want it to.  

python gaussMiner --help

  -h, --help   show this help message and exit
  --latexXYZ   print all xyz coordinates from logfiles in filepath a file in
               latex tabular format to be used in the longtable environment
  --XYZs       print all xyz coordinates from logfiles to individual xyz files
  --gjf        prepare gjf files from final logfiles coordinates
  --dataBase   prepare a comprehensive table of available properties
