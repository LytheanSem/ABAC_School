import java.util.Scanner;

public class numcon {
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
        return Integer.toBinaryString(decimalNumber);
    }

    private static int binaryToDecimal(String binaryNumber) {
        return Integer.parseInt(binaryNumber, 2);
    }

    private static String decimalToHexadecimal(int decimalNumber) {
        return Integer.toHexString(decimalNumber).toUpperCase();
    }

    private static int hexadecimalToDecimal(String hexNumber) {
        return Integer.parseInt(hexNumber, 16);
    }

    private static String binaryToHexadecimal(String binaryNumber) {
        int decimal = binaryToDecimal(binaryNumber);
        return decimalToHexadecimal(decimal);
    }
}
