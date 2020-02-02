plugins {
    java
    id("me.champeau.gradle.jmh") version "0.5.0"
}

dependencies {
    val jUnit4Version: String by rootProject.extra

    jmh(project(":main", "testArchive"))
    jmh("junit", "junit", jUnit4Version)
}
