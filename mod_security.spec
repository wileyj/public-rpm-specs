%define         _dirname mod_security-2.6.3
%define         _httpd_min_ver 2.0.47

Summary: Security module for the Apache HTTP Server
Name: mod_security 
Version: 2.6.3
Release: 1.%{dist}
License: GPLv2
Vendor: %{vendor}
Packager: %{packager}
URL: http://www.modsecurity.org/
Group:          System Environment/Daemons
Source: http://www.modsecurity.org/download/modsecurity-apache_%{version}.tar.gz
Requires:  httpd
AutoReq:  0
BuildRequires:	 apr-devel, apr-util-devel, apr, apr-util
BuildRequires:	 httpd-tools
BuildRequires:   httpd >= 2.2
BuildRequires:   httpd-devel
BuildRequires:   libcurl-devel,expat-devel, pcre-devel pcre , libxml2 , libxml2-devel , openldap-devel

%define opt_apache /opt/apache2.2

%description
ModSecurity is an open source intrusion detection and prevention engine
for web applications. It operates embedded into the web server, acting
as a powerful umbrella - shielding web applications from attacks.

%prep
%setup -n modsecurity-apache_%{version}

%build
./configure --with-apxs=%{opt_apache}/bin/apxs --with-apu=/usr/bin/apu-1-config --with-apr=/usr/bin/apr-1-config
make %{_smp_mflags}
make %{_smp_mflags} mlogc

%install

install -d -m755 %{buildroot}%{opt_apache}/modules
install -D -m755 $RPM_BUILD_DIR/modsecurity-apache_%{version}/apache2/.libs/mod_security2.so %{buildroot}%{opt_apache}/modules/mod_security2.so
install -d %{buildroot}%{opt_apache}/modsecurity.d/

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files 
%defattr (-,root,root)
%doc CHANGES LICENSE README.* modsecurity* doc
%{opt_apache}/modules/mod_security2.so
%dir %{opt_apache}/modsecurity.d


%changelog
