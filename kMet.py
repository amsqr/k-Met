#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os,sys,glob
import re
from decimal import *
import re, collections
from phonetic_algorithms import PhoneticAlgorithms
import difflib
#from zlib import compress

 
# kMet Phonetic Clustering Algorithm
# Copyright (C) 2012 Alejandro Mosquera <amsqr2@gmail.com>
 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


print "kMet 0.1"
print "Support: amsqr2@gmail.com\n\n"

class kMet(object):

	""" kMet Phonetic Clustering Algorithm """
	
	def __init__(self):
                self.groups={}
                self.phon_dict={}

        
        def save_phon_dict(self,words,dict_name):
                f = open(words,'w')
                for k in dict_name:
                        f.write(str(k) + '|||' + str(dict_name[k]) + '\n')
                f.close()

                
                
        def text2phon(self,word,pword):
                
                phon = PhoneticAlgorithms().double_metaphone(pword)
                phon = str(phon).split(',')
                phon1= str(phon[0])[1:]
                phon2= str(phon[1])[1:-1]
                #print phon1,phon2
                if phon1 in self.phon_dict:
                        lista=self.phon_dict[phon1]
                        lista=lista.split('###')
                        found=0
                        if word not in lista:
                                self.phon_dict[phon1]=self.phon_dict[phon1] + word +'###'                        
                else:
                        
                        self.phon_dict[phon1]=word+'###'

                if phon2 in self.phon_dict:
                        lista=self.phon_dict[phon2]
                        lista=lista.split('###')
                        found=0
                        if word not in lista:
                                self.phon_dict[phon2]=self.phon_dict[phon2] + word +'###'
                else:
                        if phon2!='None':                        
                                self.phon_dict[phon2]=word+'###'
                                
                                
                        

        ##def zip_sim(stringA, stringB):
        ##	a = len(compress(stringA))
        ##	b = len(compress(stringB))
        ##	c = len(compress(stringA + stringB))
        ##	return 1.0 -(0.0 +a +b -c )/max (a ,b )


        def replace_numbers(self,foo):
                vocals=['a','e','i','o','u']
                if (foo.isdigit()==False):
                        foo2=foo
                        foo=foo.replace('0','o')
                        foo=foo.replace('3','e')
                        foo=foo.replace('5','s')
                        foo=foo.replace('6','g')
                        foo=foo.replace('7','t')
                        foo=foo.replace('9','g')
                        foo=foo.replace('8','eight')
                        foo=foo.replace('4','for')
                        foo=foo.replace('2','to')
                        foo=foo.replace('1','one')
                return foo



        def cluster(self,met, words):
                
            clustered = False
            for key in self.groups:
                # Check for similarity
                seq=difflib.SequenceMatcher(a=key,b=met)
                dis=seq.ratio()
                if dis>0.80:
                    if words!='' and words not in self.groups[key]:
                            self.groups[key].append(words)
                    clustered = True
                    break
            
            if not clustered:
                    if not self.groups.has_key(met):
                        self.groups[met] = []
                    
                    self.groups[met].append(words)


        def process_text(self,text):
            punt_list=['.',',','!','?',';',':']
            s=list(text)
            texto=''.join([ o for o in s if not o in  punt_list ]).split()

            for word in texto:
                if word in punt_list or word.find('http:')>-1 or word.find('www.')>-1:
                    pass
                else:
                    pattern = re.compile('[\W_]+')
                    word=pattern.sub('',word)
                    if word!='':
                        self.text2phon(word,self.replace_numbers(word))
            
            for met in self.phon_dict:
                    #print met
                    lista = self.phon_dict[met].split('###')
                    for l in lista:
                        self.cluster(met,l)
            
        

def main():
        kcluster=kMet()
        kcluster.process_text('praises prices precious, process, presses, precise, purses, growing, grunge, grunge, carrying, crying, caring, carnage, crank, grinch, chronic, crank, to, the, do, they, day, needed, nudity, noted, knitted, knotted, that, thought, they, those, this, thought, without')
        #print kcluster.groups
        for g in kcluster.groups:
                print str(g).replace("'",'') + '###' + str(kcluster.groups[g]).replace("['",'').replace("']",'').replace("', '",'|||')
    
                


if __name__ == '__main__':

	main()
	
