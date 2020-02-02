plugins {
    java
}

dependencies {
    val jUnit4Version: String by rootProject.extra
    val javaparserVersion: String by rootProject.extra

    implementation("junit", "junit", jUnit4Version)
    implementation("com.github.javaparser", "javaparser-core", javaparserVersion)

    testImplementation("junit", "junit", jUnit4Version)
}

configurations.register("testArchive") {
    extendsFrom(configurations.testCompile.get())
}

tasks.register<Jar>(name = "jarTest") {
    from(project.sourceSets.test.get().output)
    archiveClassifier.set("test")
}

artifacts {
    add("testArchive", tasks.getByName("jarTest"))
}