package se.chalmers.ju2jmh.api;

import org.junit.rules.MethodRule;
import org.junit.rules.TestRule;
import org.junit.rules.Timeout;
import org.junit.runner.Description;
import org.junit.runners.model.FrameworkMethod;
import org.junit.runners.model.Statement;

public class Rules {
    private Rules() {
        throw new AssertionError("Should not be instantiated.");
    }

    public static Statement apply(TestRule rule, Statement statement,  Description description) {
        if (rule.getClass() == Timeout.class) {
            return statement;
        }
        return rule.apply(statement, description);
    }

    public static <T> Statement apply(
            MethodRule rule, Statement statement, FrameworkMethod method, T target) {
        return rule.apply(statement, method, target);
    }

    public static Description description(Class<?> clazz, String name) {
        return Description.createTestDescription(clazz, name);
    }

    public static FrameworkMethod frameworkMethod(Class<?> clazz, String name) {
        try {
            return new FrameworkMethod(clazz.getMethod(name));
        } catch (NoSuchMethodException e) {
            throw new RuntimeException(e);
        }
    }
}
