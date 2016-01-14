%define opt_apache /opt/apache2.2

Summary: GeoIP module for the Apache HTTP Server
Name: mod_geoip
Version: 1.2.8
Release: 1.%{dist}
License: ASL 1.1
Vendor: %{vendor}
Packager: %{packager}
Group: System Environment/Daemons
URL: http://www.maxmind.com/app/mod_geoip
Source: http://www.maxmind.com/download/geoip/api/mod_geoip2/mod_geoip2_%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: GeoIP >= 1.4.8
Requires : httpd
BuildRequires:	 apr-devel, apr-util-devel, apr, apr-util
BuildRequires:	 httpd-tools
BuildRequires:   httpd
BuildRequires:   httpd-devel
BuildRequires:  GeoIP-devel >= 1.4.8

%description
mod_geoip is an Apache module for finding the country that a web request
originated from.  It uses the GeoIP library and database to perform
the lookup.  It is free software, licensed under the Apache license.

%prep

%setup -q -n mod_geoip2_%{version}

%build
%{opt_apache}/bin/apxs -Wc,"%{optflags}" -Wl,"-lGeoIP" -c mod_geoip.c

%install
install -Dp .libs/mod_geoip.so %{buildroot}%{opt_apache}/modules/mod_geoip.so

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr (-,root,root)
%doc INSTALL README* Changes
%{opt_apache}/modules/mod_geoip.so


%changelog
