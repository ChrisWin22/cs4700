#BNF
#<expression> ::= <booleanExpression> || <numberExpression> || <number> || <mathExpression>
#<mathExpression> ::= <operator> <mathExpression> <mathExpression> || <number>
#<number> ::= integer
#<booleanExpression> ::= <booleanOperator> <booleanExpression> <booleanExpression> || <booleanNotOperator> <booleanExpression> || <number>


from random import random, randint
#from newCode import createParseTree, evaluate

import os
PATH = "C:/Users/Woo Kei Cheung/Desktop/CSHW/cs4700/HW5"
if not os.path.exists(PATH):
    os.makedirs(PATH)
    
# define all the possible operators and how many arguments they take
# for extended language
# HINT HINT HINT HINT HINT HINT HINT
OperatorsAll = ['+', '-', '*', '/', 'if', 'and', 'or', 'not', '>', 'eq' ]
OperatorsBoolBool = ['and', 'or', 'not', 'eq']
OperatorsBoolNumb = ['>', 'eq']
OperatorsNumb = ['+', '-', '*', '/']
LanguageConstants = ['True', 'False']
NumberOfArguments = {}
ArgumentCount = [(1, ['not']),(2, ['+', '-', '*', '/', 'and', 'or', 'eq', '>']), (3, ['if'])]
# # fill the mapping from operator to argument count
for (count, operators) in ArgumentCount:
    for op in operators:
        NumberOfArguments[op] = count
        
Operators = ['+', '-', '*', '/']
    
############## STARTER CODE ####################################################
def createParseTree(tokenList):
    token = tokenList.pop(0)
    if isinstance(token, int) or token in LanguageConstants:
        return token
    operator = tokenList.pop(0)
    NOA = NumberOfArguments[operator]
    if NOA == 1:
        firstArg = createParseTree(tokenList)
        tokenList.pop(0)
        return [operator] + [firstArg]
    elif NOA == 2:
        firstArg = createParseTree(tokenList)
        secondArg = createParseTree(tokenList)
        tokenList.pop(0) # pop the ')'
        return [operator] + [firstArg] + [secondArg]
    elif NOA == 3:
        firstArg = createParseTree(tokenList)
        secondArg = createParseTree(tokenList)
        thirdArg = createParseTree(tokenList)
        tokenList.pop(0) # pop the ')'
        return [operator] + [firstArg] + [secondArg] + [thirdArg]
    else:
        raise Exception("Unknown number of arguments")

     
def createParseTreeX(tokenList):
    if tokenList == []:
        raise Exception("Run out of tokens")
    token = tokenList.pop(0)
    if isinstance(token, int):
        return tokenList
    if not token == "(":
        raise Exception("Found %s instead of (" % (token,))
    if tokenList == []:
        raise Exception("Missing Operator")
    operator = tokenList.pop(0) 
    if not operator in Operators:
        raise Exception("Unknown operator %s" % operator)
    firstArg = createParseTreeX(tokenList)
    secondArg = createParseTreeX(tokenList)
    if tokenList == []:
        raise Exception("Missing )")
    close = tokenList.pop(0) # pop the ')'
    if not ')' == close: # pop the ')'
        raise Exception("Found %s instead of )" % (close,))
    return [operator] + [firstArg] + [secondArg]
     
def processAllGood ():
    # Generate a set of correct random test problems
    with open(PATH + 'correctSyntax.txt', 'r') as file:  # Use file to refer to the file object
        programs = file.readlines()
    for i in range(0, len(programs)):
        parse(programs[i])
        print("Index = %d \n" % i)

# only simple math to start with
Operators = ['+', '-', '*', '/']
def generateRandomProgram(maxDepth = 10):
    # generates a string that is a legal sentence in the grammar of our L language
    if random() < 0.1 or maxDepth < 0:
        return str(randint(0, 100))
    elif random() < 0.3:
        return generateRandomExpressionBool(maxDepth - 1)
    elif random() < 0.3:
        return generateRandomExpressionNumb(maxDepth - 1)
    else:
        return "(if %s %s %s)" % (generateRandomExpressionBool(maxDepth - 1), 
                                  generateRandomProgram(maxDepth - 1), 
                                  generateRandomProgram(maxDepth - 1))
                                  
def generateRandomExpressionNumb(maxDepth):
    if random() < 0.1 or maxDepth < 0:
        return str(randint(0, 100))
    return "(%s %s %s)" % (OperatorsNumb[randint(0,len(OperatorsNumb)-1)],
                            generateRandomExpressionNumb(maxDepth-1),
                            generateRandomExpressionNumb(maxDepth-1))
                                  
def generateRandomExpressionBool(maxDepth):
    if random() < 0.1 or maxDepth < 0:
        return ['True', 'False'][randint(0,1)]
    elif random() < 0.5:
        operator = OperatorsBoolBool[randint(0, len(OperatorsBoolBool)-1)]
        if NumberOfArguments[operator] == 1:
            return "(%s %s)" % (operator, 
                                generateRandomExpressionBool(maxDepth - 1))
        if NumberOfArguments[operator] == 2:
            return "(%s %s %s)" % (operator, 
                                   generateRandomExpressionBool(maxDepth - 1),
                                   generateRandomExpressionBool(maxDepth - 1))
    else:
        operator = OperatorsBoolNumb[randint(0, len(OperatorsBoolNumb)-1)]
        return "(%s %s %s)" % (operator,
                                generateRandomExpressionNumb(maxDepth - 1),
                                generateRandomExpressionNumb(maxDepth - 1))

def atom(token):
    # changes a token to an actual integer 
    if token.isdigit():
        return int(token)
    return token
    
def genGood ():
    # Generate a set of correct random test problems
    with open(PATH + 'correctSyntax.txt', 'w') as file:  # Use file to refer to the file object
        for _ in range(0, 1000):
            file.write(generateRandomExpressionNumb(1 + randint(0,10)) + "\n")
            
def genBad ():
    with open(PATH + 'errorSyntax.txt', 'w') as file:  # Use file to refer to the file object
        for _ in range(0, 1000):
            program = generateBadRandomExpression(1 + randint(0,10)) #(1 + randint(0,10))
            try: #try to parse the expression
                parse(program)
            # Only if it does not parse then we save
            except Exception as error:
                file.write(program + "\n")
                
BadOps = ['_', '=','(','%']
BadNumbers = ['1.2344','x','y']
def generateBadRandomExpression(maxDepth = 10):
    # generates a string that is a legal sentence in the grammar of our simple lisp language
    if random() < 0.1 or maxDepth < 0:
        return str(randint(0, 100))
    if random() < 0.05 or maxDepth < 0:
        return str(BadNumbers[randint(0, len(BadNumbers)-1)])
    elif random() < 0.05:
        return "(%s %s %s" % (Operators[randint(0, 3)], 
                                generateBadRandomExpression(maxDepth - 1), 
                                generateBadRandomExpression(maxDepth - 1))
    elif random() < 0.05:
        return "%s %s %s)" % (Operators[randint(0, 3)], 
                                generateBadRandomExpression(maxDepth - 1), 
                                generateBadRandomExpression(maxDepth - 1))
    else:
        return "(%s %s %s)" % (Operators[randint(0, 3)], 
                                generateBadRandomExpression(maxDepth - 1), 
                                generateBadRandomExpression(maxDepth - 1))

def evalL(parseTree):
    if isinstance(parseTree, int) or parseTree in LanguageConstants:
        return parseTree
    operator = parseTree[0]
    if operator == '+':
        return evalL (parseTree[1]) + evalL (parseTree[2])
    elif operator == '-':
        return evalL (parseTree[1]) - evalL (parseTree[2])
    elif operator == '*':
        return evalL (parseTree[1]) * evalL (parseTree[2])
    elif operator == '/':
        return evalL (parseTree[1]) / evalL (parseTree[2])
    elif operator == 'if':
        if parseTree[1] == 'True':
            return evalL (parseTree[2]) + evalL (parseTree[3])
    elif operator == 'and':
        return evalL (parseTree[1]) and evalL (parseTree[2])
    elif operator == 'or':
        return evalL (parseTree[1]) or evalL (parseTree[2])
    elif operator == 'not':
        return (not evalL(parseTree[1]))
    elif operator == '>':
        return evalL (parseTree[1]) > evalL (parseTree[2])
    elif operator == 'eq':
        return evalL (parseTree[1]) == evalL (parseTree[2])
    else:
        raise Exception("Evaluation Error: No Operator")

def quote(parseTree):
    return parseTree
                        
### takes a program string and returns a parse tree
def parse(programStr):
    # returns the input string as a parse tree, represented as either an int or a list of expressions
    return createParseTree(tokenize(programStr))
    
### does error checking
def parseX(programStr):
    # returns the input string as a parse tree, represented as either an int or a list of expressions
    return createParseTreeX(tokenize(programStr))
                            
### prettyPrint an expression (parsed list of tokens)
def prettyPrintExp(expression, depth = 0):
    # takes a parse tree and prints it out so it is easier to read (maybe)
    if isinstance(expression, int):
        print("%s %s" % (' ' * depth, expression))
    else:
        print("%s(%s " % (' ' * depth, expression[0]))
        prettyPrintExp(expression[1], depth+2)
        prettyPrintExp(expression[2], depth+2)
        print("%s) " % (' ' * (depth+1)))
        
### prettyPrint a list of tokens
def prettyPrint(tokenList, depth = 0):
    token = tokenList.pop(0)
    # atom, just print at depth and return
    if isinstance(token, int) or token in LanguageConstants:
        print("%s%s" % (' ' * depth, token))
    else:
        # compound expression
        operator = tokenList.pop(0)
        print("%s(%s" % (' ' * depth, operator))
        NOA = NumberOfArguments[operator] 
        if NOA == 1:
            prettyPrint(tokenList, depth+1)
        elif NOA == 2:
            prettyPrint(tokenList, depth+1)
            prettyPrint(tokenList, depth+1)
        elif NOA == 3:
            prettyPrint(tokenList, depth+1)
            prettyPrint(tokenList, depth+1)
            prettyPrint(tokenList, depth+1)
        else:
            raise Exception("Unknown number of arguments")
        tokenList.pop(0) # remove )
        print("%s)" % (' ' * depth,))
        
### very simple code that just checks whether the number of open parentheses
### is the same as the number of closed parentheses
def checkBalanced(tokenList):
    depth = 0
    while not tokenList == []:
        token = tokenList.pop(0)
        if token == '(': #consume and add 1 to depth
            depth = depth + 1
        if token == ')':
            depth = depth - 1
    return depth == 0
    
### takes a string representing an expression in simple lisp and returns a list of tokens
def tokenize(programStr):
    tokens = programStr.replace('(', ' ( ').replace(')', ' ) ').split()
    if all(legalToken(token) for token in tokens):
        return [atom(token) for token in tokens]
    else:
        badTokens = str([token for token in tokens if not legalToken(token)])[1:][:-1]
        raise Exception("Unknown token found %s" % (badTokens,))
  
### returns True if the token is legal      
def legalToken(token):
    # returns True if legal for our simple lisp
    return token.isdigit() or token in OperatorsAll + [')', '('] or token in LanguageConstants
            

# Do some testing
# for _ in range(0,15):
#     print(generateRandomProgram(3))
# TEST BAD
# for _ in range(100): 
#     exp = generateBadRandomExpression(5)
#     try: #try to parse the expression
#         parseTree = parseX(exp)
#     except Exception as error:
#         print("\n")
#         print(exp)
#         print("Parse error: %s" % (error,))
# 
# TEST GOOD
# for _ in range(100): 
#     exp = generateRandomProgram(3)
#     parseTree = parse(exp)
#     prettyPrint(tokenize(exp))
expr = generateRandomProgram(1)
expr = ("(and False True)")
print(expr)
parsed = parse(expr)
print(evalL(parsed))

#genGood()
#genBad()             


    

                    
#processAllGood()
                                
                                