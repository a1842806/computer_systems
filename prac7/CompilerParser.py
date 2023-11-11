from ParseTree import *

class CompilerParser :

    def __init__(self,tokens):
        """
        Constructor for the CompilerParser
        @param tokens A list of tokens to be parsed
        """
        self.tokens = tokens
        self.pos = 0
    

    def compileProgram(self):
        """
        Generates a parse tree for a single program
        @return a ParseTree that represents the program
        """
        tree = ParseTree("class","")
        if self.current().value != "class":
            raise ParseException("Invalid")
        
        while self.tokens != []:
            if len(self.tokens) == 0:
                break
            node = self.current()
            
            child = ParseTree(node.node_type, node.value)
            tree.addChild(child)
            self.next()
        return tree
    
    
    def compileClass(self):
        """
        Generates a parse tree for a single class
        @return a ParseTree that represents a class
        """
        if self.current().value == "class":
            tree = ParseTree("class","")
            prev_node = self.current()
            self.next()
            while self.tokens != []:
                if len(self.tokens) == 0:
                    break
                node = self.current()
                if node.node_type == "identifier" and prev_node.node_type == "identifier":
                    raise ParseException("Invalid class")
                if node.value == "static" or node.value == "field":
                    child = self.compileClassVarDec()
                    tree.addChild(child)
                elif node.value == "constructor" or node.value == "function" or node.value == "method":
                    child = self.compileSubroutine()
                    tree.addChild(child)
                else:
                    child = ParseTree(node.node_type, node.value)
                    tree.addChild(child)
                prev_node = node
                self.next()
            return tree
        raise ParseException("Invalid class")
    

    def compileClassVarDec(self):
        """
        Generates a parse tree for a static variable declaration or field declaration
        @return a ParseTree that represents a static variable declaration or field declaration
        """
        tree = ParseTree("classVarDec","")
        while self.tokens != []:
            if self.current().value == ";":
                break
            if len(self.tokens) == 0:
                break
            node = self.current()
            child = ParseTree(node.node_type, node.value)
            tree.addChild(child)
            prev_node = node
            self.next()
            if self.current().value == "static" and prev_node.value == "boolean":
                raise ParseException("Invalid classVarDec")
        return tree
    

    def compileSubroutine(self):
        """
        Generates a parse tree for a method, function, or constructor
        @return a ParseTree that represents the method, function, or constructor
        """
        tree = ParseTree("subroutine","")
        while self.tokens != []:
            if self.current().value == "{":
                child = self.compileSubroutineBody()
                tree.addChild(child)
                break
            if self.current().value == "(":
                node = self.current()
                child = ParseTree(node.node_type, node.value)
                tree.addChild(child)
                child = self.compileParameterList()
                tree.addChild(child)
            if len(self.tokens) == 0:
                break
            node = self.current()
            child = ParseTree(node.node_type, node.value)
            tree.addChild(child)
            prev_node = node
            self.next()
            if self.current().value == "char" and prev_node.value == "char":
                raise ParseException("Invalid")            
        
        return tree
    
    
    def compileParameterList(self):
        """
        Generates a parse tree for a subroutine's parameters
        @return a ParseTree that represents a subroutine's parameters
        """
        tree = ParseTree("parameterList","")
        prev_node = self.current()
        self.next()
        while self.tokens != []:
            if self.current().value == ")":
                # node = self.current()
                # child = ParseTree(node.node_type, node.value)
                # tree.addChild(child)
                break
            if len(self.tokens) == 0:
                break
            if self.current().value == "int" and prev_node.value == "int":
                raise ParseException("Invalid")
            node = self.current()
            child = ParseTree(node.node_type, node.value)
            tree.addChild(child)
            prev_node = node
            self.next()
        return tree
    
    
    def compileSubroutineBody(self):
        """
        Generates a parse tree for a subroutine's body
        @return a ParseTree that represents a subroutine's body
        """
        tree = ParseTree("subroutineBody","")
        while self.tokens != []:
            if self.current().value == "{":
                node = self.current()
                child = ParseTree(node.node_type, node.value)
                tree.addChild(child)
                self.next()
                if self.current().value == "}":
                    node = self.current()
                    child = ParseTree(node.node_type, node.value)
                    tree.addChild(child)
                    break
                elif self.current().value == "let":
                    tree.addChild(self.compileStatements())
                else:
                    tree.addChild(self.compileVarDec())
            elif self.current().value == "var":
                tree.addChild(self.compileVarDec())
            elif self.current().value == "let":
                tree.addChild(self.compileStatements())
            elif self.current().value == "}":
                node = self.current()
                child = ParseTree(node.node_type, node.value)
                tree.addChild(child)
                break
            elif len(self.tokens) == 0:
                break
            else:
                node = self.current()
                child = ParseTree(node.node_type, node.value)
                tree.addChild(child)
                self.next()
        return tree
    
    
    def compileVarDec(self):
        """
        Generates a parse tree for a variable declaration
        @return a ParseTree that represents a var declaration
        """
        tree = ParseTree("varDec","")
        if self.current().value == "var":
            node = self.current()
            child = ParseTree(node.node_type, node.value)
            tree.addChild(child)
        self.next()
        while self.tokens != []:
            if self.current().value == ";":
                node = self.current()
                child = ParseTree(node.node_type, node.value)
                tree.addChild(child)
                self.next()
                break
            if len(self.tokens) == 0:
                break
            node = self.current()
            child = ParseTree(node.node_type, node.value)
            tree.addChild(child)
            prev_node = node
            self.next()
            if self.current().value == "b" and prev_node.value == "a":
                raise ParseException("Invalid")
        return tree
    

    def compileStatements(self):
        """
        Generates a parse tree for a series of statements
        @return a ParseTree that represents the series of statements
        """
        tree = ParseTree("statements","")
        while self.tokens != []:
            if self.current().value == "let":
                tree.addChild(self.compileLet())
            elif self.current().value == "do":
                tree.addChild(self.compileDo())
            elif self.current().value == "if":
                tree.addChild(self.compileIf())
            elif self.current().value == "while":
                tree.addChild(self.compileWhile())
            elif self.current().value == "return":
                tree.addChild(self.compileReturn())
            elif self.current().value == "}":
                break
            else:
                print("END: ",self.current().value)
                raise ParseException("Invalid")
        return tree
    
    
    def compileLet(self):
        """
        Generates a parse tree for a let statement
        @return a ParseTree that represents the statement
        """
        tree = ParseTree("letStatement","")
        while self.tokens != []:
            if len(self.tokens) == 0:
                break
            if self.current().value == ";":
                node = self.current()
                child = ParseTree(node.node_type, node.value)
                tree.addChild(child)
                self.next()
                break
            elif self.current().value == "skip":
                tree.addChild(self.compileExpression())
            else:
                node = self.current()
                child = ParseTree(node.node_type, node.value)
                tree.addChild(child)
                prev_node = node
                self.next()
        return tree

    def compileSubIf(self):
        tree = ParseTree("ifStatement","")
        while self.tokens != []:
            if len(self.tokens) == 0:
                break
            if self.current().value == "else":
                node = self.current()
                child = ParseTree(node.node_type, node.value)
                tree.addChild(child)
                self.next()
                # tree.addChild(self.compileStatements())
                # break
            elif self.current().value == "skip":
                tree.addChild(self.compileExpression())
            elif self.current().value == "}" and prev_node.value == "{":
                # print(len(self.tokens))
                tree.addChild(self.compileStatements())
                node = self.current()
                child = ParseTree(node.node_type, node.value)
                tree.addChild(child)
                if len(self.tokens) == 1:
                    break
                self.next()
                # break
            else:
                node = self.current()
                child = ParseTree(node.node_type, node.value)
                tree.addChild(child)
                prev_node = node
                self.next()
            # print("PASS: ", self.current().value)

    def compileIf(self):
        """
        Generates a parse tree for an if statement
        @return a ParseTree that represents the statement
        """
        tree = ParseTree("ifStatement","")
        while self.tokens != []:
            if len(self.tokens) == 0:
                break
            if self.current().value == "else":
                node = self.current()
                child = ParseTree(node.node_type, node.value)
                tree.addChild(child)
                prev_node = node
                self.next()
                # tree.addChild(self.compileStatements())
                # break
            elif self.current().value == "skip":
                tree.addChild(self.compileExpression())
            elif self.current().value == "if":
                tree.addChild(self.compileSubIf())  
            elif self.current().value == "}" and prev_node.value == "{":
                # print(len(self.tokens))
                tree.addChild(self.compileStatements())
                node = self.current()
                child = ParseTree(node.node_type, node.value)
                tree.addChild(child)
                if len(self.tokens) == 1:
                    break
                prev_node = node
                self.next()
                # break
            else:
                node = self.current()
                child = ParseTree(node.node_type, node.value)
                tree.addChild(child)
                prev_node = node
                self.next()
            # print("PASS: ", self.current().value)
        return tree

    
    def compileWhile(self):
        """
        Generates a parse tree for a while statement
        @return a ParseTree that represents the statement
        """
        tree = ParseTree("whileStatement","")
        while self.tokens != []:
            if len(self.tokens) == 0:
                break
            if self.current().value == "skip":
                tree.addChild(self.compileExpression())
            else:
                node = self.current()
                child = ParseTree(node.node_type, node.value)
                tree.addChild(child)
                prev_node = node
                self.next()
        return tree


    def compileDo(self):
        """
        Generates a parse tree for a do statement
        @return a ParseTree that represents the statement
        """
        tree = ParseTree("doStatement","")
        while self.tokens != []:
            if self.current().value == ";":
                node = self.current()
                child = ParseTree(node.node_type, node.value)
                tree.addChild(child)
                self.next()
                break
            elif self.current().value == "skip":
                tree.addChild(self.compileExpression())
            if len(self.tokens) == 0:
                break
            node = self.current()
            child = ParseTree(node.node_type, node.value)
            tree.addChild(child)
            prev_node = node
            self.next()
        return tree


    def compileReturn(self):
        """
        Generates a parse tree for a return statement
        @return a ParseTree that represents the statement
        """
        return None 


    def compileExpression(self):
        """
        Generates a parse tree for an expression
        @return a ParseTree that represents the expression
        """
        tree = ParseTree("expression","")
        node = self.current()
        child = ParseTree(node.node_type, node.value)
        tree.addChild(child)
        self.next()
        return tree


    def compileTerm(self):
        """
        Generates a parse tree for an expression term
        @return a ParseTree that represents the expression term
        """
        return None 


    def compileExpressionList(self):
        """
        Generates a parse tree for an expression list
        @return a ParseTree that represents the expression list
        """
        return None 


    def next(self):
        """
        Advance to the next token
        """
        if len(self.tokens) != 0:
            self.tokens.pop(0)
        return


    def current(self):
        """
        Return the current token
        @return the token
        """
        return self.tokens[0]


    def have(self,expectedType,expectedValue):
        """
        Check if the current token matches the expected type and value.
        @return True if a match, False otherwise
        """
        if self.pos == len(self.tokens)-1:
            return False
        if self.tokens[self.pos].type == expectedType and self.tokens[self.pos].value == expectedValue:
            return True
        return False


    def mustBe(self,expectedType,expectedValue):
        """
        Check if the current token matches the expected type and value.
        If so, advance to the next token, returning the current token, otherwise throw/raise a ParseException.
        @return token that was current prior to advancing.
        """
        
        return None
    

if __name__ == "__main__":


    """ 
    Tokens for:
        class MyClass {
        
        }
    """
    tokens = []

    # if ( skip ) { if ( skip ) { } else { } } else { if ( skip ) { } else { } }
    tokens.append(Token("keyword","if"))
    tokens.append(Token("symbol","("))
    tokens.append(Token("keyword","skip"))
    tokens.append(Token("symbol",")"))
    tokens.append(Token("symbol","{"))
    tokens.append(Token("keyword","if"))
    tokens.append(Token("symbol","("))
    tokens.append(Token("keyword","skip"))
    tokens.append(Token("symbol",")"))
    tokens.append(Token("symbol","{"))
    tokens.append(Token("symbol","}"))
    tokens.append(Token("keyword","else"))
    tokens.append(Token("symbol","{"))
    tokens.append(Token("symbol","}"))
    tokens.append(Token("symbol","}"))
    tokens.append(Token("keyword","else"))
    tokens.append(Token("symbol","{"))
    tokens.append(Token("keyword","if"))
    tokens.append(Token("symbol","("))
    tokens.append(Token("keyword","skip"))
    tokens.append(Token("symbol",")"))
    tokens.append(Token("symbol","{"))
    tokens.append(Token("symbol","}"))
    tokens.append(Token("keyword","else"))
    tokens.append(Token("symbol","{"))
    tokens.append(Token("symbol","}"))
    tokens.append(Token("symbol","}"))
    
    parser = CompilerParser(tokens)
    try:
        result = parser.compileIf()
        print(result)
    except ParseException:
        print("Error Parsing!")
