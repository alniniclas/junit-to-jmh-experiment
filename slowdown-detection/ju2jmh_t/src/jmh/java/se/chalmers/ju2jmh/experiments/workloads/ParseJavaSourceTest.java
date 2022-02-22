package se.chalmers.ju2jmh.experiments.workloads;

import com.github.javaparser.ast.CompilationUnit;
import org.junit.Test;
import static org.junit.Assert.assertEquals;

public class ParseJavaSourceTest {

    private String input = ParseJavaSource.INPUT;

    private CompilationUnit expected = ParseJavaSource.getOutput();

    @Test
    public void testRunWorkloadOnce() {
        CompilationUnit result = ParseJavaSource.runWorkload(input);
        assertEquals(expected, result);
    }

    @Test
    public void testRunWorkloadTwice() {
        CompilationUnit result1 = ParseJavaSource.runWorkload(input);
        CompilationUnit result2 = ParseJavaSource.runWorkload(input);
        assertEquals(expected, result1);
        assertEquals(expected, result2);
    }

    @Test
    public void testRunWorkloadThrice() {
        CompilationUnit result1 = ParseJavaSource.runWorkload(input);
        CompilationUnit result2 = ParseJavaSource.runWorkload(input);
        CompilationUnit result3 = ParseJavaSource.runWorkload(input);
        assertEquals(expected, result1);
        assertEquals(expected, result2);
        assertEquals(expected, result3);
    }

    @org.openjdk.jmh.annotations.State(org.openjdk.jmh.annotations.Scope.Thread)
    public static class _Benchmark {

        private _Payloads payloads;

        private ParseJavaSourceTest instance;

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

        private void runBenchmark(se.chalmers.ju2jmh.api.ThrowingConsumer<ParseJavaSourceTest> payload) throws java.lang.Throwable {
            this.instance = new ParseJavaSourceTest();
            payload.accept(this.instance);
        }

        private static class _Payloads {

            public se.chalmers.ju2jmh.api.ThrowingConsumer<ParseJavaSourceTest> testRunWorkloadOnce;

            public se.chalmers.ju2jmh.api.ThrowingConsumer<ParseJavaSourceTest> testRunWorkloadTwice;

            public se.chalmers.ju2jmh.api.ThrowingConsumer<ParseJavaSourceTest> testRunWorkloadThrice;
        }

        @org.openjdk.jmh.annotations.Setup(org.openjdk.jmh.annotations.Level.Trial)
        public void makePayloads() {
            this.payloads = new _Payloads();
            this.payloads.testRunWorkloadOnce = ParseJavaSourceTest::testRunWorkloadOnce;
            this.payloads.testRunWorkloadTwice = ParseJavaSourceTest::testRunWorkloadTwice;
            this.payloads.testRunWorkloadThrice = ParseJavaSourceTest::testRunWorkloadThrice;
        }
    }
}
