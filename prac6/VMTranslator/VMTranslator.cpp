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
    string asm_code = "@" + to_string(offset) + "\n" + "D=A\n";  
    
    if (segment != "constant") {
        string seg_base_addr = "";
        if (segment == "local") seg_base_addr = "LCL";
        else if (segment == "argument") seg_base_addr = "ARG";
        else if (segment == "this") seg_base_addr = "THIS";
        else if (segment == "that") seg_base_addr = "THAT";
        else if (segment == "temp") seg_base_addr = "R5";
        else if (segment == "pointer") seg_base_addr = "R3";
        else if (segment == "static") seg_base_addr = "R16";

        asm_code += "@" + seg_base_addr + "\n" + "A=M+D\n" + "D=M\n";  
    }
    
    asm_code += "@SP\nA=M\nM=D\n@SP\nM=M+1\n";

    return asm_code;
}

/** Generate Hack Assembly code for a VM pop operation */
string VMTranslator::vm_pop(string segment, int offset) {
    string asm_code;
    
    string seg_base_addr;
    if (segment == "local") seg_base_addr = "LCL";
    else if (segment == "argument") seg_base_addr = "ARG";
    else if (segment == "this") seg_base_addr = "THIS";
    else if (segment == "that") seg_base_addr = "THAT";
    else if (segment == "temp") seg_base_addr = "R5";
    else if (segment == "pointer") seg_base_addr = "R3";
    else if (segment == "static") seg_base_addr = "R16";
    
    // Calculate the target address
    asm_code = "@" + to_string(offset) + "\nD=A\n";
    asm_code += "@" + seg_base_addr + "\nA=M+D\nD=A\n";
    asm_code += "@R13\nM=D\n";

    // Pop from stack into D
    asm_code += "@SP\nAM=M-1\nD=M\n";

    // Store D into the target address
    asm_code += "@R13\nA=M\nM=D\n";

    return asm_code;
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
    return "";
}

/** Generate Hack Assembly code for a VM call operation */
string VMTranslator::vm_call(string function_name, int n_args){
    return "";
}

/** Generate Hack Assembly code for a VM return operation */
string VMTranslator::vm_return(){
    return "";
}