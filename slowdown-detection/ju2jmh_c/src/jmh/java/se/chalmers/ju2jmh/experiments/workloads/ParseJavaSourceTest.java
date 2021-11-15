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

        private ParseJavaSourceTest instance;

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

        private void runBenchmark(se.chalmers.ju2jmh.api.ThrowingConsumer<ParseJavaSourceTest> payload) throws java.lang.Throwable {
            this.instance = new ParseJavaSourceTest();
            payload.accept(this.instance);
        }

        @org.openjdk.jmh.annotations.State(org.openjdk.jmh.annotations.Scope.Benchmark)
        public static class _Payloads {

            public se.chalmers.ju2jmh.api.ThrowingConsumer<ParseJavaSourceTest> testRunWorkloadOnce;

            public se.chalmers.ju2jmh.api.ThrowingConsumer<ParseJavaSourceTest> testRunWorkloadTwice;

            public se.chalmers.ju2jmh.api.ThrowingConsumer<ParseJavaSourceTest> testRunWorkloadThrice;
        }

        @org.openjdk.jmh.annotations.Setup(org.openjdk.jmh.annotations.Level.Trial)
        public void makePayloads(_Payloads payloads) {
            payloads.testRunWorkloadOnce = ParseJavaSourceTest::testRunWorkloadOnce;
            payloads.testRunWorkloadTwice = ParseJavaSourceTest::testRunWorkloadTwice;
            payloads.testRunWorkloadThrice = ParseJavaSourceTest::testRunWorkloadThrice;
        }
    }
}
