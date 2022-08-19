plugins {
    java
    id("me.champeau.jmh") version "0.6.6"
}

dependencies {
    val jUnit4Version: String by rootProject.extra

    jmh(project(":main"))
    jmh(project(":main", "testArchive"))
    jmh("junit", "junit", jUnit4Version)
}
