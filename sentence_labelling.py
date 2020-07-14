#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 13:21:58 2020

@author: alexshepherd
"""

import pandas as pd
import numpy as np
import txt_analysis as TA
from tqdm import tqdm
import os
from nltk.tokenize import sent_tokenize


# TODO: create functions which check for agreement in annotations and 
# assigns labels to the sentences and allow for labelling bt relation sentences with 3-class vagueness of relation.

class Labelling:
    
    def __init__(self):
        self.labels = {"bb": 0, "bt": 1, "tt": 2}
        t = TA.TextAnalysis()
        
        try:
            self.df = pd.read_csv("sentence_labels.csv", index_col = 0)
            self.df.columns = ["index", "Text", "bb", "bt", "tt"]
        except:
            self.df = create_samples()
            
        assert self.df is not None, "Dataframe of samples does not exist."


    def create_samples(self):
        """
        Creates dataframe with sample sentences. 
    
        Returns
        -------
        samples: Pandas DataFrame
    
        """
        
        assert "sentence_labels.csv" not in os.listdir()
        
        txt = ""
        
        print("Creating samples ...")
        
        print("Merging .txt files ...")
        
        for f in tqdm(os.listdir()):
            if f.endswith(".txt"):
                # merge to make one large string.
                txt = txt + open(f).read().lower()
                
        samples = sent_tokenize(txt)
        
        print("Total number of sentences : {}".format(len(samples)))
        
        num_samples = None
        
        while num_samples is None or int(num_samples) > len(samples):
            num_samples = input("How many sentences do you want to sample? >>>")
        
        # randomly sample sentences
        sample_idxs = np.random.choice(len(samples), int(num_samples))
    
        samples = np.array(samples)[sample_idxs]
        
        samples = pd.DataFrame(samples, index = sample_idxs)
        samples = samples.reset_index()
        
        for col_name in labels.keys():
            samples.loc[:, col_name] = 0
        
        print("Saving samples to sentence_labels.csv")
        
        samples.to_csv("sentence_labels.csv")
        
        return samples
    
    def label_samples(self, df):
        """
        Labelling samples in dataframe.
    
        Parameters
        ----------
        df : Pandas DataFrame
            Samples to be labelled
    
        Returns
        -------
        None.
    
        """
        
        print("""To quit, enter 'q'. If sample doesn't belong to any defined
              category, then enter 'n'.""")
        
        # find indices where samples are unlabelled 
        unlabelled_idxs = list(self.df[
            self.df.iloc[
                :,-len(self.labels)-1:
                    ].sum(axis = 1) == 0
                ].index)
        #unlabelled_idxs = list(self.df.iloc[400:].index)
        
        for i in tqdm(unlabelled_idxs):
            print("-" * 20)
            print("{}".format(df.iloc[i,1]))
            
            label = None
            
            while label is not None or label not in list(self.labels.keys()) or label != "n":
                label = input(">>> ")
                
                if label in list(labels.keys()):
                    self.df.loc[i, label] += 1
                    break
                elif label == "q":
                    break
                elif label == "n":
                    print("not a defined category, next entry")
                    break
                else:
                    label = None
            
            self.df.to_csv("sentence_labels.csv")
            
            if label == "q":
                break
                    
            
        print("Completed / Exited ...")
    

    def agreement(self, annotators):
       """
       Checks for agreement and flags entries which show no agreement and
       asks for deciding vote.
       
    
       Parameters
       ----------
       annotators : Integer
           Number of annotators involved in labelling.
    
       Returns
       -------
       new_labels : Pandas DataFrame
           Dataset with new agreed upon labels. 
    
       """
       
       
       labelled_df = self.df[
           self.df.iloc[
               :,-len(self.labels)-1:
                   ].sum(axis = 1) != 0
               ]
           
       new_labels = None
       base_labs = np.array(list(self.labels.keys()))
       
       to_dispute = None
       
       # Go through each label and select those where entry == annotators
       
       for l in base_labs:
           agreed = self.df[self.df[l] == annotators]
           not_agreed = self.df[
               (self.df[l] < annotators) & (self.df[l] > 0)
               ]
           
           try:
               new_labels = pd.concat([new_labels, agreed])
               to_dispute = pd.concat([to_dispute, not_agreed])
               to_dispute = to_dispute.drop_duplicates(0)
           except:
               new_labels = agreed
               to_dispute = not_agreed
               
       agreed_rows = new_labels.shape[0]
       
       
       new_labels.loc[:, "bb":] /= annotators
       #new_labels.to_csv("agreed_labels.csv")
       
       for i in tqdm(to_dispute.iterrows()):
           print("-" * 20)
           print("{}".format(i[1]["Text"]))
           j = i[1]["bb":].values
           print("Labels : {}".format(base_labs[np.where(j == 1)]))
           
           label = None
           
           while label is not None or label not in list(self.labels.keys()) or label != "n":
               label = input(">>> ")
               
               if label in list(self.labels.keys()):
                   agreed_label = np.zeros(3)
                   agreed_label[np.where(base_labs == label)] += 1
                   to_dispute.loc[i[0], "bb":] = agreed_label
                   break
               elif label == "q":
                   break
               elif label == "n":
                   print("not a defined category, next entry")
                   to_dispute.loc[i[0], "bb":] = np.zeros(3)
                   break
               else:
                   label = None  
                   
               
       dispute_rows = dispute_rows[
           dispute_rows.iloc[
               :,-len(self.labels)-1:
                   ].sum(axis = 1) != 0
               ].shape[0]
       new_labels = pd.concat([new_labels, to_dispute])
       new_labels = new_labels[
           new_labels.iloc[
               :,-len(self.labels)-1:
                   ].sum(axis = 1) != 0
               ]
       
       new_labels.to_csv("sentence_labels_v2.csv")
       
       assert new_labels.shape[0] == agreed_rows + dispute_rows, """
       New labels dataframe is not complete expected {} rows, but got 
       {} rows.""".format(agreed_rows + dispute_rows, new_labels.shape[0])
       
       assert np.sum(new_labels.loc[:,"bb":]) == new_labels.shape[0], """
       Some / all entries do not have one hot encoding.
       """
 

l = Labelling()
l.agreement(2)