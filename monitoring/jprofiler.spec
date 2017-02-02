%define __jar_repack %{nil}

Name:           jprofiler
%define         realname JProfiler
Summary:        JProfiler
Version:        7.2.2
Release:        1.%{dist}
Url:            http://www.ej-technologies.com 
License:        Paid License Agreement
Vendor: %{vendor}
Packager: %{packager}
Group:          Development/Libraries/Java
Source:         %{name}-%{version}.tar.gz
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	jdk

%description
JProfiler is an award-winning all-in-one Java profiler. JProfiler's intuitive GUI helps you find performance bottlenecks, pin down memory leaks and resolve threading issues.

%prep
%setup
%build
ls -l 
%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt/%{name}-%{version}
pwd
cp -R * %{buildroot}/opt/%{name}-%{version}

%post
ln -f -s /opt/%{name}-%{version} /opt/jprofiler

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root)
/opt/%{name}-%{version}

