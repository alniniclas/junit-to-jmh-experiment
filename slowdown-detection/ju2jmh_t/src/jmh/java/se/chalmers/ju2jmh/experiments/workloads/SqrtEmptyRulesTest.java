package se.chalmers.ju2jmh.experiments.workloads;

import org.junit.ClassRule;
import org.junit.Rule;
import org.junit.rules.TestRule;

public class SqrtEmptyRulesTest extends SqrtTest {

    @ClassRule
    public static final TestRule emptyClassRuleField = EmptyTestRule.INSTANCE;

    @ClassRule
    public static TestRule emptyClassRuleMethod() {
        return EmptyTestRule.INSTANCE;
    }

    @Rule
    public final TestRule emptyRuleField = EmptyTestRule.INSTANCE;

    @Rule
    public TestRule emptyRuleMethod() {
        return EmptyTestRule.INSTANCE;
    }

    @org.openjdk.jmh.annotations.State(org.openjdk.jmh.annotations.Scope.Thread)
    public static class _Benchmark {

        private _Payloads payloads;

        private SqrtEmptyRulesTest instance;

        @org.openjdk.jmh.annotations.Benchmark
        public void benchmark_testRunWorkloadOnce() throws java.lang.Throwable {
            this.payloads.testRunWorkloadOnce.evaluate();
        }

        @org.openjdk.jmh.annotations.Benchmark
        public void benchmark_testRunWorkloadTwice() throws java.lang.Throwable {
            this.payloads.testRunWorkloadTwice.evaluate();
        }

        @org.openjdk.jmh.annotations.Benchmark
        public void benchmark_testRunWorkloadThrice() throws java.lang.Throwable {
            this.payloads.testRunWorkloadThrice.evaluate();
        }

        private static class _InstanceStatement extends org.junit.runners.model.Statement {

            private final se.chalmers.ju2jmh.api.ThrowingConsumer<SqrtEmptyRulesTest> payload;

            private final _Benchmark benchmark;

            public _InstanceStatement(se.chalmers.ju2jmh.api.ThrowingConsumer<SqrtEmptyRulesTest> payload, _Benchmark benchmark) {
                this.payload = payload;
                this.benchmark = benchmark;
            }

            @java.lang.Override
            public void evaluate() throws java.lang.Throwable {
                this.payload.accept(this.benchmark.instance);
            }
        }

        private static class _ClassStatement extends org.junit.runners.model.Statement {

            private final se.chalmers.ju2jmh.api.ThrowingConsumer<SqrtEmptyRulesTest> payload;

            private final _Benchmark benchmark;

            private final org.junit.runner.Description description;

            private final org.junit.runners.model.FrameworkMethod frameworkMethod;

            private _ClassStatement(se.chalmers.ju2jmh.api.ThrowingConsumer<SqrtEmptyRulesTest> payload, _Benchmark benchmark, org.junit.runner.Description description, org.junit.runners.model.FrameworkMethod frameworkMethod) {
                this.payload = payload;
                this.benchmark = benchmark;
                this.description = description;
                this.frameworkMethod = frameworkMethod;
            }

            @java.lang.Override
            public void evaluate() throws java.lang.Throwable {
                this.benchmark.instance = new SqrtEmptyRulesTest();
                org.junit.runners.model.Statement statement = new _InstanceStatement(this.payload, this.benchmark);
                statement = this.applyRule(this.benchmark.instance.emptyRuleField, statement);
                statement = this.applyRule(this.benchmark.instance.emptyRuleMethod(), statement);
                statement.evaluate();
            }

            private org.junit.runners.model.Statement applyRule(org.junit.rules.TestRule rule, org.junit.runners.model.Statement statement) {
                return se.chalmers.ju2jmh.api.Rules.apply(rule, statement, this.description);
            }

            private org.junit.runners.model.Statement applyRule(org.junit.rules.MethodRule rule, org.junit.runners.model.Statement statement) {
                return se.chalmers.ju2jmh.api.Rules.apply(rule, statement, this.frameworkMethod, this.benchmark.instance);
            }

            private static class _ApplyClassRulesStatement extends org.junit.runners.model.Statement {

                private final org.junit.runners.model.Statement statement;

                private final org.junit.runner.Description description;

                public _ApplyClassRulesStatement(org.junit.runners.model.Statement statement, org.junit.runner.Description description) {
                    this.statement = statement;
                    this.description = description;
                }

                @java.lang.Override
                public void evaluate() throws java.lang.Throwable {
                    org.junit.runners.model.Statement statement = this.statement;
                    statement = se.chalmers.ju2jmh.api.Rules.apply(SqrtEmptyRulesTest.emptyClassRuleField, statement, this.description);
                    statement = se.chalmers.ju2jmh.api.Rules.apply(SqrtEmptyRulesTest.emptyClassRuleMethod(), statement, this.description);
                    statement.evaluate();
                }
            }

            public static org.junit.runners.model.Statement forPayload(se.chalmers.ju2jmh.api.ThrowingConsumer<SqrtEmptyRulesTest> payload, String name, _Benchmark benchmark) {
                org.junit.runner.Description description = se.chalmers.ju2jmh.api.Rules.description(SqrtEmptyRulesTest.class, name);
                org.junit.runners.model.FrameworkMethod frameworkMethod = se.chalmers.ju2jmh.api.Rules.frameworkMethod(SqrtEmptyRulesTest.class, name);
                org.junit.runners.model.Statement statement = new _ClassStatement(payload, benchmark, description, frameworkMethod);
                statement = new _ApplyClassRulesStatement(statement, description);
                return statement;
            }
        }

        private static class _Payloads {

            public org.junit.runners.model.Statement testRunWorkloadOnce;

            public org.junit.runners.model.Statement testRunWorkloadTwice;

            public org.junit.runners.model.Statement testRunWorkloadThrice;
        }

        @org.openjdk.jmh.annotations.Setup(org.openjdk.jmh.annotations.Level.Trial)
        public void makePayloads() {
            this.payloads = new _Payloads();
            this.payloads.testRunWorkloadOnce = _ClassStatement.forPayload(SqrtEmptyRulesTest::testRunWorkloadOnce, "testRunWorkloadOnce", this);
            this.payloads.testRunWorkloadTwice = _ClassStatement.forPayload(SqrtEmptyRulesTest::testRunWorkloadTwice, "testRunWorkloadTwice", this);
            this.payloads.testRunWorkloadThrice = _ClassStatement.forPayload(SqrtEmptyRulesTest::testRunWorkloadThrice, "testRunWorkloadThrice", this);
        }
    }
}
