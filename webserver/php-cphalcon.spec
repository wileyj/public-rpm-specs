%define repo https://github.com/phalcon/cphalcon
%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="css-truncate-target"' | head -1 |  tr -d '\\-</span class="css-truncate-target">v'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1

%define realname cphalcon
%global php_ver  7
%global opt_apache /opt/apache2.2
%global opt_php /opt/php-%{php_ver}

Name:           php-cphalcon
Version:        %{gitversion}
Release:        %{rel_version}.%{dist}
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
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update

%build
cd %{name}-%{version}
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

