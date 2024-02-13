import java.util.ArrayList;
import java.util.Scanner;
public class ISAsimulator {

    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String instruction = "";
        String Opcode = "";
        String Operand = "";
        String Operand2 = "";
        Register[] registers = new Register[8];
        for (int i = 0; i < 8; i++) {
            registers[i] = new Register(0, "r" + i);
        }
        ArrayList<Instruction> steps = new ArrayList();
        System.out.println("Input instruction ");
        System.out.println("Opcode : mov, add, sub, mul and div");
        System.out.println("Operand 1 : R0 - R7");
        System.out.println("Operand 2 : R0 - R7 or a value");
        System.out.println("Type 'end 0 0' to stop the input stage");
        System.out.println("Enter Inputs : ");
        int step = 0;
        while (!(Opcode.equals("end")) && !(Operand.equals("0")) && !(Operand.equals("0"))) {
            instruction = scan.nextLine();
            if (instruction.equals("end 0 0")) {
                break;
            } else {
                String[] Input = instruction.split(" ");
                Opcode = Input[0];
                Operand = Input[1];
                Operand2 = Input[2];
                Register desReg = null;

                for (int k = 0; k <= registers.length; k++) {
                    if ((registers[k].getRegisterAddress().equals(Operand))) {
                        desReg = registers[k];
                        break;
                    }
                }
                try {
                    // input = opcode r0 5
                    int value = Integer.parseInt(Operand2);
                    switch (Opcode) {
                        case "mov":
                            desReg.setValue(value);
                            steps.add(new Instruction(step, Opcode, desReg, 1));
                            break;
                        case "add":
                            desReg.setValue(desReg.getValue() + value);
                            steps.add(new Instruction(step, Opcode, desReg, 2));
                            break;
                        case "sub":
                            desReg.setValue(desReg.getValue() - value);
                            steps.add(new Instruction(step, Opcode, desReg, 3));
                            break;
                        case "mul":
                            desReg.setValue(desReg.getValue() * value);
                            steps.add(new Instruction(step, Opcode, desReg, 4));
                            break;
                        case "div":
                            desReg.setValue(desReg.getValue() / value);
                            steps.add(new Instruction(step, Opcode, desReg, 4));

                    }
                } catch (NumberFormatException e) {
                    // input = opcode r0 r1
                    Register sourceReg = null;
                    for (int j = 0; j <= registers.length; j++) {
                        if (registers[j].getRegisterAddress().equals(Operand2)) {
                            sourceReg = registers[j];
                            break;
                        }
                    }
                    switch (Opcode) {
                        case "mov":
                            desReg.setValue(sourceReg.getValue());
                            steps.add(new Instruction(step, Opcode, desReg, Operand2, 1));
                            break;
                        case "add":
                            desReg.setValue(desReg.getValue() + sourceReg.getValue());
                            steps.add(new Instruction(step, Opcode, desReg, Operand2, 2));
                            break;
                        case "sub":
                            desReg.setValue(desReg.getValue() - sourceReg.getValue());
                            steps.add(new Instruction(step, Opcode, desReg, Operand2, 3));
                            break;
                        case "mul":
                            desReg.setValue(desReg.getValue() * sourceReg.getValue());
                            steps.add(new Instruction(step, Opcode, desReg, Operand2, 4));
                            break;
                        case "div":
                            desReg.setValue(desReg.getValue() / sourceReg.getValue());
                            steps.add(new Instruction(step, Opcode, desReg, Operand2, 4));
                    }
                }
            }
            step++;
        }
        scan.close();
        System.out.println();
        System.out.println("\nSteps    Decoded:       Encoded Instructions(24-bits):        Clock cycles");
        for (Instruction s : steps) {
            System.out.println(s.toString());
        }

        System.out.println("\n--------------------------------------------------------------------------");
        System.out.println("Steps of Register");
        for (Instruction s : steps) {
            System.out.format("%s  =  %d [%s]\n", s.getRegister().getRegisterAddress(), s.getValue(), s.valueto16bit());
        }
        System.out.println("\n--------------------------------------------------------------------------");
        System.out.println("Final Register Result");
        for (int i = 0; i < registers.length; i++) {
            System.out.format("%s  %d  [%s]\n", registers[i].getRegisterAddress(), registers[i].getValue(), registers[i].valueto16bit());
        }

        System.out.println("\n--------------------------------------------------------------------------");
        int totalClockCycle = 0;
        for (Instruction s : steps) {
            totalClockCycle += s.getClockCycle();
        }
        double cpi = totalClockCycle / step;
        System.out.println("CPI of the program : " + cpi);
        System.out.println("---------------------------------------------------------------------------");

        int pipelinedClockcycle = steps.size()+3;
        System.out.println("Pipelined Execution of Program");
        System.out.println("====================================");
        System.out.println("It is assumed that the CPU has 4-pipeline stages: IF (instruction fetch)");
        System.out.println("ID (instruction decoding, EX (Execution) and WB (Write back).");
        System.out.println("And each stage completes within one clock cycle and RAW hazard (any) will be");
        System.out.println("solved with FORWARDING (from the output register of ALU to the input of next)");
        System.out.println("instruction's ALU stage) without causing any stall.\n");
        System.out.printf("%23s","");
        for (int z = 1; z <= pipelinedClockcycle; z++) {
            System.out.printf("%5d", z);
        }
        for (Instruction s : steps) {
            if (s.getOperand2().equals("")) {
                System.out.printf("%n%d. %-5s%-4s%-2d :", s.getStep()+1, s.getOpcode(), s.getRegister().getRegisterAddress(), s.getValue());
            } else {
                System.out.printf("%n%d. %-5s%-4s%-2s :", s.getStep()+1, s.getOpcode(), s.getRegister().getRegisterAddress(), s.getOperand2());
            }

            for (int j=0; j <= s.getStep()+1; j++) {
                System.out.printf("%5s", "");
            }
            System.out.print("IF | ID | EX | WB");
        }
        System.out.println("\n\nPipelined execution took "+ pipelinedClockcycle +" clock cycles for the program executions.");
    }
}


public class Register {
    private String registerAddress;
    private int value;

    public Register(int value, String registerAddress) {
        this.registerAddress = registerAddress;
        this.value = value;
    }

    public int getValue() {
        return value;
    }

    public void setValue(int value) {
        this.value = value;
    }

    @Override
    public String toString() {
        return String.format("%s  %d  [%s]", registerAddress, value, valueto16bit());
    }

    public String valueto16bit() {
        String binaryValue = Integer.toBinaryString(value);
        int padding = 16 - binaryValue.length();
        if (padding > 0) {
            StringBuilder paddedValue = new StringBuilder();
            for (int i = 0; i < padding; i++) {
                paddedValue.append('0');
            }
            paddedValue.append(binaryValue);
            return paddedValue.toString();
        } else {
            return binaryValue;
        }
    }

    public String addressto3bit() {
        switch (this.registerAddress) {
            case "r0":
                return "000";
            case "r1":
                return "001";
            case "r2":
                return "010";
            case "r3":
                return "011";
            case "r4":
                return "100";
            case "r5":
                return "101";
            case "r6":
                return "110";
            case "r7":
                return "111";
        }
        return "";
    }

    public String getRegisterAddress() {
        return registerAddress;
    }

    public void setRegisterAddress(String registerAddress) {
        this.registerAddress = registerAddress;
    }
}


public class Instruction {
    private int step;
    private String opcode;
    private Register register;
    private String operand2;
    private int value;
    private int clockCycle;

    public Instruction(int step, String opcode, Register register, int clockCycle) {
        this.step = step;
        this.opcode = opcode;
        this.register = register;
        this.operand2 = "";
        this.value = register.getValue();
        this.clockCycle = clockCycle;
    }

    public Instruction(int step, String opcode, Register register, String operand2, int clockCycle) {
        this.step = step;
        this.opcode = opcode;
        this.register = register;
        this.operand2 = operand2;
        this.value = register.getValue();
        this.clockCycle = clockCycle;
    }

    public String opcode5bit() {
        switch (this.opcode) {
            case "mov":
                return "00001";
            case "add":
                return "00010";
            case "mul":
                return "00100";
            case "sub":
                return "00011";
            case "div":
                return "00101";
        }
        return "";
    }

    public String valueto16bit() {
        String binaryValue = Integer.toBinaryString(value);
        return String.format("%016d", Integer.parseInt(binaryValue));
    }


    public int getStep() {
        return step;
    }

    public void setStep(int step) {
        this.step = step;
    }

    public String getOpcode() {
        return opcode;
    }

    public void setOpcode(String opcode) {
        this.opcode = opcode;
    }

    public Register getRegister() {
        return register;
    }

    public void setRegister(Register register) {
        this.register = register;
    }

    public int getClockCycle() {
        return clockCycle;
    }

    public void setClockCycle(int clockCycle) {
        this.clockCycle = clockCycle;
    }

    public String getOperand2() {
        return operand2;
    }

    public void setOperand2(String operand2) {
        this.operand2 = operand2;
    }

    public int getValue() {
        return value;
    }

    public void setValue(int value) {
        this.value = value;
    }

    @Override
    public String toString() {
        if (this.operand2.equals("")) {
            return String.format("[%d]  %-5s%-4s  %-4s  :  %-35s  %-5d", this.step, this.opcode, this.register.getRegisterAddress(), this.register.getValue(), this.opcode5bit() + " " + this.register.addressto3bit() + " " + this.valueto16bit(), this.clockCycle);
        } else {
            return String.format("[%d]  %-5s%-4s  %-4s  :  %-35s  %-5d", this.step, this.opcode, this.register.getRegisterAddress(), this.operand2, this.opcode5bit() + " " + this.register.addressto3bit() + " " + this.valueto16bit(), this.clockCycle);
        }
    }
}


