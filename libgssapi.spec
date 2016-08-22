Summary: Generic Security Services Application Programming Interface Library
Name: libgssapi
Version: 0.11
Release: 1.%{dist}
URL: http://www.citi.umich.edu/projects/nfsv4/linux/
License: GPL
Vendor: %{vendor}
Packager: %{packager}
Source0: http://www.citi.umich.edu/projects/nfsv4/linux/libgssapi/libgssapi-0.11.tar.gz
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: pkgconfig
Requires(postun): /sbin/ldconfig
Requires(pre): /sbin/ldconfig
PreReq: krb5-libs >= 1.5

%description
This library exports a gssapi interface, but doesn't implement any gssapi
mechanisms itself; instead it calls gssapi routines in other libraries,
depending on the mechanism.

%package devel
Summary: Development files for the gssapi library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

Patch0: libgssapi-0.7-gssapi_mech.patch

%description devel
This package includes header files and libraries necessary for
developing programs which use the gssapi library.

%prep
%setup -q
%patch0 -p1

%configure --prefix=%{buildroot}
# Get rid of rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%build
make all 

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/etc
%makeinstall
install -m 644 doc/gssapi_mech.conf %{buildroot}/etc/gssapi_mech.conf
sed -i "s|${RPM_BUILD_ROOT}||g" $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libgssapi.pc


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/libgssapi.so.*
%{_libdir}/libgssapi.la
%config(noreplace) /etc/gssapi_mech.conf

%files devel
%defattr(0644,root,root,755)
%{_libdir}/libgssapi.so
%{_libdir}/libgssapi.a
%dir %{_includedir}/gssglue
%dir %{_includedir}/gssglue/gssapi
%{_includedir}/gssglue/gssapi/gssapi.h
%{_libdir}/pkgconfig/libgssapi.pc

%changelog
