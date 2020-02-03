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
    public static class _Benchmark extends se.chalmers.ju2jmh.experiments.workloads.SqrtTest._Benchmark {

        @java.lang.Override
        public org.junit.runners.model.Statement applyClassRuleFields(org.junit.runners.model.Statement statement, org.junit.runner.Description description) {
            statement = this.applyRule(SqrtEmptyRulesTest.emptyClassRuleField, statement, description);
            statement = super.applyClassRuleFields(statement, description);
            return statement;
        }

        @java.lang.Override
        public org.junit.runners.model.Statement applyClassRuleMethods(org.junit.runners.model.Statement statement, org.junit.runner.Description description) {
            statement = this.applyRule(SqrtEmptyRulesTest.emptyClassRuleMethod(), statement, description);
            statement = super.applyClassRuleMethods(statement, description);
            return statement;
        }

        @java.lang.Override
        public org.junit.runners.model.Statement applyRuleFields(org.junit.runners.model.Statement statement, org.junit.runner.Description description) {
            statement = this.applyRule(this.implementation().emptyRuleField, statement, description);
            statement = super.applyRuleFields(statement, description);
            return statement;
        }

        @java.lang.Override
        public org.junit.runners.model.Statement applyRuleMethods(org.junit.runners.model.Statement statement, org.junit.runner.Description description) {
            statement = this.applyRule(this.implementation().emptyRuleMethod(), statement, description);
            statement = super.applyRuleMethods(statement, description);
            return statement;
        }

        private SqrtEmptyRulesTest implementation;

        @java.lang.Override
        public void createImplementation() throws java.lang.Throwable {
            this.implementation = new SqrtEmptyRulesTest();
        }

        @java.lang.Override
        public SqrtEmptyRulesTest implementation() {
            return this.implementation;
        }
    }
}
