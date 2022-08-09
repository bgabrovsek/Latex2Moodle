from itertools import product
from random import choice
import re

def tags(s, sub):
    """
    dobi vsebino tag-a \sub{...}
    """
    result = []
    start = 0
    while True:
        start = s.find(sub + "{", start)
        if start == -1: return result
        start += len(sub) +1 # use s
        # search until a } bracket
        i = start
        bracket_depth = 0

        #print("start",start,s[start:])

        while bracket_depth >= 0:
            #print("brac", bracket_depth)
            if s[i] == '{' : bracket_depth += 1
            if s[i] == '}' : bracket_depth -= 1
            i += 1
            if i > len(s):
                raise OverflowError("index too big")

        result.append(s[start:i-1])


        # tart += 1 to find overlapping m

    return result




def double_tags(s, sub):
    """
    dobi vsebino dvojnega tag-a \sub{...}{...}
    """
    result = []
    start = 0
    while True:
        start = s.find(sub + "{", start)
        if start == -1: return result
        start += len(sub) +1 # use s
        # search until a } bracket
        i = start
        bracket_depth = 0

        #print("start",start,s[start:])
        # first tag
        while bracket_depth >= 0:
            #print("brac", bracket_depth)
            if s[i] == '{' : bracket_depth += 1
            if s[i] == '}' : bracket_depth -= 1
            i += 1
            if i > len(s):
                raise OverflowError("index too big")
        # second tag

        if s[i] != "{": raise ValueError("No second tag detected.")
        end1 = i-1
        start2 = i+1
        i += 1
        bracket_depth = 0
        while bracket_depth >= 0:
            #print("brac", bracket_depth)
            if s[i] == '{' : bracket_depth += 1
            if s[i] == '}' : bracket_depth -= 1
            i += 1
            if i > len(s):
                raise OverflowError("index too big")


        result.append((s[start:end1],s[start2:i-1]))


        # tart += 1 to find overlapping m

    return result


def tag(s, sub):
    res = tags(s, sub)
    return res[0] if len(res) > 0 else None


def read(filename):
    """
    preberi latex datoteko
    """
    with open(filename, 'r', encoding='utf-8') as f:
        s = f.read()
    #    s = f.readlines()


 #   s = [l[:l.find['#']] for l in s]
#    s =


    #print(s)


    d = dict() # main dictionary

    d['category'] = tag(s, 'category')
    d['name'] = tag(s, 'name')
    d['range'] = double_tags(s, 'range')
    d['conditions'] = tags(s, 'condition')
    d['randomize'] = (s.find('randomize') > -1)
    d['n'] = tag(s,'num')
    d['text'] = tag(s, 'exercise')

    d['n'] = (int(d['n']) if d['n'] is not None else 150)



    d['params'] = [p[0] for p in d['range']]
    return d

#    print(s_latex)



def split_math(s):
    """ splits s into text and math mode"""
    result = []
    start = 0
    i = 0
    dollars = 0
    while True:
        # end of math?
        if dollars and s[i] == "$":
            result.append((dollars,s[start:i]))
            #print("MATH", "$"*dollars, start, i, "\""+s[start:i]+"\"")
            i += 1
            if i < len(s) and s[i] == "$":
                i += 1
            dollars = 0
            start = i
        if i >= len(s):
            result.append((dollars, s[start:i]))
            break
        # new math?
        if not dollars and s[i] == "$":

            result.append((dollars,s[start:i]))

            i += 1
            dollars = 1  # single $
            if i < len(s) and s[i] == "$":
                dollars = 2
                i += 1
            start = i


        i += 1
        if i >= len(s):
            result.append((dollars, s[start:i]))
            break
    return result

def get_all_eval_variables(s):
    vars = ""
    for sub in tags(s, "eval"):
        vars += "".join(re.findall("[a-zA-Z]+", sub))
    return set(vars)


def clean_and_insert(expression, parameters = None, values = None):
    """ evaluate string expression with parameters having values """
    s = expression

    # clean up
    s = s.replace("^","**")
    while s.find(' ') > -1:
        s = s.replace(' ','')
    i = 0
    while i < len(s)-1:
        if (s[i].isalpha() or  s[i].isnumeric()) and s[i+1].isalpha():
            s = s[:i+1] + "*" + s[i+1:]
            i += 1
        i += 1

    # insert parameter values
    if parameters is not None and values is not None:
        for par, val in zip(parameters, values):
            s = s.replace(par, "(" + str(val) + ")")

    #parse_expr(new_expression, evaluate=True)

    return s


def clean_eq(s):
    q = s
    replacements = [("<=","Đ"),("\\leq","Đ"),(">=","đ"),("\\geq","đ"),("!=","ć"),("\\neq","ć"),("==","Ć"),("=","Ć"),
                    ("Đ","<="),              ("đ",">="),              ("ć","!="),              ("Ć","==")]
    while q.find(' ') > -1:
        q = q.replace(' ','')
    for s1, s2 in replacements:
        q = q.replace(s1, s2)
    return q




def loop_through_parameters(d):
    range_list = [eval('[' + x[1] + ']') for x in d['range']]
    if d['randomize']:
        while True:
            yield [choice(q) for q in range_list]
    else:
        for r in product(*range_list):
            yield r
    return


#new_expression = expression.replace("^", "**")
#for p, val in zip(d['params'], vals):
#    new_expression = new_expression.replace(p, "(" + str(val) + ")")

#evaluated = sympify(new_expression)  # parse_expr(new_expression, evaluate=True)
