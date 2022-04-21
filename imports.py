from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from nltk import word_tokenize
import nltk
import re
from pdfminer.high_level import extract_text
import docx2txt
import spacy
nlp = spacy.load('en_core_web_trf')

import streamlit as st
import pandas as pd

