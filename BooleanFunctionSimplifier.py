def generateVariables(lgth):
    alp = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return alp[:lgth]

def produceCombination(lgth):
    combList = []
    ini = "0"*lgth
    combList.append(ini);
    n=0
    while ini!="1"*lgth:
        n1=n
        ini = ""
        for i in range(lgth):
            ini = str(n1%2) + ini
            n1 = n1//2
        n=n+1
        combList.append(ini)
    return combList
def produceCombinationFromMinterms(minterms,n):
    comb=[]
    for i in minterms:
        st = ""
        for j in range(n):
            st = str(i%2) + st
            i//=2
        comb.append(st)
    return comb
def genCombWithoutIndex(comb,indexToOmit):
    toReturnList = []
    for j in comb:
        toBeAdded = ""
        for k in range(len(j)):
            if(k==indexToOmit):
                continue
            toBeAdded = toBeAdded + j[k]
        toReturnList.append(toBeAdded)
    return toReturnList

def generateKey(mainIndices,indexToOmit):
    str1 = ""
    for i in mainIndices:
        if(i==indexToOmit):
            continue
        str1 = str1+str(i)
    return str1

def attack(mainIndices,comb):
    comb = list(set(comb))
    dict1 = {}
    AffectedCombIndices = []
    NonAffectedComb = []
    length = len(comb[0])-1
    combList = produceCombination(length)

    for i in range(length+1):
        indexToOmit = mainIndices[i]
        key = generateKey(mainIndices,indexToOmit)
        toAddList = []
        gcwithoutIndex = genCombWithoutIndex(comb,i)
        for j in combList:
            count = 0
            h=0
            indices = []
            for k in gcwithoutIndex:
                if k==j:
                    indices.append(h)
                    count=count+1
                h=h+1
            
            if count==2:
                toAddList.append(j)
                AffectedCombIndices = AffectedCombIndices + indices
        
        toAddList = list(set(toAddList))
        dict1[key] = toAddList
    for i in range(len(comb)):
        if i not in AffectedCombIndices:
            NonAffectedComb.append(comb[i])
    removeKeys = []
    for i in dict1:
        if dict1[i]==[]:
            removeKeys.append(i)
    for i in removeKeys:
        del dict1[i]
    return dict1,{mainIndices:NonAffectedComb}

def simplifier(comb):
    if(comb==[]):
        return None
    #comb = comb+dontCare
    nonAffected = {}
    lgth = len(comb[0])
    variables = generateVariables(lgth)
    dict11 = {variables:comb}

    while dict11!={} and len(list(dict11.keys())[0])!=0:
        newDict = {}
        for i in dict11:
            tup = attack(i,dict11[i])
            tupDict = tup[0]
            for j in tupDict:
                if j in newDict:
                    lst = newDict[j]
                    lst = list(set(lst+tupDict[j]))
                    newDict[j] = lst
                else:
                    newDict[j] = tupDict[j]
            tupNonAffected = tup[1]
##            for j in tupNonAffected:
##                for k in tupNonAffected[j]:
##                    if k in dontCare:
##                        tupNonAffected[j].remove(k)
                    
            #print(tupNonAffected)
            for j in tupNonAffected:
                if j in nonAffected:
                    lst = nonAffected[j]
                    lst = list(set(lst+tupNonAffected[j]))
                    nonAffected[j] = lst
                else:
                    nonAffected[j] = tupNonAffected[j]
        
        dict11 = newDict


    removeKeys = []
    for i in nonAffected:
        if nonAffected[i]==[]:
            removeKeys.append(i)
    for i in removeKeys:
        del nonAffected[i]

    return nonAffected

def extractReadable(nonAffected):
    if(nonAffected==None):
        print(0)
    elif(nonAffected=={}):
        print(1)
    else:
        exp = ""
        for i in nonAffected:
            values = nonAffected[i]
            for j in values:
                for k in range(len(j)):

                    if(j[k]=="0"):
                        exp+=i[k]+"n"
                    elif(j[k]=="1"):
                        exp+=i[k]
                exp+=" + "
        print(exp[:-3])

#comb = ["0000","0001","0100","0101","1100","1000","0010","1101","1001"]
#comb = ["0011","0010","0100","0101","1111","1110","1000","1001"]
#comb = ["000","001","010","011","100","101","110","111"]
#comb=["0","1"]
#comb=[]

comb = produceCombinationFromMinterms([2,4,5,6,7,12,13,15,112],7)
#dontCare = produceCombinationFromMinterms([10,11,12,13,14,15],4)
nonAffected =  simplifier(comb)
print(nonAffected)
extractReadable(nonAffected)
    



