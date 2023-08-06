# Rule Based Bengali Stemmer

## Usage
    from stemmer.stemmer import BengaliStemmer
    
    stemmer = BengaliStemmer()
    stemmer.stem('জনপ্রিয়তা')  # 'জনপ্রি'
    stemmer.stem(' সেটাই')    # 'সে'

## Rules Documentation
#### `X + n :` 
When X appears at the end of a word and word length is at least n, remove it
#### `Y -> Z + n :` 
When Y appears at the end of a word and word length is at least n, replace it with Z
#### `Y.Z -> A.B + n :`
When Y, followed by some character a, followed by Z appears at the end of a word 
and word length is at least n, replace it with AaB    
