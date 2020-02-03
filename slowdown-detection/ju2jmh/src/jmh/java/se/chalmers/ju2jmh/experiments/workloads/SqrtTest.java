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

        private SqrtTest implementation;

        @java.lang.Override
        public void createImplementation() throws java.lang.Throwable {
            this.implementation = new SqrtTest();
        }

        @java.lang.Override
        public SqrtTest implementation() {
            return this.implementation;
        }
    }
}
