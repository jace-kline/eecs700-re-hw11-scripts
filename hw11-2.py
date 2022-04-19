#@author Jace Kline 2881618
#@category HW11
#@keybinding 
#@menupath 
#@toolbar 

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

def solve():

    listing = currentProgram.getListing()
    fs = [ f for f in get_function_list() if f.getName() is not None ]

    # initialize empty map (function name -> gadgets)
    _map = dict([ (f.getName(), []) for f in fs ])

    for f in fs:
        fname = f.getName()
        ins_iter = listing.getInstructions(f.getBody(), True)
        for ins in ins_iter:
            if ins.getMnemonicString() in gadget_terminators:
                gadget = backtrack_find_gadget(ins)
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
