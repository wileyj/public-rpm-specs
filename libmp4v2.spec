Summary: Library for working with files using the mp4 container format
Name: libmp4v2
Version: 1.5.0.1
Release: 3.%{dist}
License: MPL
Group: System Environment/Libraries
URL: http://resare.com/libmp4v2/

Vendor: %{vendor}
Packager: %{packager}

Source0: http://resare.com/libmp4v2/dist/libmp4v2-%{version}.tar.bz2
### Only here to be in the source package, "just in case, and FYI"
Source1: http://resare.com/libmp4v2/mklibmp4v2/mklibmp4v2-r51.tar.bz2
Patch0: libmp4v2-1.5.0.1-gcc44.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gcc-c++

%description
The libmp4v2 library provides an abstraction layer for working with files
using the mp4 container format. This library is developed by mpeg4ip project
and is an exact copy of the library distributed in the mpeg4ip package.

%package devel
Summary: Header files, libraries and development documentation for %{name}.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup
%patch0 -p0

%build
%configure \
    --disable-static \
    --disable-dependency-tracking
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"
%{__rm} -rf %{buildroot}%{_mandir}/manm/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-, root, root, 0755)
%doc COPYING README TODO
%{_bindir}/mp4art
%{_bindir}/mp4dump
%{_bindir}/mp4extract
%{_bindir}/mp4info
%{_bindir}/mp4tags
%{_bindir}/mp4trackdump
%{_libdir}/libmp4v2.so.*

%files devel
%defattr(-, root, root, 0755)
%doc API_CHANGES INTERNALS
%doc %{_mandir}/man?/*
%{_includedir}/mp4.h
%{_libdir}/libmp4v2.so
%exclude %{_libdir}/libmp4v2.la

%changelog
