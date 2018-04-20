import random
from functools import reduce

class Value:
    def __init__(self, name):
        self.name = name

    def to_latex(self):
        return self.name

    def to_wolfram(self):
        return self.name


class Term:
    @staticmethod
    def operation_to_latex(operation):
        if operation == "MUL":
            return  ""
        elif operation == "SUB":
            return " - "
        elif operation == "ADD":
            return " + "
        elif operation == "DIV":
            return " / "
        elif operation == "EXP":
            return "^"
        else:
            return ""

    @staticmethod
    def operation_to_wolfram(operation):
        if operation == "MUL":
            return  "*"
        elif operation == "SUB":
            return " - "
        elif operation == "ADD":
            return " + "
        elif operation == "DIV":
            return " / "
        elif operation == "EXP":
            return "\\^{}"
        else:
            return ""
        
    def __init__(self, valuea, operation, valueb):
        self.lvalue = valuea
        self.rvalue = valueb
        self.op = operation

    def to_latex(self):
        if self.op == "DIV":
            return "\\frac{" + self.lvalue.to_latex()  + "}{ " + self.rvalue.to_latex() + " }"
        return self.lvalue.to_latex() + Term.operation_to_latex(self.op) + self.rvalue.to_latex()

    def to_wolfram(self):
        if type(self.lvalue) is Term:
            left = "(" +  self.lvalue.to_wolfram() + ")"
        else:
            left = self.lvalue.to_wolfram()
        right = self.rvalue.to_wolfram()
        if type(self.rvalue) is Term:
            right = "(" + right + ")"
            
        return left + Term.operation_to_wolfram(self.op) + right
        



def create_function(variables=None):
    term_count = random.choice(range(2,4))
    parameter_count = random.choice(range(2,4))
    variables = variables or list(map(lambda x: ["x", "y", "z"][x-1], range(1,parameter_count+1)))
    result = None
    used_variables = set()
    for i in range(0, term_count):
        factor_count = random.choice(range(1,4))
        values = []
        for j in range(0, factor_count):
              while True:
                  variable = random.choice(variables)
                  if variable in used_variables and random.random() > 0.5:
                          break
                  elif random.random() > 0.2:
                      break

                  
              values.append(variable) 
        for temp in values:
            if temp not in used_variables:
                used_variables.add(temp)
        
                
        terms = {}
        factor = []
        for value in values:
            terms[value] = terms.setdefault(value, 0) + 1
        for variable in (terms.keys()):
            if terms[variable] > 1:
                variable = Term(Value(variable), "EXP", Value(str(terms[variable])))
            else:
                variable = Value(variable)
            factor.append(variable)
    
        new_term = reduce((lambda x, y: Term(x, "MUL", y)), factor)
        if random.random() > 0.5:
            coefficient = random.choice(range(2,10))
            new_term = Term(Value(str(coefficient)), "MUL", new_term)
        if random.random() > 0.8:
            coefficient = random.choice(range(2,26))
            new_term = Term(new_term, "DIV", Value(str(coefficient)))
        if result is None:
            result = new_term
        else:
            result = Term(result,  "ADD", new_term)
    return (result, variables)

def create_question():
    (question, variables) = create_function()
    (condition, _unused) = create_function(variables)
    return "\\item{\\[ \\max_{x,y,z} " + question.to_latex() +"\\quad \\text{subject to} \\quad " + condition.to_latex() + "\]\\\\ \\textbf{Wolfram:} \\code{ optimize " + question.to_wolfram() + "} \\newline \\code{ subject to " + condition.to_wolfram() + "}}"

def create_worksheet():
    result = "%note: to use the code listings put the following in your preamble:\n"
    result += "% \\usepackage{xcolor}\n"
    result += "% \\definecolor{light-gray}{gray}{0.95}\n"
    result += "% \\newcommand{\\code}[1]{\\colorbox{light-gray}{\\texttt{#1}}}\n"
    result = result + "\\begin{itemize}\n"
    for i in range(0, 10):
        result += create_question() +"\n"
    result += "\\end{itemize}\n"
    return result

with open("questions.tex", "w") as f:
    f.write(create_worksheet())
