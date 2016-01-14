Name:           libmad
Version:        0.15.1b
Release:        8.%{dist}
Summary:        MPEG audio decoder library
Group:          System Environment/Libraries
License:        GPLv2
Vendor: %{vendor}
Packager: %{packager}
URL:            http://www.underbit.com/products/mad/
Source0:        http://download.sourceforge.net/mad/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
MAD is a high-quality MPEG audio decoder. It currently supports MPEG-1
and the MPEG-2 extension to Lower Sampling Frequencies, as well as the
so-called MPEG 2.5 format. All three audio layers (Layer I, Layer II,
and Layer III a.k.a. MP3) are fully implemented.

%package        devel
Summary:        MPEG audio decoder library development files
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
%{summary}.


%prep
%setup -q
sed -i -e /-fforce-mem/d configure* # -fforce-mem gone in gcc 4.2, noop earlier
touch -r aclocal.m4 configure.ac

# Create an additional pkgconfig file
%{__cat} << EOF > mad.pc
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: mad
Description: MPEG Audio Decoder
Requires:
Version: %{version}
Libs: -L%{_libdir} -lmad -lm
Cflags: -I%{_includedir}
EOF



%build

%configure \
%ifarch x86_64 ia64
    --enable-fpm=64bit \
%endif
    --disable-dependency-tracking \
    --enable-accuracy \
    --disable-debugging \
    --disable-static    

make %{?_smp_mflags} CPPFLAGS="$RPM_OPT_FLAGS"


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
%{__install} -D -p -m 0644 mad.pc %{buildroot}%{_libdir}/pkgconfig/mad.pc


%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc CHANGES COPYING COPYRIGHT CREDITS README TODO
%{_libdir}/libmad.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libmad.so
%{_libdir}/pkgconfig/mad.pc
%{_includedir}/mad.h


%changelog
