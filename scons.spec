%global __os_install_post /usr/lib/rpm/amazon/brp-compress \
  %{!?__debug_package:/usr/lib/rpm/amazon/brp-strip %{__strip}} \
  /usr/lib/rpm/amazon/brp-strip-static-archive %{__strip} \
  /usr/lib/rpm/amazon/brp-strip-comment-note %{__strip} %{__objdump} \
  /usr/lib/rpm/amazon/brp-python-hardlink

%define name scons
%define version 2.4.1
%define release 1
%define _unpackaged_files_terminate_build 0

Summary: an Open Source software construction tool
Name: %{name}
Version: %{version}
Release: %{release}.%{dist}
Source0: %{name}-%{version}.tar.gz
#Copyright: The SCons Foundation
License: MIT, freely distributable
Group: Development/Tools
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
BuildArchitectures: noarch
Vendor: The SCons Development Team <scons-dev@scons.org>
Packager: The SCons Development Team <scons-dev@scons.org>
Requires: python >= 2.4
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
python setup.py build

%install
python setup.py install --root=$RPM_BUILD_ROOT --install-lib=/usr/lib/scons --install-scripts=/usr/bin --install-data=/usr/share

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root)
%doc %{_mandir}/man1/scons.1*
%doc %{_mandir}/man1/sconsign.1*
%doc %{_mandir}/man1/scons-time.1*
/usr/bin/%{name}*
%dir /usr/lib/%{name}
/usr/lib/%{name}/*
