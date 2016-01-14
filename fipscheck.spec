Summary:	A library for integrity verification of FIPS validated modules
Name:		fipscheck
Version:	1.4.1
Release:	3.%{dist}
License:	BSD
Vendor: %{vendor}
Packager: %{packager}
Group:		System Environment/Libraries
# This is a Red Hat maintained package which is specific to
# our distribution.
URL:		http://fedorahosted.org/fipscheck/
Source0:	http://fedorahosted.org/releases/f/i/%{name}/%{name}-%{version}.tar.bz2
# Prelink blacklist
Source1:	fipscheck.conf

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: 	openssl-devel >= 0.9.8j

Requires:      %{name}-lib%{?_isa} = %{version}-%{release}

%description
FIPSCheck is a library for integrity verification of FIPS validated
modules. The package also provides helper binaries for creation and
verification of the HMAC-SHA256 checksum files.

%package lib
Summary:	Library files for %{name}
Group:		System Environment/Libraries

Requires:	%{_bindir}/fipscheck

%description lib
This package contains the FIPSCheck library.

%package devel
Summary:	Development files for %{name}
Group:		System Environment/Libraries

Requires:	%{name}-lib%{?_isa} = %{version}-%{release}

%description devel
This package contains development files for %{name}.

%prep
%setup -q

%build
%configure --disable-static

make %{?_smp_mflags}

# Add generation of HMAC checksums of the final stripped binaries
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    $RPM_BUILD_ROOT%{_bindir}/fipshmac -d $RPM_BUILD_ROOT%{_libdir}/fipscheck $RPM_BUILD_ROOT%{_bindir}/fipscheck $RPM_BUILD_ROOT%{_libdir}/libfipscheck.so.1.2.1 \
    ln -s libfipscheck.so.1.2.1.hmac $RPM_BUILD_ROOT%{_libdir}/fipscheck/libfipscheck.so.1.hmac \
%{nil}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -delete

mkdir -p $RPM_BUILD_ROOT%{_libdir}/fipscheck

# Prelink blacklist
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/prelink.conf.d
install -m644 %{SOURCE1} \
	$RPM_BUILD_ROOT/%{_sysconfdir}/prelink.conf.d/fipscheck.conf

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%post lib -p /sbin/ldconfig

%postun lib -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING README AUTHORS
%{_bindir}/fipscheck
%{_bindir}/fipshmac
%{_libdir}/fipscheck/fipscheck.hmac
%{_mandir}/man8/*

%files lib
%defattr(-,root,root,-)
%{_libdir}/libfipscheck.so.*
%dir %{_libdir}/fipscheck
%{_libdir}/fipscheck/libfipscheck.so.*.hmac
%dir %{_sysconfdir}/prelink.conf.d
%{_sysconfdir}/prelink.conf.d/fipscheck.conf

%files devel
%defattr(-,root,root,-)
%{_includedir}/fipscheck.h
%{_libdir}/libfipscheck.so
%{_mandir}/man3/*

%changelog
