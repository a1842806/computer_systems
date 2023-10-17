class VMTranslator:

    def vm_push(segment, offset):
        asm_code = "@" + str(offset) + "\n" + "D=A\n"

        if segment != "constant":
            seg_base_addr = ""
            if segment == "local": seg_base_addr = "LCL"
            elif segment == "argument": seg_base_addr = "ARG"
            elif segment == "this": seg_base_addr = "THIS"
            elif segment == "that": seg_base_addr = "THAT"
            elif segment == "temp": seg_base_addr = "R5"
            elif segment == "pointer": seg_base_addr = "R3"
            elif segment == "static": 
                asm_code = "@" + str(offset + 16) + "\n" + "D=M\n"
                asm_code += "@SP\nA=M\nM=D\n@SP\nM=M+1\n"
                return asm_code

            asm_code += "@" + seg_base_addr + "\n" + "A=M+D\n" + "D=M\n"

        asm_code += "@SP\nA=M\nM=D\n@SP\nM=M+1\n"

        return asm_code

    def vm_pop(segment, offset):
        asm_code = ""
        
        seg_base_addr = ""
        if segment == "local": seg_base_addr = "LCL"
        elif segment == "argument": seg_base_addr = "ARG"
        elif segment == "this": seg_base_addr = "THIS"
        elif segment == "that": seg_base_addr = "THAT"
        elif segment == "temp": seg_base_addr = "R5"
        elif segment == "pointer": seg_base_addr = "R3"
        elif segment == "static": 
            seg_base_addr = "R16"
            asm_code += "@SP\nAM=M-1\nD=M\n"
            asm_code += "@" + str(offset + 16) + "\nM=D\n"
            return asm_code
        
        # Calculate the target address
        asm_code += "@" + str(offset) + "\nD=A\n"
        asm_code += "@" + seg_base_addr + "\nA=M+D\nD=A\n"
        asm_code += "@R13\nM=D\n"

        # Pop from stack into D
        asm_code += "@SP\nAM=M-1\nD=M\n"

        # Store D into the target address
        asm_code += "@R13\nA=M\nM=D\n"

        return asm_code

    def vm_add():
        asm_code = "@SP\nAM=M-1\nD=M\nA=A-1\nM=M+D\n"
        return asm_code

    def vm_sub():
        asm_code = "@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n"
        return asm_code

    def vm_neg():
        asm_code = "@SP\nA=M-1\nM=-M\n"
        return asm_code

    def vm_eq():
        asm_code = f"@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n"  
        asm_code += f"@EQ\nD;JEQ\n"  
        asm_code += f"@SP\nA=M-1\nM=0\n"  
        asm_code += f"@EQ_END\n0;JMP\n"
        asm_code += f"(EQ)\n@SP\nA=M-1\nM=-1\n"  
        asm_code += f"(EQ_END)\n"
        return asm_code

    def vm_gt():
        asm_code = f"@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n"  
        asm_code += f"@GT\nD;JGT\n"  
        asm_code += f"@SP\nA=M-1\nM=0\n"  
        asm_code += f"@GT_END\n0;JMP\n"
        asm_code += f"(GT)\n@SP\nA=M-1\nM=-1\n"  
        asm_code += f"(GT_END)\n"
        return ""

    def vm_lt():
        asm_code = f"@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n"  
        asm_code += f"@LT\nD;JLT\n"  
        asm_code += f"@SP\nA=M-1\nM=0\n"  
        asm_code += f"@LT_END\n0;JMP\n"
        asm_code += f"(LT)\n@SP\nA=M-1\nM=-1\n"  
        asm_code += f"(LT_END)\n"
        return ""

    def vm_and():
        asm_code = "@SP\nAM=M-1\nD=M\nA=A-1\nM=M&D\n"
        return asm_code

    def vm_or():
        asm_code = "@SP\nAM=M-1\nD=M\nA=A-1\nM=M|D\n"
        return asm_code

    def vm_not():
        asm_code = "@SP\nAM=M-1\nM=!M\n"
        return asm_code

    def vm_label(label):
        asm_code = f"({label})\n"
        return asm_code

    def vm_goto(label):
        asm_code = f"@{label}\n0;JMP\n"
        return asm_code

    def vm_if(label):
        asm_code = "@SP\nAM=M-1\nD=M\n"
        asm_code += f"@{label}\nD;JNE\n"
        return asm_code

    def vm_function(function_name, n_vars):
        hackAssemblyElementList = []

        # generate Hack assembly code
        hackAssemblyElementList.append("(" + function_name +")")
        for _ in range(n_vars):
            hackAssemblyElementList.append('@SP')
            hackAssemblyElementList.append('AM=M+1')
            hackAssemblyElementList.append('A=A-1')
            hackAssemblyElementList.append('M=0')

        result = '\n'.join(hackAssemblyElementList)
        return result


    def vm_call(function_name, n_args):
        hackAssemblyElementList = []

        # generate Hack assembly code
        # push return address
        hackAssemblyElementList.append('@'+ function_name)
        hackAssemblyElementList.append('D=A')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('M=D')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M+1') 
        # push LCL
        hackAssemblyElementList.append('@LCL')
        hackAssemblyElementList.append('D=M')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('M=D')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M+1')
        # push ARG
        hackAssemblyElementList.append('@ARG')
        hackAssemblyElementList.append('D=M')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('M=D')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M+1')
        # push THIS
        hackAssemblyElementList.append('@THIS')
        hackAssemblyElementList.append('D=M')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('M=D')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M+1') 
        # push THAT
        hackAssemblyElementList.append('@THAT')
        hackAssemblyElementList.append('D=M')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('A=M')
        hackAssemblyElementList.append('M=D')
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('M=M+1')
        # ARG = SP - 5 - number of arguments
        hackAssemblyElementList.append('D=M')
        hackAssemblyElementList.append("@" + str(5+n_args))
        hackAssemblyElementList.append('D=D-A')    
        hackAssemblyElementList.append('@ARG')
        hackAssemblyElementList.append('M=D')
        # LCL = SP
        hackAssemblyElementList.append('@SP')
        hackAssemblyElementList.append('D=M')
        hackAssemblyElementList.append('@LCL')
        hackAssemblyElementList.append('M=D')
        # goto function_name
        hackAssemblyElementList.append('@' + function_name)
        hackAssemblyElementList.append('0;JMP')
        # (return address)
        hackAssemblyElementList.append('('+ function_name + ')')
        result = '\n'.join(hackAssemblyElementList)
        return result

    def vm_return():
        hackAssemblyElementList = []

        # generate Hack assembly code
        # endFrame = LCL // endFrame is a temporary variable
        hackAssemblyElementList.append("@LCL")
        hackAssemblyElementList.append("D=M")
        hackAssemblyElementList.append("@frame")
        hackAssemblyElementList.append("M=D")
        # retAddr = *(endFrame - 5) // gets the return address
        hackAssemblyElementList.append("@5")
        hackAssemblyElementList.append('D=D-A')
        hackAssemblyElementList.append('A=D')
        hackAssemblyElementList.append("D=M")
        hackAssemblyElementList.append("@return")
        hackAssemblyElementList.append("M=D")
        # *ARG = pop()  // repositions the return value for the caller
        hackAssemblyElementList.append("@SP")
        hackAssemblyElementList.append("M=M-1")
        hackAssemblyElementList.append("A=M")
        hackAssemblyElementList.append("D=M")
        hackAssemblyElementList.append("@ARG")
        hackAssemblyElementList.append("A=M")
        hackAssemblyElementList.append("M=D")
        # SP = ARG + 1 // repositions SP of the caller
        hackAssemblyElementList.append("@ARG")
        hackAssemblyElementList.append("D=M+1")
        hackAssemblyElementList.append("@SP")
        hackAssemblyElementList.append("M=D")
        # THAT = *(endFrame - 1) // restores THAT of the caller
        hackAssemblyElementList.append("@frame")
        hackAssemblyElementList.append("D=M")
        hackAssemblyElementList.append("@1")
        hackAssemblyElementList.append('D=D-A')
        #hackAssemblyElementList.append('D=D-1')
        hackAssemblyElementList.append('A=D')
        hackAssemblyElementList.append("D=M")
        hackAssemblyElementList.append("@THAT")
        hackAssemblyElementList.append("M=D")
        # THIS = *(endFrame - 2) // restores THIS of the caller
        hackAssemblyElementList.append("@frame")
        hackAssemblyElementList.append("D=M")
        hackAssemblyElementList.append("@2")
        hackAssemblyElementList.append('D=D-A')        
        hackAssemblyElementList.append('A=D')
        hackAssemblyElementList.append("D=M")
        hackAssemblyElementList.append("@THIS")
        hackAssemblyElementList.append("M=D")
        # ARG = *(endFrame - 3) // restores ARG of the caller
        hackAssemblyElementList.append("@frame")
        hackAssemblyElementList.append("D=M")
        hackAssemblyElementList.append("@3")
        hackAssemblyElementList.append('D=D-A')            
        hackAssemblyElementList.append('A=D')
        hackAssemblyElementList.append("D=M")
        hackAssemblyElementList.append("@ARG")
        hackAssemblyElementList.append("M=D")
        # LCL = *(endFrame - 4) // restores LCL of the caller
        hackAssemblyElementList.append("@frame")
        hackAssemblyElementList.append("D=M")
        hackAssemblyElementList.append("@4")
        hackAssemblyElementList.append('D=D-A')            
        hackAssemblyElementList.append('A=D')
        hackAssemblyElementList.append("D=M")
        hackAssemblyElementList.append("@LCL")
        hackAssemblyElementList.append("M=D")        
        # goto retAddr // goes to return address in the caller's code
        hackAssemblyElementList.append("@return")
        hackAssemblyElementList.append("A=M")
        hackAssemblyElementList.append("0;JMP")
        result = '\n'.join(hackAssemblyElementList)
        return result

# A quick-and-dirty parser when run as a standalone script.
if __name__ == "__main__":
    import sys

    if(len(sys.argv) > 1):
        with open(sys.argv[1], "r") as a_file:
            for line in a_file:
                tokens = line.strip().lower().split()
                if(len(tokens)==1):
                    if(tokens[0]=='add'):
                        print(VMTranslator.vm_add())
                    elif(tokens[0]=='sub'):
                        print(VMTranslator.vm_sub())
                    elif(tokens[0]=='neg'):
                        print(VMTranslator.vm_neg())
                    elif(tokens[0]=='eq'):
                        print(VMTranslator.vm_eq())
                    elif(tokens[0]=='gt'):
                        print(VMTranslator.vm_gt())
                    elif(tokens[0]=='lt'):
                        print(VMTranslator.vm_lt())
                    elif(tokens[0]=='and'):
                        print(VMTranslator.vm_and())
                    elif(tokens[0]=='or'):
                        print(VMTranslator.vm_or())
                    elif(tokens[0]=='not'):
                        print(VMTranslator.vm_not())
                    elif(tokens[0]=='return'):
                        print(VMTranslator.vm_return())
                elif(len(tokens)==2):
                    if(tokens[0]=='label'):
                        print(VMTranslator.vm_label(tokens[1]))
                    elif(tokens[0]=='goto'):
                        print(VMTranslator.vm_goto(tokens[1]))
                    elif(tokens[0]=='if-goto'):
                        print(VMTranslator.vm_if(tokens[1]))
                elif(len(tokens)==3):
                    if(tokens[0]=='push'):
                        print(VMTranslator.vm_push(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='pop'):
                        print(VMTranslator.vm_pop(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='function'):
                        print(VMTranslator.vm_function(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='call'):
                        print(VMTranslator.vm_call(tokens[1],int(tokens[2])))