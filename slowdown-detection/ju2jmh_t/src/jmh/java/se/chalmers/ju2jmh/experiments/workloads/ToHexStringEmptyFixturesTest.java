package se.chalmers.ju2jmh.experiments.workloads;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;

public class ToHexStringEmptyFixturesTest extends ToHexStringTest {

    @BeforeClass
    public static void emptyBeforeClass() {
    }

    @AfterClass
    public static void emptyAfterClass() {
    }

    @Before
    public void emptyBefore() {
    }

    @After
    public void emptyAfter() {
    }

    @org.openjdk.jmh.annotations.State(org.openjdk.jmh.annotations.Scope.Thread)
    public static class _Benchmark {

        private _Payloads payloads;

        private ToHexStringEmptyFixturesTest instance;

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

        private void runBenchmark(se.chalmers.ju2jmh.api.ThrowingConsumer<ToHexStringEmptyFixturesTest> payload) throws java.lang.Throwable {
            ToHexStringEmptyFixturesTest.emptyBeforeClass();
            try {
                this.instance = new ToHexStringEmptyFixturesTest();
                this.instance.emptyBefore();
                try {
                    payload.accept(this.instance);
                } finally {
                    this.instance.emptyAfter();
                }
            } finally {
                ToHexStringEmptyFixturesTest.emptyAfterClass();
            }
        }

        private static class _Payloads {

            public se.chalmers.ju2jmh.api.ThrowingConsumer<ToHexStringEmptyFixturesTest> testRunWorkloadOnce;

            public se.chalmers.ju2jmh.api.ThrowingConsumer<ToHexStringEmptyFixturesTest> testRunWorkloadTwice;

            public se.chalmers.ju2jmh.api.ThrowingConsumer<ToHexStringEmptyFixturesTest> testRunWorkloadThrice;
        }

        @org.openjdk.jmh.annotations.Setup(org.openjdk.jmh.annotations.Level.Trial)
        public void makePayloads() {
            this.payloads = new _Payloads();
            this.payloads.testRunWorkloadOnce = ToHexStringEmptyFixturesTest::testRunWorkloadOnce;
            this.payloads.testRunWorkloadTwice = ToHexStringEmptyFixturesTest::testRunWorkloadTwice;
            this.payloads.testRunWorkloadThrice = ToHexStringEmptyFixturesTest::testRunWorkloadThrice;
        }
    }
}
