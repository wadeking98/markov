#! /usr/bin/env python3
import sys
import numpy as np
import random

def tokenize(string, tok_type, size):
    """
    splits the string into tokens specified by size or
    splits into words specified by size
    """
    if tok_type == "char":
        tokens = [string[i:i+size] for i in range(0,len(string),size)]
    else:
        string = string.replace("\n", " ")
        string = string.split(" ")
        curr_token = ""
        tokens = []
        for curr_word in range(len(string)):
            curr_token += string[curr_word]+" "
            if (curr_word+1)%size == 0:
                tokens.append(curr_token)
                curr_token = ""
        
    #add the start and end chars
    tokens.append("%")
    tokens.insert(0,"@")

    return tokens

def gen_tok_mat(input_vec, tok_type, size):
    return [tokenize(string,tok_type,size) for string in input_vec]


def gen_char_list(tok_mat):
    char_list = []
    for tokens in tok_mat:
        for char in tokens:
            if not char in char_list:
                char_list.append(char)
    return char_list


def gen_char_mat(char_list, tok_mat):
    mat = np.zeros((len(char_list),len(char_list)))
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            mat[i][j] = trans_prob(char_list[i],char_list[j],tok_mat)

    return mat


def trans_prob(a,b, tok_mat):
    num = 0
    total_trans = 0
    for tokens in tok_mat:
        total_trans += tokens.count(a)
    #for every token except the terminal token
    for tokens in tok_mat:
        for i in range(len(tokens)-1):
            #count the transitions from a to b
            if (tokens[i] == a) and (tokens[i+1]==b):
                num+=1
    return num/total_trans
            

def rand_choice(prob_vec):
    """
    chooses a random number from 0-len(prob_vec) based
    on the probabilities within the vector.
    The probabilities must add to 1
    """
    rand = random.random()
    curr_threshold = 0

    #return an index if the random number falls within its probability threshold
    for i in range(len(prob_vec)-1):
        #increase the current threshold
        curr_threshold += prob_vec[i]
        if (rand > curr_threshold) and (rand <= curr_threshold+prob_vec[i+1]):
            return i+1
    #we shouldnt get to here, but if we do it returns -1
    return -1
            


def walk(mat, char_list, curr_char):
    curr_idx = char_list.index(curr_char)
    next_idx = rand_choice(mat[curr_idx])
    if curr_char == "%":
        return ""
    elif curr_char == "@":
        return walk(mat,char_list,char_list[next_idx])
    return curr_char+walk(mat,char_list,char_list[next_idx])
        
        


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print("err: input file name, char node size, and length required")
        exit(1)
    
    split_type = sys.argv[1]
    size = int(sys.argv[2])
    input_name = sys.argv[3]

    input_raw = ""

    with open(input_name,"r") as input_file:
        input_raw = input_file.read()

    input_clean = ""
    for split in input_raw.split("\n"):
        input_clean += split
    
    input_clean = input_clean.lower()

    input_vec = input_clean.split("~")


    #now we have our clean input

    print("The program is training on your input...")

    tokens = tokenize(input_clean,split_type,size)

    tok_mat = gen_tok_mat(input_vec,split_type,size)

    char_list = gen_char_list(tok_mat)

    mat = gen_char_mat(char_list,tok_mat)

    

    usr_input = input("press enter to see an output example or 'q' to quit\n")
    while(usr_input != "q"):
        print("\n"+walk(mat,char_list,"@")+"\n")
        usr_input = input("press enter to see an output example or 'q' to quit \n")
