package se.chalmers.ju2jmh.experiments.workloads;

import org.junit.Rule;
import org.junit.rules.TestRule;
import org.junit.rules.Timeout;

public class SqrtTimeoutRuleTest extends SqrtTest {

    @Rule
    public final TestRule emptyRuleField = Timeout.seconds(60);

    @org.openjdk.jmh.annotations.State(org.openjdk.jmh.annotations.Scope.Thread)
    public static class _Benchmark extends se.chalmers.ju2jmh.experiments.workloads.SqrtTest._Benchmark {

        @java.lang.Override
        public org.junit.runners.model.Statement applyRuleFields(org.junit.runners.model.Statement statement, org.junit.runner.Description description) {
            statement = this.applyRule(this.implementation().emptyRuleField, statement, description);
            statement = super.applyRuleFields(statement, description);
            return statement;
        }

        private SqrtTimeoutRuleTest implementation;

        @java.lang.Override
        public void createImplementation() throws java.lang.Throwable {
            this.implementation = new SqrtTimeoutRuleTest();
        }

        @java.lang.Override
        public SqrtTimeoutRuleTest implementation() {
            return this.implementation;
        }
    }
}
