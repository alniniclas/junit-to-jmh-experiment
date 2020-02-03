package se.chalmers.ju2jmh.experiments.workloads;

import org.junit.rules.TestRule;
import org.junit.runner.Description;
import org.junit.runners.model.Statement;

public class EmptyTestRule implements TestRule {

    public static EmptyTestRule INSTANCE = new EmptyTestRule();

    @Override
    public Statement apply(Statement base, Description description) {
        return base;
    }
}
