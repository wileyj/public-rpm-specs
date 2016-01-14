%global major 5
%global minor 5
%global php_prefix /opt/php-%{major}.%{minor}
%global php_sysconfdir %{php_prefix}/etc
%global php_bindir %{php_prefix}/bin
%global peardir %{php_prefix}/share/pear
%global php_extdir %(/opt/php-%{major}.%{minor}/bin/php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)
%global php_zendabiver %((echo 0; /opt/php-%{major}.%{minor}/bin/php -i 2>/dev/null | sed -n 's/^PHP Extension => //p') | tail -1)
%global php_version %((echo 0; /opt/php-%{major}.%{minor}/bin/php-config --version 2>/dev/null) | tail -1)


%global xmlrpcver 1.5.4
%global getoptver 1.3.1
%global arctarver 1.3.7
%global structver 1.0.4
%global xmlutil   1.2.1

Summary: PHP Extension and Application Repository framework
Name: php-pear
Version: 1.9.4
Release:	 20140919.%{dist}
Epoch: 4
License: BSD and PHP and LGPLv2+
Packager: %{packager}
Vendor: %{vendor}
Group: Development/Languages
URL: http://pear.php.net/package/PEAR
Source0: http://download.pear.php.net/package/PEAR-%{version}.tgz
# wget http://cvs.php.net/viewvc.cgi/pear-core/install-pear.php?revision=1.39 -O install-pear.php
Source1: install-pear.php
Source2: relocate.php
Source3: strip.php
Source10: pear.sh
Source11: pecl.sh
Source12: peardev.sh
Source13: macros.pear
Source20: http://pear.php.net/get/XML_RPC-%{xmlrpcver}.tgz
Source21: http://pear.php.net/get/Archive_Tar-%{arctarver}.tgz
Source22: http://pear.php.net/get/Console_Getopt-%{getoptver}.tgz
Source23: http://pear.php.net/get/Structures_Graph-%{structver}.tgz
Source24: http://pear.php.net/get/XML_Util-%{xmlutil}.tgz

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-xml, gnupg
Provides: php-pear(Console_Getopt) = %{getoptver}
Provides: php-pear(Archive_Tar) = %{arctarver}
Provides: php-pear(PEAR) = %{version}
Provides: php-pear(Structures_Graph) = %{structver}
Provides: php-pear(XML_RPC) = %{xmlrpcver}
Provides: php-pear(XML_Util) = %{xmlutil}
Obsoletes: php-pear-XML-Util <= %{xmlutil}
Provides:  php-pear-XML-Util = %{xmlutil}-%{release}
BuildRequires: php > 5.5
Requires: php > 5.5

%description
PEAR is a framework and distribution system for reusable PHP
components.  This package contains the basic PEAR components.

%prep
%setup -cT

# Create a usable PEAR directory (used by install-pear.php)
for archive in %{SOURCE0} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24}
do
    tar xzf  $archive --strip-components 1 || tar xzf  $archive --strip-path 1
    file=${archive##*/}
    [ -f LICENSE ] && mv LICENSE LICENSE-${file%%-*}
    [ -f README ]  && mv README  README-${file%%-*}
done
tar xzf %{SOURCE24} package.xml
mv package.xml XML_Util.xml

# apply patches on used PEAR during install
# -- no patch

%build
# This is an empty build section.

%install
rm -rf $RPM_BUILD_ROOT

export PHP_PEAR_SYSCONF_DIR=%{php_sysconfdir}
export PHP_PEAR_SIG_KEYDIR=%{php_sysconfdir}/pearkeys
export PHP_PEAR_SIG_BIN=%{_bindir}/gpg
export PHP_PEAR_INSTALL_DIR=%{peardir}

# 1.4.11 tries to write to the cache directory during installation
# so it's not possible to set a sane default via the environment.
# The ${PWD} bit will be stripped via relocate.php later.
export PHP_PEAR_CACHE_DIR=${PWD}%{_localstatedir}/cache/php-pear
export PHP_PEAR_TEMP_DIR=/var/tmp

install -d $RPM_BUILD_ROOT%{peardir} \
           $RPM_BUILD_ROOT%{_localstatedir}/cache/php-pear \
           $RPM_BUILD_ROOT%{_localstatedir}/www/html \
           $RPM_BUILD_ROOT%{peardir}/.pkgxml \
           $RPM_BUILD_ROOT%{php_sysconfdir}/rpm \
           $RPM_BUILD_ROOT%{php_sysconfdir}/pear

export INSTALL_ROOT=$RPM_BUILD_ROOT

%{php_bindir}/php -n -dmemory_limit=32M -dshort_open_tag=0 -dsafe_mode=0 \
         -derror_reporting=E_ALL -ddetect_unicode=0 \
      %{SOURCE1} -d %{peardir} \
                 -c %{php_sysconfdir}/pear \
                 -b %{php_bindir} \
                 -w %{_localstatedir}/www/html \
                 %{SOURCE0} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24} %{SOURCE20}

# Replace /usr/bin/* with simple scripts:
install -d -m 755 $RPM_BUILD_ROOT%{php_bindir}
install -m 755 %{SOURCE10} $RPM_BUILD_ROOT%{php_bindir}/pear
install -m 755 %{SOURCE11} $RPM_BUILD_ROOT%{php_bindir}/pecl
install -m 755 %{SOURCE12} $RPM_BUILD_ROOT%{php_bindir}/peardev

# Sanitize the pear.conf
%{php_bindir}/php -n %{SOURCE2} $RPM_BUILD_ROOT%{php_sysconfdir}/pear.conf $RPM_BUILD_ROOT | 
  %{php_bindir}/php -n %{SOURCE2} php://stdin $PWD > new-pear.conf
%{php_bindir}/php -n %{SOURCE3} new-pear.conf ext_dir |
  %{php_bindir}/php -n %{SOURCE3} php://stdin http_proxy > $RPM_BUILD_ROOT%{php_sysconfdir}/pear.conf

%{php_bindir}/php -r "print_r(unserialize(substr(file_get_contents('$RPM_BUILD_ROOT%{php_sysconfdir}/pear.conf'),17)));"

install -m 644 -c %{SOURCE13} \
           $RPM_BUILD_ROOT%{php_sysconfdir}/rpm/macros.pear     

# apply patches on installed PEAR tree
pushd $RPM_BUILD_ROOT%{peardir} 
# -- no patch
popd

# Why this file here ?
rm -rf $RPM_BUILD_ROOT/.depdb* $RPM_BUILD_ROOT/.lock $RPM_BUILD_ROOT/.channels $RPM_BUILD_ROOT/.filemap

# Need for re-registrying XML_Util
install -m 644 XML_Util.xml $RPM_BUILD_ROOT%{peardir}/.pkgxml/

%{__mkdir_p} %{buildroot}%{_bindir}
%__ln_s %{php_bindir}/pear %{buildroot}%{_bindir}/pear
%__ln_s %{php_bindir}/peardev %{buildroot}%{_bindir}/peardev
%__ln_s %{php_bindir}/pecl %{buildroot}%{_bindir}/pecl

%check
# Check that no bogus paths are left in the configuration, or in
# the generated registry files.
grep $RPM_BUILD_ROOT $RPM_BUILD_ROOT%{php_sysconfdir}/pear.conf && exit 1
grep %{_libdir} $RPM_BUILD_ROOT%{php_sysconfdir}/pear.conf && exit 1
grep '"/tmp"' $RPM_BUILD_ROOT%{php_sysconfdir}/pear.conf && exit 1
grep /usr/local $RPM_BUILD_ROOT%{php_sysconfdir}/pear.conf && exit 1
grep -rl $RPM_BUILD_ROOT $RPM_BUILD_ROOT && exit 1


%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
#rm new-pear.conf


%triggerpostun -- php-pear-XML-Util
# re-register extension unregistered during postun of obsoleted php-pear-XML-Util
%{php_bindir}/pear install --nodeps --soft --force --register-only %{pear_xmldir}/XML_Util.xml >/dev/null || :


%files
%defattr(-,root,root,-)
%{peardir}
%{php_bindir}/*
%{_bindir}/pear
%{_bindir}/peardev
%{_bindir}/pecl
%config(noreplace) %{php_sysconfdir}/pear.conf
%config %{php_sysconfdir}/rpm/macros.pear
%dir %{_localstatedir}/cache/php-pear
%dir %{_localstatedir}/www/html
%dir %{php_sysconfdir}/pear
%doc README* LICENSE*


%changelog
