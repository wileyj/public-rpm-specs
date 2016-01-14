%{?el5:%define _without_giflib 1}
%{?el4:%define _without_giflib 1}
%{?el3:%define _without_giflib 1}
%{?el2:%define _without_giflib 1}

%{?el4:%define _without_modxorg 1}
%{?el3:%define _without_modxorg 1}

Summary: Powerful image loading and rendering library
Name: imlib2
Version: 1.4.4
Release: 1.%{dist}
License: BSD
Vendor: %{vendor}
Packager: %{packager}
Group: System Environment/Libraries
URL: http://enlightenment.org/pages/imlib2.html


Source: http://dl.sf.net/project/enlightenment/imlib2-src/%{version}/imlib2-%{version}.tar.bz2
Patch0: imlib2-1.2.1-X11-path.patch
Patch1: imlib2-1.3.0-multilib.patch
Patch2: imlib2-1.3.0-loader_overflows.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: bzip2-devel
BuildRequires: freetype-devel >= 1.2
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
BuildRequires: zlib-devel
# The ltdl.h file is required...
BuildRequires: libtool, gcc-c++
%{?_without_giflib:BuildRequires: libungif-devel}
%{!?_without_giflib:BuildRequires: giflib-devel}
%{?_without_modxorg:BuildRequires: XFree86-devel}
%{!?_without_modxorg:BuildRequires: libXext-devel}

%description
Imlib2 is an advanced replacement library for libraries like libXpm that
provides many more features with much greater flexibility and speed than
standard libraries, including font rasterization, rotation, RGBA space
rendering and blending, dynamic binary filters, scripting, and more.


%package devel
Summary: Imlib2 header, static libraries and documentation
Group: Development/Libraries
Requires: %{name} = %{version}
%{?_without_modxorg:Requires: XFree86-devel}
%{!?_without_modxorg:Requires: libX11-devel}
Requires: pkgconfig

%description devel
Header, static libraries and documentation for Imlib2.

%prep
%setup
#patch0 -p1 -b .x11-path
#patch1 -p1 -b .multilib
#patch2 -p1 -b .overflow

%{__perl} -pi.orig -e 's|/lib(?=[^/\w])|/%{_lib}|g' configure

touch aclocal.m4
touch configure
touch config.h.in
touch `find -name Makefile.in`

%build
%configure \
    --disable-dependency-tracking \
    --disable-static \
    --x-libraries="%{_prefix}/X11R6/%{_lib}" \
    --with-pic \
%ifarch %{ix86}
    --enable-mmx \
%else
    --disable-mmx \
%endif
%ifarch x86_64
    --enable-amd64
%else
    --disable-amd64
%endif
%{__make} %{?_smp_mflags}
#LIBTOOL="%{_bindir}/libtool"

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"
#LIBTOOL="%{_bindir}/libtool"

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING doc/ README
%{_bindir}/imlib2_*
%{_datadir}/imlib2/
%{_libdir}/libImlib2.so.*
%{_libdir}/imlib2/

%files devel
%defattr(-, root, root, 0755)
%{_bindir}/imlib2-config
%{_includedir}/Imlib2.h
### Required by kdelibs bug (RHbz #142244)
%{_libdir}/libImlib2.la
%{_libdir}/libImlib2.so
%{_libdir}/pkgconfig/imlib2.pc
%exclude %{_libdir}/imlib2/filters/*.la
%exclude %{_libdir}/imlib2/loaders/*.la

%changelog
