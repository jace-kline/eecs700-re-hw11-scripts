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
# Example: Enumerate and find basic information about functions
# @category: EECS700

# Get the current program's function names
function = getFirstFunction()
while function is not None:
    name = function.getName()
    startAddr = function.getBody().getMinAddress().getOffset()
    endAddr = function.getBody().getMaxAddress().getOffset()
    print "Function: %s, Start Address: 0x%x, End Address: 0x%x\n" % (name, startAddr, endAddr)

    # Print stack information
    sFrame = function.getStackFrame()
    pSize = sFrame.getParameterSize()
    print "Function parameters take %d bytes\n" % (pSize)
    for pval in sFrame.getParameters():
        print "%s %s" % (pval.getDataType().getName(), pval.getName())

    sSize = sFrame.getLocalSize()
    print "Local variable take %d bytes\n" % (sSize)
    for lval in sFrame.getLocals():
        print "%s %s" % (lval.getDataType().getName(), lval.getName())
    
    function = getFunctionAfter(function)
print
