#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 08:47:00 2020

@author: alexshepherd
"""

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import re
import logging
import string

logging.basicConfig(level = logging.INFO, format = "%(levelname)s  %(asctime)s (%(funcName)s) : %(message)s") 


class TextAnalysis:
    """
    Text Analysis class which can perform exploratory analysis
    """
    
    def __init__(self):
        
        self.punctuation = list(string.punctuation)
        self.punctuation.append("\xa0")
        self.punctuation.append("\n")
        self.punctuation.extend(stopwords.words('english'))
    
    def clean_text(self, txt, doc2vec = False, s_words = True):
        """
        Cleans text by the following:
            - Removes stopwords and punctuation
            - Make text lower case
            - Tokenise words
               
        :param txt: (String) raw text
        :param doc2vec: (Boolean) if doc2vec is true, then we will leave full stops.
        :param s_words: (Boolean) include removing stopwords?
        
        :return c_text: (String) cleaned text
        """
        
        c_txt = txt.lower()

        # Step 2 remove punctuation
        for punc in self.punctuation:
            try:
                #code.interact(local = locals(), banner = "@, # removal")
                if punc in c_txt:
                    logging.info("Removing {} from text...".format(punc))
                    if punc in stopwords.words('english'):
                        if s_words:
                            c_txt = re.sub(r" {0} ".format(punc), " ", c_txt)
                        else:
                            continue
                    elif punc == "!":
                        if doc2vec:
                            continue
                    elif punc == "\n":
                        c_txt = re.sub(r"{0}".format(punc), " ", c_txt)
                        
                    else:
                        try:
                            if punc != ".":
                                c_txt = re.sub(r"{0}".format(punc), "", c_txt)
                            elif not doc2vec:
                                c_txt = re.sub(r"\{0}".format(punc), "", c_txt)
                        except:
                            c_txt = re.sub(r"\{0}".format(punc), "", c_txt)
                else:
                    pass
            except Exception as e:
                logging.error(e)
                pass
                

        # Step 3 tokenize
        if not doc2vec:
            c_txt = word_tokenize(c_txt)
        else:
            c_txt = sent_tokenize(c_txt)
            
        return c_txt
    
    def word_count(self, txt):
        """
        Find number of words in text.
        
        :param txt: (String) text
        
        :return count: (Integer) word count
        """
        
        return len(word_tokenize(txt))
        
    
s = TextAnalysis()