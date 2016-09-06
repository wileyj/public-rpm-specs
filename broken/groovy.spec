# Note to packagers: When rebasing this to a later version, do not
# forget to ensure that sources 1 and 2 are up to date as well as
# the Requires list.

Name:           groovy
Version:        2.4.5
Release:        7.%{?dist}
Summary:        Dynamic language for the Java Platform

# Some of the files are licensed under BSD and CPL terms, but the CPL has been superceded
# by the EPL. We include copies of both for completeness.
# groovyConsole uses CC-BY licensed icons
# (see: subprojects/groovy-console/target/tmp/groovydoc/groovy/ui/icons/credits.txt)
License:        ASL 2.0 and BSD and EPL and Public Domain and CC-BY
URL:            http://groovy-lang.org

Source0:        https://dl.bintray.com/groovy/maven/apache-groovy-src-%{version}-incubating.zip
Source1:        groovy-script.sh
Source3:        groovy.desktop
Source4:        cpl-v10.txt
Source5:        epl-v10.txt
Source6:        http://central.maven.org/maven2/org/codehaus/groovy/groovy-all/%{version}/groovy-all-%{version}.pom

Patch0:         0001-Port-to-Servlet-API-3.1.patch
Patch1:         0002-Gradle-local-mode.patch
Patch2:         0003-Bintray.patch
Patch3:         0004-Remove-android-support.patch
Patch4:         0005-Port-to-QDox-2.0.patch


BuildRequires:  gradle-local >= 2.1-0.9
BuildRequires:  javapackages-local
BuildRequires:  java-devel >= 1.8
BuildRequires:  ant
BuildRequires:  antlr-tool
BuildRequires:  ant-antlr
BuildRequires:  aqute-bnd
BuildRequires:  gpars
BuildRequires:  multiverse
BuildRequires:  apache-parent
BuildRequires:  testng
BuildRequires:  jline
BuildRequires:  apache-commons-cli
BuildRequires:  apache-commons-beanutils
BuildRequires:  apache-commons-collections
BuildRequires:  checkstyle
BuildRequires:  jarjar
BuildRequires:  glassfish-jsp-api
BuildRequires:  glassfish-servlet-api
BuildRequires:  objectweb-asm3
BuildRequires:  bsf
BuildRequires:  apache-ivy
BuildRequires:  jansi
BuildRequires:  junit
BuildRequires:  xstream
BuildRequires:  desktop-file-utils
BuildRequires:  unzip
BuildRequires:  mvn(org.apache.ant:ant-junit)
BuildRequires:  mvn(org.apache.ant:ant-launcher)
BuildRequires:  mvn(javax.servlet:servlet-api)
BuildRequires:  mvn(javax.servlet:jsp-api)

Requires:       %{name}-lib = %{version}-%{release}
Requires:       glassfish-jsp-api
Requires:       glassfish-servlet-api
# FIXME: this dependency is missing in generated POM files from some reason...
Requires:       apache-commons-cli

# optional in pom.xml, but present in upstream binary tarball
Requires:       xstream
Requires:       xpp3-minimal
Requires:       gpars
Requires:       apache-ivy

# Joint compilation requires tools.jar from java-devel
Suggests:       java-devel

BuildArch:      noarch

%description
Groovy is an agile and dynamic language for the Java Virtual Machine,
built upon Java with features inspired by languages like Python, Ruby and
Smalltalk.  It seamlessly integrates with all existing Java objects and
libraries and compiles straight to Java bytecode so you can use it anywhere
you can use Java.


%package lib
Summary:        Groovy JAR artifact
Obsoletes:      %{name}-javadoc < 2

%description lib
This package contains Groovy JAR artifact.


%prep
%setup -q
cp %{SOURCE4} %{SOURCE5} .
# Remove bundled JARs and classes
find \( -name *.jar -o -name *.class \) -delete

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%gradle_build -f -G distBin -- -x groovydoc -x javadoc

%install
%mvn_artifact %{SOURCE6} target/libs/groovy-all-%{version}-indy.jar
%mvn_install

unzip target/distributions/apache-groovy-binary-%{version}.zip
rm -rf groovy-%{version}/{*LICENSE.txt,NOTICE.txt,bin/*.bat,META-INF}
install -d -m 755 %{buildroot}%{_datadir}/
cp -a groovy-%{version} %{buildroot}%{_datadir}/%{name}

for mod in groovy groovy-ant groovy-bsf groovy-console groovy-docgenerator \
           groovy-groovydoc groovy-groovysh groovy-jmx groovy-json \
           groovy-jsr223 groovy-nio groovy-servlet groovy-sql groovy-swing \
           groovy-templates groovy-test groovy-testng groovy-xml; do
    ln -sf ../../java/%{name}/$mod.jar %{buildroot}%{_datadir}/%{name}/lib/$mod-%{version}.jar
    ln -sf ../../java/%{name}/$mod.jar %{buildroot}%{_datadir}/%{name}/indy/$mod-%{version}-indy.jar
done

ln -sf ../../java/%{name}/groovy-all.jar %{buildroot}%{_datadir}/%{name}/embeddable/groovy-all-%{version}.jar
ln -sf ../../java/%{name}/groovy-all.jar %{buildroot}%{_datadir}/%{name}/embeddable/groovy-all-%{version}-indy.jar

find %{buildroot}%{_datadir}/%{name}/lib/ ! -name "groovy*" -type f -print -delete
xmvn-subst %{buildroot}%{_datadir}/%{name}/

# $GROOVY_HOME/lib probably contains much more JARs (optional deps?) than is actually needed.
# These extra JARs can cause problems, e.g. rhbz#1184269.
# From that reason, let's symlink needed JARs manually for now.
ln -sf `build-classpath ant/ant` %{buildroot}%{_datadir}/%{name}/lib/ant.jar
ln -sf `build-classpath ant/ant-antlr` %{buildroot}%{_datadir}/%{name}/lib/ant-antlr.jar
ln -sf `build-classpath ant/ant-junit` %{buildroot}%{_datadir}/%{name}/lib/ant-junit.jar
ln -sf `build-classpath ant/ant-launcher` %{buildroot}%{_datadir}/%{name}/lib/ant-launcher.jar
ln -sf `build-classpath bsf` %{buildroot}%{_datadir}/%{name}/lib/bsf.jar
ln -sf `build-classpath commons-cli` %{buildroot}%{_datadir}/%{name}/lib/commons-cli.jar
ln -sf `build-classpath commons-logging` %{buildroot}%{_datadir}/%{name}/lib/commons-logging.jar
ln -sf `build-classpath gpars/gpars` %{buildroot}%{_datadir}/%{name}/lib/gpars.jar
ln -sf `build-classpath hamcrest/core` %{buildroot}%{_datadir}/%{name}/lib/hamcrest-core.jar
ln -sf `build-classpath apache-ivy/ivy` %{buildroot}%{_datadir}/%{name}/lib/ivy.jar
ln -sf `build-classpath jansi/jansi` %{buildroot}%{_datadir}/%{name}/lib/jansi.jar
ln -sf `build-classpath beust-jcommander` %{buildroot}%{_datadir}/%{name}/lib/jcommander.jar
ln -sf `build-classpath jline/jline` %{buildroot}%{_datadir}/%{name}/lib/jline.jar
ln -sf `build-classpath glassfish-jsp-api` %{buildroot}%{_datadir}/%{name}/lib/jsp-api.jar
# part of JDK7+ (?)
#ln -sf `build-classpath jsr166y` %{buildroot}%{_datadir}/%{name}/lib/jsr166y.jar
ln -sf `build-classpath junit` %{buildroot}%{_datadir}/%{name}/lib/junit.jar
ln -sf `build-classpath multiverse/multiverse-core` %{buildroot}%{_datadir}/%{name}/lib/multiverse-core.jar
# Android support, removed by patch
#ln -sf `build-classpath openbeans` %{buildroot}%{_datadir}/%{name}/lib/openbeans.jar
ln -sf `build-classpath qdox` %{buildroot}%{_datadir}/%{name}/lib/qdox.jar
ln -sf `build-classpath glassfish-servlet-api` %{buildroot}%{_datadir}/%{name}/lib/servlet-api.jar
ln -sf `build-classpath testng` %{buildroot}%{_datadir}/%{name}/lib/testng.jar
ln -sf `build-classpath xpp3-minimal` %{buildroot}%{_datadir}/%{name}/lib/xpp3-minimal.jar
ln -sf `build-classpath xstream/xstream` %{buildroot}%{_datadir}/%{name}/lib/xstream.jar
# upstream bundles extra166y in gpars
ln -sf `build-classpath extra166y` %{buildroot}%{_datadir}/%{name}/lib/extra166y.jar

# Startup scripts
install -d -m 755 %{buildroot}%{_bindir}/
for cmd in grape groovy groovyc groovyConsole groovydoc groovysh java2groovy; do
    class=$(awk '/^startGroovy/{print$2}' %{buildroot}%{_datadir}/%{name}/bin/$cmd)
    install -p -m 755 %{SOURCE1} %{buildroot}%{_bindir}/$cmd
    sed -i "s/@CLASS@/$class/" %{buildroot}%{_bindir}/$cmd
    ln -sf %{_bindir}/$cmd %{buildroot}%{_datadir}/%{name}/bin/$cmd
done

# Configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/
mv %{buildroot}%{_datadir}/%{name}/conf/groovy-starter.conf %{buildroot}%{_sysconfdir}/
ln -s %{_sysconfdir}/groovy-starter.conf %{buildroot}%{_datadir}/%{name}/conf/

# Desktop icon
install -d %{buildroot}%{_datadir}/pixmaps
install -d %{buildroot}%{_datadir}/applications
install -p -m644 subprojects/groovy-console/src/main/resources/groovy/ui/ConsoleIcon.png \
        %{buildroot}%{_datadir}/pixmaps/groovy.png
desktop-file-install --dir %{buildroot}%{_datadir}/applications \
        %{SOURCE3}

# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/%{name}.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Ryan Lerch <rlerch@redhat.com> -->
<!--
SentUpstream: No public bugtracker
-->
<application>
  <id type="desktop">groovy.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <summary>Interactive console for the Groovy programming language</summary>
  <description>
    <p>
      Groovy is a dynamic programming language that is commonly used as a
      scripting language for the Java platform. This application provides an
      interactive console for evaluating scripts in the Groovy language.
    </p>
  </description>
  <url type="homepage">http://groovy-lang.org/</url>
  <screenshots>
    <screenshot type="default">https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/groovy/a.png</screenshot>
  </screenshots>
  <!-- FIXME: change this to an upstream email address for spec updates
  <updatecontact>someone_who_cares@upstream_project.org</updatecontact>
  -->
</application>
EOF

%files
%{_datadir}/%{name}
%{_bindir}/*
%{_datadir}/pixmaps/*
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/applications/*
%config(noreplace) %{_sysconfdir}/*

%files lib -f .mfiles
%doc LICENSE NOTICE README.adoc

%changelog
* Fri Feb 19 2016 Michal Srb <msrb@redhat.com> - 2.4.5-7
- Fix a typo

* Fri Feb 19 2016 Michal Srb <msrb@redhat.com> - 2.4.5-6
- Add missing symlink to extra166y (Resolve: rhbz#1301952)
- Fix xpp3 symlink (Resolves: rhbz#1299674, thanks to Richard Chan)

* Mon Feb 08 2016 Michal Srb <msrb@redhat.com> - 2.4.5-5
- Restore symlinks to groovy-all

* Mon Feb 08 2016 Michal Srb <msrb@redhat.com> - 2.4.5-4
- Install groovy-all with metadata (Resolves: rhbz#1305015)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 28 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4.5-2
- Build with %%gradle_build

* Fri Sep 25 2015 Michal Srb <msrb@redhat.com> - 2.4.5-1
- Update to upstream release 2.4.5

* Fri Sep 04 2015 Michal Srb <msrb@redhat.com> - 2.4.4-1
- Update to upstream release 2.4.4
- Resolves: CVE-2015-3253
- Fix tarball URL

* Tue Jul 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4.3-5
- Add suggests on java-devel

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 11 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4.3-3
- Fix build script

* Fri Apr 10 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4.3-2
- Rebuild to regenerate OSGi metadata

* Fri Apr 10 2015 Michal Srb <msrb@redhat.com> - 2.4.3-1
- Update to upstream release 2.4.3

* Fri Apr 10 2015 Michal Srb <msrb@redhat.com> - 2.4.2-1
- Update to upstream release 2.4.2

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 2.4.1-3
- Add an AppData file for the software center

* Thu Mar 26 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4.1-2
- Remove build dependency on cobertura

* Mon Mar 16 2015 Michal Srb <msrb@redhat.com> - 2.4.1-1
- Update to upstream release 2.4.1

* Fri Mar 13 2015 Michal Srb <msrb@redhat.com> - 2.4.0-2
- Fix URL

* Thu Jan 22 2015 Michal Srb <msrb@redhat.com> - 2.4.0-1
- Update to 2.4.0
- Fix java.lang.LinkageError when using @Grab (Resolves: rhbz#1184269)

* Sun Jan  4 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-2
- Update desktop file

* Wed Nov 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-1
- Non-bootstrap build

* Wed Nov 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-0.9
- Bootstrap build using prebuilt binaries

* Wed Nov 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-0.8
- Remove javadoc package

* Wed Nov 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-0.7
- Install launcher scripts

* Wed Nov 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-0.6
- Install desktop icon

* Wed Nov 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-0.5
- Port to QDox 2.0

* Sun Nov  9 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-0.4
- Use new XMvn resolver factory method

* Tue Nov  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-0.3
- Install all artifacts and scripts

* Tue Nov  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-0.2
- Add alias for org.codehaus.groovy:groovy

* Fri Oct 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-0.1
- Update to upstream version 2.3.7

* Tue Aug 19 2014 Michal Srb <msrb@redhat.com> - 1.8.9-15
- Introduce groovy-lib subpackage
- Resolves: rhbz#1098500

* Mon Aug 18 2014 Michal Srb <msrb@redhat.com> - 1.8.9-14
- Fix Ivy JAR location in wrapper script

* Mon Aug 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8.9-13
- Fix Ivy JAR location

* Sun Jun 22 2014 Michal Srb - 1.8.9-12
- Migrate to %%mvn_artifact
- Fix dep on jline1 in run script

* Mon Jun 16 2014 Michal Srb <msrb@redhat.com> - 1.8.9-11
- Fix FTBFS

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8.9-9
- Use .mfiles generated during build

* Mon Jan 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8.9-8
- Add Requires on java-devel
- Resolves: rhbz#736753

* Fri Dec 06 2013 Michal Srb <msrb@redhat.com> - 1.8.9-7
- Groovy needs asm3

* Thu Oct 24 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8.9-6
- Migrate from jline to jline1
- Resolves: rhbz#1022969

* Sat Aug 18 2013 Matt Spaulding <mspaulding06@gmail.com> - 1.8.9-5
- Fix setting classpath (RHBZ#982378)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 10 2013 Michal Srb <msrb@redhat.com> - 1.8.9-3
- Fix license tag (+CC-BY)

* Thu Jun  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8.9-2
- Remove bundled JARs and classes
- Add workaround for rhbz#971483
- Add Public Domain to licenses
- Install ASL 2.0 license text, resolves: rhbz#858257

* Sat Apr 20 2013 gil cattaneo <puntogil@libero.it> - 1.8.9-1
- Update to 1.8.9

* Thu Apr 11 2013 Matt Spaulding <mspaulding06@gmail.com> - 1.8.8-4
- Now accepts classpath argument (RHBZ #810885)

* Mon Apr  8 2013 Andy Grimm <agrimm@gmail.com> - 1.8.8-3
- Apply patch for GROOVY-6085 (RHBZ #949352) 

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Tom Callaway <spot@fedoraproject.org> - 1.8.8-1
- Update to 1.8.8
- Fix licensing issues

* Wed Jul 25 2012 Johannes Lips <hannes@fedoraproject.org> - 1.8.7-1
- Update to 1.8.7

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 21 2012 Alexander Kurtakov <akurtako@redhat.com> 1.8.6-4
- Move to tomcat v7 apis.
- Guideline fixes.

* Fri Mar 09 2012 Johannes Lips <hannes@fedoraproject.org> - 1.8.6-3
- fixed the path of jvm in the startup script 

* Sat Mar 03 2012 Johannes Lips <hannes@fedoraproject.org> - 1.8.6-2
- fixed the startup script by adding jansi as dep

* Wed Feb 22 2012 Johannes Lips <hannes@fedoraproject.org> - 1.8.6-1
- Update to 1.8.6

* Tue Jan 03 2012 Johannes Lips <hannes@fedoraproject.org> - 1.8.5-1
- Update to 1.8.5

* Sun Nov 20 2011 Johannes Lips <hannes@fedoraproject.org> - 1.8.4-1
- Update to 1.8.4

* Thu Oct 13 2011 Johannes Lips <hannes@fedoraproject.org> - 1.8.3-2
- remove the nojansi patch since jansi is in fedora

* Thu Oct 13 2011 Johannes Lips <hannes@fedoraproject.org> - 1.8.3-1
- Update to 1.8.3

* Tue Sep 06 2011 Johannes Lips <hannes@fedoraproject.org> - 1.8.2-1
- Update to 1.8.2

* Sat Aug 13 2011 Johannes Lips <hannes@fedoraproject.org> - 1.8.1-3
- adjusted the maven pom dir

* Sat Aug 13 2011 Johannes Lips <hannes@fedoraproject.org> - 1.8.1-2
- updated the nojansi patch

* Sat Aug 13 2011 Johannes Lips <hannes@fedoraproject.org> - 1.8.1-1
- Update to 1.8.1

* Wed May 04 2011 Johannes Lips <hannes@fedoraproject.org> - 1.8.0-2
- Minor changes to reflect changes to packaging guidelines

* Fri Apr 29 2011 Johannes Lips <hannes@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Nov 6 2010 Alexander Kurtakov <akurtako@redhat.com> 1.7.2-3
- Build with servlet and jsp apis from tomcat6.

* Thu Jun 17 2010 Lubomir Rintel <lkundrak@v3.sk> - 1.7.2-2
- Fix a typo

* Tue Apr 20 2010 Lubomir Rintel <lkundrak@v3.sk> - 1.7.2-1
- Bump version

* Fri Apr 02 2010 Lubomir Rintel <lkundrak@v3.sk> - 1.7.1-1
- Bump version
- Revert addition of jansi dependency

* Fri Apr 02 2010 Lubomir Rintel <lkundrak@v3.sk> - 1.7.0-2
- Add maven depmap

* Wed Feb 17 2010 Lubomir Rintel <lkundrak@v3.sk> - 1.7.0-1
- New upstream version
- Use asm 3.1 instead of asm2

* Wed Dec 04 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.6.7-1
- New upstream version
- Make Jochen happy

* Thu Dec 03 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.6.6-2
- Build with OpenJDK

* Mon Nov 30 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.6.6-1
- Bump to 1.6.6
- Don't mistakenly require itself (Jochen Schmitt, #534168#c3)

* Fri Nov 27 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.6.5-2
- Hopefully fix mockbuild

* Mon Nov 09 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.6.5-1
- Initial Fedora packaging
