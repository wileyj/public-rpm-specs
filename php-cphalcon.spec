
%define major    2
%define minor    0
%define revision 0
%define realname cphalcon
%global php_ver  5.5
%global opt_apache /opt/apache2.2
%global opt_php /opt/php-%{php_ver}

Name:           php-cphalcon
Version:        %{major}.%{minor}.%{revision}
Release:        1.%{dist}
Summary:	php web framework
License: BSD and PHP and LGPLv2+
Packager: %{packager}
Vendor: %{vendor}
Group: Development/Languages
URL:            https://github.com/phalcon/cphalcon
Source0:        %{realname}-%{version}.tar.gz
Source1:	cphalcon.ini
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	php >= %{php_ver}, php-devel >= %{php_ver}
Requires:	php >= %{php_ver}, php-devel >= %{php_ver}

%description 
Phalcon is a web framework implemented as a C extension offering high performance and lower resource consumption.

%prep
rm -rf %{buildroot}

%setup -q -n %{realname}
export PATH=$PATH:%{php_ver}/bin
cd build
#sed -i -e 's/make install/make install DESTDIR=$RPM_BUILD_ROOT/g' install
sed -i -e 's/make install \&\&//g' install
sh -x install
mkdir -p $RPM_BUILD_ROOT%{opt_php}/lib/php/modules/
mkdir -p $RPM_BUILD_ROOT%{opt_apache}/conf
%__install -p -m 0755 64bits/modules/phalcon.so $RPM_BUILD_ROOT%{opt_php}/lib/php/modules/phalcon.so
%__install -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{opt_apache}/conf/cphalcon.ini

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root,-)
%{opt_apache}/conf/cphalcon.ini
%{opt_php}/lib/php/modules/phalcon.so

