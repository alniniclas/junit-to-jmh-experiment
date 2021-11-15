package se.chalmers.ju2jmh.api;

@FunctionalInterface
public interface ThrowingConsumer<T> {
    void accept(T t) throws Throwable;
}