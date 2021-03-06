# -*- coding: utf-8 -*-
"""
Created on Sat Jun 5 15:30:03 2021

@author: ryanz
"""

def chunks(l, n):
    """
    split list equally into smaller sublists

    Parameters
    ----------
    l : list to split
    n : number of elements per sublist

    Yields
    ------
    smaller lists of l with len(n) each

    """
    for i in range(0, len(l), n):
        yield l[i:i+n]


def is_CJK(char):
    return any([start <= ord(char) <= end for start, end in 
                [(4352, 4607), (11904, 42191), (43072, 43135), (44032, 55215), 
                 (63744, 64255), (65072, 65103), (65381, 65500), 
                 (131072, 196607)]
                ])

from unidecode import unidecode

def sanitize_uni(string, for_search = False):
    '''
    convert known/common un-unidecodable and unicode strings to ASCII and clean string for tag-matching

    '''
  
    ret= []
    for i in string:
        if i in MULT_CHAR_MAP:
            for char in MULT_CHAR_MAP[i]:
                ret.append(char)
            continue
        i = CHAR_MAP.get(i, i)
        if i in VALID_CHARS:
            ret.append(i)
            continue
        
        ret.append(" ")
        # n = unidecode(i)
        # if n=="":
        #     ret.append(" ")
        # elif n in VALID_CHARS:
        #     ret.append(n)
            
    if for_search:
        return ''.join(ret)

    while len(ret)>0:
        if ret[0] in PRE_REMOVE:
            ret.pop(0)
        elif ret[-1] in POST_REMOVE:
            ret.pop(-1)
        else:
            break

    return ''.join(ret)


def sanitize_tag_uni(string):
    '''
    get rid of non-ASCII characters that cannot be converted, but keep convertable characters in original form
    '''
    string = [i for i in string if CHAR_MAP.get(i, i) in VALID_CHARS or i in MULT_CHAR_MAP or (unidecode(i)!="" and unidecode(i) in VALID_CHARS)]
    while len(string)>0:
        if string[0] in PRE_REMOVE:
            string.pop(0)
        elif string[-1] in POST_REMOVE:
            string.pop(-1)
        else:
            break

    return ''.join(string)


### constants + maps

VALID_CHARS = "/\*^+-_.!?@%&()\u03A9\u038F" + "abcdefghijklmnopqrstuvwxyz" + "abcdefghijklmnopqrstuvwxyz0123456789 ".upper()
PRE_REMOVE = "/\*^+-_.!?#%() "
POST_REMOVE = "/\*^+-.!?# "

CHAR_MAP = {
    "??": 'A', "??": 'A', "@": 'A', "??": "A", "??": "A", "??": "A", "??": "A", "??": "A", "??": "A", "??": "A", "??": "A", "??": "a", "??": "a", "??": "a", "??": "a", "??": "a", "??": "a", "??": "a", "??": "a", "??": "a",
    
    "???": "b", "??": "B", "??": "B",
    
    "??": "c", "??": "c", "??": "c", "??": "c", "??": "C",
    
    "??": "e", "??": "e", "??": "e", "??": "e", "??": "e", "???": "e", "??": "E", "???": "E", "??": "E", "??": "E", "??": "E", "??": "E", "??": "E", "??": "E", "??": "E", "??": "E", "??": "E",
    
    "??": "H",

    "??": "i", "??": "i", "??": "i", "??": "i", "??": "i", "??": "i", "??": "i", "??": "i", "??": "I", "??": "I", "??": "I", "??": "I", "??": "I", "??": "I",
    
    "??": "k", 

    "??": "n", "??": "n", "??": "n", "??": "N", "??": "N",

    "??": "o", "???": "o", "??": "o", "??": "o", "??": "o", "??": "o", "??": "o", "??": "o", "??": "o", "??": "o", "??": "o", "??": "o", "??": "O", "??": "O", "??": "O", "??": "O", "??": "O", "??": "O", "??": "O", "??": "O", "??": "O", "??": "O", "??": "O", "??": "O", "??": "O", "???": "O",
    
    "???": "P", "??": "p",
    
    "??": "r", "??": "r", "??": "R",
    
    "$": "S", "??": "S",
    
    "??": "t",
    
    "??": "u", "??": "u", "??": "u", "??": "u", "??": "u", "??": "u", "??": "u", "??": "U", "??": "U", "??": "U", "??": "U", "??": "U", "??": "u",
    
    "??": "v",

    "??": "w", "??": "w", "??": "w", "??": "W",
    
    "??": "X",
    
    "??": "y", "??": "y", "??": "y", "??": "Y", "??": "Y", "??": "Y", "??": "Y", "??": "Y",
    
    "??": "Z"
}

MULT_CHAR_MAP = {
    "??": 'AE',
    "??": "ae",

    "??": "oe",
    "??": "OE",

    "???": "TM"
}

if __name__ == "__main__":
    import time
    i = ""
    sans = []
    t = time.time()
    for _ in range(100):
        sans.append(sanitize_uni(i))
    print(time.time()-t)
    print(sans[0])
    
