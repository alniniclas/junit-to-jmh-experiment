package se.chalmers.ju2jmh.experiments.workloads;

public class Sqrt {
    public static final double INPUT = 25.0;
    public static final double OUTPUT = runWorkload(INPUT);

    public static double runWorkload(double input) {
        return Math.sqrt(input);
    }
}
