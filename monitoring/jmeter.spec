%define __jar_repack %{nil}
%define __os_install_post %{nil}
%define _unpackaged_files_terminate_build 0
%define _find_requires 0

%define long_name apache-jmeter
Summary: Apache Jmeter Binary Build
Name: jmeter
Version: 3.1
Release: 1.%{dist}
License: Apache License
Vendor: %{vendor}
Packager: %{packager}
Group: Applications/System
URL: http://jakarta.apache.org/jmeter/
Requires: jdk 

Source: http://archive.apache.org/dist/jmeter/binaries//%{long_name}-%{version}.tgz
BuildRoot: %{_tmppath}/%{long_name}-%{version}-%{release}-root
BuildArch: noarch
AutoReq: 0

%description
Apache JMeter is open source software, a 100% pure Java desktop application designed to load test functional behavior and measure performance. It was originally designed for testing Web Applications but has since expanded to other test functions.

%prep
%setup -n %{long_name}-%{version}

%install
export DONT_STRIP=1
%{__rm} -rf %{buildroot}
mkdir -p %{buildroot}/opt/%{name}
cp -R bin %{buildroot}/opt/%{name}/
cp -R lib %{buildroot}/opt/%{name}/
cp -R extras %{buildroot}/opt/%{name}/
chmod -R 755 %{buildroot}/opt/%{name}/

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-, root, www, 0755)
%dir /opt/%{name}
/opt/%{name}/*

%changelog
