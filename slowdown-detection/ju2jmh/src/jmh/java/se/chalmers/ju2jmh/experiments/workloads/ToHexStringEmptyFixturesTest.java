package se.chalmers.ju2jmh.experiments.workloads;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;

public class ToHexStringEmptyFixturesTest extends ToHexStringTest {

    @BeforeClass
    public static void emptyBeforeClass() {
    }

    @AfterClass
    public static void emptyAfterClass() {
    }

    @Before
    public void emptyBefore() {
    }

    @After
    public void emptyAfter() {
    }

    @org.openjdk.jmh.annotations.State(org.openjdk.jmh.annotations.Scope.Thread)
    public static class _Benchmark extends se.chalmers.ju2jmh.experiments.workloads.ToHexStringTest._Benchmark {

        @java.lang.Override
        public void beforeClass() throws java.lang.Throwable {
            super.beforeClass();
            ToHexStringEmptyFixturesTest.emptyBeforeClass();
        }

        @java.lang.Override
        public void afterClass() throws java.lang.Throwable {
            ToHexStringEmptyFixturesTest.emptyAfterClass();
            super.afterClass();
        }

        @java.lang.Override
        public void before() throws java.lang.Throwable {
            super.before();
            this.implementation().emptyBefore();
        }

        @java.lang.Override
        public void after() throws java.lang.Throwable {
            this.implementation().emptyAfter();
            super.after();
        }

        private ToHexStringEmptyFixturesTest implementation;

        @java.lang.Override
        public void createImplementation() throws java.lang.Throwable {
            this.implementation = new ToHexStringEmptyFixturesTest();
        }

        @java.lang.Override
        public ToHexStringEmptyFixturesTest implementation() {
            return this.implementation;
        }
    }
}
