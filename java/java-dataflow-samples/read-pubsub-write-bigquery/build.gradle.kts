plugins {
    application
    id("com.diffplug.spotless") version "6.8.0"
}

group = "com.cloudcode.dataflow"
version = "0.0.1"

val mainClassName = "ReadPubsubWriteBigQuery"

val autoValueVersion = "1.11.0"
val beamVersion = "2.45.0"
val jupiterVersion = "5.9.0"
val mockitoVersion = "5.1.1"
val slf4jVersion = "1.7.32"

spotless {
    java {
        importOrder()
        removeUnusedImports()
        googleJavaFormat()
    }
}

repositories {
    mavenCentral()
    maven {
        // Required for Beam to resolve confluent dependency error
        url = uri("https://packages.confluent.io/maven/")
    }
}

dependencies {
    implementation(platform("org.apache.beam:beam-sdks-java-bom:$beamVersion"))
    implementation("org.apache.beam:beam-runners-direct-java")
    implementation("org.apache.beam:beam-runners-google-cloud-dataflow-java")
    implementation("org.apache.beam:beam-sdks-java-io-google-cloud-platform")

    implementation("org.slf4j:slf4j-jdk14:$slf4jVersion")

    compileOnly("com.google.auto.value:auto-value-annotations:$autoValueVersion")
    annotationProcessor("com.google.auto.value:auto-value:$autoValueVersion")

    testImplementation("org.junit.jupiter:junit-jupiter-api:$jupiterVersion")
    testImplementation("org.junit.jupiter:junit-jupiter-params:$jupiterVersion")
    testRuntimeOnly("org.junit.jupiter:junit-jupiter-engine")

    testCompileOnly("com.google.auto.value:auto-value-annotations:$autoValueVersion")
    testAnnotationProcessor("com.google.auto.value:auto-value:$autoValueVersion")
}

tasks.named<Test>("test") {
    useJUnitPlatform()
    testLogging {
        setEvents(mutableListOf("PASSED", "SKIPPED", "FAILED"))
    }
}

val usePublicIps = false
val runner = "dataflow"
val subscription: String? by project
val dataset: String? by project
val projectId: String? by project
val region: String? by project
val network: String? by project
val subnetwork: String? by project
val serviceAccountEmail: String? by project
val tempLocation: String? by project
val labels = "{\"cloud-code-sample\": \"${project.name}\"}"

tasks.named<JavaExec>("run") {
    mainClass.set("${project.group}.$mainClassName")
    args = listOf(
            "--usePublicIps=$usePublicIps",
            "--runner=$runner",
            "--subscription=$subscription",
            "--dataset=$dataset",
            "--project=$projectId",
            "--region=$region",
            "--network=$network",
            "--subnetwork=regions/$region/subnetworks/$subnetwork",
            "--serviceAccount=$serviceAccountEmail",
            "--tempLocation=$tempLocation",
            "--streaming=true",
            "--labels=$labels",
    )
}
