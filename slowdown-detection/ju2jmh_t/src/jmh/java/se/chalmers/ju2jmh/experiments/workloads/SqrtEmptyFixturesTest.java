package se.chalmers.ju2jmh.experiments.workloads;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;

public class SqrtEmptyFixturesTest extends SqrtTest {

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

        private SqrtEmptyFixturesTest instance;

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

        private void runBenchmark(se.chalmers.ju2jmh.api.ThrowingConsumer<SqrtEmptyFixturesTest> payload) throws java.lang.Throwable {
            SqrtEmptyFixturesTest.emptyBeforeClass();
            try {
                this.instance = new SqrtEmptyFixturesTest();
                this.instance.emptyBefore();
                try {
                    payload.accept(this.instance);
                } finally {
                    this.instance.emptyAfter();
                }
            } finally {
                SqrtEmptyFixturesTest.emptyAfterClass();
            }
        }

        private static class _Payloads {

            public se.chalmers.ju2jmh.api.ThrowingConsumer<SqrtEmptyFixturesTest> testRunWorkloadOnce;

            public se.chalmers.ju2jmh.api.ThrowingConsumer<SqrtEmptyFixturesTest> testRunWorkloadTwice;

            public se.chalmers.ju2jmh.api.ThrowingConsumer<SqrtEmptyFixturesTest> testRunWorkloadThrice;
        }

        @org.openjdk.jmh.annotations.Setup(org.openjdk.jmh.annotations.Level.Trial)
        public void makePayloads() {
            this.payloads = new _Payloads();
            this.payloads.testRunWorkloadOnce = SqrtEmptyFixturesTest::testRunWorkloadOnce;
            this.payloads.testRunWorkloadTwice = SqrtEmptyFixturesTest::testRunWorkloadTwice;
            this.payloads.testRunWorkloadThrice = SqrtEmptyFixturesTest::testRunWorkloadThrice;
        }
    }
}
