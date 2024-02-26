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
    def __init__(self, step, opcode, register, operand, operand_value, clkcyc):
        self.step = step
        self.opcode = opcode
        self.register = register
        self.operand = operand
        self.operand_value = operand_value
        self.clkcyc = clkcyc

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
        operand2 = self.operand_value[-16:]
        return f"[{opcode} {operand1} {operand2}]"

    def __str__(self):
        decoded_form = f"{self.step + 1}. {self.opcode} {self.register.get_reg_adr()}"
        if self.operand != "":
            decoded_form += f" {self.operand}"
        decoded_form = decoded_form.ljust(20)
        encoded_form = self.encode_instruction().ljust(40)
        return f"{decoded_form} {encoded_form}            {self.clkcyc}"


def main():
    regs = [Registers(0, f"r{i}") for i in range(8)]
    instructions = []

    print("Input instructions:")
    print("- For Opcode: mov, add, mul, sub, and div")
    print("- For Operand 1: R0 - R7")
    print("- For Operand 2: R0 - R7 or a value")
    print("- Type 'end 0 0' to stop the input request")
    print("Enter instructions:")
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
            operation_mapping[opcode](register, operand2_reg)
            instructions.append(InstructionSet(
                step, opcode, register, operand2_reg.to_3bit_adr(), operand2_reg.to_32bit_val(), 1))
        step += 1

    print("\n Decoded Form               Encoded Form               Clock Cycles")
    total_clk_cycles = 0
    for instruction in instructions:
        print(instruction)
        total_clk_cycles += instruction.clkcyc

    print("\nSteps of the Register")
    for instruction in instructions:
        reg_adr = instruction.register.to_3bit_adr()
        reg_val = instruction.register.get_reg_val()
        print(
            f"{reg_adr} = {reg_val:3}  [{instruction.register.to_32bit_val()}]")

    print("\nValues of registers after the execution of the instruction set")
    for reg in regs:
        reg_adr = reg.get_reg_adr()
        reg_val = reg.get_reg_val()
        print(f"{reg_adr}   {reg_val:3}  [{reg.to_32bit_val()}]")

    cpi = total_clk_cycles / len(instructions)
    print("\nCPI of the program is", round(cpi, 2))

    clkcys_with_pipeline = max(instruction.step + 1 for instruction in instructions) + 3
    print("\nThe pipelined version showing execution of the program")
    print("*" * (clkcys_with_pipeline * 6 + 5))
    print(f"{'':17}", end="")
    for x in range(1, clkcys_with_pipeline + 1):
        print(f"{x:5d}", end="")

    for instruction in instructions:
        if instruction.operand == "":
            print(
                f"\n{instruction.step + 1}. {instruction.opcode}{instruction.register.get_reg_adr()}{instruction.operand_value:2}", end=" ")
        else:
            print(
                f"\n{instruction.step + 1}. {instruction.opcode}{instruction.register.get_reg_adr()}{instruction.operand}", end=" ")
        for _ in range(instruction.step + 1):
            print(f"{'':5}", end="")
        print(f"{instruction.clkcyc} | {instruction.clkcyc} | {instruction.clkcyc} | {instruction.clkcyc}", end="")

    print(
        f"\n\nPipelined execution took {clkcys_with_pipeline} clock cycles to complete the program execution")


if __name__ == "__main__":
    main()