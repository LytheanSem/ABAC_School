class Register:
    def __init__(self, value, register_address):
        self.register_address = register_address
        self.value = value

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def __str__(self):
        return "{}  {}  [{}]".format(self.register_address, self.value, self.valueto16bit())

    def valueto16bit(self):
        binary_value = bin(self.value)[2:]
        return binary_value.zfill(16)

    def addressto3bit(self):
        address_map = {"r0": "000", "r1": "001", "r2": "010", "r3": "011", "r4": "100", "r5": "101", "r6": "110", "r7": "111"}
        return address_map.get(self.register_address, "")

class Instruction:
    def __init__(self, step, opcode, register, clock_cycle):
        self.step = step
        self.opcode = opcode
        self.register = register
        self.operand2 = ""
        self.value = register.get_value()
        self.clock_cycle = clock_cycle

    def opcode5bit(self):
        opcode_map = {"mov": "00001", "add": "00010", "mul": "00100", "sub": "00011", "div": "00101"}
        return opcode_map.get(self.opcode, "")

    def valueto16bit(self):
        binary_value = bin(self.value)[2:]
        return binary_value.zfill(16)

    def __str__(self):
        if self.operand2 == "":
            return "[{}]  {:<5}{}    {:<4}  :  {:<35}  {:<5}".format(self.step, self.opcode, self.register.register_address, self.value, self.opcode5bit() + " " + self.register.addressto3bit() + " " + self.valueto16bit(), self.clock_cycle)
        else:
            return "[{}]  {:<5}{}    {:<2}  :  {:<35}  {:<5}".format(self.step, self.opcode, self.register.register_address, self.operand2, self.opcode5bit() + " " + self.register.addressto3bit() + " " + self.valueto16bit(), self.clock_cycle)

def main():
    instruction = ""
    Opcode = ""
    Operand = ""
    Operand2 = ""
    registers = [Register(0, "r{}".format(i)) for i in range(8)]
    steps = []
    print("Input instruction ")
    print("Opcode : mov, add, sub, mul and div")
    print("Operand 1 : R0 - R7")
    print("Operand 2 : R0 - R7 or a value")
    print("Type 'end 0 0' to stop the input stage")
    print("Enter Inputs : ")
    step = 0
    while True:
        instruction = input()
        if instruction == "end 0 0":
            break
        else:
            Input = instruction.split(" ")
            Opcode = Input[0]
            Operand = Input[1]
            Operand2 = Input[2]
            desReg = None
            for k in range(len(registers)):
                if registers[k].register_address == Operand:
                    desReg = registers[k]
                    break
            try:
                value = int(Operand2)
                if Opcode == "mov":
                    desReg.set_value(value)
                    steps.append(Instruction(step, Opcode, desReg, 1))
                elif Opcode == "add":
                    desReg.set_value(desReg.get_value() + value)
                    steps.append(Instruction(step, Opcode, desReg, 2))
                elif Opcode == "sub":
                    desReg.set_value(desReg.get_value() - value)
                    steps.append(Instruction(step, Opcode, desReg, 3))
                elif Opcode == "mul":
                    desReg.set_value(desReg.get_value() * value)
                    steps.append(Instruction(step, Opcode, desReg, 4))
                elif Opcode == "div":
                    desReg.set_value(desReg.get_value() / value)
                    steps.append(Instruction(step, Opcode, desReg, 4))
            except ValueError:
                sourceReg = None
                for j in range(len(registers)):
                    if registers[j].register_address == Operand2:
                        sourceReg = registers[j]
                        break
                if Opcode == "mov":
                    desReg.set_value(sourceReg.get_value())
                    steps.append(Instruction(step, Opcode, desReg, 1))
                elif Opcode == "add":
                    desReg.set_value(desReg.get_value() + sourceReg.get_value())
                    steps.append(Instruction(step, Opcode, desReg, 2))
                elif Opcode == "sub":
                    desReg.set_value(desReg.get_value() - sourceReg.get_value())
                    steps.append(Instruction(step, Opcode, desReg, 3))
                elif Opcode == "mul":
                    desReg.set_value(desReg.get_value() * sourceReg.get_value())
                    steps.append(Instruction(step, Opcode, desReg, 4))
                elif Opcode == "div":
                    desReg.set_value(desReg.get_value() / sourceReg.get_value())
                    steps.append(Instruction(step, Opcode, desReg, 4))
        step += 1

    print("\nSteps    Decoded:       Encoded Instructions(24-bits):        Clock cycles")
    for s in steps:
        print(s)

    print("\n--------------------------------------------------------------------------")
    print("Steps of Register")
    for s in steps:
        s.register.set_value(s.value)
        print("{}  =  {} [{}]".format(s.register.register_address, s.value, s.valueto16bit()))

    print("\n--------------------------------------------------------------------------")
    print("Final Register Result")
    for reg in registers:
        print("{}  {}  [{}]".format(reg.register_address, reg.value, reg.valueto16bit()))

    print("\n--------------------------------------------------------------------------")
    totalClockCycle = sum(s.clock_cycle for s in steps)
    totalInstructions = len(steps)
    cpi = totalClockCycle / totalInstructions  # Correcting CPI calculation
    print("CPI of the program : ", cpi)
    print("---------------------------------------------------------------------------")

    pipelinedClockcycle = len(steps) + 3
    print("Pipelined Execution of Program")
    print("====================================")
    print("It is assumed that the CPU has 4-pipeline stages: IF (instruction fetch)")
    print("ID (instruction decoding, EX (Execution) and WB (Write back).")
    print("And each stage completes within one clock cycle and RAW hazard (any) will be")
    print("solved with FORWARDING (from the output register of ALU to the input of next)")
    print("instruction's ALU stage) without causing any stall.\n")
    
    # Print pipeline stage headers
    print("{:<30}".format(""), end="")
    for z in range(1, pipelinedClockcycle + 1):
        print("{:>5}".format(z), end="")
    print()
    
    # Print instructions with pipeline stages
    for s in steps:
        print("{:<2}. {:<5}  {:<2}  {:<2} :{:>15}".format(s.step + 1, s.opcode, s.register.register_address, s.value, "IF | ID | EX | WB"))
    
    print("\n\nPipelined execution took {} clock cycles for the program executions.".format(pipelinedClockcycle))

if __name__ == "__main__":
    main()
