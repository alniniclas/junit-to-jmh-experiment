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

        private SqrtEmptyFixturesTest instance;

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

        @org.openjdk.jmh.annotations.State(org.openjdk.jmh.annotations.Scope.Benchmark)
        public static class _Payloads {

            public se.chalmers.ju2jmh.api.ThrowingConsumer<SqrtEmptyFixturesTest> testRunWorkloadOnce;

            public se.chalmers.ju2jmh.api.ThrowingConsumer<SqrtEmptyFixturesTest> testRunWorkloadTwice;

            public se.chalmers.ju2jmh.api.ThrowingConsumer<SqrtEmptyFixturesTest> testRunWorkloadThrice;
        }

        @org.openjdk.jmh.annotations.Setup(org.openjdk.jmh.annotations.Level.Trial)
        public void makePayloads(_Payloads payloads) {
            payloads.testRunWorkloadOnce = SqrtEmptyFixturesTest::testRunWorkloadOnce;
            payloads.testRunWorkloadTwice = SqrtEmptyFixturesTest::testRunWorkloadTwice;
            payloads.testRunWorkloadThrice = SqrtEmptyFixturesTest::testRunWorkloadThrice;
        }
    }
}
