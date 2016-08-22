%define	name	freetds
%define	version	0.82
%ifarch x86_64
%define _libdir /usr/lib64
%else
%define _libdir /usr/lib
%endif
# compute some additional dependency from vendor name
# 

# RedHat
%define tds_builddep_redhat unixODBC-devel >= 2.0.0
%define tds_dep_suse glibc-locale

# SUSE
%define tds_builddep_suse unixODBC-devel >= 2.0.0

%undefine tds_builddep
%{expand:%%{expand:%%{?tds_builddep_%{?_vendor}:%%%%define tds_builddep %%{?tds_builddep_%{?_vendor}}}}}
%undefine tds_dep
%{expand:%%{expand:%%{?tds_dep_%{?_vendor}:%%%%define tds_dep %%{?tds_dep_%{?_vendor}}}}}
 
Name: %{name} 
Version: %{version} 
Release: 3.%{dist}
Vendor: %{vendor}
Packager: %{packager}
License: LGPL 
Group: System Environment/Libraries 
Source: http://ibiblio.org/pub/Linux/ALPHA/freetds/stable/%{name}-%{version}.tar.gz 
Patch: blk_version_150.patch
BuildRoot: %{_tmppath}/%{name}-buildroot
%{?tds_builddep:BuildRequires: %{tds_builddep}}
%{?tds_dep:Requires: %tds_dep}
Summary: FreeTDS is a free re-implementation of the TDS (Tabular DataStream) protocol that is used by Sybase and Microsoft for their database products. 
 
%description 
FreeTDS is a project to document and implement the TDS (Tabular DataStream) 
protocol. TDS is used by Sybase and Microsoft for client to database server 
communications. FreeTDS includes call level interfaces for DB-Lib, CT-Lib, 
and ODBC.  
 
%package devel 
Group: Development/Libraries 
Summary: Include files needed for development with FreeTDS 
Requires: freetds = %{version}

%package unixodbc
Group: System Environment/Libraries
Summary: FreeTDS ODBC Driver for unixODBC
Requires: unixODBC >= 2.0.0
%{?tds_dep:Requires: %tds_dep}

%package doc
Group: Documentation
Summary: User documentation for FreeTDS
 
%description devel
The freetds-devel package contains the files necessary for development with 
the FreeTDS libraries. 

%description unixodbc
The freetds-unixodbc package contains ODBC driver build for unixODBC.

%description doc
The freetds-doc package contains the useguide and reference of FreeTDS 
and can be installed even if FreeTDS main package is not installed

%prep
%setup 
%patch -p0
 
%build
ODBCDIR=`odbc_config --prefix || true`
if test ! -r "$ODBCDIR/include/sql.h"; then
	ODBCDIR=/usr/local
fi
if test ! -r "$ODBCDIR/include/sql.h"; then
	ODBCDIR=/usr
fi
%configure --with-tdsver=4.2 --with-unixodbc="$ODBCDIR"
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"
 
%install 
rm -rf "$RPM_BUILD_ROOT"
make DESTDIR="$RPM_BUILD_ROOT" install
rm -rf "$RPM_BUILD_ROOT/%{_datadir}/doc/freetds-%{version}"

%post 
/sbin/ldconfig 2> /dev/null

%postun
/sbin/ldconfig 2> /dev/null

%post unixodbc
echo "[FreeTDS]
Description = FreeTDS unixODBC Driver
Driver = %{_libdir}/libtdsodbc.so.0
Setup = %{_libdir}/libtdsodbc.so.0" | odbcinst -i -d -r > /dev/null 2>&1 || true
echo "[SQL Server]
Description = FreeTDS unixODBC Driver
Driver = %{_libdir}/libtdsodbc.so.0
Setup = %{_libdir}/libtdsodbc.so.0" | odbcinst -i -d -r > /dev/null 2>&1 || true

%preun unixodbc
odbcinst -u -d -n 'FreeTDS' > /dev/null 2>&1 || true
odbcinst -u -d -n 'SQL Server' > /dev/null 2>&1 || true

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
 
%files 
%defattr(-,root,root) 
%doc AUTHORS BUGS COPYING* ChangeLog INSTALL NEWS README TODO 
%{_bindir}/*
%{_mandir}/man?/*
%{_libdir}/libct.so.*
%{_libdir}/libsybdb.so.*
%config %{_sysconfdir}/*
 
%files devel 
%defattr (-,root,root) 
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_includedir}/*

%files unixodbc
%defattr(-,root,root)
%{_libdir}/libtdsodbc.so*

%files doc
%defattr (-,root,root)
%doc doc/doc/freetds-%{version}/userguide doc/images doc/doc/freetds-%{version}/reference
 
%changelog
