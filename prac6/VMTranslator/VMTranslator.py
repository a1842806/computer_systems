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
        ss_ASM = []
        ss_ASM.append("(" + function_name + ") // function " + function_name + " " + str(n_vars))
        for n in range(n_vars, 0, -1):
            ss_ASM.append("@SP")
            ss_ASM.append("AM=M+1")
            ss_ASM.append("A=A-1")
            ss_ASM.append("M=0")
        return "\n".join(ss_ASM) + "\n"

    def vm_call(function_name, n_args):
        ss_ASM = []
        ss_ASM.append("@return_address // call " + function_name + " " + str(n_args))
        ss_ASM.append("D=A")
        ss_ASM.append("@SP")
        ss_ASM.append("AM=M+1")
        ss_ASM.append("A=A-1")
        ss_ASM.append("M=D")

        for register in ["LCL", "ARG", "THIS", "THAT"]:
            ss_ASM.append("@" + register)
            ss_ASM.append("D=M")
            ss_ASM.append("@SP")
            ss_ASM.append("AM=M+1")
            ss_ASM.append("A=A-1")
            ss_ASM.append("M=D")

        ss_ASM.append("@SP")
        ss_ASM.append("D=M")
        ss_ASM.append("@5")
        ss_ASM.append("D=D-A")
        ss_ASM.append("@" + str(n_args))
        ss_ASM.append("D=D-A")
        ss_ASM.append("@ARG")
        ss_ASM.append("M=D")

        ss_ASM.append("@SP")
        ss_ASM.append("D=M")
        ss_ASM.append("@LCL")
        ss_ASM.append("M=D")

        ss_ASM.append("@funcName")
        ss_ASM.append("0;JMP")

        ss_ASM.append("(return_address)")
        
        return "\n".join(ss_ASM) + "\n"

    def vm_return():
        asm_code = []
        asm_code.append("@LCL // return")
        asm_code.append("D=M")
        asm_code.append("@R13")
        asm_code.append("M=D")

        asm_code.append("@R13")
        asm_code.append("D=M")
        asm_code.append("@5")
        asm_code.append("A=D-A")
        asm_code.append("D=M")
        asm_code.append("@R14")
        asm_code.append("M=D")

        asm_code.append("@SP")
        asm_code.append("AM=M-1")
        asm_code.append("D=M")
        asm_code.append("@ARG")
        asm_code.append("A=M")
        asm_code.append("M=D")

        asm_code.append("@ARG")
        asm_code.append("D=M+1")
        asm_code.append("@SP")
        asm_code.append("M=D")

        asm_code.append("@R13")
        asm_code.append("D=M")
        asm_code.append("@1")
        asm_code.append("A=D-A")
        asm_code.append("D=M")
        asm_code.append("@THAT")
        asm_code.append("M=D")

        asm_code.append("@R13")
        asm_code.append("D=M")
        asm_code.append("@2")
        asm_code.append("A=D-A")
        asm_code.append("D=M")
        asm_code.append("@THIS")
        asm_code.append("M=D")

        asm_code.append("@R13")
        asm_code.append("D=M")
        asm_code.append("@3")
        asm_code.append("A=D-A")
        asm_code.append("D=M")
        asm_code.append("@ARG")
        asm_code.append("M=D")

        asm_code.append("@R13")
        asm_code.append("D=M")
        asm_code.append("@4")
        asm_code.append("A=D-A")
        asm_code.append("D=M")
        asm_code.append("@LCL")
        asm_code.append("M=D")

        asm_code.append("@R14")
        asm_code.append("A=M")
        asm_code.append("0;JMP")

        return '\n'.join(asm_code) + "\n"


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

        