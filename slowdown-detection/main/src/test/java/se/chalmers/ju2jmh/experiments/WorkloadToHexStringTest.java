package se.chalmers.ju2jmh.experiments;

import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class WorkloadToHexStringTest {
    private final double input = WorkloadToHexString.INPUT;
    private final String expected = WorkloadToHexString.OUTPUT;

    @Test
    public void testRunWorkloadOnce() {
        String result = WorkloadToHexString.runWorkload(input);

        assertEquals(expected, result);
    }

    @Test
    public void testRunWorkloadTwice() {
        String result1 = WorkloadToHexString.runWorkload(input);
        String result2 = WorkloadToHexString.runWorkload(input);

        assertEquals(expected, result1);
        assertEquals(expected, result2);
    }

    @Test
    public void testRunWorkloadThrice() {
        String result1 = WorkloadToHexString.runWorkload(input);
        String result2 = WorkloadToHexString.runWorkload(input);
        String result3 = WorkloadToHexString.runWorkload(input);

        assertEquals(expected, result1);
        assertEquals(expected, result2);
        assertEquals(expected, result3);
    }
}
