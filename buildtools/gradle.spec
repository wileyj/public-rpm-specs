%define repo https://github.com/gradle/gradle
%define gitversion %(echo `curl -s https://github.com/gradle/gradle/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">' | cut -f1 -d "+" | sed 's/REL_//'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1`)
%define _javadir /usr/java
%define gradle_prefix /opt/%{name}
%define release_ver 1

Name:           gradle
Version:        %{gitversion}
Release:        %{release_ver}.%{revision}.%{?dist}
Summary:        Build automation tool
License:        ASL 2.0
URL:            http://www.gradle.org/
BuildArch:      noarch
BuildRequires:  jdk
Requires:	jdk


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
source /etc/profile
source /etc/profile.d/jdk.sh

%build
cd %{name}-%{version}
./gradlew 

%install
cd %{name}-%{version}
./gradlew install -Pgradle_installPath=%{buildroot}%{gradle_prefix}
install -p -m 755 subprojects/launcher/build/startScripts/%{name} %{buildroot}%{gradle_prefix}/bin/%{name}
%{__rm} -rf %{buildroot}%{gradle_prefix}/bin/%{name}.bat
%{__rm} -rf "build/integ\ test/media/bin/gradle.bat"
%{__rm} -rf "build/integ\ test/media"
find "build/integ\ test/lib" -type f -name 'gradle*' | sed 's:.*/\(gradle-.*\).*:ln -sf %{_javadir}/%{name}/\1.jar &:' | bash -x
%__mkdir_p %{buildroot}/etc/profile.d

cat <<EOF> %{buildroot}/etc/profile.d/%{name}.sh
alias gradle='%{gradle_prefix}/bin/%{name}'
EOF

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%%{name}-contrib-%{version}" != "/" ] && %__rm -rf %{_builddir}/%%{name}-contrib-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
[ "%{_builddir}/%{pkgname}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{pkgname}-%{version}

%files 
%dir %{gradle_prefix}
%{gradle_prefix}/*
%{gradle_prefix}
%{_sysconfdir}/profile.d/%{name}.sh


%changelog
