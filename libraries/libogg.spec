Name:		libogg
Version:	1.3.0
Release:	1.%{dist}
Summary:	Ogg Bitstream Library

Group:		System Environment/Libraries
License:	BSD
Vendor: %{vendor}
Packager: %{packager}
URL:		http://www.xiph.org/
Source:		http://www.xiph.org/pub/ogg/vorbis/download/%{name}-%{version}.tar.gz
Prefix:		%{_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
# We're forced to use an epoch since both Red Hat and Ximian use it in their
# rc packages
Epoch:		2
# Dirty trick to tell rpm that this package actually provides what the
# last rc and beta was offering
Provides:	%{name} = %{epoch}:1.0rc3-%{release}
Provides:	%{name} = %{epoch}:1.0beta4-%{release}

%description
Libogg is a library for manipulating ogg bitstreams.  It handles
both making ogg bitstreams and getting packets from ogg bitstreams.

%package devel
Summary: 	Ogg Bitstream Library Development
Group: 		Development/Libraries
Requires: 	libogg 
# Dirty trick to tell rpm that this package actually provides what the
# last rc and beta was offering
Provides:	%{name}-devel = %{epoch}:1.0rc3-%{release}
Provides:	%{name}-devel = %{epoch}:1.0beta4-%{release}


%description devel
The libogg-devel package contains the header files, static libraries
and documentation needed to develop applications with libogg.

%prep
%setup -q -n %{name}-%{version}

%build
export CFLAGS="-fPIC -O3 -mfpmath=sse -m128bit-long-double -mno-align-stringops -minline-all-stringops -m64 -fstack-protector --param=ssp-buffer-size=4 -pipe -D_FORTIFY_SOURCE=2 -fexceptions "
export FFLAGS="-fPIC -O3 -mfpmath=sse -m128bit-long-double -mno-align-stringops -minline-all-stringops -m64 -fstack-protector --param=ssp-buffer-size=4 -pipe -D_FORTIFY_SOURCE=2 -fexceptions "
export CXXFLAGS="-fPIC -O3 -mfpmath=sse -m128bit-long-double -mno-align-stringops -minline-all-stringops -m64 -fstack-protector --param=ssp-buffer-size=4 -pipe -D_FORTIFY_SOURCE=2 -fexceptions "

 ./configure --prefix=%{_prefix} --enable-static --libdir=%{_libdir}

make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libogg.so.*
%dir %{_docdir}/libogg-%{version}/
%{_docdir}/libogg-%{version}/*

%files devel
%defattr(-,root,root)
%{_includedir}/ogg/ogg.h
%{_includedir}/ogg/os_types.h
%{_includedir}/ogg/config_types.h
%{_libdir}/libogg.a
%{_libdir}/libogg.so
%{_libdir}/libogg.la
%{_libdir}/pkgconfig/ogg.pc
%{_datadir}/aclocal/ogg.m4

%changelog
