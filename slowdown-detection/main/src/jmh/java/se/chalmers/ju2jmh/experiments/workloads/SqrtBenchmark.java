package se.chalmers.ju2jmh.experiments.workloads;

import org.openjdk.jmh.annotations.Benchmark;
import org.openjdk.jmh.annotations.Scope;
import org.openjdk.jmh.annotations.State;
import org.openjdk.jmh.infra.Blackhole;

@State(Scope.Thread)
public class SqrtBenchmark {
    private double input = Sqrt.INPUT;

    @Benchmark
    public void benchmarkRunWorkloadOnce(Blackhole blackhole) {
        double result = Sqrt.runWorkload(input);

        blackhole.consume(result);
    }

    @Benchmark
    public void benchmarkRunWorkloadTwice(Blackhole blackhole) {
        double result1 = Sqrt.runWorkload(input);
        double result2 = Sqrt.runWorkload(input);

        blackhole.consume(result1);
        blackhole.consume(result2);
    }

    @Benchmark
    public void benchmarkRunWorkloadThrice(Blackhole blackhole) {
        double result1 = Sqrt.runWorkload(input);
        double result2 = Sqrt.runWorkload(input);
        double result3 = Sqrt.runWorkload(input);

        blackhole.consume(result1);
        blackhole.consume(result2);
        blackhole.consume(result3);
    }
}
