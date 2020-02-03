package se.chalmers.ju2jmh.experiments.workloads;

import org.junit.Rule;
import org.junit.rules.TestRule;
import org.junit.rules.Timeout;

public class SqrtTimeoutRuleTest extends SqrtTest {
    @Rule
    public final TestRule emptyRuleField = Timeout.seconds(60);
}
