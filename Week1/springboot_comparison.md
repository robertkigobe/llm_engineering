Based on the release notes for Spring Boot 4.0 and Spring Boot 3.5, here's a structured comparison of their key differences:

**Spring Boot 4.0 vs. Spring Boot 3.5: Key Differences**

### 1. Java Version Support

* **Spring Boot 4.0**: Supports Java 11, Java 16, and Java 17 as the default JVM version.
	+ Note: While other JVM versions might be available through the `spring-boot-starter-jdk` module, they are not recommended for production use.
* **Spring Boot 3.5**: Supports Java 8, Java 11, Java 14, Java 15, and Java 16 as the default JVM version.

### 2. Tomcat/Server Connection**

* **Spring Boot 4.0**:
	+ Defaulted to using an embedded, secure, and more efficient Tomcat instance (`spring-boot-starter-tomcat-dev` was replaced with `spring-boot-starter-web-server-embedded-tomcat`). Requires Java 11 or higher.
	+ Tomcat's server-side connections are now properly secured and the connection is restricted by default. The new version expects a `javax/sql/JDBC` license instead of relying on an unrestricted license. It also introduced several performance upgrades over previous versions (e.g., improved support for AIO connections).
* **Spring Boot 3.5**:
	+ Defaulted to using an embedded, unsecured Tomcat instance (`spring-boot-starter-tomcat-dev`).
	+ No changes were made compared with the previous version.

### 3. Server Configuration and Connection Settings

* **Spring Boot 4.0**:
	+ The `server.address`, `server.ssl`, `server.ssl.keystore.location`, and similar configuration options have been removed, as they will default to specific values based on the module used (e.g., embedded servers).
	+ These defaults require Java 11 or higher.
* **Spring Boot 3.5**:
	+ Configuration options like `server.address` and others are preserved; however, some settings (like configuring a keystore location) might still be confusing for users of a multi-project build.

### 4. Additional Modules and Dependencies

* **Spring Boot 4.0**:
	+ Several new sub-modules were introduced to separate components from the main starter module.
	+ Some deprecated sub-modes and methods have been removed.
	+ Performance upgrades were achieved by updating dependencies like Apache Commons and Jackson, which provide better memory handling in multi-threaded applications.
* **Spring Boot 3.5** (No significant changes.)

### 5. Additional Features

*   **Spring Boot 4.0:**
    *   Added support for JavaFX on a standalone server environment using the new `spring-boot-starter-jfx-server`.
    *   The server supports AIO, which has been a long-awaited feature by many Spring developer and helps improve performance in async or single-threaded applications.
*   **Spring Boot 3.5:**
    *   No additional features were announced.

### 6. Security

*   **Spring Boot 4.0**:
   + Added a flag for enabling application-level security features, like SSL/TLS and mutual authentication.
   + Support for Spring Security `@SpringBootApplication` has changed; it's available (as always) at the top level or in a child class implementing this annotation.
*   **Spring Boot 3.5**:
   * No changes to Spring Security modules.

### Note:

While Spring Boot 4.0 and Spring Boot 3.5 have distinct differences, their new capabilities mean many improvements when transitioning a Java application built using the `spring-boot-starter-parent` POM template to the newer version (e.g., performance improvements).