#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 09:56:02 2020

@author: alexshepherd
"""

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import re
import string
import numpy as np 
import pandas as pd

class CleanUp:
    
    def __init__(self):
        self.punctuation = list(string.punctuation)
        self.punctuation.extend(["\xa0", "\n"])
        self.punctuation.extend(stopwords.words('english'))
        

    def clean_text(self, txt, s_tokenize = False):
            """
            Helper method to clean text of punctuation, contractions and adds sentence beginning markers at beginning of sentences.
            Also removes hashtags and mentions.
    
            :param txt: String raw text
    
            :return c_txt: Nested list of sentences containing list of tokens which form the cleaned the sentences.
            """
    
            #print("Cleaning text...")
            # Step 1 tokenize by sentence
            c_txt = txt.lower()
            c_txt = sent_tokenize(c_txt)
            if not s_tokenize:
                c_txt = [" ".join(c_txt)]
            #print(len(c_txt))
            
            clean = []
            
            for sent in c_txt:
    
                # Step 2 remove punctuation
                for punc in self.punctuation:
                    try:
                        #code.interact(local = locals(), banner = "@, # removal")
                        if punc == "@":
                            sent = re.sub(r"{0}\w+".format(punc), " ", sent)
                        if punc in sent:
                            if punc in stopwords.words('english'):
                                sent = re.sub(r" {0} ".format(punc), " ", sent)
                            else:
                                try:
                                    if punc != ".":
                                        sent = re.sub(r"{0}".format(punc), " ", sent)
                                    else:
                                        sent = re.sub(r"\{0}".format(punc), " ", sent)
                                except:
                                    sent = re.sub(r"\{0}".format(punc), "", sent)
                        else:
                            pass
                    except Exception as e:
                        pass
    
                # Remove non-ASCII characters
                if sent.isascii():
                    pass
                else:
                    txt = sent
                    sent = ""
                    for char in txt:
                        if char.isascii():
                            sent = sent + char
                        else:
                            pass
    
                # Replace digits with DIGIT flag
                sent = re.sub(r"\d+", " DIGIT ", sent)
                sent = re.sub(r"\s{2,}", " ", sent)
                
                clean.append(sent)
            
            if not s_tokenize:
                return clean[0]
            else:
                return clean
    
            # Step 3 tokenize
            #c_txt = word_tokenize(c_txt)
    
    def length(self, txt):
        c_txt = word_tokenize(txt)
        return len(c_txt)
    
    
class JobAnalysis:
    
    def __init__(self, skills_df):
        
        if skills_df is None:
            self.vocab = pd.read_csv("word_count_all.csv")
        else:
            self.vocab = skills_df
        # business and technical words which appeared in job listing
        self.business_words = []
        self.technical_words = []
    
            
    def skills_match(self, txt, output_skills = False):
        """
        Returns proportion of skills match.

        :param entry: (Pandas) entry in dataframe
        
        :return skills_match: (Float) ratio between skills which I possess on
        job spec vs all skills present on job spec.
        """


        skills_vocab = self.vocab[~self.vocab["Skills"].isna()]
        
        txt = list(set(word_tokenize(txt)))

        skills = pd.DataFrame(txt).reset_index()

        # all skills displayed in text
        try:
            all_skills = skills[skills[0].isin(list(skills_vocab["word"].values))]
        except:
            all_skills = skills[skills[0].isin(list(skills_vocab["Skills"].values))]
        
        total_skills = all_skills.shape[0]
        
        # skills vocab which includes only those which user states that they have
        skills_vocab = skills_vocab[~skills_vocab["Skills I have"].isna()]
        
        try:
            matched_skills = all_skills[
                all_skills[0].isin(list(skills_vocab["word"].values))]
        except:
            matched_skills = all_skills[
                all_skills[0].isin(list(skills_vocab["Skills"].values))]
        
        skills = matched_skills.shape[0]
        
        
        try:
            skills_match = skills / total_skills
        except:
            skills_match = 0
        
        if output_skills:
            unmatched_skills = set(all_skills[0]) - set(matched_skills[0])
            return [skills_match, list(matched_skills.values[:,1]), list(unmatched_skills)]
        else:
            return skills_match
