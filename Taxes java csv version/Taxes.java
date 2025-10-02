import java.io.FileReader;

import com.opencsv.CSVReader;

public class Taxes {

    public static void main(String[] args) {
        CSVReader reader = null;
        try {
            reader = new CSVReader(new FileReader("G:\\My Drive\\juraj@andrews\\Code\\taxes\\Taxes java csv version\\Taxes.java"));
            String[] nextLine;
            while ((nextLine = reader.readNext()) != null) {
                for (String token : nextLine) {
                    System.out.print(token);
                }
                System.out.print("\n");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
