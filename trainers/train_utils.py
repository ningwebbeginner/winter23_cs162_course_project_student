import csv
import glob
import json
import random
import logging
import os
from enum import Enum
from typing import List, Optional, Union

import tqdm
import numpy as np

import torch
from transformers import (
    WEIGHTS_NAME,
    AdamW,
    AutoConfig,
    AutoModelForMaskedLM,
    AutoTokenizer,
)

def evaluate_standard(preds, labels, scoring_method):

    # The accuracy, precision, recall and F1 scores to return
    acc, prec, recall, f1 = 0.0, 0.0, 0.0, 0.0

    ########################################################
    # TODO: Please finish the standard evaluation metrics.
    # You need to compute the accuracy, precision, recall
    # and F1 score for the predictions and gold labels.
    # Please also make your sci-kit learn scores are computed
    # using `scoring_method` for the `average` argument.
    acc = accuracy_score(labels, preds)


    prec, recall, f1, _ = precision_recall_fscore_support(labels, preds, average=scoring_method)
    # End of TODO
    ########################################################

    return acc, prec, recall, f1

def pairwise_accuracy(guids, preds, labels):

    acc = 0.0  # The accuracy to return.
    
    ########################################################
    # TODO: Please finish the pairwise accuracy computation.
    # Hint: Utilize the `guid` as the `guid` for each
    # statement coming from the same complementary
    # pair is identical. You can simply pair the these
    # predictions and labels w.r.t the `guid`. 
    pairs = {}
    for guid, pred, label in zip(guids, preds, labels):
        if guid not in pairs:
            pairs[guid] = ([], [])
        pairs[guid][0].append(pred)
        pairs[guid][1].append(label)


    correct_count = 0
    total_count = 0
    for pair in pairs.values():
        if len(pair[0]) == 2:
            total_count += 1
            if pair[0][0] == pair[1][0] and pair[0][1] == pair[1][1] or pair[0][0] != pair[1][0] and pair[0][1] != pair[1][1]:
                correct_count += 1

    acc = correct_count / total_count if total_count > 0 else 0.0
    # End of TODO
    ########################################################
     
    return acc

if __name__ == "__main__":

    # Unit-testing the pairwise accuracy function.
    guids = [0, 0, 1, 1, 2, 2, 3, 3]
    preds = np.asarray([0, 0, 1, 0, 0, 1, 1, 1])
    labels = np.asarray([1, 0, 1, 1, 0, 1, 1, 1])
    acc, prec, rec, f1 = evaluate_standard(preds, labels, "binary")
    pair_acc = pairwise_accuracy(guids, preds, labels)

    if acc == 0.75 and prec == 1.0 and round(rec,2) == 0.67 and f1 == 0.8:
        print("Your `evaluate_standard` function is correct!")
    else:
        raise NotImplementedError("Your `evaluate_standard` function is INCORRECT!")

    if pair_acc == 0.5:
        print("Your `pairwise_accuracy` function is correct!")
    else:
        raise NotImplementedError("Your `pairwise_accuracy` function is INCORRECT!")
