#include <string>

#include "VMTranslator.h"

using namespace std;

/**
 * VMTranslator constructor
 */
VMTranslator::VMTranslator() {
    // Your code here
}

/**
 * VMTranslator destructor
 */
VMTranslator::~VMTranslator() {
    // Your code here
}

/** Generate Hack Assembly code for a VM push operation */
string VMTranslator::vm_push(string segment, int offset){
    return "";
}

/** Generate Hack Assembly code for a VM pop operation */
string VMTranslator::vm_pop(string segment, int offset){    
    return "";
}

/** Generate Hack Assembly code for a VM add operation */
string VMTranslator::vm_add(){
    return "";
}

/** Generate Hack Assembly code for a VM sub operation */
string VMTranslator::vm_sub(){
    return "";
}

/** Generate Hack Assembly code for a VM neg operation */
string VMTranslator::vm_neg(){
    return "";
}

/** Generate Hack Assembly code for a VM eq operation */
string VMTranslator::vm_eq(){
    return "";
}

/** Generate Hack Assembly code for a VM gt operation */
string VMTranslator::vm_gt(){
    return "";
}

/** Generate Hack Assembly code for a VM lt operation */
string VMTranslator::vm_lt(){
    return "";
}

/** Generate Hack Assembly code for a VM and operation */
string VMTranslator::vm_and(){
    return "";
}

/** Generate Hack Assembly code for a VM or operation */
string VMTranslator::vm_or(){
    return "";
}

/** Generate Hack Assembly code for a VM not operation */
string VMTranslator::vm_not(){
    return "";
}

/** Generate Hack Assembly code for a VM label operation */
string VMTranslator::vm_label(string label){
    return "";
}

/** Generate Hack Assembly code for a VM goto operation */
string VMTranslator::vm_goto(string label){
    return "";
}

/** Generate Hack Assembly code for a VM if-goto operation */
string VMTranslator::vm_if(string label){
    return "";
}

/** Generate Hack Assembly code for a VM function operation */
string VMTranslator::vm_function(string function_name, int n_vars){
    string asm_code = "";

    asm_code += "(" + function_name + ") // function " + function_name + " " + to_string(n_vars) + "\n";
    for (int n = n_vars; n > 0; n--)
    {
        asm_code += "@SP\n";
        asm_code += "AM=M+1\n";
        asm_code += "A=A-1\n";
        asm_code += "M=0\n";
    }
    return asm_code;

}

/** Generate Hack Assembly code for a VM call operation */
string VMTranslator::vm_call(string function_name, int n_args){
    string asm_code = "";

    asm_code += "@return_address // call " + function_name + " " + to_string(n_args) + "\n";
    asm_code += "D=A\n";
    asm_code += "@SP\n";
    asm_code += "AM=M+1\n";
    asm_code += "A=A-1\n";
    asm_code += "M=D\n";

    asm_code += "@LCL\n";
    asm_code += "D=M\n";
    asm_code += "@SP\n";
    asm_code += "AM=M+1\n";
    asm_code += "A=A-1\n";
    asm_code += "M=D\n";

    asm_code += "@ARG\n";
    asm_code += "D=M\n";
    asm_code += "@SP\n";
    asm_code += "AM=M+1\n";
    asm_code += "A=A-1\n";
    asm_code += "M=D\n";

    asm_code += "@THIS\n";
    asm_code += "D=M\n";
    asm_code += "@SP\n";
    asm_code += "AM=M+1\n";
    asm_code += "A=A-1\n";
    asm_code += "M=D\n";

    asm_code += "@THAT\n";
    asm_code += "D=M\n";
    asm_code += "@SP\n";
    asm_code += "AM=M+1\n";
    asm_code += "A=A-1\n";
    asm_code += "M=D\n";

    asm_code += "@SP\n";
    asm_code += "D=M\n";
    asm_code += "@5\n";
    asm_code += "D=D-A\n";
    asm_code += "@" + to_string(n_args) + "\n";
    asm_code += "D=D-A\n";
    asm_code += "@ARG\n";
    asm_code += "M=D\n";

    asm_code += "@SP\n";
    asm_code += "D=M\n";
    asm_code += "@LCL\n";
    asm_code += "M=D\n";

    asm_code += "@funcName\n";
    asm_code += "0;JMP\n";

    asm_code += "(return_address)\n";

    return asm_code;
}

/** Generate Hack Assembly code for a VM return operation */
string VMTranslator::vm_return() {
    string asm_code = "";

    asm_code += "@LCL\n";
    asm_code += "D=M\n";
    asm_code += "@R13\n";
    asm_code += "M=D\n";

    asm_code += "@R13\n";
    asm_code += "D=M\n";
    asm_code += "@5\n";
    asm_code += "A=D-A\n";
    asm_code += "D=M\n";
    asm_code += "@R14\n";
    asm_code += "M=D\n";

    asm_code += "@SP\n";
    asm_code += "AM=M-1\n";
    asm_code += "D=M\n";
    asm_code += "@ARG\n";
    asm_code += "A=M\n";
    asm_code += "M=D\n";

    asm_code += "@ARG\n";
    asm_code += "D=M+1\n";
    asm_code += "@SP\n";
    asm_code += "M=D\n";

    asm_code += "@R13\n";
    asm_code += "D=M\n";
    asm_code += "@1\n";
    asm_code += "A=D-A\n";
    asm_code += "D=M\n";
    asm_code += "@THAT\n";
    asm_code += "M=D\n";

    asm_code += "@R13\n";
    asm_code += "D=M\n";
    asm_code += "@2\n";
    asm_code += "A=D-A\n";
    asm_code += "D=M\n";
    asm_code += "@THIS\n";
    asm_code += "M=D\n";

    asm_code += "@R13\n";
    asm_code += "D=M\n";
    asm_code += "@3\n";
    asm_code += "A=D-A\n";
    asm_code += "D=M\n";
    asm_code += "@ARG\n";
    asm_code += "M=D\n";

    asm_code += "@R13\n";
    asm_code += "D=M\n";
    asm_code += "@4\n";
    asm_code += "A=D-A\n";
    asm_code += "D=M\n";
    asm_code += "@LCL\n";
    asm_code += "M=D\n";

    asm_code += "@R14\n";
    asm_code += "A=M\n";
    asm_code += "0;JMP\n";

    return asm_code + "\n";
}
