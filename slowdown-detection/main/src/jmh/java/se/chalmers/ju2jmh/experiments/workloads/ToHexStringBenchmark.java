package se.chalmers.ju2jmh.experiments.workloads;

import org.openjdk.jmh.annotations.Benchmark;
import org.openjdk.jmh.annotations.Scope;
import org.openjdk.jmh.annotations.State;
import org.openjdk.jmh.infra.Blackhole;

@State(Scope.Thread)
public class ToHexStringBenchmark {
    private double input = ToHexString.INPUT;

    @Benchmark
    public void benchmarkRunWorkloadOnce(Blackhole blackhole) {
        String result = ToHexString.runWorkload(input);

        blackhole.consume(result);
    }

    @Benchmark
    public void benchmarkRunWorkloadTwice(Blackhole blackhole) {
        String result1 = ToHexString.runWorkload(input);
        String result2 = ToHexString.runWorkload(input);

        blackhole.consume(result1);
        blackhole.consume(result2);
    }

    @Benchmark
    public void benchmarkRunWorkloadThrice(Blackhole blackhole) {
        String result1 = ToHexString.runWorkload(input);
        String result2 = ToHexString.runWorkload(input);
        String result3 = ToHexString.runWorkload(input);

        blackhole.consume(result1);
        blackhole.consume(result2);
        blackhole.consume(result3);
    }
}
