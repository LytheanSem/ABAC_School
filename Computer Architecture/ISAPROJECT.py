class Registers:
    def __init__(self, reg_val, reg_adr):
        self.reg_val = reg_val
        self.reg_adr = reg_adr

    def set_reg_adr(self, reg_adr):
        self.reg_adr = reg_adr

    def get_reg_adr(self):
        return self.reg_adr

    def set_reg_val(self, reg_val):
        self.reg_val = reg_val

    def get_reg_val(self):
        return self.reg_val

    def to_32bit_val(self):
        if self.reg_val >= 0:
            return f"{self.reg_val:032b}"
        else:
            return bin(self.reg_val & 0xFFFFFFFF)[2:]

    def to_3bit_adr(self):
        reg_map = {"r0": "000", "r1": "001", "r2": "010", "r3": "011",
                   "r4": "100", "r5": "101", "r6": "110", "r7": "111"}
        return reg_map.get(self.reg_adr, "")


class InstructionSet:
    def __init__(self, step, opcode, register, clkcyc, operand="", value=None):
        self.step = step
        self.opcode = opcode
        self.register = register
        self.clkcyc = clkcyc
        self.operand = operand
        self.value = value if value is not None else register.get_reg_val()

    def five_bit_opcode(self):
        opcode_map = {
            "mov": "00001",
            "add": "00010",
            "mul": "00100",
            "sub": "00011",
            "div": "00101",
        }
        return opcode_map.get(self.opcode, "00000")

    def encode_instruction(self):
        opcode = self.five_bit_opcode()
        operand1 = self.register.to_3bit_adr()
        operand2 = self.to_32bit_val()[-24:]
        return f"[{opcode} {operand1} {operand2}]"

    def to_32bit_val(self):
        if self.value >= 0:
            return f"{self.value:032b}"
        else:
            return bin(self.value & 0xFFFFFFFF)[2:]

    def __str__(self):
        decoded_form = f"[{self.step}] {self.opcode}{self.register.get_reg_adr()}"
        if self.operand != "":
            decoded_form += f" {self.operand}"
        decoded_form = decoded_form.ljust(15)
        encoded_form = self.encode_instruction()
        return f"{decoded_form} {encoded_form}"


def main():
    regs = [Registers(0, f"r{i}") for i in range(8)]
    regs.append(Registers(0, "r7"))  # Add r7 as a remainder register

    instructions = []

    print("Input instructions:")
    print("Opcode: mov, add, mul, sub, and div")
    print("Operand 1: R0 - R6")
    print("Operand 2: R0 - R6 or a value")
    print("r7 is used to store the remainder")
    print("Type 'end 0 0' to start the simulation")
    print("Type the opcode and Operand down below (for example: mov r1 345): ")
    step = 0

    while True:
        instruction = input()
        if instruction == "end 0 0":
            break

        opcode, operand1, operand2 = instruction.split()
        operand2_reg = None
        register = None

        for reg in regs:
            if reg.get_reg_adr() == operand1:
                register = reg
            if reg.get_reg_adr() == operand2:
                operand2_reg = reg

        if operand2_reg is None:
            operand2_reg = Registers(int(operand2), operand2)

        if operand1 != operand2:
            operation_mapping = {
                "mov": lambda dest, src: dest.set_reg_val(src.get_reg_val()),
                "add": lambda dest, src: dest.set_reg_val(dest.get_reg_val() + src.get_reg_val()),
                "sub": lambda dest, src: dest.set_reg_val(dest.get_reg_val() - src.get_reg_val()),
                "mul": lambda dest, src: dest.set_reg_val(dest.get_reg_val() * src.get_reg_val()),
                "div": lambda dest, src: dest.set_reg_val(dest.get_reg_val() // src.get_reg_val()),
            }

            # Update this section to handle r7 as a remainder
            operation_mapping[opcode](register, operand2_reg)
            instructions.append(InstructionSet(
                step, opcode, register, 1, operand2_reg.get_reg_adr(), operand2_reg.get_reg_val()))

            # Handle r7 as a remainder
            if opcode == "div":
                remainder = register.get_reg_val() % operand2_reg.get_reg_val()
                regs[7].set_reg_val(remainder)  # Save remainder to r7

        step += 1


    print_output(instructions, regs)


def print_output(instructions, regs):
    print("\n Decoded Form                   Encoded Form                   Clock Cycles")
    for instruction in instructions:
        decoded_form = f"{instruction.step + 1}. {instruction.opcode} {instruction.register.get_reg_adr()}"
        if instruction.operand != "":
            decoded_form += f" {instruction.operand}"
        decoded_form = decoded_form.ljust(20)
        encoded_form = instruction.encode_instruction().ljust(47)
        print(f"{decoded_form} {encoded_form}{instruction.clkcyc}")

    # Result
    print("\nValues of registers after the execution:")
    for reg in regs:
        reg_adr = reg.get_reg_adr()
        reg_val = reg.get_reg_val()
        if reg_adr == 'r7' and reg_val == 0:
            continue  # Skip printing r7 if its value is 0
        print(f"{reg_adr}   {reg_val:3}  [{reg.to_32bit_val()}]")

    # Clock cycle Calculation
    total_clk_cycles = sum(instruction.clkcyc for instruction in instructions)
    # print(f"\ntotal_clk_cycles = {total_clk_cycles}")
    # print(f"len(instruction) = {len(instructions)}")
    # CPI Calculation
    cpi = total_clk_cycles / len(instructions)
    print("\nCPI value is", cpi)

    clkcys_with_pipeline = len(instructions) + 3
    print("\nThe pipelined version showing execution of the program")
    print("*" * 65)
    print(f"{'':15}", end="")
    for x in range(1, clkcys_with_pipeline + 1):
        print(f"{x:5d}", end="")

    for instruction in instructions:
        if instruction.operand == "":
            print(
                f"\n{instruction.step + 1}. {instruction.opcode} {instruction.register.get_reg_adr()} {instruction.value:2}", end=" ")
        else:
            print(
                f"\n{instruction.step + 1}. {instruction.opcode} {instruction.register.get_reg_adr()} {instruction.operand}", end=" ")
        for _ in range(instruction.step + 1):
            print(" " * 5, end="")
        print("IF | ID | EX | WB", end="")

    print(
        f"\n\nPipelined execution took {clkcys_with_pipeline} clock cycles to complete the program execution")

if __name__ == "__main__":
    main()

