# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 17:23:58 2016

@author: megan squire
"""
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

LANGUAGE = "english"
SENTENCES_COUNT = 4

parser = PlaintextParser.from_file("sampleText.txt", Tokenizer(LANGUAGE))
stemmer = Stemmer(LANGUAGE)

print("====== Luhn ======")
summarizerLuhn = LuhnSummarizer(stemmer)
summarizerLuhn.stop_words = get_stop_words(LANGUAGE)
for sentenceLuhn in summarizerLuhn(parser.document, SENTENCES_COUNT):
    print(sentenceLuhn)

print("====== TextRank ======")
summarizerTR = TextRankSummarizer(stemmer)
summarizerTR.stop_words = get_stop_words(LANGUAGE)
for sentenceTR in summarizerTR(parser.document, SENTENCES_COUNT):
    print(sentenceTR)

print("====== LSA ======")
summarizerLSA = LsaSummarizer(stemmer)
summarizerLSA.stop_words = get_stop_words(LANGUAGE)
for sentenceLSA in summarizerLSA(parser.document, SENTENCES_COUNT):
    print(sentenceLSA)

print("====== Edmonson ======")
summarizerEd = EdmundsonSummarizer(stemmer)
summarizerEd.bonus_words = ('foo')
summarizerEd.stigma_words = ('foo')
summarizerEd.null_words = ('foo')
for sentenceEd in summarizerEd(parser.document, SENTENCES_COUNT):
    print(sentenceEd)
