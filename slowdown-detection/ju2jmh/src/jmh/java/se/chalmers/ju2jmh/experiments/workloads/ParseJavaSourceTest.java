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

        private ParseJavaSourceTest implementation;

        @java.lang.Override
        public void createImplementation() throws java.lang.Throwable {
            this.implementation = new ParseJavaSourceTest();
        }

        @java.lang.Override
        public ParseJavaSourceTest implementation() {
            return this.implementation;
        }
    }
}
