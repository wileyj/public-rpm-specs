%global with_python3 1

Summary: Library providing XML and HTML support
Name: libxml2
Version: 2.9.3
Release: 1.%{?dist}%{?extra_release}
License: MIT
Group: Development/Libraries
Source: ftp://xmlsoft.org/libxml2/libxml2.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%if 0%{?with_python3}
BuildRequires: python3-devel
%endif
BuildRequires: zlib-devel
BuildRequires: pkgconfig
BuildRequires: xz-devel
URL: http://xmlsoft.org/

%description
This library allows to manipulate XML files. It includes support
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified. The output
can be a simple SAX stream or and in-memory DOM like representations.
In this case one can use the built-in XPath and XPointer implementation
to select sub nodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an
URI library.

%package devel
Summary: Libraries, includes, etc. to develop XML and HTML applications
Group: Development/Libraries
Requires: libxml2 = %{version}-%{release}
Requires: zlib-devel
Requires: xz-devel
Requires: pkgconfig

%description devel
Libraries, include files, etc you can use to develop XML applications.
This library allows to manipulate XML files. It includes support
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified. The output
can be a simple SAX stream or and in-memory DOM like representations.
In this case one can use the built-in XPath and XPointer implementation
to select sub nodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an
URI library.

%package static
Summary: Static library for libxml2
Group: Development/Libraries
Requires: libxml2 = %{version}-%{release}

%description static
Static library for libxml2 provided for specific uses or shaving a few
microseconds when parsing, do not link to them for generic purpose packages.

%if 0%{?with_python3}
%package -n %{name}-python3
Summary: Python 3 bindings for the libxml2 library
Group: Development/Libraries
Requires: libxml2 = %{version}-%{release}
Obsoletes: %{name}-python3 < 2.9.2-6
Obsoletes: %{name}-python <= 2.9.2-6
Provides: %{name}-python3 = %{version}-%{release}

%description -n %{name}-python3
The libxml2-python3 package contains a Python 3 module that permits
applications written in the Python programming language, version 3, to use the
interface supplied by the libxml2 library to manipulate XML files.

This library allows to manipulate XML files. It includes support
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DTDs, either
at parse time or later once the document has been modified.
%endif

%package -n %{name}-python
Summary: Python bindings for the libxml2 library
Group: Development/Libraries
Requires: libxml2 = %{version}-%{release}
Obsoletes: %{name}-python < 2.9.2-6
Provides: %{name}-python = %{version}-%{release}
Provides: %{name}-python = %{version}-%{release}

%description -n %{name}-python
The libxml2-python package contains a Python 2 module that permits applications
written in the Python programming language, version 2, to use the interface
supplied by the libxml2 library to manipulate XML files.

This library allows to manipulate XML files. It includes support
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DTDs, either
at parse time or later once the document has been modified.


%prep
%setup -q -n %{name}
./autogen.sh

mkdir py3doc
cp doc/*.py py3doc
sed -i 's|#!/usr/bin/%{python} |#!%{__python3} |' py3doc/*.py

%build
%if 0%{?with_python3}
%configure --with-python=%{__python3}
%else
%configure
%endif
make %{_smp_mflags}
find doc -type f -exec chmod 0644 \{\} \;
%install
rm -fr %{buildroot}
make install DESTDIR=%{buildroot}
touch -m --reference=$RPM_BUILD_ROOT/%{_includedir}/libxml2/libxml/parser.h $RPM_BUILD_ROOT/%{_bindir}/xml2-config
(cd doc/examples ; make clean ; rm -rf .deps Makefile)
gzip -9 -c doc/libxml2-api.xml > doc/libxml2-api.xml.gz


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)

%{!?_licensedir:%global license %%doc}
%license Copyright
%doc AUTHORS NEWS README TODO
%doc %{_mandir}/man1/xmllint.1*
%doc %{_mandir}/man1/xmlcatalog.1*
%doc %{_mandir}/man3/libxml.3*

%{_libdir}/lib*.so.*
%{_bindir}/xmllint
%{_bindir}/xmlcatalog
/usr/share/doc/libxml2*

%files devel
%defattr(-, root, root)

%doc %{_mandir}/man1/xml2-config.1*
%doc AUTHORS NEWS README Copyright
%doc doc/*.html doc/html doc/*.gif doc/*.png
%doc doc/tutorial doc/libxml2-api.xml.gz
%doc doc/examples
%doc %dir %{_datadir}/gtk-doc/html/libxml2
%doc %{_datadir}/gtk-doc/html/libxml2/*.devhelp
%doc %{_datadir}/gtk-doc/html/libxml2/*.html
%doc %{_datadir}/gtk-doc/html/libxml2/*.png
%doc %{_datadir}/gtk-doc/html/libxml2/*.css

%{_libdir}/lib*.so
%{_libdir}/*.sh
%{_includedir}/*
%{_bindir}/xml2-config
%{_datadir}/aclocal/libxml.m4
%{_libdir}/pkgconfig/libxml-2.0.pc
%{_libdir}/cmake/libxml2/libxml2-config.cmake

%files static
%defattr(-, root, root)

%{_libdir}/*a

%if 0%{?with_python3}
%files -n %{name}-python3
%defattr(-, root, root)
%{python3_sitearch}/*
%endif

%files -n %{name}-python
%defattr(-, root, root)
%{python3_sitearch}/*
%doc python/TODO
%doc python/libxml2class.txt
%doc doc/*.py
%doc doc/python.html


%changelog
