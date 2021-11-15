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
    public static class _Benchmark {

        private SqrtTest instance;

        @org.openjdk.jmh.annotations.Benchmark
        public void benchmark_testRunWorkloadOnce(_Payloads payloads) throws java.lang.Throwable {
            this.runBenchmark(payloads.testRunWorkloadOnce);
        }

        @org.openjdk.jmh.annotations.Benchmark
        public void benchmark_testRunWorkloadTwice(_Payloads payloads) throws java.lang.Throwable {
            this.runBenchmark(payloads.testRunWorkloadTwice);
        }

        @org.openjdk.jmh.annotations.Benchmark
        public void benchmark_testRunWorkloadThrice(_Payloads payloads) throws java.lang.Throwable {
            this.runBenchmark(payloads.testRunWorkloadThrice);
        }

        private void runBenchmark(se.chalmers.ju2jmh.api.ThrowingConsumer<SqrtTest> payload) throws java.lang.Throwable {
            this.instance = new SqrtTest();
            payload.accept(this.instance);
        }

        @org.openjdk.jmh.annotations.State(org.openjdk.jmh.annotations.Scope.Benchmark)
        public static class _Payloads {

            public se.chalmers.ju2jmh.api.ThrowingConsumer<SqrtTest> testRunWorkloadOnce;

            public se.chalmers.ju2jmh.api.ThrowingConsumer<SqrtTest> testRunWorkloadTwice;

            public se.chalmers.ju2jmh.api.ThrowingConsumer<SqrtTest> testRunWorkloadThrice;
        }

        @org.openjdk.jmh.annotations.Setup(org.openjdk.jmh.annotations.Level.Trial)
        public void makePayloads(_Payloads payloads) {
            payloads.testRunWorkloadOnce = SqrtTest::testRunWorkloadOnce;
            payloads.testRunWorkloadTwice = SqrtTest::testRunWorkloadTwice;
            payloads.testRunWorkloadThrice = SqrtTest::testRunWorkloadThrice;
        }
    }
}
