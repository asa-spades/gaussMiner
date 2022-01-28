from pathlib import Path  
import os
import glob
import re
class logFileObj(object):
    def __init__(self, fileStringPath, filePath = None, name = None, xyz = None, latexXYZ = None, energyFree = None, energySCF = None, 
                 molFormula = None, program = None, homo = None, lumo =  None, alphaOcc = None, alphaVirtual = None,
                homoMinusOne = None, homoOrbNumber = None, homoMinusOneOrbNumber = None, betaHomo = None, betaLumo = None, 
                 betaOcc = None, betaVirtual = None):
        #The following are the class attributes 
        # I had a self.datablock but the python literature idicates I might have problems with that file being kept open in that case
        self.fileStringPath = fileStringPath
        self.filePath = Path(fileStringPath)
        self.name = self.filePath.name
        # Im not sure if I really want these to be attributes or things I get from methods
        self.energyFree = energyFree
        self.energySCF = energySCF
        self.molFormula = molFormula
        self.program = program
        self.homo = homo
        self.lumo = lumo
        self.alphaOcc = alphaOcc
        self.alphaVirtual = alphaVirtual
        self.homoMinusOne = homoMinusOne
        self.homoOrbNumber = homoOrbNumber
        self.homoMinusOneOrbNumber = homoMinusOneOrbNumber
        self.latexXYZ = latexXYZ
        self.betaHomo = betaHomo
        self.betaOcc = betaOcc
        self.betaVirtual = betaVirtual
        self.betaLumo = betaLumo
        #The following are the class methods
    def getText(self): # this method is just to test my object creation
        return('Test object creation by returning this text')
    
    def getFinalSCF(self):
        regSCF = re.compile(r'.*SCF Done.*')
        regSCFenerg = re.compile(r'-\d*\.\d*')
        finalSCFenerg = ''
        finalSCFenergString = ''
        with open(self.filePath) as dataBlock:
            readDataBlock = dataBlock.read()
            SCFmatches = regSCF.findall(readDataBlock)
            try:
                finalSCFenergString = SCFmatches[-1]
            except IndexError:
                pass
            finalSCFenerg = regSCFenerg.search(finalSCFenergString)
            try:
                return(float(finalSCFenerg.group()))
            except AttributeError:
                pass
            
    def getEnergyFree(self):
        regFreeStatement = re.compile(r'.*Sum of electronic and thermal Free Energies.*')
        regFreeEnerg = re.compile(r'-\d*\.\d*')
        finalFreeEnergStr = ''
        finalFreeEnerg = ''
        with open(self.filePath) as dataBlock:
            readDataBlock = dataBlock.read()
            regMatches = regFreeStatement.findall(readDataBlock)
            try:
                finalFreeEnergStr = regMatches[-1]
            except IndexError:
                pass
            finalFreeEnergy = regFreeEnerg.search(finalFreeEnergStr)
            try:
                return(float(finalFreeEnergy.group()))
            except AttributeError:
                pass            
            
    def getMOs(self): #potential error wont work on log files strung together as written
        molecOrbDict = {}
        with open(self.filePath) as dataBlock:
            dataLines = dataBlock.readlines()
            occOrbsReg = re.compile(r'(Alpha\s{2}occ[.]\seigenvalues\s-{2})((\s*-?\d*[.]\d*)*)')
            virtualOrbsReg = re.compile(r'(Alpha\svirt[.]\seigenvalues\s-{2})((\s*-?\d*[.]\d*)*)')
            orbsOcc = ''
            orbsVirtual = ''
            for line in dataLines:
                occRegMatches = occOrbsReg.search(line)
                try:
                    orbsOcc += occRegMatches.group(2)
                    molecOrbDict['occOrbs'] = orbsOcc.split()
                except AttributeError:
                    pass
            for line in dataLines:
                virtRegMatches = virtualOrbsReg.search(line)
                try:
                    orbsVirtual += virtRegMatches.group(2)
                    molecOrbDict['virtOrbs'] = orbsVirtual.split()
                except AttributeError:
                    pass
       # This snippet deletes any sets of alpha energies before the last set in the log file
        i = 1
        while i < len(molecOrbDict['occOrbs']):
            if float(molecOrbDict['occOrbs'][i]) < float(molecOrbDict['occOrbs'][(i-1)]):
                del molecOrbDict['occOrbs'][:i]
            else:
                i += 1
        i = 1
        while i < len(molecOrbDict['virtOrbs']):
            if float(molecOrbDict['virtOrbs'][i]) < float(molecOrbDict['virtOrbs'][(i-1)]):
                del molecOrbDict['virtOrbs'][:i]
            else:
                i += 1
        # This snippet of code converts the strings in these lists to floats
        molecOrbDict['occOrbs'] = list(map(float, molecOrbDict['occOrbs']))
        molecOrbDict['virtOrbs'] = list(map(float, molecOrbDict['virtOrbs']))
        return(molecOrbDict)
    
    def getBetaMOs(self): #potential error wont work on log files strung together as written
        betaMolecOrbDict = {}
        with open(self.filePath) as dataBlock:
            dataLines = dataBlock.readlines()
            occOrbsReg = re.compile(r'(Beta\s{2}occ[.]\seigenvalues\s-{2})((\s*-?\d*[.]\d*)*)')
            virtualOrbsReg = re.compile(r'(Beta\svirt[.]\seigenvalues\s-{2})((\s*-?\d*[.]\d*)*)')
            betaOrbsOcc = ''
            betaOrbsVirtual = ''
            for line in dataLines:
                occRegMatches = occOrbsReg.search(line)
                try:
                    betaOrbsOcc += occRegMatches.group(2)
                    betaMolecOrbDict['betaOccOrbs'] = betaOrbsOcc.split()
                except AttributeError:
                    pass
            for line in dataLines:
                virtRegMatches = virtualOrbsReg.search(line)
                try:
                    betaOrbsVirtual += virtRegMatches.group(2)
                    betaMolecOrbDict['betaVirtOrbs'] = betaOrbsVirtual.split()
                except AttributeError:
                    pass
       # This snippet deletes any sets of alpha energies before the last set in the log file
        i = 1
        while i < len(betaMolecOrbDict['betaOccOrbs']):
            if float(betaMolecOrbDict['betaOccOrbs'][i]) < float(betaMolecOrbDict['betaOccOrbs'][(i-1)]):
                del betaMolecOrbDict['betaOccOrbs'][:i]
            else:
                i += 1
        i = 1
        while i < len(betaMolecOrbDict['betaVirtOrbs']):
            if float(betaMolecOrbDict['betaVirtOrbs'][i]) < float(betaMolecOrbDict['betaVirtOrbs'][(i-1)]):
                del betaMolecOrbDict['betaVirtOrbs'][:i]
            else:
                i += 1
        # This snippet of code converts the strings in these lists to floats
        betaMolecOrbDict['betaOccOrbs'] = list(map(float, betaMolecOrbDict['betaOccOrbs']))
        betaMolecOrbDict['betaVirtOrbs'] = list(map(float, betaMolecOrbDict['betaVirtOrbs']))
        return(betaMolecOrbDict)
    
    def getCoords(self):
        inputPath = self.filePath
        with open(inputPath, "r") as f:

            latexHeader = r'\hline'
            latexAlign = '&'
            latexLineEnd = r'\\'

            finalCoordsStart = ''
            finalCoordsEnd = ''
            coordsLength = 0
            coordsList = []
            isStruct = False
            start = 0
            dataBlock = []
            for i,line in enumerate(f):
                dataBlock.append(line.strip())
                if line.find('Standard orientation') != -1:
                    isStruct = True
                    start = i + 5
                    finalCoordsStart = start
                if line.find('-----') != -1 and i > int(start) and isStruct == True:
                    finalCoordsEnd = i
                    isStruct = False
           # print(dataBlock[int(finalCoordsStart):int(finalCoordsEnd)])
            coordsList = (dataBlock[int(finalCoordsStart):int(finalCoordsEnd)])
            coordsLength += (len(coordsList))
            latexLengthSpecifierLine = [str(coordsLength), latexAlign, latexAlign, latexAlign, latexLineEnd]
            coordsList.insert(0,latexLengthSpecifierLine)
            latexHeaderLine = [self.name, latexAlign, str(self.energyFree), latexAlign, latexAlign, latexLineEnd + latexHeader]
            coordsList.insert(1,latexHeaderLine)
            for i in range(2,len(coordsList)):
                coordsLine = coordsList[i].split()
                del(coordsLine[0])
                del(coordsLine[1])
                coordsLine[0] = periodicTable[coordsLine[0]]
                coordsLine[1] = latexAlign + coordsLine[1]
                coordsLine[2] = latexAlign + coordsLine[2]
                coordsLine[3] = latexAlign + coordsLine[3] + latexLineEnd
                coordsList[i] = coordsLine
            return(coordsList)



                
#   def isNormalterm(self):
    
#    def whatIsJobType(self):
        
#    def 
    
    
# this is the element dictionary
periodicTable = {"1" : "H", "2" : "He", "3" : "Li", "4" : "Be", "5" : "B", \
"6"  : "C", "7"  : "N", "8"  : "O",  "9" : "F", "10" : "Ne", \
"11" : "Na" , "12" : "Mg" , "13" : "Al" , "14" : "Si" , "15" : "P", \
"16" : "S"  , "17" : "Cl" , "18" : "Ar" , "19" : "K"  , "20" : "Ca", \
"21" : "Sc" , "22" : "Ti" , "23" : "V"  , "24" : "Cr" , "25" : "Mn", \
"26" : "Fe" , "27" : "Co" , "28" : "Ni" , "29" : "Cu" , "30" : "Zn", \
"31" : "Ga" , "32" : "Ge" , "33" : "As" , "34" : "Se" , "35" : "Br", \
"36" : "Kr" , "37" : "Rb" , "38" : "Sr" , "39" : "Y"  , "40" : "Zr", \
"41" : "Nb" , "42" : "Mo" , "43" : "Tc" , "44" : "Ru" , "45" : "Rh", \
"46" : "Pd" , "47" : "Ag" , "48" : "Cd" , "49" : "In" , "50" : "Sn", \
"51" : "Sb" , "52" : "Te" , "53" : "I"  , "54" : "Xe" , "55" : "Cs", \
"56" : "Ba" , "57" : "La" , "58" : "Ce" , "59" : "Pr" , "60" : "Nd", \
"61" : "Pm" , "62" : "Sm" , "63" : "Eu" , "64" : "Gd" , "65" : "Tb", \
"66" : "Dy" , "67" : "Ho" , "68" : "Er" , "69" : "Tm" , "70" : "Yb", \
"71" : "Lu" , "72" : "Hf" , "73" : "Ta" , "74" : "W"  , "75" : "Re", \
"76" : "Os" , "77" : "Ir" , "78" : "Pt" , "79" : "Au" , "80" : "Hg", \
"81" : "Tl" , "82" : "Pb" , "83" : "Bi" , "84" : "Po" , "85" : "At", \
"86" : "Rn" , "87" : "Fr" , "88" : "Ra" , "89" : "Ac" , "90" : "Th", \
"91" : "Pa" , "92" : "U"  , "93" : "Np" , "94" : "Pu" , "95" : "Am", \
"96" : "Cm" , "97" : "Bk" , "98" : "Cf" , "99" : "Es" ,"100" : "Fm", \
"101": "Md" ,"102" : "No" ,"103" : "Lr" ,"104" : "Rf" ,"105" : "Db", \
"106": "Sg" ,"107" : "Bh" ,"108" : "Hs" ,"109" : "Mt" ,"110" : "Ds", \
"111": "Rg" ,"112" : "Uub","113" : "Uut","114" : "Uuq","115" : "Uup", \
"116": "Uuh","117" : "Uus","118" : "Uuo"}

# This snippet creates a dictionary of logfile objects
# to do: extend this to input dir
def listLogsMakelogFileObj(): 
    
    '''This function is designed to get a list of log files and turn them into a series of logfile objects
    that have a group of methods making their parsing and metadata collection easier'''
    
    workingDir = Path.cwd() #defines the working directory as current working directory path object
    logPathList = list(workingDir.glob('*.log')) # makes a list of path object with stated pattern
    
    logObjectDictionary = {}
    for logPath in logPathList:
        logPathString = str(logPath)
        logObject = logFileObj(logPathString)
        logObjectDictionary[logPathString] = logObject
    
    return(logObjectDictionary)

# creating the dictionary of logFile objects with filePath string keys
logFileObjs = listLogsMakelogFileObj()

# assigning SCF energy metaData to logFile objects using the corresponding method.
for key in logFileObjs.keys():
    logFileObjs[key].energySCF = logFileObjs[key].getFinalSCF()
for key in logFileObjs.keys():
    logFileObjs[key].energyFree = logFileObjs[key].getEnergyFree()

#This code snippet assigns alpha electron energies as attributes to log file objects
for key in logFileObjs.keys():
    try: 
        alphaEnergiesDict = logFileObjs[key].getMOs()
        logFileObjs[key].alphaOcc = alphaEnergiesDict['occOrbs']
        logFileObjs[key].alphaVirtual = alphaEnergiesDict['virtOrbs']
        logFileObjs[key].homo = alphaEnergiesDict['occOrbs'][-1]
        logFileObjs[key].lumo = alphaEnergiesDict['virtOrbs'][0]
        logFileObjs[key].homoMinusOne = alphaEnergiesDict['occOrbs'][-2]
        logFileObjs[key].homoOrbNumber = len(alphaEnergiesDict['occOrbs'])
        logFileObjs[key].homoMinusOneOrbNumber = len(alphaEnergiesDict['occOrbs']) - 1
    except KeyError:
        pass
for key in logFileObjs.keys():
    try: 
        betaEnergiesDict = logFileObjs[key].getBetaMOs()
        logFileObjs[key].betaOcc = betaEnergiesDict['betaOccOrbs']
        logFileObjs[key].betaVirtual = betaEnergiesDict['betaVirtOrbs']
        logFileObjs[key].betaHomo = betaEnergiesDict['betaOccOrbs'][-1]
        logFileObjs[key].betaLumo = betaEnergiesDict['betaVirtOrbs'][0]
    except KeyError:
        pass

workDir = Path.cwd()
outPutFileName = str(workDir.name) + '_csv.txt'
print(outPutFileName)
with open(outPutFileName, "a+") as fOut:
    fOut.write('name, energySCF, energyFree, homo, homoMinusOne, homoMinusOneOrbNumber, lumo, betaHomo, betaLumo\n')
    for key in logFileObjs.keys():
        fOut.write(f'{logFileObjs[key].name}, {logFileObjs[key].energySCF}, {logFileObjs[key].energyFree}, \
{logFileObjs[key].homo}, {logFileObjs[key].homoMinusOne}, {logFileObjs[key].homoMinusOneOrbNumber},  {logFileObjs[key].lumo}, {logFileObjs[key].betaHomo}, {logFileObjs[key].betaLumo}\n')
        
for key in logFileObjs.keys():
    try: 
        logFileObjs[key].latexXYZ = logFileObjs[key].getCoords()
    except (KeyError, ValueError):
        pass

workDir = Path.cwd()
outPutFileName = str(workDir.name) + '_latexXYZ.txt'
print(outPutFileName)
with open(outPutFileName, "a+") as fOut:
    for key in logFileObjs.keys():
        try:
            for i in range(len(logFileObjs[key].latexXYZ)):
                fOut.write(' '.join(logFileObjs[key].latexXYZ[i]) + '\n')
        except TypeError:
            pass

