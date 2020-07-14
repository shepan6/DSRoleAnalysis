#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 17:28:51 2020

@author: alexshepherd
"""

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
import re
from nltk.tokenize import sent_tokenize
from tqdm import tqdm 
import logging



# Read data

data = pd.read_csv("sentence_labels_v2.csv", index_col = 0)


# Data preprocessing

class DataPreprocess:
    
    """
    Preprocessing text data for encoder-decoder model. 
    """
    
    def __init__(self, filename):
        
        self.data = pd.read_csv(filename, index_col = 0)
    
    def sentencisize(self, text):
        """
        

        Parameters
        ----------
        text : TYPE
            DESCRIPTION.

        Returns
        -------
        all_sentences : TYPE
            DESCRIPTION.

        """
        sentences = sent_tokenize(txt)
        
        all_sentences = []
        
        for s in sentences:
            try:
                all_sentences.extend(s.split("\n"))
            except:
                all_sentences.append(s)
        
        return all_sentences
    
    def preprocess_sentence(self, sentence):
        
        sentence = sentence.lower()
        sentence = re.sub(" +", " ", sentence)
        sentence = re.sub("'", '', sentence)
        sentence = re.sub(r"([?.!,¿])", r" \1 ", sentence)
        sentence =  '<start>' + sentence + '<end>'
        
        return sentence
    
    def preprocess_data(self):
        """
        Main preprocessing method which converts data into 

        Returns
        -------
        processed_data : TYPE
            DESCRIPTION.

        """
        
        processed_data = self.sentencisize()
        processed_data = [self.preprocess_sentence(s) for s in processed_data]

        
        
        return zip(processed_data, self.data.loc[:, "none":].values)

# Model architecture

# Sequential decoder (with attention) to neural network decoder