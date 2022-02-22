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
    public static class _Benchmark {

        private _Payloads payloads;

        private ToHexStringTest instance;

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

        private void runBenchmark(se.chalmers.ju2jmh.api.ThrowingConsumer<ToHexStringTest> payload) throws java.lang.Throwable {
            this.instance = new ToHexStringTest();
            payload.accept(this.instance);
        }

        private static class _Payloads {

            public se.chalmers.ju2jmh.api.ThrowingConsumer<ToHexStringTest> testRunWorkloadOnce;

            public se.chalmers.ju2jmh.api.ThrowingConsumer<ToHexStringTest> testRunWorkloadTwice;

            public se.chalmers.ju2jmh.api.ThrowingConsumer<ToHexStringTest> testRunWorkloadThrice;
        }

        @org.openjdk.jmh.annotations.Setup(org.openjdk.jmh.annotations.Level.Trial)
        public void makePayloads() {
            this.payloads = new _Payloads();
            this.payloads.testRunWorkloadOnce = ToHexStringTest::testRunWorkloadOnce;
            this.payloads.testRunWorkloadTwice = ToHexStringTest::testRunWorkloadTwice;
            this.payloads.testRunWorkloadThrice = ToHexStringTest::testRunWorkloadThrice;
        }
    }
}
