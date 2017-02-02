%global with_python3 0
%define name scons
%define version 2.5.1
%define release 1.%{?dist}
%define _unpackaged_files_terminate_build 0

Summary: an Open Source software construction tool
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.gz
License: MIT, freely distributable
Group: Development/Tools
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
BuildArchitectures: noarch
Vendor: The SCons Development Team <scons-dev@scons.org>
Packager: The SCons Development Team <scons-dev@scons.org>
%if 0%{?with_python3}
Requires: python3
%else
Requires: python
%endif
Url: http://www.scons.org/

%description
SCons is an Open Source software construction tool--that is, a build
tool; an improved substitute for the classic Make utility; a better way
to build software.  SCons is based on the design which won the Software
Carpentry build tool design competition in August 2000.

SCons "configuration files" are Python scripts, eliminating the need
to learn a new build tool syntax.  SCons maintains a global view of
all dependencies in a tree, and can scan source (or other) files for
implicit dependencies, such as files specified on #include lines.  SCons
uses MD5 signatures to rebuild only when the contents of a file have
really changed, not just when the timestamp has been touched.  SCons
supports side-by-side variant builds, and is easily extended with user-
defined Builder and/or Scanner objects.

%prep
%setup

%build
%if 0%{?with_python3}
%{__python3} setup.py build
%else
%{__python} setup.py build
%endif

%install
%if 0%{?with_python3}
%{__python3} setup.py install --root=$RPM_BUILD_ROOT --install-lib=/usr/lib/scons --install-scripts=/usr/bin --install-data=/usr/share
%else
%{__python} setup.py install --root=$RPM_BUILD_ROOT --install-lib=/usr/lib/scons --install-scripts=/usr/bin --install-data=/usr/share
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(0755,root,root) /usr/bin/scons*
%dir /usr/lib/scons
/usr/lib/scons/*
%doc %{_mandir}/man1/scons.1*
%doc %{_mandir}/man1/sconsign.1*
%doc %{_mandir}/man1/scons-time.1*
