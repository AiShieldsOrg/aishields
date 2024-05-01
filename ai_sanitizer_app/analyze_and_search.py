#=== THIS CODE REQUIRES NODE.JS AND PUPPETEER TO RUN. INSTALL HERE: https://nodejs.org/en ===
#=== THEN IN THE COMMAND LINE IN THE FOLDER CONTAINING googlesearch2.js, RUN: npm install puppeteer

from rake_nltk import Rake
import subprocess
import pandas as pd
import json
import os

#=== NEEDS TO BE THE LOCATION OF googlesearch2.js === 
SEARCH_SCRIPT_DIRECTORY = ''

if SEARCH_SCRIPT_DIRECTORY == '':
    SEARCH_SCRIPT_DIRECTORY = os.getcwd()

#=== This portion can be replaced with an interface for prompt/AI output text ===
from tkinter import Tk
from tkinter import filedialog

root = Tk()
root.withdraw()


#filepath to AI output
filepath = filedialog.askopenfilename()
#=== ===


# Initialize RAKE
rake = Rake()


#=== Text filter function
def remove_special_chars(text):
    # Define the characters you want to remove
    remove_chars = '*$'
    
    # Create a translation table that maps the characters to be removed to None
    translation_table = str.maketrans('', '', remove_chars)
    
    # Use the translate() method to remove the specified characters
    cleaned_text = text.translate(translation_table)
    
    return cleaned_text

if filepath:
    f = open(filepath,"r")
    input_text = f.read()
    rake.extract_keywords_from_text(input_text)
    
    #get the unique list of phrases
    keyword_phrase = list(set(rake.get_ranked_phrases_with_scores()))
    
    #sort by the score (highest)
    sorted_keywords = sorted(keyword_phrase, key= lambda x: x[0], reverse=True)
    
    #just for looking
    for phrase in sorted_keywords:
        print(phrase)
        
    NUMBER_OF_SEARCHES = 4
    
    output = []
    
    #filter. Only using the first 4 keyphrases
    #then running webscraper for the keyphrases
    for pair in sorted_keywords[:NUMBER_OF_SEARCHES-1]:
        
        term = remove_special_chars(pair[1])
        result = subprocess.run(["node", "googlesearch2.js", term], cwd=SEARCH_SCRIPT_DIRECTORY ,capture_output=True,text=True)
        
        #generating a list of links from the result of the script
        link_list = result.stdout.split()
        
        #dictionary to be converted to JSON
        data = dict()
        data["score"] = pair[0]
        data["keyphrase"] = term
        data["links"] = link_list
        
        output.append(data)
        
    for data in output:
        with open(data["keyphrase"] + "_data.json","w") as file:
            json.dump(data, file)
        
        
        
         
        
    
    
    
    
    
    
        
        
    
    
