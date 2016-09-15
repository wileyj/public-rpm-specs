%define realname gradle

Name:           gradle213
Version:        2.13
Release:        1.%{?dist}
Summary:        Build automation tool
License:        ASL 2.0
URL:            http://www.gradle.org/
BuildArch:      noarch
Source0:	%{realname}-%{version}.tar.gz

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
if [ -d %{realname}-%{version} ];then
    rm -rf %{realname}-%{version}
fi

%setup -n %{realname}-%{version} -T -b 0

%build
true

%install
%__mkdir_p %{buildroot}/opt/%{name}
%__cp -R * %{buildroot}/opt/%{name}/


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{realname}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{realname}-%{version}

%files 
%dir /opt/%{name}
/opt/%{name}/*


%changelog
