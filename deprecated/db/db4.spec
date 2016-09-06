%define java_arches %{ix86} alpha ia64 ppc sparc sparcv9 x86_64 s390 s390x
%define __soversion 4.8
%define realname db4
%define prefix /usr/local/db4
%define _pbindir %{prefix}/bin
%define _plibdir %{prefix}/lib64
%define _pincludedir %{prefix}/include
Summary: The Berkeley DB database library (version 4) for C
Name: db4
Version: 4.8.30
Release: 3.%{dist}
Source0: http://download.oracle.com/berkeley-db/db-%{version}.tar.gz
Source1: http://download.oracle.com/berkeley-db/db.1.85.tar.gz
Patch10: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.1
Patch11: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.2
Patch12: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.3
Patch13: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.4
Patch20: db-1.85-errno.patch
Patch22: db-4.6.21-1.85-compat.patch
Patch24: db-4.5.20-jni-include-dir.patch
URL: http://www.oracle.com/database/berkeley-db/
License: BSD
Vendor: %{vendor}
Packager: %{packager}
Group: System Environment/Libraries
# unversioned obsoletes are OK here as these BDB versions never occur again
Obsoletes: db1, db2, db3, db4
BuildRequires: perl, libtool, ed, util-linux
BuildRequires: tcl-devel >= 8.4.13
#BuildRequires: jdk
BuildRoot: %{_tmppath}/%{realname}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. The Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. The Berkeley DB supports C, C++, Java, and Perl APIs. It is
used by many applications, including Python and Perl, so this should
be installed on all systems.

%package cxx
Summary: The Berkeley DB database library (version 4) for C++
Group: System Environment/Libraries

%description cxx
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. The Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. The Berkeley DB supports C, C++, Java, and Perl APIs. It is
used by many applications, including Python and Perl, so this should
be installed on all systems.

%package utils
Summary: Command line tools for managing Berkeley DB (version 4) databases
Group: Applications/Databases
#Requires: db4 = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
Obsoletes: db1-utils, db2-utils, db3-utils, db4-utils

%description utils
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. DB supports C, C++, Java and Perl APIs.

%package devel
Summary: C development files for the Berkeley DB (version 4) library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-cxx = %{version}-%{release}
Obsoletes: db1-devel, db2-devel, db3-devel, db4-devel

%description devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the header files,
libraries, and documentation for building programs which use the
Berkeley DB.

%package devel-static
Summary: Berkeley DB (version 4) static libraries
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description devel-static
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains static libraries
needed for applications that require statical linking of
Berkeley DB.

%package tcl
Summary: Development files for using the Berkeley DB (version 4) with tcl
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description tcl
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the libraries
for building programs which use the Berkeley DB in Tcl.

#%package java
#Summary: Development files for using the Berkeley DB (version 4) with Java
#Group: Development/Libraries
#Requires: %{name} = %{version}-%{release}

#%description java
#The Berkeley Database (Berkeley DB) is a programmatic toolkit that
#provides embedded database support for both traditional and
#client/server applications. This package contains the libraries
#for building programs which use the Berkeley DB in Java.

%prep
%setup -q -n db-%{version} -a 1

pushd db.1.85/PORT/linux
%patch10 -p0 -b .1.1
popd
pushd db.1.85
%patch11 -p0 -b .1.2
%patch12 -p0 -b .1.3
%patch13 -p0 -b .1.4
%patch20 -p1 -b .errno
popd

%patch22 -p1 -b .185compat
%patch24 -p1 -b .4.5.20.jni

# Remove tags files which we don't need.
find . -name tags | xargs rm -f
# Define a shell function for fixing HREF references in the docs, which
# would otherwise break when we split the docs up into subpackages.
fixup_href() {
	for doc in $@ ; do
		chmod u+w ${doc}
		sed	-e 's,="../api_c/,="../../%{name}-devel-%{version}/api_c/,g' \
			-e 's,="api_c/,="../%{name}-devel-%{version}/api_c/,g' \
			-e 's,="../api_cxx/,="../../%{name}-devel-%{version}/api_cxx/,g' \
			-e 's,="api_cxx/,="../%{name}-devel-%{version}/api_cxx/,g' \
			-e 's,="../api_tcl/,="../../%{name}-devel-%{version}/api_tcl/,g' \
			-e 's,="api_tcl/,="../%{name}-devel-%{version}/api_tcl/,g' \
			-e 's,="../java/,="../../%{name}-devel-%{version}/java/,g' \
			-e 's,="java/,="../%{name}-devel-%{version}/java/,g' \
			-e 's,="../examples_c/,="../../%{name}-devel-%{version}/examples_c/,g' \
			-e 's,="examples_c/,="../%{name}-devel-%{version}/examples_c/,g' \
			-e 's,="../examples_cxx/,="../../%{name}-devel-%{version}/examples_cxx/,g' \
			-e 's,="examples_cxx/,="../%{name}-devel-%{version}/examples_cxx/,g' \
			-e 's,="../ref/,="../../%{name}-devel-%{version}/ref/,g' \
			-e 's,="ref/,="../%{name}-devel-%{version}/ref/,g' \
			-e 's,="../images/,="../../%{name}-devel-%{version}/images/,g' \
			-e 's,="images/,="../%{name}-devel-%{version}/images/,g' \
			-e 's,="../utility/,="../../%{name}-utils-%{version}/utility/,g' \
			-e 's,="utility/,="../%{name}-utils-%{version}/utility/,g' ${doc} > ${doc}.new
		touch -r ${doc} ${doc}.new
		cat ${doc}.new > ${doc}
		touch -r ${doc}.new ${doc}
		rm -f ${doc}.new
	done
}

set +x
# Fix all of the HTML files.
fixup_href `find . -name "*.html"`
set -x

cd dist
./s_config

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -fPIC"

# Build the old db-185 libraries.
make -C db.1.85/PORT/%{_os} OORG="$CFLAGS"

/bin/sh libtool --mode=compile	%{__cc} $RPM_OPT_FLAGS -Idb.1.85/PORT/%{_os}/include -D_REENTRANT -c db_dump185/db_dump185.c -o dist/$1/db_dump185.lo
/bin/sh libtool --mode=link	%{__cc} -o dist/$1/db_dump185 dist/$1/db_dump185.lo db.1.85/PORT/%{_os}/libdb.a
cd build_unix
../dist/configure -C \
	--prefix=%{_prefix} \
	--libdir=%{_plibdir} \
	--includedir=%{_pincludedir} \
	--bindir=%{_pbindir} \
        --enable-compat185 --enable-dump185 \
        --enable-shared --enable-static \
        --enable-tcl --with-tcl=%{_libdir} \
        --enable-cxx 
perl -pi -e 's/^predep_objects=".*$/predep_objects=""/' libtool
perl -pi -e 's/^postdep_objects=".*$/postdep_objects=""/' libtool
perl -pi -e 's/-shared -nostdlib/-shared/' libtool
make %{?_smp_mflags}

# XXX hack around libtool not creating ./libs/libdb_java-X.Y.lai
#LDBJ=./.libs/libdb_java-%{__soversion}.la
#if test -f ${LDBJ} -a ! -f ${LDBJ}i; then
#	sed -e 's,^installed=no,installed=yes,' < ${LDBJ} > ${LDBJ}i
#fi

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_pincludedir}
mkdir -p ${RPM_BUILD_ROOT}%{_plibdir}
mkdir -p ${RPM_BUILD_ROOT}%{_pbindir}
mkdir -p {RPM_BUILD_ROOT}%{_libdir}
cd $RPM_BUILD_DIR/db-%{version}/build_unix/
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_plibdir}/{libdb.a,libdb_cxx.a}
rm -f ${RPM_BUILD_ROOT}%{_plibdir}/libdb-4.so
rm -f ${RPM_BUILD_ROOT}%{_plibdir}/libdb_cxx-4.so
rm -f ${RPM_BUILD_ROOT}%{_plibdir}/libdb_tcl-4.so
rm -f ${RPM_BUILD_ROOT}%{_plibdir}/libdb_tcl.so
chmod +x ${RPM_BUILD_ROOT}%{_plibdir}/*.so*
rm -rf ${RPM_BUILD_ROOT}%{_prefix}/docs
chmod u+w ${RPM_BUILD_ROOT}%{_pbindir} ${RPM_BUILD_ROOT}%{_pbindir}/*
rm -f ${RPM_BUILD_ROOT}%{prefix}/lib/*.la
rm -f ${RPM_BUILD_ROOT}%{_plibdir}/*.la
mkdir ${RPM_BUILD_ROOT}%{_libdir}
ln -sf %{_plibdir}/libdb-%{__soversion}.so ${RPM_BUILD_ROOT}%{_libdir}/libdb-%{__soversion}.so
   
%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig
%post -p /sbin/ldconfig tcl
%postun -p /sbin/ldconfig tcl

%files
%defattr(-,root,root)
%doc LICENSE README
%{_libdir}/libdb-%{__soversion}.so
%{_plibdir}/libdb-%{__soversion}.so

%files cxx
%defattr(-,root,root)
%{_plibdir}/libdb_cxx-%{__soversion}.so

%files utils
%defattr(-,root,root)
%{_pbindir}/db*_archive
%{_pbindir}/db*_checkpoint
%{_pbindir}/db*_deadlock
%{_pbindir}/db*_dump*
%{_pbindir}/db*_hotbackup
%{_pbindir}/db*_load
%{_pbindir}/db*_printlog
%{_pbindir}/db*_recover
%{_pbindir}/db*_sql
%{_pbindir}/db*_stat
%{_pbindir}/db*_upgrade
%{_pbindir}/db*_verify

%files devel
%defattr(-,root,root)
%doc	docs/*
%doc	examples_c examples_cxx
%{_plibdir}/libdb.so
%{_plibdir}/libdb_cxx.so
#%dir %{_pincludedir}%{realname}
#%{_pincludedir}/%{realname}/db.h
#%{_pincludedir}/%{realname}/db_185.h
#%{_pincludedir}/%{realname}/db_cxx.h
%{_pincludedir}/db.h
%{_pincludedir}/db_185.h
%{_pincludedir}/db_cxx.h

%files devel-static
%defattr(-,root,root)
%{_plibdir}/libdb-%{__soversion}.a
%{_plibdir}/libdb_cxx-%{__soversion}.a
%{_plibdir}/libdb_tcl-%{__soversion}.a
#%ifarch %{java_arches}
#%{_plibdir}/libdb_java-%{__soversion}.a
#%endif

%files tcl
%defattr(-,root,root)
%{_plibdir}/libdb_tcl-%{__soversion}.so

#%ifarch %{java_arches}
#%files java
#%defattr(-,root,root)
#%doc docs/java
#%doc examples_java
#%{_libdir}/libdb_java*.so
#%{_datadir}/java/*.jar
#%endif

%changelog
