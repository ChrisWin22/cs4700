############# STARTER CODE ####################################################
from random import random, randint
import os
#PATH = "C:/Users/nickf/Dropbox/Classes/CS4700 Spring 2020/lisp interpreter/data/"
# if not os.path.exists(PATH):
#     os.makedirs(PATH)
    
Operators = ['+', '-', '*', '/']
def generateRandomExpression(maxDepth = 10):
    # generates a string that is a legal sentence in the grammar of our simple lisp language
    if random() < 0.1 or maxDepth < 0:
        return str(randint(0, 100))
    else:
        return "(%s %s %s)" % (Operators[randint(0, 3)], 
                                generateRandomExpression(maxDepth - 1), 
                                generateRandomExpression(maxDepth - 1))
                
def tokenize(chars):
    # takes a string representing an expression in simple lisp and returns a list of tokens
    # Checks for simple syntax errors
    list = chars.replace('(', ' ( ').replace(')', ' ) ').split()
    for i in list:
        if not(i == '(' or i == ')' or i in Operators or i.isdigit()):
           print(i + " is not a valid token") 
    return list


def pp(tokens, depth):
    if len(tokens) == 0:
       return 
    token = tokens.pop(0)
    if token.isdigit():
        for _ in range(0, depth):
            print(" ", end=" ")
        print(token)
        pp(tokens, depth)
    if token == '(':
        for _ in range(0, depth):
            print(" ", end=" ")
        print(token + tokens.pop(0))
        pp(tokens, depth + 1)
    if token == ')':
        depth = depth - 1
        for _ in range(0, depth):
            print(" ", end=" ")
        print(token)
        pp(tokens, depth)

    
def atom(token):
    # changes a token to an actual integer 
    if token.isdigit():
        return int(token)
    return token
    
print(atom('56'))
print(atom('('))
print(atom('0.344'))
print(atom('+'))

for _ in range(0, 10):
    exp = generateRandomExpression(2)
    #exp = "(+ 5 7)"
    print(exp)
    pp(tokenize(exp), 0)




#This is the class code from the board
#Still need to have depth manage spaces
def parsepp(parsetree, depth):
    if isinstance(parsetree, int):
        print(parsetree)
        return
    else:
        for i in range(0,depth):
            print(" ")
            i = i + 1
        print("(" + parsetree[0])
        parsepp(parsetree[1], depth + 1)
        for i in depth:
            print(" ")
            i = i + 1
        print(")")
            
            
        
#string = "(+57)"
#tokens = tokenize(string)
#parsepp(tokens, 0)
        


#write pp from a parse tree
#Example = "(+57)" -> ['+','5','7']
#Example 2 = "(+(-67)(+52)) -> ['+',[-,6,7],[+,5,2]]
#parsetree = integer or [operator, parsetree, parsetree]

       








