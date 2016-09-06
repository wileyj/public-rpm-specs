%define repo https://github.com/jenkinsci/blueocean-plugin.git
%define _prefix	/opt/%{name}
%define gitversion %(echo `curl -s https://github.com/jenkinsci/blueocean/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">'`)

Name:		jenkins-blueocean
Version:	162
Release:	1.%{dist}
Summary:	Continous Build Serve UI
URL:		http://jenkins-ci.org/
Group:		Development/Tools/Building
License:	MIT/X License, GPL/CDDL, ASL2
Vendor: 	%{vendor}
Packager: 	%{packager}
BuildRoot:	%{_tmppath}/build-%{name}-%{version}
BuildRequires:	apache-maven nodejs
Requires:	apache-maven nodejs
BuildArch:	x86_64

%description
Blue Ocean is the next generation user experience for Jenkins.
It is a multi-module maven project with a few Jenkins plugins.

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update

%build
cd %{name}-%{version}
mvn clean install -DskipTests

%install
cd %{name}-%{version}
rm -rf %{buildroot}

%__install -d %{buildroot}%{_prefix}
cp -pa * %{buildroot}%{_prefix}/

%clean
#[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
#[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
#[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
#[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root)
%dir %{_prefix}
%{_prefix}/*

%changelog
