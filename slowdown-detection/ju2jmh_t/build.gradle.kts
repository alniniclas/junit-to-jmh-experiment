plugins {
    java
    id("me.champeau.jmh") version "0.6.6"
}

dependencies {
    val jUnit4Version: String by rootProject.extra
    val javaparserVersion: String by rootProject.extra

    jmh(project(":main"))
    jmh("junit", "junit", jUnit4Version)
    jmh("com.github.javaparser", "javaparser-core", javaparserVersion)
}
