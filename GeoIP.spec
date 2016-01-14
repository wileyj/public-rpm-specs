%define tarballversion 1.4.8
Name: GeoIP           
Version: 1.4.8
Release: 1.%{dist}
Summary: C library for country/city/organization to IP address or hostname mapping     
Group: Development/Libraries         
License: LGPLv2+
Vendor: %{vendor}
Packager: %{packager}
URL: http://www.maxmind.com/app/c            
Source0: GeoIP-%{tarballversion}.tar.gz 
Source1: LICENSE.txt
Source2: fetch-geoipdata-city.pl
Source3: fetch-geoipdata.pl
Source4: README.Fedora
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Obsoletes: geoip < %{version}-%{release}
Provides: geoip = %{version}-%{release}
BuildRequires: zlib-devel libtool

%description
GeoIP is a C library that enables the user to find the country that any IP
address or hostname originates from. It uses a file based database that is
accurate as of March 2003. This database simply contains IP blocks as keys, and
countries as values. This database should be more complete and accurate than
using reverse DNS lookups.

%package devel
Summary: Development headers and libraries for GeoIP     
Group: Development/Libraries         
Requires: %{name} = %{version}-%{release}
Provides: geoip-devel = %{version}-%{release}
Obsoletes: geoip-devel < %{version}-%{release}

%description devel
Development headers and static libraries for building GeoIP-based applications

%prep
%setup -q -n %{name}-%{tarballversion}
#%patch0 -p1
install -D -m644 %{SOURCE1} LICENSE.txt
install -D -m644 %{SOURCE2} fetch-geoipdata-city.pl
install -D -m644 %{SOURCE3} fetch-geoipdata.pl
install -D -m644 %{SOURCE4} README.fedora

%build
%configure --disable-static --disable-dependency-tracking
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

# nix the stuff we don't need like .la files.
rm -f %{buildroot}/%{_libdir}/*.la

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README TODO INSTALL LICENSE* fetch-*
%{_libdir}/libGeoIP.so.*
%{_libdir}/libGeoIPUpdate.so.*
%{_bindir}/geoiplookup6
%{_bindir}/geoiplookup
%{_bindir}/geoipupdate
%config(noreplace) %{_sysconfdir}/GeoIP.conf.default
%config(noreplace) %{_sysconfdir}/GeoIP.conf
%{_datadir}/GeoIP
%{_mandir}/man1/geoiplookup.1*
%{_mandir}/man1/geoiplookup6.1*
%{_mandir}/man1/geoipupdate.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/GeoIP.h
%{_includedir}/GeoIPCity.h
%{_includedir}/GeoIPUpdate.h
%{_libdir}/libGeoIP.so
%{_libdir}/libGeoIPUpdate.so

%changelog
