import java.io.*;
public class TierCount {
	private static double factorial(double n) {
		if (n==0|n==1) {
			return 1;
		} else {
			return n*factorial(n-1);
		}
	}
	private static double choose(double n, double k) {
		return (factorial(n)/(factorial(n-k)*factorial(k)));
	}
	private static double CountSlice(double boardsize, double r, double w, double b) {
		return choose(boardsize,r)*choose(boardsize-r,w) * choose(boardsize-r-w,b);
	}
	private static PrintWriter createFile(String path) {
		try {
			File file = new File(path);
			if (!file.exists()) {
				file.createNewFile();
				//FileWriter fileWriter = new FileWriter(file);
				//PrintWriter pw = new PrintWriter(fileWriter);
			} //else {
				//FileWriter fileWriter = new FileWriter(file);
				//PrintWriter pw = new PrintWriter(fileWriter);
			//}
			FileWriter fileWriter = new FileWriter(file);
			PrintWriter pw = new PrintWriter(fileWriter);
			return pw;
		} catch (IOException e) {
			e.printStackTrace();
		}
		return null;
	}
			
	public static void main(String[] args) {
		System.out.printf("\n\nKuba Tiered Count\n\n");
		String fileName = "/Users/maxgilchrist/CSolver/Kuba/Output/"+args[0]+"_"+args[1]+"_"+args[2]+"_"+args[3]+".txt";
		PrintWriter pw = createFile(fileName);
		pw.printf("Kuba Tiered Count\n\n");
		double boardsize = Double.parseDouble(args[0]);
		double red = Double.parseDouble(args[1]);
		double white = Double.parseDouble(args[2]);
		double black = Double.parseDouble(args[3]);
		double rwb; double rw; double r; double total = 0;

		for (double i = 1; i < red + 1; i++) {
			r = 0;
			for(double j = 1; j < white + 1; j++) {
				rw = 0;
				for (double k = 1; k < black + 1; k++) {
					rwb = 0;
					rwb = CountSlice(boardsize,i,j,k);
					System.out.printf("\n               R=%.0f W=%.0f  B=%.0f Count=%.0f\n",i,j,k,rwb);			
					pw.printf("\n               R=%.0f W=%.0f  B=%.0f Count=%.0f\n",i,j,k,rwb);			
					rw += rwb;
				
				}
				r += rw;
				System.out.printf("\n          R=%.0f W=%.0f Count=%.0f\n", i, j, rw);
				pw.printf("\n               R=%.0f W=%.0f Count=%.0f\n", i, j, rw);
			}
			total += r;
			System.out.printf("\n     R=%.0f Count=%.0f\n", i, r);
			pw.printf("\n     R=%.0f Count=%.0f\n", i, r);
		}
		System.out.printf("\nBoardSize=%.0f Red=%.0f White=%.0f Black=%.0f TotalPositions=%.0f\n\n",boardsize,red,white,black,total);
		pw.printf("\nBoardSize=%.0f Red=%.0f White=%.0f Black=%.0f TotalPositions=%.0f\n\n",boardsize,red,white,black,total);
		pw.close();
	}

}
