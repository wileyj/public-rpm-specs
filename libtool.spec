Name:       libtool
Version:    2.4.6
Release:    1.%{dist}
Summary:    libtool
Group:      Development/Tools
License:    GNU GPL
URL:        http://www.gnu.org/software/libtool/
Vendor:     %{vendor}
Packager:   %{packager}
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  x86_64 
BuildRequires:  autoconf 
Requires:   autoconf
Requires(post):  info
Requires(preun): info
AutoReq: no

%description
The libtool package contains the GNU libtool, a set of shell scripts which
automatically configure UNIX and UNIX-like architectures to generically build
shared libraries.  Libtool provides a consistent, portable interface which
simplifies the process of using shared libraries.
libtool

%package -n libltdl
Summary:    Shared library files for %{name}
Group:      Development/Libraries

%description -n libltdl
Shared library files for libtool DLL library from the libtool package.

%package -n libltdl-devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   libltdl = %{version}-%{release}

%description -n libltdl-devel
This package contains static libraries and header files need for development.


%setup -q -c -T
%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone git://git.savannah.gnu.org/libtool.git %{name}-%{version}
cd %{name}-%{version}

%build
cd %{name}-%{version}
./bootstrap
%configure --prefix=/usr --docdir=/usr/share/doc/automake-1.11
make %{?_smp_mflags}

%install
cd %{name}-%{version}
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

rm -rf %{buildroot}%{_infodir}/dir


%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%post
%install_info %{name}.info

%preun
%uninstall_info %{name}.info

%post -n libltdl -p /sbin/ldconfig
%postun -n libltdl -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/libtool
%{_bindir}/libtoolize
%dir %{_datadir}/libtool/
%{_infodir}/%{name}.info*
%{_mandir}/man1/libtool.1.gz
%{_mandir}/man1/libtoolize.1.gz
   %{_datarootdir}/aclocal/%{name}.m4
   %{_datarootdir}/aclocal/ltargz.m4
   %{_datarootdir}/aclocal/ltdl.m4
   %{_datarootdir}/aclocal/ltoptions.m4
   %{_datarootdir}/aclocal/ltsugar.m4
   %{_datarootdir}/aclocal/ltversion.m4
   %{_datarootdir}/aclocal/lt~obsolete.m4
   %{_datarootdir}/%{name}/COPYING.LIB
   %{_datarootdir}/%{name}/Makefile.am
   %{_datarootdir}/%{name}/Makefile.in
   %{_datarootdir}/%{name}/README
   %{_datarootdir}/%{name}/aclocal.m4
   %{_datarootdir}/%{name}/build-aux/compile
   %{_datarootdir}/%{name}/build-aux/config.guess
   %{_datarootdir}/%{name}/build-aux/config.sub
   %{_datarootdir}/%{name}/build-aux/depcomp
   %{_datarootdir}/%{name}/build-aux/install-sh
   %{_datarootdir}/%{name}/build-aux/ltmain.sh
   %{_datarootdir}/%{name}/build-aux/missing
   %{_datarootdir}/%{name}/config-h.in
   %{_datarootdir}/%{name}/configure
   %{_datarootdir}/%{name}/configure.ac
   %{_datarootdir}/%{name}/loaders/dld_link.c
   %{_datarootdir}/%{name}/loaders/dlopen.c
   %{_datarootdir}/%{name}/loaders/dyld.c
   %{_datarootdir}/%{name}/loaders/load_add_on.c
   %{_datarootdir}/%{name}/loaders/loadlibrary.c
   %{_datarootdir}/%{name}/loaders/preopen.c
   %{_datarootdir}/%{name}/loaders/shl_load.c
   %{_datarootdir}/%{name}/lt__alloc.c
   %{_datarootdir}/%{name}/lt__argz.c
   %{_datarootdir}/%{name}/lt__dirent.c
   %{_datarootdir}/%{name}/lt__strl.c
   %{_datarootdir}/%{name}/lt_dlloader.c
   %{_datarootdir}/%{name}/lt_error.c
   %{_datarootdir}/%{name}/ltdl.c
   %{_datarootdir}/%{name}/ltdl.h
   %{_datarootdir}/%{name}/ltdl.mk
   %{_datarootdir}/%{name}/slist.c

%files -n libltdl
%defattr(-,root,root)
%dir %{_datadir}/libtool/libltdl/
%{_datadir}/libtool/libltdl/*
%{_libdir}/libltdl.so.*

%files -n libltdl-devel
%defattr(-,root,root)
%{_includedir}/ltdl.h
%{_includedir}/libltdl
%{_libdir}/libltdl.a
%{_libdir}/libltdl.la
%{_libdir}/libltdl.so

%changelog
