# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "zdenak11"
__date__ = "$20.4.2015 18:29:43$"

import os
import yaml
import re
import collections # requires Python 2.7 -- see note below if you're using an earlier version

baseFolder = os.getcwd()

def merge_dict(d1, d2):
    """
    Modifies d1 in-place to contain values from d2.  If any value
    in d1 is a dictionary (or dict-like), *and* the corresponding
    value in d2 is also a dictionary, then merge them in-place.
    """
    for k,v2 in d2.items():
        v1 = d1.get(k) # returns None if v1 has no value for this key
        if ( isinstance(v1, collections.Mapping) and 
             isinstance(v2, collections.Mapping) ):
            merge_dict(v1, v2)
        else:
            d1[k] = v2

def nested_set(dict, keys, value):
    for key in keys[:-1]:
        dict = dict.setdefault(key, {})
    dict[keys[-1]] = value
    

def saveDictionary(filename, dict):
    with open(filename, 'w+') as outfile:
        outfile.write(yaml.dump(dict, default_flow_style=False, default_style='"'))
        
def loadDictionary(filename):
    with open(filename, 'r') as inputfile:
        dict = yaml.load(inputfile)
    return dict

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

def findKeys(filename, dictionary):
    param = 0
    first = ''
    last = ''
    namespace = ''
    translator_format_start = ''
    translator_format_end = ''
    keys = []
    with open(filename + '.tmp', 'w') as outputfile:
        with open(filename, 'r') as inputfile:
            for line in inputfile:
                if param == 0:
                    if 'extractor_setting' in line:
                        param = 1
                        outputfile.write(line)
                        continue
                    else:
                        outputfile.write(line)
                elif param == 1:
                    first = re.sub('\n$','',line)
                    param = 2
                    outputfile.write(line)
                    continue
                elif param == 2:
                    last = re.sub('\n$','',line)
                    param = 3
                    outputfile.write(line)
                    continue
                elif param == 3:
                    namespace = re.sub('\n$','',line)
                    param = 4
                    outputfile.write(line)
                    continue
                elif param == 4:
                    translator_format_start = re.sub('\n$','',line)
                    param = 5
                    outputfile.write(line)
                    continue
                elif param == 5:
                    translator_format_end = re.sub('\n$','',line)
                    param = 6
                    outputfile.write(line)
                    continue
                elif param == 6:
                    if first in line:
                        key = find_between(line, first, last)
                        keys.append(key)
                        newline = line.replace(first + key + last, translator_format_start + key + translator_format_end)
                        outputfile.write(newline)
                    else:
                        outputfile.write(line)
    if param != 0:                    
        location = namespace.split('.')
        d = dict(empty='empty')
        for item in keys:
            d[item] = ''
        d.pop('empty', None)
        addDict = dict(empty='empty')
        nested_set(addDict, location, d)
        addDict.pop('empty', None)
        merge_dict(addDict, dictionary)
        dictionary = addDict
    
    return dictionary

modules=set()
exclude=['config', 'model', 'lang', 'router']
dictionary = loadDictionary(os.path.join(baseFolder, 'lang', 'front.neon'))
for root, dirnames, filenames in os.walk(baseFolder):
    dirnames[:] = [d for d in dirnames if d not in exclude]
    
    for dir in dirnames:
        if 'Module' in dir:
            dirnames.remove(dir)
            modules.add(dir)
            
    for filename in filenames:
        if filename.endswith(('.php', '.latte')):
            dictionary = findKeys(os.path.join(root, filename), dictionary)
            os.rename(os.path.join(root, filename), os.path.join(root, filename + '.bak'))
            os.rename(os.path.join(root, filename + '.tmp'), os.path.join(root, filename))


for m in modules:
    if os.path.exists(os.path.join(baseFolder, 'lang', re.sub('\Module$', '.neon', m))):
        modulDictionary = loadDictionary(os.path.join(baseFolder,'lang', re.sub('\Module$', '.neon', m)))
    else:
        modulDictionary = dict(empty='empty')
        modulDictionary.pop('empty', None)
    
    for root, dirnames, filenames in os.walk(os.path.join(baseFolder, m)):
        dirnames[:] = [d for d in dirnames if d not in exclude]
        for filename in filenames:
            if filename.endswith(('.php', '.latte')):
                modulDictionary = findKeys(os.path.join(root, filename), modulDictionary)
                os.rename(os.path.join(root, filename), os.path.join(root, filename + '.bak'))
                os.rename(os.path.join(root, filename + '.tmp'), os.path.join(root, filename))
                
    saveDictionary(os.path.join(baseFolder, 'lang', re.sub('\Module$', '.neon', m)), modulDictionary)            
    
    
saveDictionary(os.path.join(baseFolder, 'lang','front.neon'), dictionary)