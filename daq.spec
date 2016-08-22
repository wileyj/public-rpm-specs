%define version 2.0.6

Summary: Data Acquisition Library
License: GNU General Public License
Vendor: %{vendor}
Packager: %{packager}
Group: Libraries/Network
Name: daq
Prefix: %{_prefix}
Provides: daq
Release: 1.%{dist}
Source: daq-%{version}.tar.gz
URL: http://www.snort.org/
Version: %{version}

BuildRoot: /tmp/daqrpm-%{version}
BuildRequires: autoconf, automake, flex, libpcap-devel

%description
Data Acquisition library for Snort.

%prep
%setup -q

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root)
%{_includedir}/daq.h
%{_includedir}/daq_common.h
%{_includedir}/sfbpf_dlt.h
%{_includedir}/daq_api.h
%{_includedir}/sfbpf.h
%{_libdir}/libdaq_static_modules.la
%{_libdir}/libdaq_static_modules.a
%{_libdir}/libsfbpf.a
%{_libdir}/libdaq.so
%{_libdir}/libsfbpf.la
%{_libdir}/libdaq.la
%{_libdir}/daq
%{_libdir}/daq/daq_dump.so
%{_libdir}/daq/daq_ipfw.la
%{_libdir}/daq/daq_dump.la
%{_libdir}/daq/daq_afpacket.la
%{_libdir}/daq/daq_pcap.so
%{_libdir}/daq/daq_pcap.la
%{_libdir}/daq/daq_ipfw.so
%{_libdir}/daq/daq_afpacket.so
%{_libdir}/libsfbpf.so*
%{_libdir}/libdaq_static.la
%{_libdir}/libdaq.so*
%{_libdir}/libsfbpf.so
%{_libdir}/libdaq.a
%{_libdir}/libdaq_static.a
%{_bindir}/daq-modules-config

