#@author Jace Kline 2881618
#@category HW11
#@keybinding 
#@menupath 
#@toolbar

from ghidra.program.model.lang import OperandType

gadget_instrs = ["NOP", "POP", "PUSH", "MOV", "ADD", "SUB", "MUL", "DIV", "XOR"]
gadget_terminators = ["RET", "JMP", "CALL"]

def get_function_list():
    fs = []
    f = getFirstFunction()
    while True:
        fs.append(f)
        f = getFunctionAfter(f)
        if bool(f) == False:
            break

    return fs

# given a gadget terminator instruction, backtrack to find entire gadget
def backtrack_find_gadget(ins):
    gadget = [ins]
    ins_backtracker = ins.getPrevious()
    while bool(ins_backtracker):
        if ins_backtracker.getMnemonicString() in gadget_instrs:
            gadget = [ins_backtracker] + gadget
            ins_backtracker = ins_backtracker.getPrevious()
        else:
            break
    return gadget

def is_valid_terminator(ins):
    # get the string representation of the instruction: "CALL", "JMP", "RET"
    repr = ins.getMnemonicString()
    if repr in gadget_terminators:
        # if "RET", 0 operands -> True
        if repr == "RET":
            return True
        # if "CALL" or "JMP", check operand
        else:
            # get the first operand of the instruction
            # return true if it is a register
            op_type = OperandType()
            op_int = ins.getOperandType(0)
            return op_type.isRegister(op_int)
    
    return False

def solve():
    listing = currentProgram.getListing()
    fs = [ f for f in get_function_list() if f.getName() is not None ]

    # initialize empty map (function name -> gadgets)
    _map = dict([ (f.getName(), []) for f in fs ])

    for f in fs:
        fname = f.getName()
        ins_iter = listing.getInstructions(f.getBody(), True)
        for ins in ins_iter:
            if is_valid_terminator(ins):
                # backtrack from terminator to collect gadget instruction sequence
                gadget = backtrack_find_gadget(ins)
                # if the gadget is greater than 1 instruction, add to map
                if len(gadget) > 1:
                    _map[fname].append(gadget)

    for (fname, gadgets) in _map.items():
        if len(gadgets) > 0:
            print("ROP Gadgets in Function: {}".format(fname))
            for gadget in gadgets:
                print("Gadget is: "),
                for ins in gadget:
                    print("\"{}\", ".format(ins.toString())),
                print

solve()
