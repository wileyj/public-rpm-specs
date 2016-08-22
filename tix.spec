%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}
%{!?tcl_sitelib: %global tcl_sitelib %{_datadir}/tcl%{tcl_version}}
%global tixmajor 8.4
%global tcltkver 8.4.13

Summary: A set of extension widgets for Tk
Name: tix
Epoch: 1
Version: %{tixmajor}.3
Release: 17.%{?dist}
License: BSD
Group: Development/Languages
URL: http://tix.sourceforge.net/
Source0: http://downloads.sourceforge.net/project/%{name}/%{name}/%{version}/Tix%{version}-src.tar.gz
#  0: Fixes BZ#81297 (soname of libraries)
Patch0: tix-8.4.2-link.patch
Patch1: tix-8.4.3-tcl86.patch
Requires: tcl(abi) = 8.5
Requires: tcl >= %{tcltkver}, tk >= %{tcltkver}
Requires: /etc/ld.so.conf.d
Buildrequires: tcl-devel >= %{tcltkver}, tk-devel >= %{tcltkver}
BuildRequires: libX11-devel

%description
Tix, the Tk Interface eXtension, is a powerful set of user interface
components that expands the capabilities of your Tcl/Tk and Python
applications. Using Tix together with Tk will greatly enhance the
appearance and functionality of your application.

%package devel
Summary: Tk Interface eXtension development files
Group: Development/Languages
Requires: tix = %{epoch}:%{version}-%{release}

%description devel
Tix, the Tk Interface eXtension, is a powerful set of user interface
components that expands the capabilities of your Tcl/Tk and Python
applications. Using Tix together with Tk will greatly enhance the
appearance and functionality of your application.

This package contains the tix development files needed for building
tix applications.

%package doc
Summary: Tk Interface eXtension documentation
Group: Development/Languages
Requires: tix = %{epoch}:%{version}-%{release}

%description doc
Tix, the Tk Interface eXtension, is a powerful set of user interface
components that expands the capabilities of your Tcl/Tk and Python
applications. Using Tix together with Tk will greatly enhance the
appearance and functionality of your application.

This package contains the tix documentation

%prep
%setup -q -n Tix%{version}
%patch0 -p1 -b .link
%patch1 -p1 -b .tcl86

# Remove executable permission of images in html documentation
chmod ugo-x docs/html/gif/tix/*.png docs/html/gif/tix/*.gif \
  docs/html/gif/tix/*/*.gif

# Fix end-of-line encoding
sed -i 's/\r//' docs/Release-8.4.0.txt

%build
%configure --with-tcl=%{_libdir} --with-tk=%{_libdir} --libdir=%{tcl_sitearch}
make all %{?_smp_mflags} PKG_LIB_FILE=libTix.so

%install
make install DESTDIR=$RPM_BUILD_ROOT PKG_LIB_FILE=libTix.so

# move shared lib to tcl sitearch
mv $RPM_BUILD_ROOT%{tcl_sitearch}/Tix%{version}/libTix.so \
	$RPM_BUILD_ROOT%{tcl_sitearch}
pwd
# make links
ln -sf ../libTix.so \
	$RPM_BUILD_ROOT%{tcl_sitearch}/Tix%{version}/libTix.so
ln -sf tcl%{tcl_version}/Tix%{version}/libTix.so $RPM_BUILD_ROOT%{_libdir}/libTix.so
ln -sf tcl%{tcl_version}/Tix%{version}/libTix.so $RPM_BUILD_ROOT%{_libdir}/libtix.so

# install demo scripts
mkdir -p $RPM_BUILD_ROOT%{tcl_sitelib}/Tix%{tixmajor}
cp -a demos $RPM_BUILD_ROOT%{tcl_sitelib}/Tix%{tixmajor}

# the header and man pages were in the previous package, keeping for now...
mkdir -p $RPM_BUILD_ROOT%{_includedir}
install -m 0644 generic/tix.h $RPM_BUILD_ROOT%{_includedir}/tix.h
mkdir -p $RPM_BUILD_ROOT%{_mandir}/mann
cp man/*.n $RPM_BUILD_ROOT%{_mandir}/mann

# Handle unique library path (so apps can actually find the library)
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
echo "%{tcl_sitearch}" > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/tix-%{_arch}.conf

# ship docs except pdf
rm -rf docs/pdf
find docs -name .cvsignore -exec rm '{}' ';'

# these files end up in the doc directory
rm -f $RPM_BUILD_ROOT%{_libdir}/Tix%{tixmajor}/README.txt
rm -f $RPM_BUILD_ROOT%{_libdir}/Tix%{tixmajor}/license.terms

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%{tcl_sitearch}/libTix.so
%{tcl_sitearch}/Tix%{version}
%{_sysconfdir}/ld.so.conf.d/*
%doc *.txt *.html license.terms

%files devel
%{_includedir}/tix.h
%{_libdir}/libtix.so
%{_libdir}/libTix.so
%{_mandir}/mann/*.n*

%files doc
%doc docs/*
%doc %{tcl_sitelib}/Tix%{tixmajor}

%changelog
