%define	major	0

Name:		libnut
%define	svnrev	677
Version:	0.0.%{svnrev}
Release:	1.%{dist}
Url:		http://wiki.multimedia.cx/index.php?title=NUT
License:	MIT
Vendor: %{vendor}
Packager: %{packager}
Group:		System/Libraries
Summary:	NUT Multimedia Container Library
BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root
# svn checkout svn://svn.mplayerhq.hu/nut/src/trunk libnut ; tar -Jcf libnut-r$(LC_ALL=C svn info libnut | sed -n 's/Revision: //p').tar.xz libnut
Source0:	%{name}-r%{svnrev}.tar.xz
Patch0:		libnut-libdir.patch
Patch1:		libnut-shared.patch
Patch2:		libnut-r675-ldflags.patch

%description
Library for manipulation with NUT multimedia streams.

Unlike many popular containers, a NUT file can largely be viewed as a
byte stream, opposed to having a global block structure. NUT files
consist of a sequence of packets, which can contain global headers,
file metadata, stream headers for the individual media streams,
optional index data to accelerate seeking, and, of course, the actual
encoded media frames.

%package lib
Group:		System/Libraries
Summary:	NUT Multimedia Container Library
Provides:    %{name}-lib
%description lib
Library for manipulation with NUT multimedia streams.

Unlike many popular containers, a NUT file can largely be viewed as a
byte stream, opposed to having a global block structure. NUT files
consist of a sequence of packets, which can contain global headers,
file metadata, stream headers for the individual media streams,
optional index data to accelerate seeking, and, of course, the actual
encoded media frames.

%package 	devel
Group:		Development/C
Summary:	Development files for NUT Multimedia Container Library
Requires:	%{name}-lib
Provides:	%{name}-devel 
# package was not libified a long long time ago and an obsolete was forgotten
# at the time, causing file conflicts on upgrade (Anssi 03/2012):
Obsoletes:	libnut-devel < 0-0.275

%description devel
This package contains development files for the NUT Multimedia Container
Library.

%package	utils
Group:		Video
Summary:	NUT Multimedia Container Utilites

%description	utils
Utilities for manipulation with NUT multimedia streams.

Unlike many popular containers, a NUT file can largely be viewed as a
byte stream, opposed to having a global block structure. NUT files
consist of a sequence of packets, which can contain global headers,
file metadata, stream headers for the individual media streams,
optional index data to accelerate seeking, and, of course, the actual
encoded media frames.

%prep
%setup -q -n %{name}
%patch0 -p0 -b .libdir~
%patch1 -p1 -b .shared~
%patch2 -p1 -b .ldflags~

%build
#export CFLAGS="%{optflags} -fPIC"
export CFLAGS="-fPIC -O3 -mfpmath=sse -m128bit-long-double -mno-align-stringops -minline-all-stringops -m64 -fstack-protector --param=ssp-buffer-size=4 -pipe -D_FORTIFY_SOURCE=2 -fexceptions "
export FFLAGS="-fPIC -O3 -mfpmath=sse -m128bit-long-double -mno-align-stringops -minline-all-stringops -m64 -fstack-protector --param=ssp-buffer-size=4 -pipe -D_FORTIFY_SOURCE=2 -fexceptions "
export CXXFLAGS="-fPIC -O3 -mfpmath=sse -m128bit-long-double -mno-align-stringops -minline-all-stringops -m64 -fstack-protector --param=ssp-buffer-size=4 -pipe -D_FORTIFY_SOURCE=2 -fexceptions "
export PATH="$PATH:%{_libdir}";

%{__make} DESTDIR=%{buildroot} libdir=%{_libdir} includedir=%{_includedir} bindir=%{_bindir}

rm -rf %{buildroot}
%{__make} install  DESTDIR=%{buildroot} libdir=%{_libdir} includedir=%{_includedir} bindir=%{_bindir}
install -d  %{buildroot}/usr/lib64
install -d  %{buildroot}/usr/include
install -m 755 libnut/libnut.so.0 %{buildroot}/usr/lib64/libnut.so.0 
install -m 755 libnut/libnut.a %{buildroot}/usr/lib64/libnut.a
install -m 644 libnut/libnut.h %{buildroot}/usr/include/libnut.h
cd %{buildroot}/usr/lib64
ln -s -f libnut.so.0 libnut.so
cd $RPM_BUILD_DIR


%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files utils
%defattr(-, root, root)
/usr/local/bin/nutmerge
/usr/local/bin/nutparse
/usr/local/bin/nutindex

%files lib
%defattr(-, root, root)
%{_libdir}/libnut.so.0
%{_libdir}/libnut.so
%{_libdir}/libnut.a

%files devel
%defattr(-, root, root)
%{_includedir}/libnut.h
