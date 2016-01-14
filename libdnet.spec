Summary:	Simple portable interface to lowlevel networking routines
Name:		libdnet
Version:	1.12
Release:	6.%{dist}
License:	BSD
Vendor: %{vendor}
Packager: %{packager}
Group:		System Environment/Libraries
URL:		https://github.com/dugsong/libdnet
Source:		%{name}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
libdnet provides a simplified, portable interface to several
low-level networking routines, including network address
manipulation, kernel arp(4) cache and route(4) table lookup and
manipulation, network firewalling (IP filter, ipfw, ipchains,
pf, ...), network interface lookup and manipulation, raw IP
packet and Ethernet frame, and data transmission.

%package devel
Summary:	Header files for libdnet library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
%{summary}.

%package progs
Summary:	Sample applications to use with libdnet
Group:		Applications/Internet
Requires:	%{name} = %{version}-%{release}

%description progs
%{summary}.

%prep
%setup -q -n %{name}

%build
git pull

%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

%clean
#[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
#[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
#[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc LICENSE README THANKS TODO
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%exclude %{_libdir}/*.la
%{_includedir}/*
%{_mandir}/man3/*.3*

%files progs
%defattr(-,root,root,-)
%{_sbindir}/*
%{_mandir}/man8/*.8*

%changelog
