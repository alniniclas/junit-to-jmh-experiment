package se.chalmers.ju2jmh.api;

public class ExceptionTest<T> implements ThrowingConsumer<T> {
    private final ThrowingConsumer<T> test;
    private final Class<? extends Throwable> expected;

    public ExceptionTest(ThrowingConsumer<T> test,
            Class<? extends Throwable> expected) {
        this.test = test;
        this.expected = expected;
    }

    @Override
    public void accept(T t) throws Throwable {
        try {
            test.accept(t);
        } catch (Throwable e) {
            if (expected.isInstance(e)) {
                return;
            }
            throw e;
        }
        throw new AssertionError(
                "Expected " + expected.getCanonicalName() + " but none was thrown");
    }
}
