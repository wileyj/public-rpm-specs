%global with_python3 1

Name: libtalloc
Version: 2.1.5
Release: 1.%{dist}
Group: System Environment/Daemons
Summary: The talloc library
License: LGPLv3+
Vendor: %{vendor}
Packager: %{packager}
URL: http://talloc.samba.org/
Source: https://www.samba.org/ftp/talloc/talloc-%{version}.tar.gz
BuildRequires: autoconf
BuildRequires: libxslt
BuildRequires: docbook-style-xsl
BuildRequires: doxygen

%description
A library that implements a hierarchical allocator with destructors.

%package devel
Group: Development/Libraries
Summary: Developer tools for the Talloc library
Requires: libtalloc = %{version}-%{release}

%description devel
Header files needed to develop programs that link against the Talloc library.

%if 0%{?with_python3}
%package -n py3talloc
Group: Development/Libraries
Summary: Developer tools for the Talloc library
Requires: libtalloc = %{version}-%{release}
Obsoletes: pytalloc < %{version}-%{release}

%description -n py3talloc
Py3talloc libraries for creating python bindings using talloc

%package -n py3talloc-devel
Group: Development/Libraries
Summary: Developer tools for the Talloc library
Requires: python3 pytalloc = %{version}-%{release}
Obsoletes: pytalloc-devel <= %{version}-%{release}

%description -n py3talloc-devel
Development libraries for pyt3alloc
%endif

%package -n pytalloc
Group: Development/Libraries
Summary: Developer tools for the Talloc library
Requires: python3 libtalloc = %{version}-%{release}
Obsoletes: pytalloc <= %{version}-%{release}

%description -n pytalloc
Pytalloc libraries for creating python bindings using talloc

%package -n pytalloc-devel
Group: Development/Libraries
Summary: Developer tools for the Talloc library
Requires: python3 pytalloc = %{version}-%{release}
Obsoletes: pytalloc-devel < %{version}-%{release}

%description -n pytalloc-devel
Development libraries for pytalloc

%prep
%setup -q -n talloc-%{version}

%build
%configure \
    --disable-rpath \
    --disable-rpath-install \
    --bundled-libraries=NONE \
    --builtin-libraries=replace \
%if 0%{?with_python3}
    --extra-python=%{__python3} \
%endif
    --disable-silent-rules 

make %{?_smp_mflags} V=1
doxygen doxy.config

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name "*.so*" -exec chmod -c +x {} \;

rm -f $RPM_BUILD_ROOT%{_libdir}/libtalloc.a
rm -f $RPM_BUILD_ROOT/usr/share/swig/*/talloc.i
cp -a doc/man/* $RPM_BUILD_ROOT/%{_mandir}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%if 0%{?with_python3}
%post -n py3talloc -p /sbin/ldconfig
%postun -n py3talloc -p /sbin/ldconfig
%endif
%post -n pytalloc -p /sbin/ldconfig
%postun -n pytalloc -p /sbin/ldconfig

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root,-)
%{_libdir}/libtalloc.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/talloc.h
%{_libdir}/libtalloc.so
%{_libdir}/pkgconfig/talloc.pc
%{_mandir}/man3/talloc*.3.gz
%{_mandir}/man3/libtalloc*.3.gz

%if 0%{?with_python3}
%files -n py3talloc
%defattr(-,root,root,-)
%{_libdir}/libpytalloc-util*
%{python3_sitearch}/*

%files -n py3talloc-devel
%defattr(-,root,root,-)
%{_includedir}/pytalloc.h
%{_libdir}/pkgconfig/pytalloc-util.pc
%endif

%files -n pytalloc
%defattr(-,root,root,-)
%{_libdir}/libpytalloc-util.so*
%{python_sitearch}/*

%files -n pytalloc-devel
%defattr(-,root,root,-)
%{_includedir}/pytalloc.h
%{_libdir}/pkgconfig/pytalloc-util.pc

%changelog
