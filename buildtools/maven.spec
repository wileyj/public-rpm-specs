%define repo https://github.com/apache/maven
%define gitversion %(echo `curl -s https://github.com/apache/maven/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">v'`)
%define _prefix /opt/%{name}
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1 | cut -c1-7`)
%define rel_version 1



Name:           maven
Summary:        software project management tool
Version:        %{rel_version}.%{gitversion}.%{revision}
Release:        1.%{dist}
Url:            http://maven.apache.org
License:        Apache
Vendor: 	%{vendor}
Packager: 	%{packager}
Group:          Application/Web
# require the binary apache-maven package, since mvn is required to build maven. of course it is. 
BuildRequires:	apache-maven

%description
Maven is a software project management and comprehension tool. Based on
the concept of a Project Object Model (POM), Maven can manage a project's
build, reporting and documentation from a central piece of information.

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
source /etc/profile
source /etc/profile.d/maven_path.sh

%build
cd %{name}-%{version}

%install
cd %{name}-%{version}
/opt/apache-maven/bin/mvn -DdistributionTargetFolder="%{buildroot}%{_prefix}-%{version}" clean package

%{__mkdir_p} %{buildroot}/etc/profile.d
%{__mkdir_p} %{buildroot}/%{_bindir}
cat <<EOF> %{buildroot}/etc/profile.d/maven.sh
#export MAVEN_OPTS="-Xmx512m -Xms256m -XX:MaxPermSize=256m"
export MAVEN_HOME=%{_prefix}
EOF
%__ln_s -f  %{_prefix}-%{version} %{buildroot}%{_prefix}
%__ln_s -f %{_prefix}-%{version}/bin/mvn %{buildroot}%{_bindir}/mvn
%post

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%dir %{_prefix}-%{version}
%{_prefix}-%{version}/*
%{_prefix}
%{_bindir}/mvn
/etc/profile.d/maven.sh

