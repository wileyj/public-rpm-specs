Summary: Routines to help with network packet contruction and handling
Name: libnet
Version: 1.1.2.1
Release: 2.%{dist}
License: GPL
Group: Development/Libraries
URL: http://www.packetfactory.net/projects/libnet/

Vendor: %{vendor}
Packager: %{packager}

Source: http://www.packetfactory.net/libnet/dist/libnet-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Libnet is a high-level API (toolkit) allowing the application programmer to
construct and inject network packets. It provides a portable and simplified
interface for low-level network packet shaping, handling and injection.

Libnet hides much of the tedium of packet creation from the application
programmer such as multiplexing, buffer management, arcane packet header
information, byte-ordering, OS-dependent issues, and much more. Libnet
features portable packet creation interfaces at the IP layer and link layer,
as well as a host of supplementary and complementary functionality.

Using libnet, quick and simple packet assembly applications can be whipped up
with little effort. With a bit more time, more complex programs can be written
(Traceroute and ping were easily rewritten using libnet and libpcap).

%package devel
Group: Development/Libraries
Summary: Developer tools for the Libnet library
Requires: %{name} = %{version}

%description devel
Header files needed to develop programs that link against the libnet library.


%prep
%setup -n %{name}

%build
%{expand: %%define optflags %{optflags} -fPIC}
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall
%{__install} -D -m0755 libnet-config %{buildroot}%{_bindir}/libnet-config

%{__install} -d -m0755 %{buildroot}%{_mandir}/man3/
%{__install} -D -m0644 doc/man/man3/*.3 %{buildroot}%{_mandir}/man3/

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-, root, root, 0755)
%doc README doc/BUGS doc/CHANGELOG doc/CONTRIB doc/COPYING doc/DESIGN_NOTES
%doc doc/MIGRATION doc/PACKET* doc/PORTED doc/RAWSOCKET* doc/TODO doc/html/
%doc %{_mandir}/man3/*.3*
%{_bindir}/libnet-config
%{_libdir}/libnet.a
%files devel
%{_includedir}/libnet.h
%{_includedir}/libnet/

%changelog
