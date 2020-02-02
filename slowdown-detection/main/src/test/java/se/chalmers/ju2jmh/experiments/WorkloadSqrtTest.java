package se.chalmers.ju2jmh.experiments;

import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class WorkloadSqrtTest {
    private final double input = WorkloadSqrt.INPUT;
    private final double expected = WorkloadSqrt.OUTPUT;

    @Test
    public void testRunWorkloadOnce() {
        double result = WorkloadSqrt.runWorkload(input);

        assertEquals(expected, result, 0.0);
    }

    @Test
    public void testRunWorkloadTwice() {
        double result1 = WorkloadSqrt.runWorkload(input);
        double result2 = WorkloadSqrt.runWorkload(input);

        assertEquals(expected, result1, 0.0);
        assertEquals(expected, result2, 0.0);
    }

    @Test
    public void testRunWorkloadThrice() {
        double result1 = WorkloadSqrt.runWorkload(input);
        double result2 = WorkloadSqrt.runWorkload(input);
        double result3 = WorkloadSqrt.runWorkload(input);

        assertEquals(expected, result1, 0.0);
        assertEquals(expected, result2, 0.0);
        assertEquals(expected, result3, 0.0);
    }
}
