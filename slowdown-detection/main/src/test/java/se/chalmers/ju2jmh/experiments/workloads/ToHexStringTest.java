package se.chalmers.ju2jmh.experiments.workloads;

import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class ToHexStringTest {
    private double input = ToHexString.INPUT;
    private String expected = ToHexString.OUTPUT;

    @Test
    public void testRunWorkloadOnce() {
        String result = ToHexString.runWorkload(input);

        assertEquals(expected, result);
    }

    @Test
    public void testRunWorkloadTwice() {
        String result1 = ToHexString.runWorkload(input);
        String result2 = ToHexString.runWorkload(input);

        assertEquals(expected, result1);
        assertEquals(expected, result2);
    }

    @Test
    public void testRunWorkloadThrice() {
        String result1 = ToHexString.runWorkload(input);
        String result2 = ToHexString.runWorkload(input);
        String result3 = ToHexString.runWorkload(input);

        assertEquals(expected, result1);
        assertEquals(expected, result2);
        assertEquals(expected, result3);
    }
}
