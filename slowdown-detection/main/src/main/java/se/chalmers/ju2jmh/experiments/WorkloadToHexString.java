package se.chalmers.ju2jmh.experiments;

public class WorkloadToHexString {
    public static final double INPUT = -12.345E-67;
    public static final String OUTPUT = runWorkload(INPUT);

    public static String runWorkload(double input) {
        return Double.toHexString(input);
    }
}
