%define real_name mcrypt

Summary: Data encryption library
Name: libmcrypt
Version: 2.5.7
Release: 1.%{dist}
License: LGPL
Vendor: %{vendor}
Packager: %{packager}
Group: System Environment/Libraries
URL: http://mcrypt.sf.net/

Source: http://dl.sf.net/mcrypt/libmcrypt-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: libtool >= 1.3.4

%description
libmcrypt is a data encryption library. The library is thread safe
and provides encryption and decryption functions. This version of the
library supports many encryption algorithms and encryption modes. Some
algorithms which are supported:
SERPENT, RIJNDAEL, 3DES, GOST, SAFER+, CAST-256, RC2, XTEA, 3WAY,
TWOFISH, BLOWFISH, ARCFOUR, WAKE and more.

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

%build
%configure \
	--program-prefix="%{?_program_prefix}" \
	--disable-dependency-tracking \
	--enable-static
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
%post
/sbin/ldconfig 2>/dev/null

%postun
/sbin/ldconfig 2>/dev/null

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING.LIB KNOWN-BUGS NEWS README THANKS TODO
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root, 0755)
%doc doc/README* doc/example.c
%doc %{_mandir}/man?/*
%{_bindir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_includedir}/*.h
%{_datadir}/aclocal/*.m4
%exclude %{_libdir}/*.la

%changelog
