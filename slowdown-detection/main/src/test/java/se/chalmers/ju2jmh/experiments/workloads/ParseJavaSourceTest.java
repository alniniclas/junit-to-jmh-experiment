package se.chalmers.ju2jmh.experiments.workloads;

import com.github.javaparser.ast.CompilationUnit;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class ParseJavaSourceTest {
    private final String input = ParseJavaSource.INPUT;
    private final CompilationUnit expected = ParseJavaSource.getOutput();

    @Test
    public void testRunWorkloadOnce() {
        CompilationUnit result = ParseJavaSource.runWorkload(input);

        assertEquals(expected, result);
    }

    @Test
    public void testRunWorkloadTwice() {
        CompilationUnit result1 = ParseJavaSource.runWorkload(input);
        CompilationUnit result2 = ParseJavaSource.runWorkload(input);

        assertEquals(expected, result1);
        assertEquals(expected, result2);
    }

    @Test
    public void testRunWorkloadThrice() {
        CompilationUnit result1 = ParseJavaSource.runWorkload(input);
        CompilationUnit result2 = ParseJavaSource.runWorkload(input);
        CompilationUnit result3 = ParseJavaSource.runWorkload(input);

        assertEquals(expected, result1);
        assertEquals(expected, result2);
        assertEquals(expected, result3);
    }
}
