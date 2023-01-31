import csv
import pandas as pd
import math

instructions=pd.read_csv("RISC-V_Instructions.csv") #read in all of the instruction info into a pd dataframe
registers=pd.read_csv("Registers.csv") #read in register name conversions into a pd dataframe
testCases=pd.read_csv("Lab3_unit_tests.csv", sep="|") #read in test cases into a pd dataframe
digits=["-","0","1","2","3","4","5","6","7","8","9"] #this list will be used to scan for immediate values

def decimalToTwos(decimalString, bits): #converts decimal value to 12 bit two's complement
    decimal=int(decimalString)
    if decimal>=0: #if the immediate is greater than 0, simply convert to binary and pad 0's
        binary=bin(decimal).split("0b")[1].zfill(bits)
        return binary
    else: #if immediate is less than 0, do conversion math
        actualBits=math.ceil(math.log2(-1*decimal))+1 #accounting for bit overflow if too large of an immediate is given
        if actualBits>bits:
            binary=bin(-1*decimal-2**actualBits).split("0b")[1][-bits:] #incorporates invert bits, add 1 method to multiply by -1 in two's complement
        else:
            binary=bin(-1*decimal-2**bits).split("0b")[1].zfill(bits) #incorporates invert bits, add 1 method to multiply by -1 in two's complement
        return binary
def getInput(): #gets instruction input from the user
    userInput=input("Enter an Instruction: ")
    if(userInput=="quit"):
        print("\n--Program Finished--")
        return userInput, False
    else:
        return userInput, True
def registerConversion(value): #converts register ABI to base names if possible
    row=registers.loc[registers["name"]==value]
    try:
        x=row['actual'].iloc[0]
        return x
    except IndexError:
        return value
def inputParsing(instruction): #parses the input into something that can easily be worked with
    parsedInput=instruction.split()
    for i in range(len(parsedInput)):
        parsedInput[i]=parsedInput[i].replace(",","")
    if(len(parsedInput)==3): #takes care of case where you have an offset of a memory address
        for i in range(len(parsedInput[2])):
            if(parsedInput[2][i]=='('):
                parsedInput.append(parsedInput[2][0:i])
                parsedInput[2]=parsedInput[2][i+1:-1]
                break
    for i in range(len(parsedInput)): # convert ABI to base
        replaceValue=registerConversion(parsedInput[i])
        parsedInput[i]=replaceValue
    return parsedInput
def createBinaryValues(parsedInput):
    isDecimal=True
    for digit in parsedInput[-1]: #check if there is an immediate value in the instruction
        if digit not in digits:
            isDecimal=False
            break
    if isDecimal: #if there is an immediate value given, convert it to 12 bit two's complement
        if instructions.loc[instructions["name"]==parsedInput[0]]["type"].iloc[0]==("U"):
            parsedInput[-1]=decimalToTwos(parsedInput[-1],32)
        elif instructions.loc[instructions["name"]==parsedInput[0]]["type"].iloc[0]==("J"):
            parsedInput[-1]=decimalToTwos(parsedInput[-1],20)
        else:
            parsedInput[-1]=decimalToTwos(parsedInput[-1],12)
    for i in range(1,len(parsedInput)): #convert register names to corresponding 5 bit binary numbers
        if (parsedInput[i][0]=="x"):
            parsedInput[i]=bin(int(parsedInput[i][1:]))[2:].zfill(5)
    instructionType=instructions.loc[instructions["name"]==parsedInput[0]]["type"].iloc[0] #keeps track of instruction type so we know how to format binary string
    opcode=str(instructions.loc[instructions["name"]==parsedInput[0]]["Opcode"].iloc[0]).zfill(7) #converting instruction into opcode
    funct3=str(instructions.loc[instructions["name"]==parsedInput[0]]["funct3"].iloc[0]).zfill(3) #capturing funct3 binary string
    funct7=str(instructions.loc[instructions["name"]==parsedInput[0]]["funct7"].iloc[0]).zfill(7) #capturing funct7 binary string
    return instructionType, opcode, funct3, funct7
def createOutput(parsedInput, instructionType, opcode, funct3, funct7):
    outputString=""
    if instructionType=="R": #putting together R-type binary string
        outputString+=funct7+parsedInput[3]+parsedInput[2]+funct3+parsedInput[1]+opcode
    elif instructionType=="I": #putting together I-type binary string
        outputString+=parsedInput[-1]+parsedInput[2]+funct3+parsedInput[1]+opcode 
    elif instructionType=="S": #putting together S-type binary string
        outputString+=parsedInput[-1][:7]+parsedInput[1]+parsedInput[2]+funct3+parsedInput[-1][7:]+opcode
    elif instructionType=="U": #putting together U-type binary string
        outputString+=parsedInput[-1][12:]+parsedInput[1]+opcode
    elif instructionType=="J": #putting together J-type binary string
        outputString+=parsedInput[-1][0]+parsedInput[-1][10:]+parsedInput[-1][9]+parsedInput[-1][1:9]+parsedInput[1]+opcode
    elif instructionType=="B": #putting together SB-type binary string
        outputString+=parsedInput[-1][0]+parsedInput[-1][2:8]+parsedInput[2]+parsedInput[1]+funct3+parsedInput[-1][8:]+parsedInput[-1][1]+opcode
    else:
        outputString="working on it"
    return outputString
def testingFunction(): #function that tests all of the given tests
    correctCount=0
    incorrectCount=0
    answer=""
    for i in range (testCases.shape[0]):
        userInput=testCases.iat[i,0] #this string will contain each instruction
        print(f'Instruction: {userInput}')
        desiredOutput=testCases.iat[i,1] #this is the expected binary string for each instruction
        if userInput=="ecall": #hard coding in ecall edge case
            answer="00000000000000000000000001110011"
        elif userInput=="ebreak": #hard coding in ebreak edge case
            answer="00000000000100000000000001110011"
        if answer=="": #if input given was not ecall or ebreak, convert from instruction to binary
            try:
                parsedInput=inputParsing(userInput) #cleans up instruction given to remove commas, spaces, parentheses, etc.
                [instructionType, opcode, funct3, funct7]=createBinaryValues(parsedInput) #generates relevant binary values so we can create our binary instruction
                answer=createOutput(parsedInput, instructionType, opcode, funct3, funct7) #pieces together binary strings to create a contiguous binary instruction
            except: #if there is an error in converting to binary, mention that to the user
                answer="Unrecognized instruction"
        print(f'Expected binary string: {desiredOutput}')
        print(f'My binary string:       {answer}')
        if desiredOutput==answer: #if our conversion was correct, note that
            print(f'Test {i+1} passed')
            correctCount+=1
        else: #if our conversion was incorrect, note that
            print(f'Test {i+1} failed (type {instructionType})')
            print(f'Expected {desiredOutput}')
            print(f'Got      {answer}')
        answer="" #here to make sure an ebreak/ecall won't make all the tests after fail
    print(f'\n{correctCount}/{testCases.shape[0]} test cases passed ({(correctCount*100/testCases.shape[0]):.2f}%)') #print statistics about the test cases

#testingFunction() #uncomment this line if you would like to see my program run against all of the test cases
while True:
    userInput=getInput()
    if userInput[1] is False:
        break
    if userInput[0]=="ecall": #hard coding in ecall edge case
        print('00000000000000000000000001110011')
        continue
    elif userInput[0]=="ebreak": #hard coding in ebreak edge case
        print('00000000000100000000000001110011')
        continue
    try:
        parsedInput=inputParsing(userInput[0])
        [instructionType, opcode, funct3, funct7]=createBinaryValues(parsedInput)
        print(f'Result: {createOutput(parsedInput, instructionType, opcode, funct3, funct7)}')
    except:
        print("Unrecognized Instruction")
        continue