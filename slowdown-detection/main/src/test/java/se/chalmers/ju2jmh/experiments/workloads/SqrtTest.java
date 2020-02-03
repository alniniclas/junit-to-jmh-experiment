package se.chalmers.ju2jmh.experiments.workloads;

import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class SqrtTest {
    private double input = Sqrt.INPUT;
    private double expected = Sqrt.OUTPUT;

    @Test
    public void testRunWorkloadOnce() {
        double result = Sqrt.runWorkload(input);

        assertEquals(expected, result, 0.0);
    }

    @Test
    public void testRunWorkloadTwice() {
        double result1 = Sqrt.runWorkload(input);
        double result2 = Sqrt.runWorkload(input);

        assertEquals(expected, result1, 0.0);
        assertEquals(expected, result2, 0.0);
    }

    @Test
    public void testRunWorkloadThrice() {
        double result1 = Sqrt.runWorkload(input);
        double result2 = Sqrt.runWorkload(input);
        double result3 = Sqrt.runWorkload(input);

        assertEquals(expected, result1, 0.0);
        assertEquals(expected, result2, 0.0);
        assertEquals(expected, result3, 0.0);
    }
}
