   
def evalProgram(codeList, trace = False):
    #top level code that takes a list of parsed statements
    global Trace
    Trace = trace
    return evalElBlock(codeList, {}, [])
    
def evalEl(code, bindings = [], depth = 0):
    # evaluates code (parsed statement) with the bindings so far
    # bindings is a list of dictionaries, each with bindings
    # created from : a set statement, a def statement or a user function call
    if Trace or depth == 0:
        print("%sEval %s" % (" "*depth, toString(code)))
    answer = evalElHelp(code, bindings, depth)
    if Trace or depth == 0:
        print("%sAns  %s " % (" "*depth, toString(answer)))
    return answer
     
def evalElHelp(code, bindings, depth):
    # evaluates a single code statement with current bindings
    if isinstance(code, int):
        return code
    if "True" == code:
        return True
    if "False" == code:
        return False
    if "nil" == code: #nil is the empty list
        return []
    if isinstance(code, str): # variable
        return findValue(code, bindings, depth)
    # do all composite code
    fun = code[0]
    #numerical functions
    if fun == '+':
        return evalEl(code[1], bindings, depth +1) + evalEl(code[2], bindings, depth +1)
    if fun == '-':
        return evalEl(code[1], bindings, depth +1) - evalEl(code[2], bindings, depth +1)    
    if fun == '*':
        return evalEl(code[1], bindings, depth +1) * evalEl(code[2], bindings, depth +1)    
    if fun == '/':
        return evalEl(code[1], bindings, depth +1) / evalEl(code[2], bindings, depth +1)
    # control functions
    if fun == 'if':
        if evalEl(code[1], bindings, depth +1):
            return evalEl(code[2], bindings, depth +1)
        else:
            return evalEl(code[3], bindings, depth +1)
    # boolean functions
    if fun == 'not':
        return not evalEl(code[1], bindings, depth +1)
    if fun == 'and':
        return evalEl(code[1], bindings, depth +1) and evalEl(code[2], bindings, depth +1)
    if fun == 'or':
        return evalEl(code[1], bindings, depth +1) or evalEl(code[2], bindings, depth +1)
    if fun == 'eq': #only works between atoms
        return simpleEqual(evalEl(code[1], bindings, depth +1), evalEl(code[2], bindings, depth +1))
    if fun == '<':
        return evalEl(code[1], bindings, depth +1) < evalEl(code[2], bindings, depth +1)
    if fun == 'atom':
        ans = evalEl(code[1], bindings, depth +1)
        return isinstance(ans, int) or isinstance(ans, str) or ans == True or ans == False or ans == []
    # data structures
    if fun == 'cons': #add the first to a list
        return [evalEl(code[1], bindings, depth +1)] + evalEl(code[2], bindings, depth +1)
    if fun == 'first': #eval then return the first
        return evalEl(code[1], bindings, depth +1)[0]
    if fun == 'rest': #eval then return the rest
         return evalEl(code[1], bindings, depth +1)[1:]
    if fun == 'quote': #stop evaluation
         return code[1]
    if fun == 'evalEl': #evaluate to get the code, then evaluate the code
         return evalEl(evalEl(code[1], bindings, depth +1))   
     #must be a user function call
    return evalElFun(code[0], code[1:], bindings, depth +1)
    
def simpleEqual(a, b):
    # only works on primitives
    if isinstance(a, int) and isinstance(b, int):
        return a == b
    if (a is True and b is True) or (a is False and b is False):
        return True
    if (a == []) and (b == []):
        return True
    return False

def evalElFun(funName, args, bindings, depth):
    ############ COMPLETE THIS CODE
    #Execute a user defined function
    block = []
    func = None
    for dic in bindings:
        if funName in dic:
            func = dic[funName]
    if func == None:
        print("Can't find function")
        return
    # HERE
    if Trace:
        print(" "*depth + "Calling function %s" % (funName,))
    #lookup the function parameters and body in bindings
    # HERE    
    #create a new binding (dictionary) to hold local variables from parmeters, sets and defs
    oneBinding = {}
    # add the mapping from parameter names to values
    # HERE
    param = func[0]
    for i in range(0, len(param)):
        # if isinstance(args[i], str):
        #     oneBinding[param[i]] = findValue(args[i], bindings, depth)
        # else:
        #     oneBinding[param[i]] = args[i]
        oneBinding[param[i]] = evalEl(args[i], [oneBinding] + bindings, depth)
    block.append(func[1])

    # work through each statement in block
    # block will the from the function definition
    return evalElBlock(block, oneBinding, bindings, depth = depth +1)
    
def evalElBlock(block, oneBinding, bindings, depth = 0):
    ############ COMPLETE THIS CODE
    # walks down the block evaluating each statement and accumulating bindings
    # into this oneBinding for this block
    if len(block) == 0: #empty block, return None
        return 
    else:
        code = block[0]
        if code[0] == 'set':
            # map the name of the variable to the eval of value
            # store the name to value mapping in oneBindings
            # HERE
            # keep going through the block
            oneBinding[code[1]] = evalEl(code[2], [oneBinding] + bindings)
            return evalElBlock(block[1:], oneBinding, bindings, depth = depth)
        elif code[0] == 'def': 
            #put mapping from name to arguments, block
            # HERE
            # keep working through block
            oneBinding[code[1]] = code[2:]
            return evalElBlock(block[1:], oneBinding, bindings, depth = depth)
        else: #found an expression, evaluate it with current bindings
            ans = evalEl(block[0], [oneBinding] + bindings, depth)
            # if last expression then return the answer
            if block[1:] == []:
                return ans
            else: #keep going through the block
                return evalElBlock(block[1:], oneBinding, bindings, depth = depth)
    
def findValue(name, bindings, depth):
    ############ COMPLETE THIS CODE
    # name is a variable, bindings is a list of dictionaries ordered most
    # recent first, search up the bindings seeing if this variable is in
    # one of the dictionaries
    # HERE
    for dic in bindings:
        if name in dic:
            return dic[name]
    print("Can't find variable " + name)
    return 0

def toString(code):
    # prints the parse tree in a more readable form
    if isinstance(code, int) or isinstance(code, str) or len(code) == 0:
        return str(code) + " "
    string = "("
    for item in code:
        string = string + toString(item)
    return string + ')'
