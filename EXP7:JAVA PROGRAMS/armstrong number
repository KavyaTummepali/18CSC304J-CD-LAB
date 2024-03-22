public class Armstrong {
    public static void main(String[] args) {
        int number = 370, orgNumber, remainder, result = 0, n = 0;
        orgNumber = number;
        for (;orgNumber != 0; orgNumber /= 10, ++n);
        orgNumber = number;
        for (;orgNumber != 0; orgNumber /= 10)
        {
            remainder = orgNumber % 10;
            result += Math.pow(remainder, n);
        }
        if(result == number)
            System.out.println(number + " is an Armstrong number.");
        else
            System.out.println(number + " is not an Armstrong number.");
    }
}
