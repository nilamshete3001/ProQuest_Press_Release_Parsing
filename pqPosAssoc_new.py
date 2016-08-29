'''
Created on Dec 18, 2015
@author: Nilam
'''
import nltk
from nltk.util import ngrams
import nltk.tokenize.punkt
from nltk.tokenize import sent_tokenize
from collections import Counter
from itertools import tee, islice
import pandas as pd
import re
import os

keywords = {'adolor'}
#keywords = {'aastrom%20biosciences', 'abgenix' , 'acadia%20pharmaceuticals' , 'acceleron%20pharma' , 'acelrx%20pharmaceuticals' , 'achaogen' , 'aclara%20biosciences' , 'acorda%20therapeutics' , 'adamas%20pharmaceuticals' , 'adeza%20biomedical' , 'adma%20biologics' , 'adolor' , 'aduro%20biotech' , 'advancis%20pharmaceutical' , 'affymetrix' , 'agile%20therapeutics' , 'agios%20pharmaceuticals' , 'akebia%20therapeutics' , 'akers%20biosciences' , 'alder%20biopharmaceuticals' , 'aldeyra%20therapeutics' , 'alexza%20pharmaceuticals' , 'algos%20pharmaceutical' , 'alimera%20sciences' , 'alnylam%20pharmaceuticals' , 'ambit%20biosciences' , 'amicus%20therapeutics' , 'amphastar%20pharmaceuticals' , 'amyris' , 'anacor%20pharmaceuticals' , 'anadys%20pharmaceuticals' , 'angiotech%20pharmaceuticals' , 'ansan%20pharmaceuticals' , 'anthera%20pharmaceuticals' , 'antivirals' , 'applied%20genetic%20technologies' , 'applied%20imaging' , 'applied%20molecular%20evolution' , 'aquinox%20pharmaceuticals' , 'aradigm' , 'aratana%20therapeutics' , 'ardelyx' , 'arena%20pharmaceuticals' , 'argos%20therapeutics' , 'arqule' , 'array%20biopharma' , 'aryx%20therapeutics' , 'atara%20biotherapeutics' , 'atossa%20genetics' , 'atyr%20pharma' , 'aurora%20biosciences' , 'auspex%20pharmaceuticals' , 'auxilium%20pharmaceuticals' , 'avalon%20pharmaceuticals' , 'avigen' , 'barrier%20therapeutics' , 'bellerophon%20therapeutics' , 'bellicum%20pharmaceuticals' , 'bg%20medicine' , 'bioanalytical%20systems' , 'biocept' , 'biomarin%20pharmaceutical' , 'biopure' , 'bioreliance' , 'biosite' , 'biotransplant' , 'bluebird%20bio' , 'blueprint%20medicines' , 'bruker%20axs' , 'cadence%20pharmaceuticals' , 'caliper%20life%20sciences' , 'cancer%20genetics' , 'cancervax' , 'capnia' , 'cara%20therapeutics' , 'carbylan%20therapeutics' , 'caredx' , 'catabasis%20pharmaceuticals' , 'catalyst%20pharmaceutical%20partners' , 'cb%20pharma%20acquisition' , 'cellular%20dynamics%20international' , 'cempra' , 'cepheid' , 'cerulean%20pharma' , 'cerus' , 'chemocentryx' , 'chimerix' , 'chirex' , 'cidara%20therapeutics' , 'cn%20biosciences' , 'codexis' , 'coherus%20biosciences' , 'coley%20pharmaceutical%20group' , 'collaborative%20clinical%20research' , 'collagenex%20pharmaceuticals' , 'collateral%20therapeutics' , 'collegium%20pharmaceutical' , 'colucid%20pharmaceuticals' , 'combichem' , 'combinatorx' , 'complete%20genomics' , 'conatus%20pharmaceuticals' , 'concert%20pharmaceuticals' , 'connetics' , 'corcept%20therapeutics' , 'corgentech' , 'corium%20international' , 'corixa' , 'cotherix' , 'critical%20therapeutics' , 'cubist%20pharmaceuticals' , 'cumberland%20pharmaceuticals' , 'curagen' , 'cytokinetics' , 'decode%20genetics' , 'dendreon' , 'depomed' , 'dermira' , 'diacrin' , 'dicerna%20pharmaceuticals' , 'dipexium%20pharmaceuticals' , 'dov%20pharmaceutical' , 'durata%20therapeutics' , 'dyax' , 'dynavax%20technologies' , 'eagle%20pharmaceuticals' , 'eden%20bioscience' , 'egalet' , 'eleven%20biotherapeutics' , 'endocyte' , 'endovascular%20technologies' , 'epix%20medical' , 'epizyme' , 'esperion%20therapeutics' , 'exact%20sciences' , 'exelixis' , 'fate%20therapeutics' , 'fibrogen' , 'five%20prime%20therapeutics' , 'flex%20pharma' , 'flexion%20therapeutics' , 'fluidigm' , 'focal' , 'foundation%20medicine' , 'fuisz%20technologies%20' , 'geltex%20pharmaceuticals' , 'genaissance%20pharmaceuticals' , 'genetic%20vectors' , 'genocea%20biosciences' , 'genomic%20health' , 'genomic%20solutions' , 'genomica' , 'genoptix' , 'genvec' , 'gtx' , 'heat%20biologics' , 'histogenics' , 'horizon%20pharma' , 'houghten%20pharmaceuticals' , 'hyperion%20therapeutics' , 'hyseq%20pharmaceuticals' , 'idenix%20pharmaceuticals' , 'ilex%20oncology' , 'illumina' , 'immune%20design' , 'inhibitex' , 'inotek%20pharmaceuticals' , 'inovalon%20holdings' , 'insulet' , 'intercardia' , 'intercept%20pharmaceuticals' , 'intermune' , 'intersect%20ent' , 'intrabiotics%20pharmaceuticals' , 'invitrogen' , 'iomai' , 'ironwood%20pharmaceuticals' , 'jazz%20pharmaceuticals' , 'juno%20therapeutics' , 'kalobios%20pharmaceuticals' , 'karyopharm%20therapeutics' , 'keravision' , 'keryx%20biopharmaceuticals' , 'kindred%20biosciences' , 'kite%20pharma' , 'kos%20pharmaceuticals' , 'kosan%20biosciences' , 'kythera%20biopharmaceuticals' , 'lantheus%20holdings' , 'loxo%20oncology' , 'lumera' , 'luminex' , 'macrogenics' , 'map%20pharmaceuticals' , 'marinus%20pharmaceuticals' , 'marshall%20edwards' , 'maxygen' , 'medical%20science%20systems' , 'medichem%20life%20sciences' , 'medicinova' , 'megabios' , 'memory%20pharmaceuticals' , 'merrimack%20pharmaceuticals' , 'metabasis%20therapeutics' , 'metra%20biosystems' , 'microcide%20pharmaceuticals' , 'minerva%20neurosciences' , 'molecular%20devices' , 'momenta%20pharmaceuticals' , 'myogen' , 'myriad%20genetics' , 'nanosphere' , 'nanostring%20technologies' , 'natera' , 'neotherapeutics' , 'nephrogenex' , 'neurocrine%20biosciences' , 'new%20river%20pharmaceuticals' , 'newlink%20genetics' , 'northwest%20biotherapeutics' , 'novacea' , 'nucryst%20pharmaceuticals' , 'oculus%20innovative%20sciences' , 'omeros' , 'omthera%20pharmaceuticals' , 'onyx%20pharmaceuticals' , 'opgen' , 'ophthotech' , 'optimer%20pharmaceuticals' , 'oravax' , 'orchid%20biosciences' , 'orexigen%20therapeutics' , 'ostex%20international' , 'oxford%20immunotec%20global%20plc' , 'pacific%20biosciences%20of%20california' , 'pacira%20pharmaceuticals' , 'pain%20therapeutics' , 'parexel%20international' , 'pdt' , 'pharmaceutical%20product%20development' , 'pharmacopeia' , 'pharmacyclics' , 'pharmasset' , 'pharmion' , 'pharsight' , 'phase%20forward' , 'portola%20pharmaceuticals' , 'pozen' , 'praecis%20pharmaceuticals' , 'pronai%20therapeutics' , 'proteon%20therapeutics' , 'ptc%20therapeutics' , 'quotient%20' , 'radius%20health' , 'receptos' , 'regado%20biosciences' , 'regulus%20therapeutics' , 'relypsa' , 'renovis' , 'replidyne' , 'revance%20therapeutics' , 'ribapharm' , 'rosetta%20genomics%20' , 'rosetta%20inpharmatics' , 'ruthigen' , 'sabratek' , 'sage%20therapeutics' , 'sagent%20pharmaceuticals' , 'sangamo%20biosciences' , 'sano' , 'scynexis' , 'seattle%20genetics' , 'senomyx' , 'sepragen' , 'sequana%20therapeutics' , 'sequenom' , 'seres%20therapeutics' , 'serologicals' , 'sgx%20pharmaceuticals' , 'sibia%20neurosciences' , 'sirtris%20pharmaceuticals' , 'somaxon%20pharmaceuticals' , 'sonus%20pharmaceuticals' , 'spark%20therapeutics' , 'spectrx' , 'spiros%20development%20ii' , 'supergen' , 'supernus%20pharmaceuticals' , 'symyx%20technologies' , 'synta%20pharmaceuticals' , 't2%20biosystems' , 'talecris%20biotherapeutics' , 'tanox' , 'targacept' , 'targanta%20therapeutics' , 'telik' , 'tercica' , 'tesaro' , 'tetraphase%20pharmaceuticals' , 'the%20medicines%20' , 'theravance' , 'third%20wave%20technologies' , 'threshold%20pharmaceuticals' , 'tokai%20pharmaceuticals' , 'tracon%20pharmaceuticals' , 'transcend%20therapeutics' , 'transgenomic' , 'transkaryotic%20therapies' , 'tranzyme' , 'trevena' , 'trimeris' , 'trubion%20pharmaceuticals' , 'tularik' , 'ultragenyx%20pharmaceutical' , 'united%20therapeutics' , 'urocor' , 'v.i.%20technologies' , 'valera%20pharmaceuticals' , 'vanda%20pharmaceuticals' , 'variagenics' , 'vbl%20therapeutics%20' , 'ventrus%20biosciences' , 'veracyte' , 'versicor' , 'viking%20therapeutics' , 'virologic' , 'virus%20research%20institute' , 'visible%20genetics' , 'vital%20therapies' , 'vysis' , 'xbiotech' , 'xcyte%20therapies' , 'xencor' , 'xenon%20pharmaceuticals' , 'xtl%20biopharmaceuticals%20' , 'zafgen' , 'zogenix' , 'zosano%20pharma' , 'zs%20pharma' , 'zymogenetics'}
newLine="\n"

#Positive and Negative words we want to search 
phrases = {"succeed", "successful", "favorable", "significant", "positive"}
#phrases = {"failed", "failure", "unfavorable", "negative", "halted", "penalized"}
neg_phrase = {"not significant", "not successful", "never succeed", "not favorable", "not positive"}

#Function for ngram creation
def ngrams(lst, n):
    tokenlist = lst
    while True:
        a, b = tee(tokenlist)
        l = tuple(islice(a, n))
        if len(l) == n:
            yield l
            next(b)
            tokenlist = b
        else:
            break
        
for key in keywords:
    corpus_root="F:/Nilam/MSBA_Degree/CISI/Press_release/Output/"+key+"/FullText/"
    date_root="F:/Nilam/MSBA_Degree/CISI/Press_release/Output/"+key+"/Detail/"
    files_in_dir = os.listdir(corpus_root)
    details = os.listdir(date_root)
    
    ls = list()
    lsDate = list()    
    
    #Extract all dates 
    for file in details:
        with open(date_root + file) as f:
            data = f.read()
            start=data.find("Date :") + 6;
            end = data.find('\n',start)
            lsDate.append((data[start:end]))
    
    count = 0;
    for file in files_in_dir:
        with open(corpus_root + file) as f:
            data = f.read()
            
            #Clean Data
            data = data.replace('FullText :b','')
            data = data.replace('\\n','');
            data = data.replace('-', ' ');
            data = re.sub('[,$:;\\\]*', '', data)
            data = re.sub('[\s]+', ' ',data)
            
            # Convert data to lower case 
            data = data.lower();
            
            #Group similar words together
            data = data.replace("phase 1/2", "phase_1 and phase_2");
            data = data.replace("phase 2/3", "phase_2 and phase_3");
            data = data.replace("phase i/ii", "phase_1 and phase_2");
            data = data.replace("phase ii/iii", "phase_2 and phase_3");
            data = data.replace("phase 1 and 2", "phase_1 and phase_2");
            data = data.replace("phase 2 and 3", "phase_2 and phase_3");
            data = data.replace("phase 1a", "phase_1");
            data = data.replace("phase 1b", "phase_1");
            data = data.replace("phase1a", "phase_1");
            data = data.replace("phase1b", "phase_1");
            data = data.replace("phase 2a", "phase_2");
            data = data.replace("phase 2b", "phase_2");
            data = data.replace("phase2a", "phase_2");
            data = data.replace("phase2b", "phase_2");
            data = data.replace("phase 3a", "phase_3");
            data = data.replace("phase 3b", "phase_3");
            data = data.replace("phase3a", "phase_3");
            data = data.replace("phase3b", "phase_3");
            data = data.replace("phase iii", "phase_3");
            data = data.replace("phase ii", "phase_2");
            data = data.replace("phase i", "phase_1");
            data = data.replace("phase 1", "phase_1");
            data = data.replace("phase1", "phase_1");             
            data = data.replace("phase 2", "phase_2");
            data = data.replace("phase2", "phase_2");            
            data = data.replace("phase 3", "phase_3");            
            data = data.replace("phase3", "phase_3");   
            data = data.replace("biologic license application", "bla");
            data = data.replace("new drug application", "nda");
            data = data.replace("results", "result")
            tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()
            sentence = sent_tokenize(data)
            
            phase_tokens = []
            phases = ['phase_2','phase_3'];
            
            for phase in phases:
                word = phase;
                #Identify sentences which contains word phase_2
                for part in sentence:                
                    if word in part:
                        phase_tokens.append(part); 
                
                #Count number of positive words present in above identified sentences 
                tokens_sub = []        
                if len(phase_tokens) > 0:
                    sub = []
                    for part1 in phase_tokens:
                        text2 = ' '.join([word1 for word1 in part1.split() if word1 in phrases])
                        tokens = nltk.word_tokenize(text2);   
                        tokens_sub += tokens 
                
                #Check if above identified words are preceded by negative word 
                print(phase_tokens)
                negCount = [];          
                myset = set(tokens_sub)
                posWords = list(myset)
                
                if len(phase_tokens) > 0:
                    sub = []
                    for pos in posWords:
                        for part1 in phase_tokens:
                            tokens = nltk.word_tokenize(part1)
                            bigrams = ngrams(tokens,2)
                            search_word = nltk.word_tokenize("not " + pos)
                            search = list(ngrams(search_word, 2))
                            search_word2 = nltk.word_tokenize("never " +pos)
                            search2 = list(ngrams(search_word2, 2))
                            search_word3 = nltk.word_tokenize("no " +pos)
                            search3 = list(ngrams(search_word3, 2))
                                                
                            if ( (set((search)).issubset(set(list(bigrams))))or (set((search2)).issubset(set(list(bigrams)))) or (set((search3)).issubset(set(list(bigrams))))):
                                negCount += nltk.word_tokenize(pos)
                            print("negativee", negCount)   
                    ls.append((Counter(tokens_sub) - Counter(negCount)))    
                else:
                    tokens = []
                    ls.append(Counter(tokens))                               
        break;
    
    df=pd.DataFrame(ls, index=[files_in_dir, lsDate]);
    header = df.dtypes.index;
    df1=pd.DataFrame();
    
    for i in range(len(header)):
        data = pd.DataFrame(df[df[header[i]] > 0])
        df1 = df1.append(data);
    
    if(len(df1.index) > 0):
        df1.to_csv('F:/Nilam/MSBA_Degree/CISI/Press_release/Level3_phase2_pos/'+key+'.csv')        