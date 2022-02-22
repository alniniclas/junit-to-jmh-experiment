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

        private _Payloads payloads;

        private SqrtTest instance;

        @org.openjdk.jmh.annotations.Benchmark
        public void benchmark_testRunWorkloadOnce() throws java.lang.Throwable {
            this.runBenchmark(this.payloads.testRunWorkloadOnce);
        }

        @org.openjdk.jmh.annotations.Benchmark
        public void benchmark_testRunWorkloadTwice() throws java.lang.Throwable {
            this.runBenchmark(this.payloads.testRunWorkloadTwice);
        }

        @org.openjdk.jmh.annotations.Benchmark
        public void benchmark_testRunWorkloadThrice() throws java.lang.Throwable {
            this.runBenchmark(this.payloads.testRunWorkloadThrice);
        }

        private void runBenchmark(se.chalmers.ju2jmh.api.ThrowingConsumer<SqrtTest> payload) throws java.lang.Throwable {
            this.instance = new SqrtTest();
            payload.accept(this.instance);
        }

        private static class _Payloads {

            public se.chalmers.ju2jmh.api.ThrowingConsumer<SqrtTest> testRunWorkloadOnce;

            public se.chalmers.ju2jmh.api.ThrowingConsumer<SqrtTest> testRunWorkloadTwice;

            public se.chalmers.ju2jmh.api.ThrowingConsumer<SqrtTest> testRunWorkloadThrice;
        }

        @org.openjdk.jmh.annotations.Setup(org.openjdk.jmh.annotations.Level.Trial)
        public void makePayloads() {
            this.payloads = new _Payloads();
            this.payloads.testRunWorkloadOnce = SqrtTest::testRunWorkloadOnce;
            this.payloads.testRunWorkloadTwice = SqrtTest::testRunWorkloadTwice;
            this.payloads.testRunWorkloadThrice = SqrtTest::testRunWorkloadThrice;
        }
    }
}
