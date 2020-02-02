package se.chalmers.ju2jmh.experiments;

import com.github.javaparser.ast.CompilationUnit;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class WorkloadParseJavaSourceTest {
    private final String input = WorkloadParseJavaSource.INPUT;
    private final CompilationUnit expected = WorkloadParseJavaSource.getOutput();

    @Test
    public void testRunWorkloadOnce() {
        CompilationUnit result = WorkloadParseJavaSource.runWorkload(input);

        assertEquals(expected, result);
    }

    @Test
    public void testRunWorkloadTwice() {
        CompilationUnit result1 = WorkloadParseJavaSource.runWorkload(input);
        CompilationUnit result2 = WorkloadParseJavaSource.runWorkload(input);

        assertEquals(expected, result1);
        assertEquals(expected, result2);
    }

    @Test
    public void testRunWorkloadThrice() {
        CompilationUnit result1 = WorkloadParseJavaSource.runWorkload(input);
        CompilationUnit result2 = WorkloadParseJavaSource.runWorkload(input);
        CompilationUnit result3 = WorkloadParseJavaSource.runWorkload(input);

        assertEquals(expected, result1);
        assertEquals(expected, result2);
        assertEquals(expected, result3);
    }
}
