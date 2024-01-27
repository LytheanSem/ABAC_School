import java.util.Scanner;

public class number_conversion {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Pick conversion type:");
        System.out.println("\nPress (1) for Decimal to Binary");
        System.out.println("Press (2) for Binary to Decimal");
        System.out.println("Press (3) for Decimal to Hexadecimal");
        System.out.println("Press (4) for Hexadecimal to Decimal");
        System.out.println("Press (5) for Binary to Hexadecimal");
        System.out.println("Press (6) for Hexadecimal to Binary");
        System.out.print("\nType your choice here: ");

        int choice = scanner.nextInt();

        switch (choice) {
            case 1:
                System.out.print("\nEnter a decimal number: ");
                int decimalNumber = scanner.nextInt();
                System.out.println("Binary equivalent: " + decimalToBinary(decimalNumber));
                break;

            case 2:
                System.out.print("\nEnter a binary number: ");
                String binaryNumber = scanner.next();
                System.out.println("Decimal equivalent: " + binaryToDecimal(binaryNumber));
                break;

            case 3:
                System.out.print("\nEnter a decimal number: ");
                int decimalNum = scanner.nextInt();
                System.out.println("Hexadecimal equivalent: " + decimalToHexadecimal(decimalNum));
                break;

            case 4:
                System.out.print("\nEnter a hexadecimal number: ");
                String hexNumber = scanner.next();
                System.out.println("Decimal equivalent: " + hexadecimalToDecimal(hexNumber));
                break;

            case 5:
                System.out.print("\nEnter a binary number: ");
                String binaryNum = scanner.next();
                System.out.println("Hexadecimal equivalent: " + binaryToHexadecimal(binaryNum));
                break;

            case 6:
                System.out.print("\nEnter a hexadecimal number: ");
                String hexNum = scanner.next();
                System.out.println("Binary equivalent: " + hexadecimalToBinary(hexNum));
                break;

            default:
                System.out.println("\nIncorrect input. Please choose a number between 1 and 6.");
        }

        scanner.close();
    }

    private static String decimalToBinary(int decimalNumber) {
        // If the input number is 0, return "0" as the binary representation
        if (decimalNumber == 0) {
            return "0";
        }

        // Array to store binary digits
        int[] binaryNum = new int[1000];

        // Counter for binary array
        int i = 0;
        while (decimalNumber > 0) {
            // Storing remainder in binary array
            binaryNum[i] = decimalNumber % 2;
            decimalNumber = decimalNumber / 2;
            i++;
        }

        // Create a StringBuilder to efficiently build the binary representation
        StringBuilder binaryBuilder = new StringBuilder();

        // Append the binary array in reverse order to the StringBuilder
        for (int j = i - 1; j >= 0; j--) {
            binaryBuilder.append(binaryNum[j]);
        }

        // Convert the StringBuilder to a String and return
        return binaryBuilder.toString();
    }

    private static int binaryToDecimal(String binaryNumber) {
        int num = Integer.parseInt(binaryNumber); // Parse the binary string to an integer
        int dec_value = 0;

        // Initializing base value to 1, i.e., 2^0
        int base = 1;

        int temp = num;
        while (temp > 0) {
            int last_digit = temp % 10;
            temp = temp / 10;

            dec_value += last_digit * base;

            base = base * 2;
        }

        return dec_value;
    }

    private static String decimalToHexadecimal(int decimalNum) {
        // If the input number is 0, return "0" as the hexadecimal representation
        if (decimalNum == 0) {
            return "0";
        }

        char[] hexaDeciNum = new char[100];

        // Counter for hexadecimal number array
        int i = 0;
        while (decimalNum != 0) {
            // Temporary variable to store remainder
            int temp = 0;

            // Storing remainder in temp variable.
            temp = decimalNum % 16;

            // Check if temp < 10
            if (temp < 10) {
                hexaDeciNum[i] = (char) (temp + 48);
                i++;
            } else {
                hexaDeciNum[i] = (char) (temp + 55);
                i++;
            }

            decimalNum = decimalNum / 16;
        }

        // Create a StringBuilder to efficiently build the hexadecimal representation
        StringBuilder hexBuilder = new StringBuilder();

        // Append the hexadecimal number array in reverse order to the StringBuilder
        for (int j = i - 1; j >= 0; j--) {
            hexBuilder.append(hexaDeciNum[j]);
        }

        // Convert the StringBuilder to a String and return
        return hexBuilder.toString();
    }

    private static int hexadecimalToDecimal(String hexNumber) {
        int len = hexNumber.length();

        // Initializing base value to 1, i.e 16^0
        int base = 1;

        int dec_val = 0;

        // Extracting characters as digits from last
        // character
        for (int i = len - 1; i >= 0; i--) {
            // if character lies in '0'-'9', converting
            // it to integral 0-9 by subtracting 48 from
            // ASCII value
            if (hexNumber.charAt(i) >= '0'
                    && hexNumber.charAt(i) <= '9') {
                dec_val += (hexNumber.charAt(i) - 48) * base;

                // incrementing base by power
                base = base * 16;
            }

            // if character lies in 'A'-'F' , converting
            // it to integral 10 - 15 by subtracting 55
            // from ASCII value
            else if (hexNumber.charAt(i) >= 'A'
                    && hexNumber.charAt(i) <= 'F') {
                dec_val += (hexNumber.charAt(i) - 55) * base;

                // incrementing base by power
                base = base * 16;
            }
        }
        return dec_val;
    }

    private static String binaryToHexadecimal(String binaryNumber) {
        // Convert binary to decimal
        int decimal = binaryToDecimal(binaryNumber);

        // Convert decimal to hexadecimal
        String hexadecimalResult = decimalToHexadecimal(decimal);

        // Return the hexadecimal result
        return hexadecimalResult;
    }

    private static String hexadecimalToBinary(String hexNumber) {
        // Convert hexadecimal to decimal
        int decimal = hexadecimalToDecimal(hexNumber);

        // Convert decimal to binary
        String binaryResult = decimalToBinary(decimal);

        // Return the binary result
        return binaryResult;
    }

}
