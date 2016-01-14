%if 0%{?el6}
    %define macro %{_rpmconfigdir}/macros.d/macros.python27
    %global __python /usr/bin/python27
%else
    %define macro %{_rpmconfigdir}/macros.d/macros.python
    %global __python /usr/bin/python
%endif

%include %{macro}

Name: libtdb
Version: 1.3.1
Release: 1.%{dist}
Group: System Environment/Daemons
Summary: The tdb library
License: LGPLv3+
Vendor: %{vendor}
Packager: %{packager}
URL: http://tdb.samba.org/
Source: http://samba.org/ftp/tdb/tdb-%{version}.tar.gz
Patch0: 0001-tdb-include-include-stdbool.h-in-tdb.h.patch
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: autoconf
BuildRequires: libxslt
BuildRequires: docbook-style-xsl
%if 0%{?el6}
BuildRequires: python27-devel
%else
BuildRequires: python-devel
%endif

Provides: bundled(libreplace)

# Patches

%description
A library that implements a trivial database.

%package devel
Group: Development/Libraries
Summary: Header files need to link the Tdb library
Requires: libtdb = %{version}-%{release}
Requires: pkgconfig

%description devel
Header files needed to develop programs that link against the Tdb library.

%package -n tdb-tools
Group: Development/Libraries
Summary: Developer tools for the Tdb library
Requires: libtdb = %{version}-%{release}

%description -n tdb-tools
Tools to manage Tdb files

%package -n python-tdb
Group: Development/Libraries
Summary: Python bindings for the Tdb library
Requires: libtdb = %{version}-%{release}

%description -n python-tdb
Python bindings for libtdb

%prep
%setup -q -n tdb-%{version}
%patch0 -p1

%build
%configure --disable-rpath \
           --bundled-libraries=NONE \
           --builtin-libraries=replace
make %{?_smp_mflags} V=1

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Shared libraries need to be marked executable for
# rpmbuild to strip them and include them in debuginfo
find $RPM_BUILD_ROOT -name "*.so*" -exec chmod -c +x {} \;

rm -f $RPM_BUILD_ROOT%{_libdir}/libtdb.a

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
%files
%defattr(-,root,root,-)
%{_libdir}/libtdb.so.*

%files devel
%defattr(-,root,root)
%doc docs/README
%{_includedir}/tdb.h
%{_libdir}/libtdb.so
%{_libdir}/pkgconfig/tdb.pc

%files -n tdb-tools
%defattr(-,root,root,-)
%{_bindir}/tdbbackup
%{_bindir}/tdbdump
%{_bindir}/tdbtool
%{_bindir}/tdbrestore
%{_mandir}/man8/tdbbackup.8*
%{_mandir}/man8/tdbdump.8*
%{_mandir}/man8/tdbtool.8*
%{_mandir}/man8/tdbrestore.8*

%files -n python-tdb
%defattr(-,root,root,-)
%if 0%{?el6}
%{python27_sitearch}/tdb.so
%else
%{python_sitearch}/tdb.so
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n python-tdb -p /sbin/ldconfig

%postun -n python-tdb -p /sbin/ldconfig

%changelog
