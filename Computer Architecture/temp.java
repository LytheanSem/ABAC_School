import java.util.Scanner;

public class temp {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Choose conversion type:");
        System.out.println("1. Decimal to Binary");
        System.out.println("2. Binary to Decimal");
        System.out.println("3. Decimal to Hexadecimal");
        System.out.println("4. Hexadecimal to Decimal");
        System.out.println("5. Binary to Hexadecimal");

        int choice = scanner.nextInt();

        switch (choice) {
            case 1:
                System.out.print("Enter a decimal number: ");
                int decimalNumber = scanner.nextInt();
                System.out.println("Binary representation: " + decimalToBinary(decimalNumber));
                break;

            case 2:
                System.out.print("Enter a binary number: ");
                String binaryNumber = scanner.next();
                System.out.println("Decimal representation: " + binaryToDecimal(binaryNumber));
                break;

            case 3:
                System.out.print("Enter a decimal number: ");
                int decimalNum = scanner.nextInt();
                System.out.println("Hexadecimal representation: " + decimalToHexadecimal(decimalNum));
                break;

            case 4:
                System.out.print("Enter a hexadecimal number: ");
                String hexNumber = scanner.next();
                System.out.println("Decimal representation: " + hexadecimalToDecimal(hexNumber));
                break;

            case 5:
                System.out.print("Enter a binary number: ");
                String binaryNum = scanner.next();
                System.out.println("Hexadecimal representation: " + binaryToHexadecimal(binaryNum));
                break;

            default:
                System.out.println("Invalid choice. Please choose a number between 1 and 5.");
        }

        scanner.close();
    }

    private static String decimalToBinary(int decimalNumber) {
        StringBuilder binary = new StringBuilder();
        while (decimalNumber > 0) {
            binary.insert(0, decimalNumber % 2);
            decimalNumber /= 2;
        }
        return binary.toString();
    }

    private static int binaryToDecimal(String binaryNumber) {
        int decimal = 0;
        int power = 0;
        for (int i = binaryNumber.length() - 1; i >= 0; i--) {
            if (binaryNumber.charAt(i) == '1') {
                decimal += Math.pow(2, power);
            }
            power++;
        }
        return decimal;
    }

    private static String decimalToHexadecimal(int decimalNumber) {
        StringBuilder hexadecimal = new StringBuilder();
        while (decimalNumber > 0) {
            int remainder = decimalNumber % 16;
            if (remainder < 10) {
                hexadecimal.insert(0, (char) ('0' + remainder));
            } else {
                hexadecimal.insert(0, (char) ('A' + remainder - 10));
            }
            decimalNumber /= 16;
        }
        return hexadecimal.toString();
    }

    private static int hexadecimalToDecimal(String hexNumber) {
        int decimal = 0;
        for (int i = hexNumber.length() - 1; i >= 0; i--) {
            char hexChar = hexNumber.charAt(i);
            if (hexChar >= '0' && hexChar <= '9') {
                decimal += (hexChar - '0') * Math.pow(16, hexNumber.length() - 1 - i);
            } else if (hexChar >= 'A' && hexChar <= 'F') {
                decimal += (hexChar - 'A' + 10) * Math.pow(16, hexNumber.length() - 1 - i);
            }
        }
        return decimal;
    }

    private static String binaryToHexadecimal(String binaryNumber) {
        int decimal = binaryToDecimal(binaryNumber);
        return decimalToHexadecimal(decimal);
    }
}
