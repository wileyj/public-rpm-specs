%if 0%{?fedora} < 18 && 0%{?rhel} < 7
%define dbdep db4-devel
%else
%define dbdep libdb-devel
%endif

%if 0%{?rhel}
%define with_freetds 0
%else
%define with_freetds 1
%endif

%define apuver 1

Summary: Apache Portable Runtime Utility library
Name: apr-util
Version: 1.5.4
Release: 1.%{dist}
License: ASL 2.0
Vendor: %{vendor}
Packager: %{packager}
Group: System Environment/Libraries
URL: http://apr.apache.org/
Source0: http://www.apache.org/dist/apr/%{name}-%{version}.tar.bz2
Patch1: apr-util-1.2.7-pkgconf.patch
Patch2: apr-util-1.3.7-nodbmdso.patch
Patch4: apr-util-1.4.1-private.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: autoconf, apr-devel >= 1.3.0
BuildRequires: %{dbdep}, expat-devel, libuuid-devel

%description
The mission of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines.  This library
contains additional utility interfaces for APR; including support
for XML, LDAP, database interfaces, URI parsing and more.

%package devel
Group: Development/Libraries
Summary: APR utility library development kit
Requires: apr-util%{?_isa} = %{version}-%{release}, apr-devel%{?_isa}, pkgconfig
Requires: %{dbdep}%{?_isa}, expat-devel%{?_isa}, openldap-devel%{?_isa}

%description devel
This package provides the support files which can be used to 
build applications using the APR utility library.  The mission 
of the Apache Portable Runtime (APR) is to provide a free 
library of C data structures and routines.

%package pgsql
Group: Development/Libraries
Summary: APR utility library PostgreSQL DBD driver
BuildRequires: postgresql94-devel
Requires: apr-util%{?_isa} = %{version}-%{release}

%description pgsql
This package provides the PostgreSQL driver for the apr-util
DBD (database abstraction) interface.

%package mysql
Group: Development/Libraries
Summary: APR utility library MySQL DBD driver
BuildRequires: mysql-devel
Requires: apr-util%{?_isa} = %{version}-%{release}

%description mysql
This package provides the MySQL driver for the apr-util DBD
(database abstraction) interface.

%package sqlite
Group: Development/Libraries
Summary: APR utility library SQLite DBD driver
BuildRequires: sqlite-devel >= 3.0.0
Requires: apr-util%{?_isa} = %{version}-%{release}

%description sqlite
This package provides the SQLite driver for the apr-util DBD
(database abstraction) interface.

%if %{with_freetds}

%package freetds
Group: Development/Libraries
Summary: APR utility library FreeTDS DBD driver
BuildRequires: freetds-devel
Requires: apr-util%{?_isa} = %{version}-%{release}

%description freetds
This package provides the FreeTDS driver for the apr-util DBD
(database abstraction) interface.

%endif

%package odbc
Group: Development/Libraries
Summary: APR utility library ODBC DBD driver
BuildRequires: unixODBC-devel
Requires: apr-util%{?_isa} = %{version}-%{release}

%description odbc
This package provides the ODBC driver for the apr-util DBD
(database abstraction) interface.

%package ldap
Group: Development/Libraries
Summary: APR utility library LDAP support
BuildRequires: openldap-devel
Requires: apr-util%{?_isa} = %{version}-%{release}

%description ldap
This package provides the LDAP support for the apr-util.

%package openssl
Group: Development/Libraries
Summary: APR utility library OpenSSL crytpo support
BuildRequires: openssl-devel
Requires: apr-util%{?_isa} = %{version}-%{release}

%description openssl
This package provides the OpenSSL crypto support for the apr-util.

%package nss
Group: Development/Libraries
Summary: APR utility library NSS crytpo support
BuildRequires: nss-devel
Requires: apr-util%{?_isa} = %{version}-%{release}

%description nss
This package provides the NSS crypto support for the apr-util.

%prep
%setup -q
%patch1 -p1 -b .pkgconf
%patch2 -p1 -b .nodbmdso
%patch4 -p1 -b .private

%build
autoheader && autoconf
# A fragile autoconf test which fails if the code trips
# any other warning; force correct result for OpenLDAP:
export ac_cv_ldap_set_rebind_proc_style=three
%configure --with-apr=%{_prefix} \
        --includedir=%{_includedir}/apr-%{apuver} \
        --with-ldap=ldap_r --without-gdbm \
        --with-sqlite3 --with-pgsql --with-mysql --with-odbc \
%if %{with_freetds}
        --with-freetds \
%else
        --without-freetds \
%endif
        --with-berkeley-db \
        --without-sqlite2 \
        --with-crypto --with-openssl --with-nss
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/aclocal
install -m 644 build/find_apu.m4 $RPM_BUILD_ROOT/%{_datadir}/aclocal

# Unpackaged files; remove the static libaprutil
rm -f $RPM_BUILD_ROOT%{_libdir}/aprutil.exp \
      $RPM_BUILD_ROOT%{_libdir}/libapr*.a

# And remove the reference to the static libaprutil from the .la
# file.
sed -i '/^old_library/s,libapr.*\.a,,' \
      $RPM_BUILD_ROOT%{_libdir}/libapr*.la

# Remove unnecessary exports from dependency_libs
sed -ri '/^dependency_libs/{s,-l(pq|sqlite[0-9]|rt|dl|uuid) ,,g}' \
      $RPM_BUILD_ROOT%{_libdir}/libapr*.la

# Trim libtool DSO cruft
rm -f $RPM_BUILD_ROOT%{_libdir}/apr-util-%{apuver}/*.*a

%check
# Run the less verbose test suites
export MALLOC_CHECK_=2 MALLOC_PERTURB_=$(($RANDOM % 255 + 1))
cd test
make %{?_smp_mflags} testall
# testall breaks with DBD DSO; ignore
export LD_LIBRARY_PATH="`echo "../dbm/.libs:../dbd/.libs:../ldap/.libs:$LD_LIBRARY_PATH" | sed -e 's/::*$//'`"
./testall -v -q || true
./testall testrmm
./testall testdbm

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE NOTICE
%{_libdir}/libaprutil-%{apuver}.so.*
%dir %{_libdir}/apr-util-%{apuver}

%files pgsql
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_dbd_pgsql*

%files mysql
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_dbd_mysql*

%files sqlite
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_dbd_sqlite*

%if %{with_freetds}

%files freetds
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_dbd_freetds*

%endif

%files odbc
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_dbd_odbc*

%files ldap
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_ldap*

%files openssl
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_crypto_openssl*

%files nss
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_crypto_nss*

%files devel
%defattr(-,root,root,-)
%{_bindir}/apu-%{apuver}-config
%{_libdir}/libaprutil-%{apuver}.*a
%{_libdir}/libaprutil-%{apuver}.so
%{_includedir}/apr-%{apuver}/*.h
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/*.m4

%changelog
