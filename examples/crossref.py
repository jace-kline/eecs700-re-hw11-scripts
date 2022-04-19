## ###
#  IP: GHIDRA
# 
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  
#       http://www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
##
# Example: Use cross-references to list all callee function in 'main'
# @category: EECS700

# Get the current program's function names
listing = currentProgram.getListing()
function = getFirstFunction()

while function is not None:
    name = function.getName()

    # Find the main function
    if (name is not None and name == "main"):
        insIter = listing.getInstructions(function.getBody(), True)
        while(insIter.hasNext()):
            ins = insIter.next()
            insAddr = ins.getMinAddress();
            insRefs = ins.getReferencesFrom()
            for ref in insRefs:
                refType = ref.getReferenceType().getName()
                if("CALL" in refType):
                    targetAddr = ref.getToAddress()
                    symbol = getSymbolAt(targetAddr)
                    if (symbol is not None):
                        symName = symbol.getName()
                        print("{} calls {} at 0x{}".format(name, symName, insAddr))

    function = getFunctionAfter(function)
print
