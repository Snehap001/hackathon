import random
import csv
import string
from PyDictionary import PyDictionary
import numpy as np
import pandas as pd
def place_word(board, word):
    # Randomly choose orientation: 0=horizontal, 1=vertical, 2=diagonal
    orientation = random.randint(0, 1)
    
    placed = False
    while not placed:
        if orientation == 0:  # Horizontal
            row = random.randint(0, len(board)-1)
            col = random.randint(0, len(board)-len(word))
            
            
            space_available = all(board[row][c] == '-' or 
              board[row][c] == word[i] 
                for i, c in enumerate(range(col, col+len(word))))
            if space_available:
                for i, c in enumerate(range(col, col+len(word))):
                    board[row][c] = word[i]
                placed = True

        elif orientation == 1:  # Vertical
            row = random.randint(0, len(board)-len(word))
            col = random.randint(0, len(board)-1)
           
            space_available = all(board[r][col] == '-' or 
                board[r][col] == word[i] 
                  for i, r in enumerate(range(row, row+len(word))))
            if space_available:
                for i, r in enumerate(range(row, row+len(word))):
                    board[r][col] = word[i]
                placed = True

        
def fill_empty(board):
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == '-':
                board[row][col] = random.choice(string.ascii_lowercase)

def create_word_search(words,word_size):
    board = [['-' for _ in range(word_size+1)] for _ in range(word_size+1)]

    for word in words:
        place_word(board, word)
        print(word,",")

    fill_empty(board)

    return board

def display_board(board):
    for row in board:
        print(' '.join(row))

def create_dictionary(file_path):
    
    dictionary_instance = PyDictionary()
    mydict=[]
    fields=["word","meaning"]
    filename="word_meaning.csv"
    # Read the text file containing words
    with open(file_path, 'r') as file:

        words = file.readlines()
    for word in words:
        dictionary = {}
        word.strip()
        f=open("word_meaning.txt","a")
        meanings=dictionary_instance.meaning(word)
        if meanings:
            if 'Noun' in meanings:
                meaning=meanings['Noun'][0]
            elif 'Verb' in meanings:
                meaning=meanings['Verb'][0]
            elif 'Adjective' in meanings:
                meaning=meanings['Adjective'][0]
            else:
                meaning="Not found"
        else:
            meaning="not found"
        dictionary['meaning']=meaning
        dictionary['word']=word.strip()
        mydict.append(dictionary)
    
        with open (filename,'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
    
            # writing headers (field names)
            
        
            # writing data rows
            writer.writerow(dictionary)
            csvfile.close()