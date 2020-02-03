package se.chalmers.ju2jmh.experiments.workloads;

import org.junit.runner.JUnitCore;
import org.junit.runner.Request;
import org.junit.runner.Result;
import org.openjdk.jmh.annotations.Benchmark;
import org.openjdk.jmh.annotations.Scope;
import org.openjdk.jmh.annotations.State;

@State(Scope.Thread)
public class ToHexStringTest_JU4Benchmark {

    private Class<?> testClass = ToHexStringTest.class;

    private JUnitCore runner = new JUnitCore();

    private Result runBenchmark(String benchmark) {
        return this.runner.run(Request.method(this.testClass, benchmark));
    }

    @Benchmark
    public Result benchmark_testRunWorkloadOnce() {
        return this.runBenchmark("testRunWorkloadOnce");
    }

    @Benchmark
    public Result benchmark_testRunWorkloadTwice() {
        return this.runBenchmark("testRunWorkloadTwice");
    }

    @Benchmark
    public Result benchmark_testRunWorkloadThrice() {
        return this.runBenchmark("testRunWorkloadThrice");
    }
}
