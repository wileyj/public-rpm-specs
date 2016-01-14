%define __os_install_post %{nil}
#%define our_find_requires %{_builddir}/java-build/usr/java/jdk1.5.0_07/find_requires
%define _unpackaged_files_terminate_build 0
%define _find_requires 0
%define home /opt/gradle/%{name}-%{version}
%define current /opt/gradle/current


Name:          gradle
Version:       2.2.1
Release:       1.%{dist}
Summary:       Groovy based build system
Group:         Development/Tools
License:       ASL 2.0
Vendor: %{vendor}
Packager: %{packager}
Url:           http://www.gradle.org/
Source0:       http://services.gradle.org/distributions/gradle-%{version}-bin.zip
AutoReq:	0
AutoProv:	0
Provides:	grade = %{version}
Requires:	jdk

%description
Gradle is a build system written in Groovy. It uses Groovy
also as the language for its build scripts. It has a powerful
multi-project build support. It has a layer on top of Ivy
that provides a build-by-convention integration for Ivy. It
gives you always the choice between the flexibility of Ant
and the convenience of a build-by-convention behavior.

%prep
%setup -n %{name}-%{version} -T -b 0

%build
export DONT_STRIP=1
%install
export DONT_STRIP=1
rm -rf %{buildroot}
mkdir -p %{buildroot}%{home}
cp -R * %{buildroot}%{home}

%post
%{__ln_s} %{home} %{current}
%{__ln_s} %{current}/bin/gradle %{_bindir}/gradle

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root)
%{home}


