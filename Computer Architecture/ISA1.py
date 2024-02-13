def encode_register(register):
    registers = {'r0': '000', 'r1': '001', 'r2': '010', 'r3': '011', 'r4': '100', 'r5': '101', 'r6': '110', 'r7': '111'}
    return registers[register]

def encode_instruction(opcode):
    opcodes = {'mov': '00001', 'add': '00010', 'sub': '00011', 'mul': '00100', 'div': '00101', 'end': '11111'}
    return opcodes[opcode]

def execute_instruction(opcode, operand1, operand2, registers):
    if opcode == 'mov':
        registers[operand1] = registers[operand2] if operand2 in registers else int(operand2)
    elif opcode == 'add':
        registers[operand1] += registers[operand2]
    elif opcode == 'sub':
        registers[operand1] -= registers[operand2]
    elif opcode == 'mul':
        registers[operand1] *= registers[operand2]
    elif opcode == 'div':
        registers[operand1] //= registers[operand2]
    elif opcode == 'end':
        return True
    return False

def print_registers(registers):
    for reg in registers:
        print(f'{reg} = {registers[reg]} [{bin(registers[reg])[2:].zfill(32)}]')

def main():
    registers = {'r0': 0, 'r1': 0, 'r2': 0, 'r3': 0, 'r4': 0, 'r5': 0, 'r6': 0, 'r7': 0}
    program_counter = 0

    print("Input:")
    input_lines = []
    while True:
        line = input()
        if line == 'end 0.0':
            break
        input_lines.append(line)

    print("\nPC:           Decoded:           Encoded instructions(32-bit)")

    for instruction in input_lines:
        tokens = instruction.split()
        opcode = tokens[0]
        operand1 = tokens[1]
        operand2 = tokens[2]

        encoded_instruction = encode_instruction(opcode) + encode_register(operand1) + encode_register(operand2)
        print(f'PC[{program_counter}]-> {opcode} {operand1}, {operand2}   :    {encoded_instruction}  {encode_register(operand1)}  {encode_register(operand2)}')

        if execute_instruction(opcode, operand1, operand2, registers):
            break

        print_registers(registers)
        program_counter += 1

    print("\nAfter the program execution contents of the registers(32-bits) are.............")
    print_registers(registers)

if __name__ == "__main__":
    main()
