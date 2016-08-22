Name:           libghttp
BuildRequires:  glib2-devel

License:        GPL v2 or later; LGPL v2.1 or later
Vendor: %{vendor}
Packager: %{packager}
Group:          System/Libraries
Summary:        A GNOME Library for HTTP Access
Version:        1.0.9
Release:        793.3.%{dist}
Source:         ftp://ftp.gnome.org/pub/stable/sources/libghttp/libghttp-%{version}.tar.bz2
Patch:          libghttp-1.0.9-autoconf.patch
Patch2:         libghttp-1.0.9-version_float.diff
Provides:       libghtt
BuildRequires:  autoconf automake gcc libtool
Obsoletes:      libghtt
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Url:            http://www.gnome.org/

%description
The gHTTP library is fully compliant with HTTP 1.1 as defined in the
draft 5 update of RFC 2068.

The gHTTP library is designed to be simple and easy to use while still
allowing you to get your feet wet in the protocol layer if you have to.
It is designed with graphical, nonthreaded applications in mind (such
as GNOME applications).  You should be able to use the library in your
application and never block data that is waiting to be sent to or
received from a remote server.	The main thread of execution should
always be available to refresh its display.



Authors:
--------
    Christopher Blizzard  <blizzard@appliedtheory.com>
    Herbert Valerio Riedel  <hvr@hvrlab.ml.org>
    Justin Maurer  <justin@openprojects.net>

%package devel
Summary:        Development Files for libghttp
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version} glibc-devel
Obsoletes:      libghtt-devel libghttd
Provides:       libghtt-devel libghttd

%description devel
This package provides the libghttp libraries and include files.



Authors:
--------
    Cf. the libghttp package.

%prep
%setup -q
%patch
%patch2

%build
autoreconf -f -i
%configure --disable-static --with-pic
make %{?jobs:-j%jobs}

%install
make DESTDIR=$RPM_BUILD_ROOT install
# pointless libtool .la file /var/tmp/libghttp-1.0.9-build/usr/lib64/libghttp.la
rm -f %{buildroot}%{_libdir}/libghttp.la

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc AUTHORS COPYING COPYING.LIB NEWS README TODO
%doc doc/ghttp.html
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/ghttpConf.sh

%changelog
