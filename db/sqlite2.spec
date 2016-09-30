Name:           sqlite2
Version:        2.8.17
Release:        1.%{dist}

Summary:        Embeddable SQL engine in a C library
Group:          System Environment/Libraries
License:        Public Domain
Packager: %{packager}
Vendor: %{vendor}
URL:            http://www.sqlite.org/
Source0:        http://www.sqlite.org/sqlite-%{version}.tar.gz
Patch1:         sqlite-2.8.15.rpath.patch
Patch2:         sqlite-2.8.15-makefile.patch
Patch3:         sqlite-2.8.3.test.rh9.patch
Patch4:         sqlite-64bit-fixes.patch
Patch5:         sqlite-2.8.15-arch-double-differences.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  ncurses-devel readline-devel %{_includedir}/tcl.h
Obsoletes:      sqlite < 3

%description
SQLite is a small, fast, embeddable SQL database engine that supports
most of SQL92, including transactions with atomic commit and rollback,
subqueries, compound queries, triggers, and views. A complete database
is stored in a single cross-platform disk file. The native C/C++ API
is simple and easy to use. Bindings for other languages are also
available.

%package        devel
Summary:        Development files for SQLite
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Obsoletes:      sqlite-devel < 3

%description    devel
SQLite is a small, fast, embeddable SQL database engine that supports
most of SQL92, including transactions with atomic commit and rollback,
subqueries, compound queries, triggers, and views.
This package contains static library and header files for developing
applications using sqlite.

%package        tcl
Summary:        Tcl bindings for sqlite
Group:          System Environment/Libraries
Requires:       tcl >= 8.3.3, %{name} = %{version}-%{release}
Obsoletes:      sqlite-tcl < 3

%description    tcl
SQLite is a small, fast, embeddable SQL database engine that supports
most of SQL92, including transactions with atomic commit and rollback,
subqueries, compound queries, triggers, and views.
This package contains tcl bindings for sqlite.

%prep
%setup -q -n sqlite-%{version}
%patch1 -p1 -b .rpath
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
sed -i.rpath 's!__VERSION__!%{version}!g' Makefile.in
# Patch additional /usr/lib locations where we don't have $(libdir)
# to substitute with.
sed -i.lib 's!@exec_prefix@/lib!%{_libdir}!g' Makefile.in

%build
CFLAGS="$RPM_OPT_FLAGS -DNDEBUG=1"
%configure --enable-utf8 --disable-static
make
make tclsqlite libtclsqlite.la doc
#obs. make test doesn't like root
#make test

%install
rm -rf $RPM_BUILD_ROOT
DIRECTORY=$RPM_BUILD_ROOT%{_libdir}/sqlite-%version
install -d $DIRECTORY
echo 'package ifneeded sqlite 2 [list load [file join $dir libtclsqlite.so]]' > $DIRECTORY/pkgIndex.tcl

%makeinstall
install -D -m 0644 sqlite.1 $RPM_BUILD_ROOT%{_mandir}/man1/sqlite.1

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/sql*
%{_libdir}/libsql*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%doc README  doc/*
%{_libdir}/libsql*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*

%files tcl
%defattr(-,root,root,-)
%doc doc/tclsqlite.html
%exclude %{_bindir}/tclsqlite
%{_libdir}/sqlite-%version

%changelog
