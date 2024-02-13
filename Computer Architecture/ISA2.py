class InstructionSetArchitecture:
    def __init__(self):
        self.registers = {'r0': '000', 'r1': '001', 'r2': '010', 'r3': '011', 'r4': '100', 'r5': '101', 'r6': '110', 'r7': '111'}
        self.opcodes = {'mov': '00001', 'add': '00010', 'sub': '00011', 'mul': '00100', 'div': '00101'}

    def encode_register(self, register):
        return self.registers.get(register, '000')  # Default value is '000' if register is not found

    def encode_instruction(self, opcode):
        return self.opcodes.get(opcode, '00000')  # Default value is '00000' if opcode is not found

    def encode_decimal(self, decimal_value):
        return bin(int(decimal_value))[2:].zfill(32) if decimal_value else '0' * 32

    def execute_instruction(self, opcode, operand1, operand2):
        if opcode == 'mov':
            return operand2
        elif opcode == 'add':
            return operand1 + operand2
        elif opcode == 'sub':
            return operand1 - operand2
        elif opcode == 'mul':
            return operand1 * operand2
        elif opcode == 'div':
            return operand1 / operand2

    def execute_program(self, instructions):
        registers = {'r0': 0, 'r1': 0, 'r2': 0, 'r3': 0, 'r4': 0, 'r5': 0, 'r6': 0, 'r7': 0}
        for i, instruction in enumerate(instructions):
            opcode, operand1, operand2 = instruction
            encoded_instruction = self.encode_instruction(opcode)
            encoded_operand1 = self.encode_register(operand1)
            encoded_operand2 = self.encode_register(operand2) if operand2 in self.registers else self.encode_decimal(operand2)
            print(f"PC[{i}] -> {opcode} {operand1}, {operand2} : {encoded_instruction} {encoded_operand1} {encoded_operand2}")

            operand1_value = registers[operand1]
            operand2_value = registers[operand2] if operand2 in self.registers else operand2

            result = self.execute_instruction(opcode, operand1_value, operand2_value)
            registers[operand1] = result
        return registers

if __name__ == "__main__":
    isa = InstructionSetArchitecture()
    instructions = [('mov', 'r1', 345), ('mov', 'r2', 339), ('sub', 'r2', 'r1'), ('mov', 'r3', 'r2'), ('mov', 'r4', 111), ('mul', 'r3', 'r4'), ('mov', 'r5', 'r3'), ('div', 'r5', 11)]
    print("Output:")
    final_registers = isa.execute_program(instructions)
    print("\nAfter the program execution, contents of the registers(32-bits) are:")
    for reg, val in final_registers.items():
        print(f"{reg} = {val} [{bin(val)[2:].zfill(32)}]")
