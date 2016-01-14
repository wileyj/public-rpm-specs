%global major 5
%global minor 5
%global revision 13 
%global php_prefix /opt/php-%{major}.%{minor}
%global php_bindir %{php_prefix}/bin
%global php_libdir %{php_prefix}/lib
%global php_sbindir %{php_prefix}/sbin
%global php_includedir %{php_prefix}/include
%global mods_available_dir %{php_prefix}/etc/mods_available
%global mods_enabled_dir %{php_prefix}/etc/mods_enabled
%define opt_apache /opt/apache2.2
%global contentdir  %{opt_apache}

# API/ABI check
%global apiver      20121113
%global zendver     20121212
%global pdover      20080721
# Extension version
%global fileinfover 1.0.5
%global pharver      2.0.2
%global zipver      1.11.0
%global jsonver     1.2.1
%global oci8ver     1.4.9

%ifarch ppc ppc64
%global oraclever 10.2.0.2
%else
%global oraclever 11.2
%endif

# version used for php embedded library soname
%global embed_version 5.4


%if 0%{?fedora} < 17 && 0%{?rhel} < 7
%global with_libzip  0
%else
%global with_libzip  1
%endif
%global with_zip     1
%global zipmod       zip

%if 0%{?fedora} < 18 && 0%{?rhel} < 7
%global db_devel  db4-devel
%else
%global db_devel  libdb-devel
%endif

%global with_oci8   %{?_with_oci8:1}%{!?_with_oci8:0}
%global with_fpm 1


%define _default_patch_fuzz 2

# %define httpd_mmn %(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)

Summary: PHP scripting language for creating dynamic web sites
Name: php
Version: %{major}.%{minor}.%{revision}
Release: 20140611.%{dist}
License: PHP
Packager: %{packager}
Vendor: %{vendor}
Group: Development/Languages
URL: http://www.php.net/

Source0: http://www.php.net/distributions/php-%{version}.tar.bz2
Source1: php.conf
Source2: php.ini
Source3: macros.php
Source4: php-fpm.conf
Source5: php-fpm-www.conf
Source6: php-fpm.service
Source7: php-fpm.logrotate
Source8: php-fpm.sysconfig
Source9: php.modconf
Source10: httpd.conf
Source99: php-fpm.init

# Build fixes
Patch5: php-5.2.0-includedir.patch
Patch6: php-5.2.4-embed.patch
Patch7: php-5.3.0-recode.patch
Patch8: php-5.4.7-libdb.patch
#Patch9: bison_build.patch
# Fixes for extension modules
# https://bugs.php.net/63171 no odbc call during timeout
Patch21: php-5.4.7-odbctimer.patch

# Functional changes
Patch40: php-5.4.0-dlopen.patch
Patch41: php-5.4.0-easter.patch
Patch42: php-5.3.1-systzdata-v10.patch
# See http://bugs.php.net/53436
Patch43: php-5.4.0-phpize.patch
# Use system libzip instead of bundled one
Patch44: php-5.4.5-system-libzip.patch
# Use -lldap_r for OpenLDAP
Patch45: php-5.4.8-ldap_r.patch
# Make php_config.h constant across builds
Patch46: php-5.4.9-fixheader.patch
# drop "Configure command" from phpinfo output
Patch47: php-5.4.9-phpinfo.patch

# Fixes for tests

# RC Patch
Patch91: php-5.3.7-oci8conf.patch


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: bzip2-devel, curl-devel >= 7.9, gmp-devel, db4-devel
BuildRequires: httpd-devel, pam-devel, autoconf, freetds-devel
BuildRequires: libstdc++-devel, openssl-devel, net-snmp-devel
#BuildRequires: zlib-devel, pcre, pcre-devel >= 6.6, smtpdaemon, readline-devel
BuildRequires: zlib-devel, pcre, pcre-devel >= 6.6, postfix, readline-devel
BuildRequires: bzip2, perl,libtool , libtool-ltdl-devel , libtool-ltdl , gcc-c++
BuildRequires: libtidy-devel, libxslt-devel, libpng-devel, libjpeg-devel, libXpm-devel, openldap-devel
BuildRequires: freetype-devel, libicu-devel, libmcrypt-devel, aspell-devel, tcp_wrappers-devel
BuildRequires: bison, bison-devel

Obsoletes: php-dbg, php3, phpfi, stronghold-php
Requires(pre): httpd
Requires: httpd
Provides: mod_php = %{version}-%{release}
Provides: php-api = %{apiver}, php-zend-abi = %{zendver}
Provides: php(api) = %{apiver}, php(zend-abi) = %{zendver}
Provides: php-bz2, php-calendar, php-ctype, php-curl, php-date, php-exif, php-devel
Provides: php-ftp, php-gettext, php-gmp, php-hash, php-iconv, php-libxml, php-ldap
Provides: php-reflection, php-session, php-shmop, php-simplexml, php-sockets
Provides: php-spl, php-tokenizer, php-openssl, php-pcre, php-xml
Provides: php-zlib, php-json, php-zip, php-fileinfo, php-cli
Obsoletes: php-openssl, php-pecl-zip, php-pecl-json, php-json, php-pecl-phar, php-pecl-Fileinfo
# For obsoleted pecl extension
Provides: php-pecl-zip = %{zipver}, php-pecl(zip) = %{zipver}
Provides: php-pecl-phar = %{pharver}, php-pecl(phar) = %{pharver}
Provides: php-pecl-Fileinfo = %{fileinfover}, php-pecl(Fileinfo) = %{fileinfover}
Requires: libtool-ltdl


%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated webpages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts.

The php package contains the module which adds support for the PHP
language to Apache HTTP Server.

%package devel
Group: Development/Languages
Summary: Devel package for php.
Requires: php
Provides: php-devel

%description devel
PHP Devel packagae.

%package docs
Group: Development/Languages
Summary: Docs for php.
Requires: php
Provides: php-docs

%description docs
PHP Documentation and manpages.


%prep

%setup -q

%patch5 -p1 -b .includedir
%patch6 -p1 -b .embed
%patch7 -p1 -b .recode
%patch8 -p1 -b .libdb
#%patch9 -p0 -b .zend
rm -f ext/json/utf8_to_utf16.*
#rm -f Zend/zend_{language,ini}_parser.[ch]
./genfiles

%patch21 -p1 -b .odbctimer

%patch40 -p1 -b .dlopen
#%patch41 -p1 -b .easter
%if 0%{?fedora} >= 16 || 0%{?rhel} >= 5
%patch42 -p1 -b .systzdata
%endif
%patch43 -p1 -b .headers
%if %{with_libzip}
%patch44 -p1 -b .systzip
%endif
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%patch45 -p1 -b .ldap_r
%endif
%patch46 -p1 -b .fixheader
%patch47 -p1 -b .phpinfo

%patch91 -p1 -b .remi-oci8


# Prevent %%doc confusion over LICENSE files
cp Zend/LICENSE Zend/ZEND_LICENSE
cp TSRM/LICENSE TSRM_LICENSE
cp ext/ereg/regex/COPYRIGHT regex_COPYRIGHT
cp ext/gd/libgd/README gd_README

mkdir build-apache

# Remove bogus test; position of read position after fopen(, "a+")
# is not defined by C standard, so don't presume anything.
rm -f ext/standard/tests/file/bug21131.phpt

# php_egg_logo_guid() removed by patch41
rm -f tests/basic/php_egg_logo_guid.phpt

# Tests that fail.
rm -f ext/standard/tests/file/bug22414.phpt \
      ext/iconv/tests/bug16069.phpt

# Safety check for API version change.
vapi=`sed -n '/#define PHP_API_VERSION/{s/.* //;p}' main/php.h`
if test "x${vapi}" != "x%{apiver}"; then
   : Error: Upstream API version is now ${vapi}, expecting %{apiver}.
   : Update the apiver macro and rebuild.
   exit 1
fi

vzend=`sed -n '/#define ZEND_MODULE_API_NO/{s/^[^0-9]*//;p;}' Zend/zend_modules.h`
if test "x${vzend}" != "x%{zendver}"; then
   : Error: Upstream Zend ABI version is now ${vzend}, expecting %{zendver}.
   : Update the zendver macro and rebuild.
   exit 1
fi

# Safety check for PDO ABI version change
vpdo=`sed -n '/#define PDO_DRIVER_API/{s/.*[ 	]//;p}' ext/pdo/php_pdo_driver.h`
if test "x${vpdo}" != "x%{pdover}"; then
   : Error: Upstream PDO ABI version is now ${vpdo}, expecting %{pdover}.
   : Update the pdover macro and rebuild.
   exit 1
fi

# Check for some extension version
ver=$(sed -n '/#define PHP_FILEINFO_VERSION /{s/.* "//;s/".*$//;p}' ext/fileinfo/php_fileinfo.h)
if test "$ver" != "%{fileinfover}"; then
   : Error: Upstream FILEINFO version is now ${ver}, expecting %{fileinfover}.
   : Update the fileinfover macro and rebuild.
   exit 1
fi
ver=$(sed -n '/#define PHP_PHAR_VERSION /{s/.* "//;s/".*$//;p}' ext/phar/php_phar.h)
if test "$ver" != "%{pharver}"; then
   : Error: Upstream PHAR version is now ${ver}, expecting %{pharver}.
   : Update the pharver macro and rebuild.
   exit 1
fi
ver=$(sed -n '/#define PHP_ZIP_VERSION_STRING /{s/.* "//;s/".*$//;p}' ext/zip/php_zip.h)
if test "$ver" != "%{zipver}"; then
   : Error: Upstream ZIP version is now ${ver}, expecting %{zipver}.
   : Update the zipver macro and rebuild.
   exit 1
fi
ver=$(sed -n '/#define PHP_JSON_VERSION /{s/.* "//;s/".*$//;p}' ext/json/php_json.h)
if test "$ver" != "%{jsonver}"; then
   : Error: Upstream JSON version is now ${ver}, expecting %{jsonver}.
   : Update the jsonver macro and rebuild.
   exit 1
fi



%build

SNMP_CONFIG=/usr/bin/net-snmp-config-%{_build_arch} ; export SNMP_CONFIG

# aclocal workaround - to be improved
cat `aclocal --print-ac-dir`/{libtool,lt*}.m4 >>aclocal.m4

# Force use of system libtool:
libtoolize --force --copy
cat `aclocal --print-ac-dir`/{libtool,lt*}.m4 >build/libtool.m4

# Regenerate configure scripts (patches change config.m4's)
touch configure.in
./buildconf --force

CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign"
export CFLAGS

# Install extension modules in %{_libdir}/php/modules.
EXTENSION_DIR=%{php_libdir}/php/modules; export EXTENSION_DIR

# Set PEAR_INSTALLDIR to ensure that the hard-coded include_path
# includes the PEAR directory even though pear is packaged
# separately.
PEAR_INSTALLDIR=%{php_prefix}/share/pear; export PEAR_INSTALLDIR
PHP_MYSQLND_ENABLED=yes; export PHP_MYSQLND_ENABLED



# Shell function to configure and build a PHP tree.
build() {
# bison-1.875-2 seems to produce a broken parser; workaround.
mkdir Zend && cp ../Zend/zend_{language,ini}_{parser,scanner}.[ch] Zend
#sed -e '87607s/if//' ../configure
ln -sf ../configure
echo %{_lib}
#cat -n configure
perl -p -i -e 's#net-snmp-config#net-snmp-config-%{_build_arch}#g' configure
SNMP_CONFIG=/usr/bin/net-snmp-config-%{_build_arch} ; export SNMP_CONFIG
PHP_MYSQLND_ENABLED=yes; export PHP_MYSQLND_ENABLED
echo "CXXFLAGS: ${CXXFLAGS}"
echo "CFLAGS: ${CFLAGS}"
echo "LDFLAGS: ${LDFLAGS}"
echo "CPPFLAGS: ${CPPFLAGS}"
#env -i
#unset CFLAGS && unset LDFLAGS && unset CPPFLAGS && unset CXXFLAGS

%configure \
	--enable-maintainer-zts \
	--prefix=%{php_prefix} \
	--bindir=%{php_prefix}/bin \
	--sbindir=%{php_prefix}/sbin \
	--includedir=%{php_prefix}/include \
	--with-libdir=%{_lib} \
	--cache-file=../config.cache \
	--with-config-file-path=%{php_prefix}/etc \
	--with-config-file-scan-dir=%{mods_enabled_dir} \
	--disable-debug \
	--with-pic \
	--disable-rpath \
	--with-bz2 \
	--with-curl \
	--enable-exif \
	--with-exec-dir=%{php_prefix}/bin \
	--with-freetype-dir=%{_prefix} \
	--with-png-dir=%{_prefix} \
	--with-xpm-dir=%{_prefix} \
	--with-gd \
	--enable-gd-native-ttf \
	--with-gettext \
	--with-gmp \
	--with-iconv \
	--with-jpeg-dir=%{_prefix} \
       	--with-icu-dir=%{_prefix} \
        --enable-intl \
	--with-ldap=%{_prefix} \
        --with-mcrypt=%{_prefix} \
	--with-mhash \
	--with-mysql=mysqlnd \
	--with-mysqli=mysqlnd \
	--with-openssl \
	--without-pear \
        --enable-pdo \
        --with-pdo-mysql=mysqlnd \
        --with-pspell \
	--with-zlib \
	--with-layout=GNU \
	--enable-magic-quotes \
	--enable-mbstring \
	--enable-sockets \
	--enable-ucd-snmp-hack \
	--enable-calendar \
	--without-mime-magic \
        --enable-soap \
        --enable-sockets \
        --with-tidy=%{_prefix} \
	--with-libxml-dir=%{_prefix} \
	--enable-xml \
        --with-xmlrpc \
        --with-xsl=%{_prefix} \
	--with-system-tzdata \
        --enable-zip \
	--enable-bcmath=shared \
	--enable-dba=shared --with-db4 \
	--enable-ftp=shared \
	--enable-pcntl=shared \
	--with-snmp=shared,%{_prefix} \
	--enable-wddx=shared \
	$*
if test $? != 0; then
  tail -500 config.log
  : configure failed
  exit 1
fi

#	--without-sqlite \
#	--without-sqlite3 \
# --with-pcre-regex=%{_prefix} \

make -j4 %{?_smp_mflags}
}

# Build Apache module, and the CLI SAPI, /usr/bin/php

pushd build-apache
build --with-apxs2=%{opt_apache}/bin/apxs
popd

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# Install the default configuration file and icons
install -m 755 -d $RPM_BUILD_ROOT%{php_prefix}/etc
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{php_prefix}/etc/php.ini
install -m 755 -d $RPM_BUILD_ROOT%{contentdir}/icons
install -m 644    *.gif $RPM_BUILD_ROOT%{contentdir}/icons/

# For third-party packaging:
install -m 755 -d $RPM_BUILD_ROOT%{php_prefix}/share/pear $RPM_BUILD_ROOT%{_datadir}/php

# install the DSO
install -m 755 -d $RPM_BUILD_ROOT%{opt_apache}/modules
install -m 755 build-apache/libs/libphp5.so $RPM_BUILD_ROOT%{opt_apache}/modules/libphp-%{major}.%{minor}.%{revision}.so
mkdir -p $RPM_BUILD_ROOT/%{opt_apache}/conf
cp %{SOURCE10} $RPM_BUILD_ROOT/%{opt_apache}/conf/httpd.conf
# Apache config fragment
#rm -f $RPM_SOURCE_DIR/php.conf

install -m 755 -d $RPM_BUILD_ROOT%{mods_available_dir}
install -m 755 -d $RPM_BUILD_ROOT%{mods_enabled_dir}
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/session

pushd build-apache
make INSTALL_ROOT=$RPM_BUILD_ROOT install
popd

# Fix the link
#(cd $RPM_BUILD_ROOT%{php_bindir}; ln -sfn phar.phar phar)

nonstandard_mods=( bcmath dba ftp pcntl snmp wddx )

for mod in ${nonstandard_mods[*]}; do
	cat > $RPM_BUILD_ROOT%{mods_available_dir}/${mod}.ini <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
    cat >> files.php <<EOF
%attr(755,root,root) %{php_libdir}/php/modules/${mod}.so
%config(noreplace) %attr(644,root,root) %{mods_available_dir}/${mod}.ini
EOF
done

# Package json, zip, curl, phar and fileinfo in -common.
#cat files.json files.zip files.curl files.phar files.fileinfo > files.common

# Install the macros file:
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rpm
sed -e "s/@PHP_APIVER@/%{apiver}/;s/@PHP_ZENDVER@/%{zendver}/;s/@PHP_PDOVER@/%{pdover}/" \
    < $RPM_SOURCE_DIR/macros.php > macros.php
install -m 644 -c macros.php \
           $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.php
#symlink the apache library for sanity
ln -sf %{opt_apache}/modules/libphp-%{major}.%{minor}.%{revision}.so  $RPM_BUILD_ROOT%{opt_apache}/modules/libphp-%{major}.%{minor}.so

#pwd=`pwd`
%{__mkdir_p} %{buildroot}%{_bindir}
%__ln_s %{php_bindir}/phpize %{buildroot}%{_bindir}/phpize
%__ln_s %{php_bindir}/php %{buildroot}%{_bindir}/php
%__ln_s %{php_bindir}/php-config %{buildroot}%{_bindir}/php-config
%__ln_s %{php_bindir}/php-cgi %{buildroot}%{_bindir}/php-cgi
%__ln_s %{php_bindir}/phar.phar %{buildroot}%{_bindir}/phar
#cd $pwd

# Remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{php_libdir}/php/modules/*.a \
       $RPM_BUILD_ROOT%{_bindir}/phptar \
       $RPM_BUILD_ROOT%{_datadir}/pear \
       $RPM_BUILD_ROOT%{_libdir}/libphp5.la \
       $RPM_BUILD_ROOT/.channels \
       $RPM_BUILD_ROOT/.depdb \
       $RPM_BUILD_ROOT/.depdblock \
       $RPM_BUILD_ROOT/.filemap \
       $RPM_BUILD_ROOT/.lock \
       $RPM_BUILD_ROOT/%{opt_apache}/conf/httpd.conf* \
       $RPM_BUILD_ROOT/%{opt_apache}/modules/libphp5.so

# Remove irrelevant docs
rm -f README.{Zeus,QNX,CVS-RULES}

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

#%files -f files.php
%files 
%defattr(-,root,root)
%config(noreplace) %{php_prefix}/etc/php.ini
%config(noreplace) %{php_prefix}/etc/mods_available/bcmath.ini
%config(noreplace) %{php_prefix}/etc/mods_available/dba.ini
%config(noreplace) %{php_prefix}/etc/mods_available/ftp.ini
%config(noreplace) %{php_prefix}/etc/mods_available/pcntl.ini
%config(noreplace) %{php_prefix}/etc/mods_available/snmp.ini
%config(noreplace) %{php_prefix}/etc/mods_available/wddx.ini
%{php_libdir}/php/modules/opcache.so
%{php_libdir}/php/modules/bcmath.so
%{php_libdir}/php/modules/dba.so
%{php_libdir}/php/modules/ftp.so
%{php_libdir}/php/modules/pcntl.so
%{php_libdir}/php/modules/snmp.so
%{php_libdir}/php/modules/wddx.so
%dir %{_localstatedir}/lib/php
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/session
%dir %{_datadir}/php
%{opt_apache}/modules/libphp-%{major}.%{minor}.%{revision}.so
%{opt_apache}/modules/libphp-%{major}.%{minor}.so
%dir %{mods_available_dir}
%{php_bindir}/php
%{_bindir}/php
%{php_bindir}/php-cgi
%{_bindir}/php-cgi
%{php_bindir}/phar.phar
%{php_bindir}/phar
%{_bindir}/phar
%{opt_apache}/icons/php.gif

%files devel
%defattr(-,root,root)
%{php_bindir}/php-config
%{_bindir}/php-config
%{php_bindir}/phpize
%{_bindir}/phpize
%{php_includedir}/php
%{_libdir}/build
%config %{_sysconfdir}/rpm/macros.php

%files docs
%defattr(-,root,root)
%{_mandir}/man1/php.1*
%{_mandir}/man1/php-cgi.1*
%{_mandir}/man1/phar.1*
%{_mandir}/man1/phar.phar.1*
%{_mandir}/man1/php-config.1*
%{_mandir}/man1/phpize.1*

%changelog
