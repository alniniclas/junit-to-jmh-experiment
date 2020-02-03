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

    @org.openjdk.jmh.annotations.State(org.openjdk.jmh.annotations.Scope.Thread)
    public static class _Benchmark extends se.chalmers.ju2jmh.api.JU2JmhBenchmark {

        @org.openjdk.jmh.annotations.Benchmark
        public void benchmark_testRunWorkloadOnce() throws java.lang.Throwable {
            this.createImplementation();
            this.runBenchmark(this.implementation()::testRunWorkloadOnce, this.description("testRunWorkloadOnce"));
        }

        @org.openjdk.jmh.annotations.Benchmark
        public void benchmark_testRunWorkloadTwice() throws java.lang.Throwable {
            this.createImplementation();
            this.runBenchmark(this.implementation()::testRunWorkloadTwice, this.description("testRunWorkloadTwice"));
        }

        @org.openjdk.jmh.annotations.Benchmark
        public void benchmark_testRunWorkloadThrice() throws java.lang.Throwable {
            this.createImplementation();
            this.runBenchmark(this.implementation()::testRunWorkloadThrice, this.description("testRunWorkloadThrice"));
        }

        private ToHexStringTest implementation;

        @java.lang.Override
        public void createImplementation() throws java.lang.Throwable {
            this.implementation = new ToHexStringTest();
        }

        @java.lang.Override
        public ToHexStringTest implementation() {
            return this.implementation;
        }
    }
}
