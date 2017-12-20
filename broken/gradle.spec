%define repo https://github.com/gradle/gradle.git
%define gitversion %(echo `curl -s https://github.com/gradle/gradle/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">'`)

%bcond_with bootstrap

Name:           gradle
Version:        %{gitversion}
Release:        1.%{?with_bootstrap:.boot}%{?dist}
Summary:        Build automation tool
License:        ASL 2.0
URL:            http://www.gradle.org/
BuildArch:      noarch

Source0:        http://services.gradle.org/distributions/gradle-%{version}%{?vertag}-src.zip
Source1:        http://services.gradle.org/versions/all#/all-released-versions.json
Source2:        gradle-font-metadata.xml
Source3:        gradle-jquery-metadata.xml
Source4:        gradle-launcher.sh
Source5:        gradle.desktop

Source9900:     gradle-bootstrap.sh
Source9901:     gradle-bootstrap-gererate-resources.py
Source9910:     gradle-bootstrap-module-list
Source9911:     gradle-bootstrap-module-dependencies
Source9920:     gradle-bootstrap-default-imports.txt
Source9921:     gradle-bootstrap-plugin.properties
Patch0:         0001-Gradle-local-mode.patch
Patch1:         0002-Port-to-Jetty-9.patch
Patch2:         0003-Remove-Class-Path-from-manifest.patch
Patch3:         0004-Implement-XMvn-repository-factory-method.patch
Patch4:         0005-Add-build-dependency-on-ASM-5.0.3.patch
Patch5:         0006-Port-from-Simple-4-to-Jetty-9.patch
Patch6:         0007-Use-unversioned-dependency-JAR-names.patch
Patch7:         0008-Port-to-Ivy-2.4.0.patch
Patch8:         0009-Port-to-Polyglot-0.1.8.patch
Patch9:         0010-Remove-S3-plugin.patch
Patch10:        0011-Port-to-Kryo-3.0.patch
Patch11:        0012-Port-to-Maven-3.3.9-and-Eclipse-Aether.patch
Patch12:        0013-Publish-all-artifacts.patch

%if %{with bootstrap}
BuildRequires:  groovy >= 2.3
BuildRequires:  javapackages-local
%else
BuildRequires:  gradle-local >= 2.2
%endif

BuildRequires:  desktop-file-utils
BuildRequires:  hostname
BuildRequires:  procps-ng
BuildRequires:  mvn(antlr:antlr)
BuildRequires:  mvn(asm:asm)
BuildRequires:  mvn(asm:asm-tree)
BuildRequires:  mvn(biz.aQute:bndlib)
BuildRequires:  mvn(biz.source_code:base64coder)
BuildRequires:  mvn(bsf:bsf)
BuildRequires:  mvn(cglib:cglib)
BuildRequires:  mvn(cglib:cglib-nodep)
BuildRequires:  mvn(ch.qos.logback:logback-classic)
BuildRequires:  mvn(ch.qos.logback:logback-core)
BuildRequires:  mvn(com.beust:jcommander)
BuildRequires:  mvn(com.esotericsoftware.kryo:kryo)
BuildRequires:  mvn(com.esotericsoftware.minlog:minlog)
BuildRequires:  mvn(com.esotericsoftware.reflectasm:reflectasm)
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-annotations)
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-core)
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-databind)
BuildRequires:  mvn(com.google.code.findbugs:findbugs)
BuildRequires:  mvn(com.google.code.findbugs:jsr305)
BuildRequires:  mvn(com.google.code.gson:gson)
BuildRequires:  mvn(com.googlecode.jarjar:jarjar)
BuildRequires:  mvn(com.googlecode.jatl:jatl)
BuildRequires:  mvn(com.google.guava:guava)
BuildRequires:  mvn(com.google.guava:guava-jdk5)
BuildRequires:  mvn(com.jcraft:jsch)
BuildRequires:  mvn(com.jcraft:jzlib)
BuildRequires:  mvn(commons-beanutils:commons-beanutils-core)
BuildRequires:  mvn(commons-cli:commons-cli)
BuildRequires:  mvn(commons-codec:commons-codec)
BuildRequires:  mvn(commons-collections:commons-collections)
BuildRequires:  mvn(commons-configuration:commons-configuration)
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(commons-lang:commons-lang)
BuildRequires:  mvn(commons-logging:commons-logging)
BuildRequires:  mvn(com.puppycrawl.tools:checkstyle)
BuildRequires:  mvn(com.sun:tools)
BuildRequires:  mvn(com.thoughtworks.qdox:qdox)
BuildRequires:  mvn(com.thoughtworks.xstream:xstream)
BuildRequires:  mvn(com.typesafe.zinc:zinc)
BuildRequires:  mvn(com.uwyn:jhighlight)
BuildRequires:  mvn(dom4j:dom4j)
BuildRequires:  mvn(isorelax:isorelax)
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(javax.mail:mail)
BuildRequires:  mvn(javax.servlet:javax.servlet-api)
BuildRequires:  mvn(javax.xml.stream:stax-api)
BuildRequires:  mvn(jaxen:jaxen)
BuildRequires:  mvn(jdom:jdom)
BuildRequires:  mvn(jline:jline)
BuildRequires:  mvn(joda-time:joda-time)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(log4j:log4j)
BuildRequires:  mvn(net.java.dev.jna:jna)
BuildRequires:  mvn(net.java.dev.msv:msv-core)
BuildRequires:  mvn(net.java.dev.msv:xsdlib)
BuildRequires:  mvn(net.jcip:jcip-annotations)
BuildRequires:  mvn(net.rubygrapefruit:native-platform)
BuildRequires:  mvn(net.sf.kxml:kxml2)
BuildRequires:  mvn(net.sf.kxml:kxml2-min)
BuildRequires:  mvn(net.sourceforge.nekohtml:nekohtml)
BuildRequires:  mvn(org.apache.ant:ant)
BuildRequires:  mvn(org.apache.ant:ant-antlr)
BuildRequires:  mvn(org.apache.ant:ant-junit)
BuildRequires:  mvn(org.apache.ant:ant-launcher)
BuildRequires:  mvn(org.apache.ant:ant-parent:pom:)
BuildRequires:  mvn(org.apache:apache:pom:)
BuildRequires:  mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:  mvn(org.apache.felix:org.osgi.core)
BuildRequires:  mvn(org.apache.geronimo.specs:geronimo-annotation_1.0_spec)
BuildRequires:  mvn(org.apache.geronimo.specs:geronimo-jms_1.1_spec)
BuildRequires:  mvn(org.apache.httpcomponents:httpclient)
BuildRequires:  mvn(org.apache.httpcomponents:httpcore)
BuildRequires:  mvn(org.apache.ivy:ivy)
BuildRequires:  mvn(org.apache.maven:maven-aether-provider)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-builder-support)
BuildRequires:  mvn(org.apache.maven:maven-compat)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-model-builder)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven:maven-repository-metadata)
BuildRequires:  mvn(org.apache.maven:maven-settings)
BuildRequires:  mvn(org.apache.maven:maven-settings-builder)
BuildRequires:  mvn(org.apache.maven.wagon:wagon-http)
BuildRequires:  mvn(org.apache.maven.wagon:wagon-http-lightweight)
BuildRequires:  mvn(org.apache.maven.wagon:wagon-http-shared)
BuildRequires:  mvn(org.apache.maven.wagon:wagon-provider-api)
BuildRequires:  mvn(org.apache.tomcat:tomcat-servlet-api)
BuildRequires:  mvn(org.apache.xbean:xbean-reflect)
BuildRequires:  mvn(org.beanshell:bsh)
BuildRequires:  mvn(org.bouncycastle:bcpg-jdk15)
BuildRequires:  mvn(org.bouncycastle:bcprov-jdk15)
BuildRequires:  mvn(org.codehaus.gpars:gpars)
BuildRequires:  mvn(org.codehaus.groovy:groovy)
BuildRequires:  mvn(org.codehaus.groovy:groovy-all)
BuildRequires:  mvn(org.codehaus.jcsp:jcsp)
BuildRequires:  mvn(org.codehaus.jettison:jettison)
BuildRequires:  mvn(org.codehaus.jsr166-mirror:extra166y)
BuildRequires:  mvn(org.codehaus.plexus:plexus-classworlds)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  mvn(org.codehaus.plexus:plexus-interpolation)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.codehaus.sonar:sonar-batch)
BuildRequires:  mvn(org.codehaus.sonar:sonar-batch-bootstrapper)
BuildRequires:  mvn(org.codehaus.sonar:sonar-plugin-api)
BuildRequires:  mvn(org.codehaus.woodstox:stax2-api)
BuildRequires:  mvn(org.codehaus.woodstox:woodstox-core-asl)
BuildRequires:  mvn(org.codenarc:CodeNarc)
BuildRequires:  mvn(org.eclipse.aether:aether-ant-tasks)
BuildRequires:  mvn(org.eclipse.aether:aether-api)
BuildRequires:  mvn(org.eclipse.aether:aether-connector-basic)
BuildRequires:  mvn(org.eclipse.aether:aether-impl)
BuildRequires:  mvn(org.eclipse.aether:aether-spi)
BuildRequires:  mvn(org.eclipse.aether:aether-transport-classpath)
BuildRequires:  mvn(org.eclipse.aether:aether-transport-file)
BuildRequires:  mvn(org.eclipse.aether:aether-transport-http)
BuildRequires:  mvn(org.eclipse.aether:aether-transport-wagon)
BuildRequires:  mvn(org.eclipse.aether:aether-util)
BuildRequires:  mvn(org.eclipse.jdt:core)
BuildRequires:  mvn(org.eclipse.jetty:jetty-annotations)
BuildRequires:  mvn(org.eclipse.jetty:jetty-jsp)
BuildRequires:  mvn(org.eclipse.jetty:jetty-plus)
BuildRequires:  mvn(org.eclipse.jetty:jetty-security)
BuildRequires:  mvn(org.eclipse.jetty:jetty-server)
BuildRequires:  mvn(org.eclipse.jetty:jetty-servlet)
BuildRequires:  mvn(org.eclipse.jetty:jetty-util)
BuildRequires:  mvn(org.eclipse.jetty:jetty-webapp)
BuildRequires:  mvn(org.eclipse.jetty:jetty-xml)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires:  mvn(org.fusesource.hawtjni:hawtjni-runtime)
BuildRequires:  mvn(org.fusesource.jansi:jansi)
BuildRequires:  mvn(org.fusesource.jansi:jansi-native)
BuildRequires:  mvn(org.gmetrics:GMetrics)
BuildRequires:  mvn(org.gradle.jarjar:jarjar)
BuildRequires:  mvn(org.hamcrest:hamcrest-core)
BuildRequires:  mvn(org.hamcrest:hamcrest-parent:pom:)
BuildRequires:  mvn(org.jboss.netty:netty:3)
BuildRequires:  mvn(org.jdom:jdom)
BuildRequires:  mvn(org.jdom:jdom2)
BuildRequires:  mvn(org.joda:joda-convert)
BuildRequires:  mvn(org.jsoup:jsoup)
BuildRequires:  mvn(org.mozilla:rhino)
BuildRequires:  mvn(org.multiverse:multiverse-core)
BuildRequires:  mvn(org.objenesis:objenesis)
BuildRequires:  mvn(org.ow2.asm:asm)
BuildRequires:  mvn(org.ow2.asm:asm-all)
BuildRequires:  mvn(org.ow2.asm:asm-analysis)
BuildRequires:  mvn(org.ow2.asm:asm-tree)
BuildRequires:  mvn(org.ow2.asm:asm-util)
BuildRequires:  mvn(org.parboiled:parboiled-core)
BuildRequires:  mvn(org.parboiled:parboiled-java)
BuildRequires:  mvn(org.pegdown:pegdown)
BuildRequires:  mvn(org.samba.jcifs:jcifs)
BuildRequires:  mvn(org.slf4j:jcl-over-slf4j)
BuildRequires:  mvn(org.slf4j:jul-to-slf4j)
BuildRequires:  mvn(org.slf4j:log4j-over-slf4j)
BuildRequires:  mvn(org.slf4j:slf4j-api)
BuildRequires:  mvn(org.sonatype.oss:oss-parent:pom:)
BuildRequires:  mvn(org.sonatype.plexus:plexus-cipher)
BuildRequires:  mvn(org.sonatype.plexus:plexus-sec-dispatcher)
BuildRequires:  mvn(org.sonatype.pmaven:pmaven-common)
BuildRequires:  mvn(org.sonatype.pmaven:pmaven-groovy)
BuildRequires:  mvn(org.spockframework:spock-core)
BuildRequires:  mvn(org.testng:testng)
BuildRequires:  mvn(org.yaml:snakeyaml)
BuildRequires:  mvn(oro:oro)
BuildRequires:  mvn(relaxngDatatype:relaxngDatatype)
BuildRequires:  mvn(stax:stax)
BuildRequires:  mvn(stax:stax-api)
BuildRequires:  mvn(xalan:serializer)
BuildRequires:  mvn(xalan:xalan)
BuildRequires:  mvn(xerces:xercesImpl)
BuildRequires:  mvn(xml-apis:xml-apis)
BuildRequires:  mvn(xml-resolver:xml-resolver)
BuildRequires:  mvn(xom:xom)
BuildRequires:  lato-fonts
BuildRequires:  liberation-mono-fonts
BuildRequires:  js-jquery
Requires:       jdk
Requires:       bash
Requires:       hicolor-icon-theme
Requires:       aether-ant-tasks
Requires:       aether-api
Requires:       aether-connector-basic
Requires:       aether-impl
Requires:       aether-spi
Requires:       aether-transport-classpath
Requires:       aether-transport-file
Requires:       aether-transport-http
Requires:       aether-transport-wagon
Requires:       aether-util
Requires:       ant
Requires:       ant-antlr
Requires:       ant-junit
Requires:       antlr-tool
Requires:       apache-commons-cli
Requires:       apache-commons-codec
Requires:       apache-commons-collections
Requires:       apache-commons-io
Requires:       apache-commons-lang
Requires:       apache-commons-logging
Requires:       apache-ivy >= 2.4
Requires:       aqute-bndlib >= 2
Requires:       atinject
Requires:       base64coder
Requires:       bea-stax
Requires:       bea-stax-api
Requires:       beust-jcommander
Requires:       bouncycastle
Requires:       bouncycastle-pg
Requires:       bsf
Requires:       bsh
Requires:       cglib
Requires:       dom4j >= 1.6.1-24
Requires:       ecj
Requires:       extra166y
Requires:       felix-osgi-core
Requires:       geronimo-annotation
Requires:       geronimo-jms
Requires:       glassfish-servlet-api
Requires:       google-gson
Requires:       gpars
Requires:       groovy-lib
Requires:       guava
Requires:       hamcrest
Requires:       hawtjni
Requires:       httpcomponents-client
Requires:       httpcomponents-core
Requires:       isorelax
Requires:       jackson-annotations
Requires:       jackson-core
Requires:       jackson-databind
Requires:       jansi
Requires:       jansi-native
Requires:       jarjar
Requires:       jatl
Requires:       javamail
Requires:       jaxen
Requires:       jcifs
Requires:       jcip-annotations
Requires:       jcl-over-slf4j
Requires:       jcsp
Requires:       jdom
Requires:       jdom2
Requires:       jettison
Requires:       jetty-annotations
Requires:       jetty-jsp >= 9.3
Requires:       jetty-plus
Requires:       jetty-security
Requires:       jetty-server
Requires:       jetty-servlet
Requires:       jetty-util
Requires:       jetty-webapp
Requires:       jetty-xml
Requires:       jline
Requires:       jna
Requires:       joda-convert
Requires:       joda-time
Requires:       jsch
Requires:       jul-to-slf4j
Requires:       junit
Requires:       jzlib
Requires:       kryo >= 3
Requires:       kxml
Requires:       log4j12
Requires:       log4j-over-slf4j
Requires:       logback
Requires:       maven >= 3.3.3
Requires:       maven-wagon-http
Requires:       maven-wagon-http-shared
Requires:       maven-wagon-provider-api
Requires:       minlog
Requires:       msv-msv
Requires:       msv-xsdlib
Requires:       multiverse
Requires:       native-platform
Requires:       nekohtml
Requires:       netty3
Requires:       objectweb-asm
Requires:       objenesis
Requires:       plexus-cipher
Requires:       plexus-classworlds
Requires:       plexus-containers-component-annotations
Requires:       plexus-containers-container-default
Requires:       plexus-interpolation
Requires:       plexus-sec-dispatcher
Requires:       plexus-utils
Requires:       qdox
Requires:       reflectasm
Requires:       relaxngDatatype
Requires:       rhino
Requires:       sisu-plexus
Requires:       slf4j
Requires:       snakeyaml
Requires:       sonar-batch-bootstrapper
Requires:       stax2-api
Requires:       tesla-polyglot-common >= 0.1.8
Requires:       tesla-polyglot-groovy >= 0.1.8
Requires:       testng
Requires:       woodstox-core
Requires:       xalan-j2
Requires:       xbean
Requires:       xerces-j2
Requires:       xml-commons-apis
Requires:       xml-commons-resolver
Requires:       xom
Requires:       xstream
Requires:       zinc

%description
Gradle is build automation evolved. Gradle can automate the building,
testing, publishing, deployment and more of software packages or other
types of projects such as generated static websites, generated
documentation or indeed anything else.

Gradle combines the power and flexibility of Ant with the dependency
management and conventions of Maven into a more effective way to
build. Powered by a Groovy DSL and packed with innovation, Gradle
provides a declarative way to describe all kinds of builds through
sensible defaults. Gradle is quickly becoming the build system of
choice for many open source projects, leading edge enterprises and
legacy automation challenges.



%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1

rm -rf gradle/wrapper/
>subprojects/diagnostics/src/main/resources/org/gradle/api/tasks/diagnostics/htmldependencyreport/jquery.jstree.js

mkdir -p build
cp %{SOURCE1} build/all-released-versions.json

%mvn_config resolverSettings/metadataRepositories/repository %{SOURCE2}
%mvn_config resolverSettings/metadataRepositories/repository %{SOURCE3}
rm -rf buildSrc/src/test
rm -rf subprojects/resources-s3
sed -i 's/"-Werror" <<//' gradle/strictCompile.gradle

%build
cd %{name}-%{version}
%if %{with bootstrap}
mkdir -p subprojects/docs/src/main/resources && cp %{SOURCE9920} subprojects/docs/src/main/resources/default-imports.txt
cp %{SOURCE9921} subprojects/core/src/main/resources/gradle-plugins.properties
%{SOURCE9900} %{SOURCE9910} %{SOURCE9911}
%else
gradle-local -x docs:distDocs --offline -s install xmvnInstall -Pgradle_installPath=$PWD/inst \
    -PfinalRelease -Dbuild.number="%{?fedora:Fedora }%{?rhel:Red Hat }%{version}-%{release}"
%endif

%install
install -d -m 755 %{buildroot}%{_javadir}/%{name}/

%if %{with bootstrap}
cp -r bootstrap-home %{buildroot}%{_datadir}/%{name}
# Launcher with dependencies needs to be in _javadir
for mod in launcher core base-services; do
    ln -s %{_datadir}/%{name}/lib/gradle-$mod.jar %{buildroot}%{_javadir}/%{name}/gradle-$mod.jar
    echo %{_javadir}/%{name}/gradle-$mod.jar >> .mfiles
done
# Dependencies of xmvn-connector-gradle need to have Maven metadata
for mod in base-services core dependency-management resources; do
    %add_maven_depmap org.gradle:gradle-$mod:%{version} ../%{name}/lib/gradle-$mod.jar
done
cp subprojects/distributions/src/toplevel/{changelog.txt,LICENSE,NOTICE} .

%else # non-bootstrap

rm -rf inst/bin/gradle.bat inst/media
ln -sf %{_bindir}/%{name} inst/bin/gradle
mv inst/{changelog.txt,LICENSE,NOTICE} .
find inst/lib -type f -name 'gradle*' | sed 's:.*/\(gradle-.*\)-%{version}.*:ln -sf %{_javadir}/%{name}/\1.jar &:' | bash -x
ln -sf $(build-classpath ecj) inst/lib/plugins/ecj.jar
xmvn-subst -s $(find inst/lib -type f)
cp -a inst %{buildroot}%{_datadir}/%{name}

%mvn_install

%endif

install -d -m 755 %{buildroot}%{_bindir}/
install -p -m 755 %{SOURCE4} %{buildroot}%{_bindir}/%{name}

desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE5}

for r in 16 24 32 48 64 128 256; do
    install -d -m 755 %{buildroot}%{_datadir}/icons/hicolor/${r}x${r}/apps/
    install -p -m 644 subprojects/distributions/src/toplevel/media/gradle-icon-${r}x${r}.png \
        %{buildroot}%{_datadir}/icons/hicolor/${r}x${r}/apps/%{name}.png
done

%post
update-desktop-database &>/dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &>/dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files -f .mfiles
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%doc changelog.txt
%doc LICENSE NOTICE

%changelog
