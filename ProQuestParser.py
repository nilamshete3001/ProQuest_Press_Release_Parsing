"""
Created on Sep 20, 2015
@author: Nilam
"""
from xml.dom import minidom
from bs4 import BeautifulSoup
from urllib import request
from urllib.request import HTTPCookieProcessor
import os

#List of all company names
keywords = {"biopure", "biodelivery%20sciences%20international", "fluidigm", "onconova%20therapeutics", "immune%20design", "pharmasset", "genoptix", "lumera", "coley%20pharmaceutical%20group", "tesaro", "amicus%20therapeutics", "argos%20therapeutics", "ista%20pharmaceuticals", "chirex", "affymetrix", "neurocrine%20biosciences", "corium%20international", "cancer%20genetics","nephrogenex", "carbylan%20therapeutics", "houghten%20pharmaceuticals", "dyax", "vitae%20pharmaceuticals", "sano", "celladon", "quotient%20", "geron","transkaryotic%20therapies", "dov%20pharmaceutical", "auspex%20pharmaceuticals", "xencor","xtl%20biopharmaceuticals%20", "histogenics", "transgenomic", "bind%20therapeutics", "sequenom","dermira","collegium%20pharmaceutical","adolor","exact%20sciences","exact%20sciences","osiris%20therapeutics", "millennium%20pharmaceuticals", "nupathe","enanta%20pharmaceuticals", "vysis", "momenta%20pharmaceuticals", "microcide%20pharmaceuticals", "spiros%20development%20ii", "connetics", "applied%20imaging", "eyetech%20pharmaceuticals", "myogen", "ardelyx", "metabasis%20therapeutics", "maxygen", "genomic%20health", "genomic%20health", "foundation%20medicine", "atyr%20pharma", "veracyte", "verastem", "jazz%20pharmaceuticals", "parexel%20international", "virologic", "aldeyra%20therapeutics","ribozyme%20pharmaceuticals", "somaxon%20pharmaceuticals", "algos%20pharmaceutical", "array%20biopharma", "replidyne", "intercept%20pharmaceuticals", , "orthovita", "depomed", "tracon%20pharmaceuticals", "omeros","aradigm", "revance%20therapeutics","cytokinetics","ostex%20international","maxim%20pharmaceuticals", "praecis%20pharmaceuticals","kalobios%20pharmaceuticals","catabasis%20pharmaceuticals", "flexion%20therapeutics","cotherix","coulter%20pharmaceutical", "acceleron%20pharma", "chemocentryx", "bruker%20axs", "map%20pharmaceuticals", "vbl%20therapeutics%20", "virus%20research%20institute", "neotherapeutics","complete%20genomics",  "capnia", "digene", "amphastar%20pharmaceuticals", "collaborative%20clinical%20research", "memory%20pharmaceuticals", "cn%20biosciences", "avigen", "ansan%20pharmaceuticals", "ruthigen", "juno%20therapeutics", "coherus%20biosciences","applied%20genetic%20technologies", "mannkind", "progenitor", "norland%20medical%20systems", "regulus%20therapeutics", "pronai%20therapeutics", "genencor%20international", "hyperion%20therapeutics", "decode%20genetics", "biomimetic%20therapeutics", "gtx", "cancervax", "trius%20therapeutics", "eagle%20pharmaceuticals", "targacept", "chiasma", "sage%20therapeutics", "ultragenyx%20pharmaceutical", "marinus%20pharmaceuticals", "biocept","acelrx%20pharmaceuticals", "keryx%20biopharmaceuticals", "orchid%20biosciences", "informax", "triangle%20pharmaceuticals", "sunesis%20pharmaceuticals", "pharmion", "kosan%20biosciences", "collateral%20therapeutics", "achillion%20pharmaceuticals", "aduro%20biotech", "biotransplant", "third%20wave%20technologies", "opgen", "corcept%20therapeutics", "cerulean%20pharma", "conatus%20pharmaceuticals", "hyseq%20pharmaceuticals", "intermune", "aquinox%20pharmaceuticals", "novacea", "loxo%20oncology", "bg%20medicine", "orexigen%20therapeutics", "supernus%20pharmaceuticals", "scynexis", "agile%20therapeutics", "angiotech%20pharmaceuticals", "dimensional%20pharmaceuticals", "conceptus", "otonomy", "kythera%20biopharmaceuticals","lexicon%20pharmaceuticals", "cleveland%20biolabs","cumberland%20pharmaceuticals", "horizon%20pharma", "egalet", "arena%20pharmaceuticals", "aclara%20biosciences", "diatide", "oravax", "pra%20health%20sciences", "orapharma", "ljl%20biosystems", "renovis", "united%20therapeutics", "genvec", "rosetta%20genomics%20", "epix%20medical", "new%20river%20pharmaceuticals", "pharmaceutical%20product%20development", "atara%20biotherapeutics", "rigel%20pharmaceuticals", "durect", "concert%20pharmaceuticals", "cara%20therapeutics", "genomica", "dendreon", "pacific%20biosciences%20of%20california", "tokai%20pharmaceuticals", "serologicals", "newlink%20genetics", "htg%20molecular%20diagnostics", "bluebird%20bio", "viking%20therapeutics", "kos%20pharmaceuticals", "collagenex%20pharmaceuticals", "dynavax%20technologies", "oculus%20innovative%20sciences", "dipexium%20pharmaceuticals", "megabios", "sibia%20neurosciences", "trubion%20pharmaceuticals", "paradigm%20genetics", "caliper%20life%20sciences", "theravance", "inotek%20pharmaceuticals", "icagen", "applied%20molecular%20evolution", "atossa%20genetics", "bioanalytical%20systems", "vital%20therapies", "exelixis", "ritter%20pharmaceuticals", "nitromed", "medichem%20life%20sciences", "ilex%20oncology", "achaogen", "combichem", "aryx%20therapeutics", "sequana%20therapeutics", "transcend%20therapeutics", "tercica", "eleven%20biotherapeutics", "fibrogen", "sepragen", "pharsight", "talecris%20biotherapeutics", "kite%20pharma", "blueprint%20medicines", "ambit%20biosciences", "zafgen", "evoke%20pharma", "threshold%20pharmaceuticals", "combinatorx", "sirtris%20pharmaceuticals", "cerus", "abgenix", "cb%20pharma%20acquisition", "allos%20therapeutics", "packard%20bioscience%20", "synaptic%20pharmaceutical", "cepheid", "roka%20bioscience", "caredx", "onyx%20pharmaceuticals", "optimer%20pharmaceuticals", "trimeris", "lantheus%20holdings", "sunpharm", "geltex%20pharmaceuticals", "sgx%20pharmaceuticals", "barrier%20therapeutics", "portola%20pharmaceuticals", "focal", "auxilium%20pharmaceuticals", "ventrus%20biosciences", "pacira%20pharmaceuticals", "seres%20therapeutics", "alexza%20pharmaceuticals", "tetralogic%20pharmaceuticals", "intersect%20ent", "phase%20forward", "intersect%20ent", "neothetics", "epizyme", "versicor", "colucid%20pharmaceuticals", "glycomimetics", "anacor%20pharmaceuticals", "andrx", "inovalon%20holdings", "v.i.%20technologies", "cadence%20pharmaceuticals", "sabratek", "molecular%20devices", "endocyte", "biomarin%20pharmaceutical", "pozen", "critical%20therapeutics", "viacell", "the%20medicines%20", "curagen", "ciphergen%20biosystems", "aastrom%20biosciences", "pharmacyclics", "biodel", "variagenics", "zosano%20pharma", "anadys%20pharmaceuticals", "seattle%20genetics", "pathogenesis", "alexion%20pharmaceuticals", "invitrogen", "omrix%20biopharmaceuticals", "globeimmune", "anthera%20pharmaceuticals", "liposcience", "medical%20science%20systems", "marshall%20edwards", "akers%20biosciences", "telik", "relypsa", "codexis", "ocular%20therapeutix", "vanda%20pharmaceuticals", "nanostring%20technologies", "metra%20biosystems", "antivirals", "uniqure%20n.v", "antigenics", "oxford%20immunotec%20global%20plc", "nivalis%20therapeutics", "inhibitex", "advancis%20pharmaceutical", "aerie%20pharmaceuticals", "integ", "medicinova", "receptos", "omthera%20pharmaceuticals", "tranzyme", "chimerix", "genmark%20diagnostics", "genetic%20vectors", "spectrx", "cidara%20therapeutics", "acadia%20pharmaceuticals", "senomyx", "t2%20biosystems", "urocor", "aveo%20pharmaceuticals", "large%20scale%20biology", "merrimack%20pharmaceuticals", "sonus%20pharmaceuticals", "myriad%20genetics", "alimera%20sciences", "idenix%20pharmaceuticals", "diacrin", "five%20prime%20therapeutics", "aegerion%20pharmaceuticals", "intrabiotics%20pharmaceuticals", "genaissance%20pharmaceuticals", "bioreliance", "minerva%20neurosciences", "karyopharm%20therapeutics", "santarus", "esperion%20therapeutics%20", "cv%20therapeutics", "akebia%20therapeutics", "bellerophon%20therapeutics", "rosetta%20inpharmatics", "progenics%20pharmaceuticals", "illumina", "eden%20bioscience", "fate%20therapeutics", "pharmacopeia", "dicerna%20pharmaceuticals", "regado%20biosciences", "esperion%20therapeutics", "sucampo%20pharmaceuticals", "oncomed%20pharmaceuticals", "tularik", "tetraphase%20pharmaceuticals", "proteon%20therapeutics", "signal%20genetics", "genomic%20solutions", "adma%20biologics", "inspire%20pharmaceuticals", "cubist%20pharmaceuticals", "nucryst%20pharmaceuticals", "aurora%20biosciences", "amyris", "radius%20health", "iomai", "arqule", "valera%20pharmaceuticals", "luminex", "corgentech", "adamas%20pharmaceuticals", "discovery%20partners%20international", "synta%20pharmaceuticals", "leukosite", "cardiovascular%20diagnostics", "insulet", "aratana%20therapeutics", "durata%20therapeutics", "zs%20pharma", "flex%20pharma", "ivery%20sciences%20international", "fuisz%20technologies%20", "cellular%20dynamics%20international", "contrafect", "bellicum%20pharmaceuticals", "stemline%20therapeutics", "corixa", "clovis%20oncology", "ophthotech", "adeza%20biomedical", "pdt", "zogenix", "macrogenics", "kempharm", "avalon%20pharmaceuticals", "nanosphere", "great%20basin", "xenon%20pharmaceuticals", "keravision", "cell%20therapeutics", "ironwood%20pharmaceuticals", "northwest%20biotherapeutics", "acorda%20therapeutics", "supergen", "genocea%20biosciences", "pain%20therapeutics", "natera", "xbiotech", "kindred%20biosciences", "sangamo%20biosciences", "tanox", "intercardia", "endovascular%20technologies", "biosite", "spark%20therapeutics", "targanta%20therapeutics", ,"visible%20genetics", "zymogenetics", "xcyte%20therapies", "calithera%20biosciences", "ribapharm", "ptc%20therapeutics", "catalyst%20pharmaceutical%20partners", "recro%20pharma", "heat%20biologics", "avalanche%20biotechnologies","agios%20pharmaceuticals", "cempra", "alnylam%20pharmaceuticals", "alder%20biopharmaceuticals",  "cempra", "trevena", "immtech%20pharmaceuticals","aviron", "symyx%20technologies"}

newLine="\n"
for key in keywords:
    
    #Query we need to send to proquest database
    url = "http://fedsearch.proquest.com/search/sru/abidateline?operation=searchRetrieve&version=1.2&maximumRecords=1000&query=dc.title="+"%22"+key+"%22"+"+and+(dc.source=%22PR%20Newswire%22+OR+dc.source=%22Business%20Wire%22+OR+dc.source=%22Knight%20Ridder%20Tribune%20Business%20News%22+OR+dc.source=%22McClatchy%20-%20Tribune%20Business%20News%22+OR+dc.source=%22News%20Bites%20US%20-%20NASDAQ%22+OR+dc.source=%22Benzinga%20Newswires%22+OR+dc.source=%22News%20Bites*%22)"
    fp = request.urlopen(url) 
    doc = minidom.parse(fp)
    
    #Get the number of articles present in XML data
    numOfRecords = doc.getElementsByTagName("zs:numberOfRecords")[0]
    indivrecords = doc.getElementsByTagName("zs:records")[0]
    
    records= indivrecords.getElementsByTagName("zs:record")
    directory = "/Nilam/MSBA_Degree/CISI/Press_release/Output/"+key
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    #Extract required data using this code
    for record in records:
        recordPos = record.getElementsByTagName("zs:recordPosition")[0].firstChild.data
        dirDetail= directory+"/Detail"
        dirFullText=directory+"/FullText"
        
        #Create directory if does not exist
        if not os.path.exists(dirDetail):
            os.makedirs(dirDetail)
        if not os.path.exists(dirFullText):
            os.makedirs(dirFullText)
        
        #Create Text files in which you want to write data
        fileDetail =  dirDetail+"/"+(key)+"_"+(recordPos)+"_detail.txt"
        fileFullText =  dirFullText+"/"+(key)+"_"+(recordPos)+"_FullText.txt"
        
        #Open files in write mode
        file1 = open(fileDetail, "w")
        file2 = open(fileFullText, "w")
        data = record.getElementsByTagName("datafield")
        
        for dataElement in data:
            #EXtract Title from data
            if dataElement.attributes["tag"].value == "245":
                subFields = dataElement.getElementsByTagName("subfield")
                for subField in subFields:
                    if subField.attributes["code"].value == "a":
                        title = (subField.firstChild.data).encode("utf-8","xmlcharrefreplace")
                        file1.write("Title :"+str(title)+newLine)
                        
            #EXtract publisher from data            
            if dataElement.attributes["tag"].value == "260":
                subFields = dataElement.getElementsByTagName("subfield")
                for subField in subFields:
                    if subField.attributes["code"].value == "b":
                        pub = (subField.firstChild.data).encode("utf-8","xmlcharrefreplace")
                        file1.write("Publisher :"+str(pub)+newLine)
                    if subField.attributes["code"].value == "c":
                        file1.write("Date :"+(subField.firstChild.data)+newLine)
                        
            ##EXtract abstract from data           
            if dataElement.attributes["tag"].value == "520":
                subFields = dataElement.getElementsByTagName("subfield")
                for subField in subFields:
                    if subField.attributes["code"].value == "a":
                        abstract = (subField.firstChild.data).encode("utf-8","xmlcharrefreplace")
                        file1.write("Abstract :"+str(abstract)+newLine)
                        
            #EXtract fulltext from data           
            if (dataElement.attributes["tag"].value == "856") & (dataElement.attributes["ind2"].value == "0"):
                subFields = dataElement.getElementsByTagName("subfield")
                for subField in subFields:
                    if subField.attributes["code"].value == "u":
                        opener = request.build_opener(HTTPCookieProcessor())
                        response = opener.open(subField.firstChild.data)
                        soup = BeautifulSoup(response)
                        if(soup.find("text")):
                            text = (soup.find("text").text).encode("utf-8","xmlcharrefreplace")
                            file2.write("FullText :"+str(text)+newLine)
                        break;
        file1.close() 
        file2.close()    
        
                    