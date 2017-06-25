#%lib_package rtmp 0
%define rtmp_version 2.4
%define rtmp_release 1

Summary: A toolkit for RTMP streams
Name: rtmpdump
Version: %{rtmp_version}
Release: %{rtmp_release}.%{dist}
License: GPLv2
Packager: %{packager}
Vendor: %{vendor}
Group: System Environment/Libraries
URL: http://rtmpdump.mplayerhq.hu/
Source0: http://rtmpdump.mplayerhq.hu/download/rtmpdump-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: openssl-devel

%description
rtmpdump is a toolkit for RTMP streams. All forms of RTMP are
supported, including rtmp://, rtmpt://, rtmpe://, rtmpte://, and
rtmps://.

%package librtmp0
Summary: rtmp library package
Group: System Environment/Libraries
Provides: librtmp0 = %{rtmp_version}
%description librtmp0
library package for rtmp

%package       devel
Summary: rtmp devel package
Group: System Environment/Libraries
Provides: rtmpdump-devel = %{rtmp_version}
Requires(pre): /usr/bin/find
%description   devel
devel package for rtmp

%prep
%setup -q

%build
export CFLAGS="-fPIC -O3 -mfpmath=sse -m128bit-long-double -mno-align-stringops -minline-all-stringops -m64 -fstack-protector --param=ssp-buffer-size=4 -pipe -D_FORTIFY_
SOURCE=2 -fexceptions " 
export FFLAGS="-fPIC -O3 -mfpmath=sse -m128bit-long-double -mno-align-stringops -minline-all-stringops -m64 -fstack-protector --param=ssp-buffer-size=4 -pipe -D_FORTIFY_
SOURCE=2 -fexceptions "
export CXXFLAGS="-fPIC -O3 -mfpmath=sse -m128bit-long-double -mno-align-stringops -minline-all-stringops -m64 -fstack-protector --param=ssp-buffer-size=4 -pipe -D_FORTIF
Y_SOURCE=2 -fexceptions "
%{__make}

%install
rm -rf %{buildroot}
make install \
  bindir=%{_bindir} \
  sbindir=%{_sbindir} \
  mandir=%{_mandir} \
  incdir=%{_includedir}/librtmp \
  libdir=%{_libdir} \
  DESTDIR=%{buildroot}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING README
%{_bindir}/rtmpdump
%{_sbindir}/rtmpgw
%{_sbindir}/rtmpsrv
%{_sbindir}/rtmpsuck
%{_mandir}/man1/rtmpdump.1*
%{_mandir}/man8/rtmpgw.8*

%files librtmp0
%defattr(-,root,root,-)
%{_libdir}/librtmp.so.0

%files devel
%defattr(-,root,root,-)
%{_includedir}/librtmp
%{_includedir}/librtmp/amf.h
%{_includedir}/librtmp/http.h
%{_includedir}/librtmp/log.h
%{_includedir}/librtmp/rtmp.h
%{_libdir}/librtmp.a
%{_libdir}/librtmp.so
%{_libdir}/pkgconfig/librtmp.pc
%{_mandir}/man3/librtmp.3.gz



%changelog
