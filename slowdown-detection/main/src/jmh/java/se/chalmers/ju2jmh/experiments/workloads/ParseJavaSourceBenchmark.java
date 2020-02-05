package se.chalmers.ju2jmh.experiments.workloads;

import com.github.javaparser.ast.CompilationUnit;
import org.openjdk.jmh.annotations.Benchmark;
import org.openjdk.jmh.annotations.Scope;
import org.openjdk.jmh.annotations.State;
import org.openjdk.jmh.infra.Blackhole;

@State(Scope.Thread)
public class ParseJavaSourceBenchmark {
    private String input = ParseJavaSource.INPUT;

    @Benchmark
    public void benchmarkRunWorkloadOnce(Blackhole blackhole) {
        CompilationUnit result = ParseJavaSource.runWorkload(input);

        blackhole.consume(result);
    }

    @Benchmark
    public void benchmarkRunWorkloadTwice(Blackhole blackhole) {
        CompilationUnit result1 = ParseJavaSource.runWorkload(input);
        CompilationUnit result2 = ParseJavaSource.runWorkload(input);

        blackhole.consume(result1);
        blackhole.consume(result2);
    }

    @Benchmark
    public void benchmarkRunWorkloadThrice(Blackhole blackhole) {
        CompilationUnit result1 = ParseJavaSource.runWorkload(input);
        CompilationUnit result2 = ParseJavaSource.runWorkload(input);
        CompilationUnit result3 = ParseJavaSource.runWorkload(input);

        blackhole.consume(result1);
        blackhole.consume(result2);
        blackhole.consume(result3);
    }
}
