#API: https://ghidra.re/ghidra_docs/api/ghidra/program/flatapi/FlatProgramAPI.html
#@author Jace Kline 2881618
#@category HW11
#@keybinding 
#@menupath 
#@toolbar 

# loaded variable: currentProgram

dangerous_fnames = ["atoi", "gets", "strcpy", "strcat", "sprintf"]

def get_function_list():
    fs = []
    f = getFirstFunction()
    while True:
        fs.append(f)
        f = getFunctionAfter(f)
        if bool(f) == False:
            break

    return fs


def get_calls():
    listing = currentProgram.getListing()
    fs = [ f for f in get_function_list() if f.getName() is not None ]

    calls = []
    for f in fs:
        fname = f.getName()
        ins_iter = listing.getInstructions(f.getBody(), True)
        for ins in ins_iter:
            ins_addr = ins.getMinAddress()
            ins_refs = ins.getReferencesFrom()
            for ref in ins_refs:
                ref_type = ref.getReferenceType().getName()
                if "CALL" in ref_type:
                    target_addr = ref.getToAddress()
                    sym = getSymbolAt(target_addr)
                    if sym is not None:
                        sym_name = sym.getName()
                        calls.append((fname, sym_name, ins_addr))

    return calls

def solve():
    _map = dict([ (name, []) for name in dangerous_fnames ])
    
    for (caller, callee, addr) in get_calls():
        if callee in dangerous_fnames and caller != callee:
            _map[callee].append((caller, addr))

    for (k, v) in _map.items():
        if len(v) > 0:
            print("Function {} is referenced from:".format(k))
            for (caller, addr) in v:
                print("{}:0x{}, ".format(caller, addr)),
            print

solve()



