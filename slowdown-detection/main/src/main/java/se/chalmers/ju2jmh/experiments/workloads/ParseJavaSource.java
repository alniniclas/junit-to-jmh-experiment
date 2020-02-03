package se.chalmers.ju2jmh.experiments.workloads;

import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;

public class ParseJavaSource {
    public static final String INPUT = String.join("\n",
            "package com.example;",
            "",
            "public class Main {",
            "",
            "    public static void main(String[] args) {",
            "        System.out.println(\"Hello World!\");",
            "    }",
            "}"
    );
    private static final CompilationUnit OUTPUT = runWorkload(INPUT);

    public static CompilationUnit getOutput() {
        return OUTPUT.clone();
    }

    public static CompilationUnit runWorkload(String input) {
        return StaticJavaParser.parse(input);
    }
}
