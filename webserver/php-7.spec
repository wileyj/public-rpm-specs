# Fedora spec file for php
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
# API/ABI check
%global apiver      20160303
%global zendver     20160303
%global pdover      20150127
# Extension version
%global jsonver     1.5.0

# Adds -z now to the linker flags
%global _hardened_build 1

# version used for php embedded library soname
%global embed_version 7.1

%global mysql_sock %(mysql_config --socket 2>/dev/null || echo /var/lib/mysql/mysql.sock)

# Regression tests take a long time, you can skip 'em with this
#global runselftest 0
%{!?runselftest: %global runselftest 1}

# Use the arch-specific mysql_config binary to avoid mismatch with the
# arch detection heuristic used by bindir/mysql_config.
%global mysql_config %{_libdir}/mysql/mysql_config

# Build ZTS extension or only NTS
%global with_zts      1

%if 0%{?__isa_bits:1}
%global isasuffix -%{__isa_bits}
%else
%global isasuffix %nil
%endif

# needed at srpm build time, when httpd-devel not yet installed
%{!?_httpd_mmn:        %{expand: %%global _httpd_mmn        %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}}

%global with_dtrace 1

# build with system libgd
%if 0%{?fedora} < 20
%global  with_libgd 0
%else
%global  with_libgd 1
%endif

%global with_zip     0
%global with_libzip  0
# Not yet compatible with firebird 3
# https://bugs.php.net/bug.php?id=73512
%global with_firebird 1

%if 0%{?fedora} < 18 && 0%{?rhel} < 7
%global db_devel  db4-devel
%else
%global db_devel  libdb-devel
%endif

%global rcver  RC1
%global rpmrel 1

Summary: PHP scripting language for creating dynamic web sites
Name: php
Version: 7.1.1
%if 0%{?rcver:1}
Release: 0.%{rpmrel}.%{rcver}%{?dist}
%else
Release: %{rpmrel}%{?dist}
%endif
# All files licensed under PHP version 3.01, except
# Zend is licensed under Zend
# TSRM is licensed under BSD
License: PHP and Zend and BSD
Group: Development/Languages
URL: http://www.php.net/

Source0: http://www.php.net/distributions/php-%{version}%{?rcver}.tar.xz
Source1: php.conf
Source2: php.ini
Source3: macros.php
Source4: php-fpm.conf
Source5: php-fpm-www.conf
Source6: php-fpm.service
Source7: php-fpm.logrotate
Source9: php.modconf
Source10: php.ztsmodconf
Source13: nginx-fpm.conf
Source14: nginx-php.conf
# Configuration files for some extensions
Source50: 10-opcache.ini
Source51: opcache-default.blacklist

# Build fixes
Patch5: php-7.0.0-includedir.patch
Patch6: php-5.6.3-embed.patch
Patch7: php-5.3.0-recode.patch
Patch8: php-7.0.2-libdb.patch

# Functional changes
Patch40: php-7.0.0-dlopen.patch
Patch42: php-7.1.0-systzdata-v14.patch
# See http://bugs.php.net/53436
Patch43: php-5.4.0-phpize.patch
# Use -lldap_r for OpenLDAP
Patch45: php-5.6.3-ldap_r.patch
# Make php_config.h constant across builds
Patch46: php-7.0.0-fixheader.patch
# drop "Configure command" from phpinfo output
Patch47: php-5.6.3-phpinfo.patch

# Upstream fixes (100+)

# Security fixes (200+)

# Fixes for tests (300+)
# Factory is droped from system tzdata
Patch300: php-5.6.3-datetests.patch


BuildRequires: bzip2-devel, curl-devel >= 7.9
BuildRequires: httpd-devel >= 2.0.46-1, pam-devel
# to ensure we are using httpd with filesystem feature (see #1081453)
BuildRequires: httpd-filesystem
# to ensure we are using nginx with filesystem feature (see #1142298)
BuildRequires: nginx-filesystem
BuildRequires: libstdc++-devel, openssl-devel
BuildRequires: sqlite-devel >= 3.6.0
BuildRequires: zlib-devel, smtpdaemon, libedit-devel
BuildRequires: pcre-devel >= 6.6
BuildRequires: bzip2, perl, libtool >= 1.4.3, gcc-c++
BuildRequires: libtool-ltdl-devel
%if %{with_libzip}
BuildRequires: libzip-devel >= 0.11
%endif
%if %{with_dtrace}
BuildRequires: systemtap-sdt-devel
%endif

%if %{with_zts}
Provides: php-zts = %{version}-%{release}
Provides: php-zts%{?_isa} = %{version}-%{release}
%endif

Requires: httpd-mmn = %{_httpd_mmn}
Provides: mod_php = %{version}-%{release}
Requires: php-common%{?_isa} = %{version}-%{release}
# For backwards-compatibility, require php-cli for the time being:
Requires: php-cli%{?_isa} = %{version}-%{release}
# To ensure correct /var/lib/php/session ownership:
Requires(pre): httpd-filesystem
# php engine for Apache httpd webserver
Provides: php(httpd)


%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated web pages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts.

The php package contains the module (often referred to as mod_php)
which adds support for the PHP language to Apache HTTP Server.

%package cli
Group: Development/Languages
Summary: Command-line interface for PHP
Requires: php-common%{?_isa} = %{version}-%{release}
Provides: php-cgi = %{version}-%{release}, php-cgi%{?_isa} = %{version}-%{release}
Provides: php-pcntl, php-pcntl%{?_isa}
Provides: php-readline, php-readline%{?_isa}

%description cli
The php-cli package contains the command-line interface
executing PHP scripts, /usr/bin/php, and the CGI interface.


%package dbg
Group: Development/Languages
Summary: The interactive PHP debugger
Requires: php-common%{?_isa} = %{version}-%{release}

%description dbg
The php-dbg package contains the interactive PHP debugger.


%package fpm
Group: Development/Languages
Summary: PHP FastCGI Process Manager
# All files licensed under PHP version 3.01, except
# Zend is licensed under Zend
# TSRM and fpm are licensed under BSD
License: PHP and Zend and BSD
BuildRequires: libacl-devel
Requires: php-common%{?_isa} = %{version}-%{release}
Requires(pre): /usr/sbin/useradd
BuildRequires: systemd-units
BuildRequires: systemd-devel
Requires: systemd-units
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
# To ensure correct /var/lib/php/session ownership:
Requires(pre): httpd-filesystem
# For php.conf in /etc/httpd/conf.d
# and version 2.4.10 for proxy support in SetHandler
Requires: httpd-filesystem >= 2.4.10
# php engine for Apache httpd webserver
Provides: php(httpd)
# for /etc/nginx ownership
Requires: nginx-filesystem

%description fpm
PHP-FPM (FastCGI Process Manager) is an alternative PHP FastCGI
implementation with some additional features useful for sites of
any size, especially busier sites.

%package common
Group: Development/Languages
Summary: Common files for PHP
# All files licensed under PHP version 3.01, except
# fileinfo is licensed under PHP version 3.0
# regex, libmagic are licensed under BSD
# main/snprintf.c, main/spprintf.c and main/rfc1867.c are ASL 1.0
License: PHP and BSD and ASL 1.0
# ABI/API check - Arch specific
Provides: php(api) = %{apiver}%{isasuffix}
Provides: php(zend-abi) = %{zendver}%{isasuffix}
Provides: php(language) = %{version}, php(language)%{?_isa} = %{version}
# Provides for all builtin/shared modules:
Provides: php-bz2, php-bz2%{?_isa}
Provides: php-calendar, php-calendar%{?_isa}
Provides: php-core = %{version}, php-core%{?_isa} = %{version}
Provides: php-ctype, php-ctype%{?_isa}
Provides: php-curl, php-curl%{?_isa}
Provides: php-date, php-date%{?_isa}
Provides: php-exif, php-exif%{?_isa}
Provides: php-fileinfo, php-fileinfo%{?_isa}
Provides: php-filter, php-filter%{?_isa}
Provides: php-ftp, php-ftp%{?_isa}
Provides: php-gettext, php-gettext%{?_isa}
Provides: php-hash, php-hash%{?_isa}
Provides: php-mhash = %{version}, php-mhash%{?_isa} = %{version}
Provides: php-iconv, php-iconv%{?_isa}
Provides: php-libxml, php-libxml%{?_isa}
Provides: php-openssl, php-openssl%{?_isa}
Provides: php-phar, php-phar%{?_isa}
Provides: php-pcre, php-pcre%{?_isa}
Provides: php-reflection, php-reflection%{?_isa}
Provides: php-session, php-session%{?_isa}
Provides: php-sockets, php-sockets%{?_isa}
Provides: php-spl, php-spl%{?_isa}
Provides: php-standard = %{version}, php-standard%{?_isa} = %{version}
Provides: php-tokenizer, php-tokenizer%{?_isa}
# For user experience, those extensions were part of php-common
Requires: php-json%{?_isa} = %{version}-%{release}
%if %{with_zip}
Provides: php-zip, php-zip%{?_isa}
Obsoletes: php-pecl-zip < 1.11
%endif
Provides: php-zlib, php-zlib%{?_isa}

%description common
The php-common package contains files used by both the php
package and the php-cli package.

%package devel
Group: Development/Libraries
Summary: Files needed for building PHP extensions
Requires: php-cli%{?_isa} = %{version}-%{release}, autoconf, automake
Requires: pcre-devel%{?_isa}
Obsoletes: php-pecl-json-devel  < %{jsonver}
Obsoletes: php-pecl-jsonc-devel < %{jsonver}
%if %{with_zts}
Provides: php-zts-devel = %{version}-%{release}
Provides: php-zts-devel%{?_isa} = %{version}-%{release}
%endif

%description devel
The php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.

%package opcache
Summary:   The Zend OPcache
Group:     Development/Languages
License:   PHP
Requires:  php-common%{?_isa} = %{version}-%{release}
Provides:  php-pecl-zendopcache = %{version}
Provides:  php-pecl-zendopcache%{?_isa} = %{version}
Provides:  php-pecl(opcache) = %{version}
Provides:  php-pecl(opcache)%{?_isa} = %{version}

%description opcache
The Zend OPcache provides faster PHP execution through opcode caching and
optimization. It improves PHP performance by storing precompiled script
bytecode in the shared memory. This eliminates the stages of reading code from
the disk and compiling it on future access. In addition, it applies a few
bytecode optimization patterns that make code execution faster.

%package imap
Summary: A module for PHP applications that use IMAP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: krb5-devel, openssl-devel, libc-client-devel

%description imap
The php-imap module will add IMAP (Internet Message Access Protocol)
support to PHP. IMAP is a protocol for retrieving and uploading e-mail
messages on mail servers. PHP is an HTML-embedded scripting language.

%package ldap
Summary: A module for PHP applications that use LDAP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: cyrus-sasl-devel, openldap-devel, openssl-devel

%description ldap
The php-ldap adds Lightweight Directory Access Protocol (LDAP)
support to PHP. LDAP is a set of protocols for accessing directory
services over the Internet. PHP is an HTML-embedded scripting
language.

%package pdo
Summary: A database access abstraction module for PHP applications
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
# ABI/API check - Arch specific
Provides: php-pdo-abi  = %{pdover}%{isasuffix}
Provides: php(pdo-abi) = %{pdover}%{isasuffix}
Provides: php-sqlite3, php-sqlite3%{?_isa}
Provides: php-pdo_sqlite, php-pdo_sqlite%{?_isa}

%description pdo
The php-pdo package contains a dynamic shared object that will add
a database access abstraction layer to PHP.  This module provides
a common interface for accessing MySQL, PostgreSQL or other
databases.

%package mysqlnd
Summary: A module for PHP applications that use MySQL databases
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-mysqli = %{version}-%{release}
Provides: php-mysqli%{?_isa} = %{version}-%{release}
Provides: php-pdo_mysql, php-pdo_mysql%{?_isa}

%description mysqlnd
The php-mysqlnd package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.

This package use the MySQL Native Driver

%package pgsql
Summary: A PostgreSQL database module for PHP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-pdo_pgsql, php-pdo_pgsql%{?_isa}
BuildRequires: krb5-devel, openssl-devel, postgresql-devel

%description pgsql
The php-pgsql package add PostgreSQL database support to PHP.
PostgreSQL is an object-relational database management
system that supports almost all SQL constructs. PHP is an
HTML-embedded scripting language. If you need back-end support for
PostgreSQL, you should install this package in addition to the main
php package.

%package process
Summary: Modules for PHP script using system process interfaces
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
Provides: php-posix, php-posix%{?_isa}
Provides: php-shmop, php-shmop%{?_isa}
Provides: php-sysvsem, php-sysvsem%{?_isa}
Provides: php-sysvshm, php-sysvshm%{?_isa}
Provides: php-sysvmsg, php-sysvmsg%{?_isa}

%description process
The php-process package contains dynamic shared objects which add
support to PHP using system interfaces for inter-process
communication.

%package odbc
Summary: A module for PHP applications that use ODBC databases
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# pdo_odbc is licensed under PHP version 3.0
License: PHP
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-pdo_odbc, php-pdo_odbc%{?_isa}
BuildRequires: unixODBC-devel

%description odbc
The php-odbc package contains a dynamic shared object that will add
database support through ODBC to PHP. ODBC is an open specification
which provides a consistent API for developers to use for accessing
data sources (which are often, but not always, databases). PHP is an
HTML-embeddable scripting language. If you need ODBC support for PHP
applications, you will need to install this package and the php
package.

%package soap
Summary: A module for PHP applications that use the SOAP protocol
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: libxml2-devel

%description soap
The php-soap package contains a dynamic shared object that will add
support to PHP for using the SOAP web services protocol.

%if %{with_firebird}
%package interbase
Summary: A module for PHP applications that use Interbase/Firebird databases
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
# for fb_config command
BuildRequires:  firebird-devel
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-firebird, php-firebird%{?_isa}
Provides: php-pdo_firebird, php-pdo_firebird%{?_isa}

%description interbase
The php-interbase package contains a dynamic shared object that will add
database support through Interbase/Firebird to PHP.

InterBase is the name of the closed-source variant of this RDBMS that was
developed by Borland/Inprise.

Firebird is a commercially independent project of C and C++ programmers,
technical advisors and supporters developing and enhancing a multi-platform
relational database management system based on the source code released by
Inprise Corp (now known as Borland Software Corp) under the InterBase Public
License.
%endif

%package snmp
Summary: A module for PHP applications that query SNMP-managed devices
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}, net-snmp
BuildRequires: net-snmp-devel

%description snmp
The php-snmp package contains a dynamic shared object that will add
support for querying SNMP devices to PHP.  PHP is an HTML-embeddable
scripting language. If you need SNMP support for PHP applications, you
will need to install this package and the php package.

%package xml
Summary: A module for PHP applications which use XML
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
Provides: php-dom, php-dom%{?_isa}
Provides: php-domxml, php-domxml%{?_isa}
Provides: php-simplexml, php-simplexml%{?_isa}
Provides: php-wddx, php-wddx%{?_isa}
Provides: php-xmlreader, php-xmlreader%{?_isa}
Provides: php-xmlwriter, php-xmlwriter%{?_isa}
Provides: php-xsl, php-xsl%{?_isa}
BuildRequires: libxslt-devel >= 1.0.18-1, libxml2-devel >= 2.4.14-1

%description xml
The php-xml package contains dynamic shared objects which add support
to PHP for manipulating XML documents using the DOM tree,
and performing XSL transformations on XML documents.

%package xmlrpc
Summary: A module for PHP applications which use the XML-RPC protocol
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libXMLRPC is licensed under BSD
License: PHP and BSD
Requires: php-xml%{?_isa} = %{version}-%{release}

%description xmlrpc
The php-xmlrpc package contains a dynamic shared object that will add
support for the XML-RPC protocol to PHP.

%package mbstring
Summary: A module for PHP applications which need multi-byte string handling
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libmbfl is licensed under LGPLv2
# onigurama is licensed under BSD
# ucgendat is licensed under OpenLDAP
License: PHP and LGPLv2 and BSD and OpenLDAP
Requires: php-common%{?_isa} = %{version}-%{release}

%description mbstring
The php-mbstring package contains a dynamic shared object that will add
support for multi-byte string handling to PHP.

%package gd
Summary: A module for PHP applications for using the gd graphics library
Group: Development/Languages
# All files licensed under PHP version 3.01
%if %{with_libgd}
License: PHP
%else
# bundled libgd is licensed under BSD
License: PHP and BSD
%endif
Requires: php-common%{?_isa} = %{version}-%{release}
%if %{with_libgd}
BuildRequires: gd-devel >= 2.1.0
%else
# Required to build the bundled GD library
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: freetype-devel
BuildRequires: libXpm-devel
BuildRequires: libwebp-devel
%endif

%description gd
The php-gd package contains a dynamic shared object that will add
support for using the gd graphics library to PHP.

%package bcmath
Summary: A module for PHP applications for using the bcmath library
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libbcmath is licensed under LGPLv2+
License: PHP and LGPLv2+
Requires: php-common%{?_isa} = %{version}-%{release}

%description bcmath
The php-bcmath package contains a dynamic shared object that will add
support for using the bcmath library to PHP.

%package gmp
Summary: A module for PHP applications for using the GNU MP library
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
BuildRequires: gmp-devel
Requires: php-common%{?_isa} = %{version}-%{release}

%description gmp
These functions allow you to work with arbitrary-length integers
using the GNU MP library.

%package dba
Summary: A database abstraction layer module for PHP applications
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
BuildRequires: %{db_devel}, tokyocabinet-devel
Requires: php-common%{?_isa} = %{version}-%{release}

%description dba
The php-dba package contains a dynamic shared object that will add
support for using the DBA database abstraction layer to PHP.

%package mcrypt
Summary: Standard PHP module provides mcrypt library support
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: libmcrypt-devel

%description mcrypt
The php-mcrypt package contains a dynamic shared object that will add
support for using the mcrypt library to PHP.

%package tidy
Summary: Standard PHP module provides tidy library support
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: libtidy-devel

%description tidy
The php-tidy package contains a dynamic shared object that will add
support for using the tidy library to PHP.

%package pdo-dblib
Summary: PDO driver Microsoft SQL Server and Sybase databases
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-pdo%{?_isa} = %{version}-%{release}
BuildRequires: freetds-devel
Provides: php-pdo_dblib, php-pdo_dblib%{?_isa}

%description pdo-dblib
The php-pdo-dblib package contains a dynamic shared object
that implements the PHP Data Objects (PDO) interface to enable access from
PHP to Microsoft SQL Server and Sybase databases through the FreeTDS libary.

%package embedded
Summary: PHP library for embedding in applications
Group: System Environment/Libraries
Requires: php-common%{?_isa} = %{version}-%{release}
# doing a real -devel package for just the .so symlink is a bit overkill
Provides: php-embedded-devel = %{version}-%{release}
Provides: php-embedded-devel%{?_isa} = %{version}-%{release}

%description embedded
The php-embedded package contains a library which can be embedded
into applications to provide PHP scripting language support.

%package pspell
Summary: A module for PHP applications for using pspell interfaces
Group: System Environment/Libraries
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: aspell-devel >= 0.50.0

%description pspell
The php-pspell package contains a dynamic shared object that will add
support for using the pspell library to PHP.

%package recode
Summary: A module for PHP applications for using the recode library
Group: System Environment/Libraries
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: recode-devel

%description recode
The php-recode package contains a dynamic shared object that will add
support for using the recode library to PHP.

%package intl
Summary: Internationalization extension for PHP applications
Group: System Environment/Libraries
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: libicu-devel >= 4.0

%description intl
The php-intl package contains a dynamic shared object that will add
support for using the ICU library to PHP.

%package enchant
Summary: Enchant spelling extension for PHP applications
Group: System Environment/Libraries
# All files licensed under PHP version 3.0
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: enchant-devel >= 1.2.4

%description enchant
The php-enchant package contains a dynamic shared object that will add
support for using the enchant library to PHP.

%package json
Summary: JavaScript Object Notation extension for PHP
# All files licensed under PHP version 3.0.1
License: PHP
Group: System Environment/Libraries
Requires: php-common%{?_isa} = %{version}-%{release}
Obsoletes: php-pecl-json          < %{jsonver}
Obsoletes: php-pecl-jsonc         < %{jsonver}
Provides:  php-pecl(json)         = %{jsonver}
Provides:  php-pecl(json)%{?_isa} = %{jsonver}
Provides:  php-pecl-json          = %{jsonver}
Provides:  php-pecl-json%{?_isa}  = %{jsonver}

%description json
The php-json package provides an extension that will add
support for JavaScript Object Notation (JSON) to PHP.



%prep
%setup -q -n php-%{version}%{?rcver}

# ensure than current httpd use prefork MPM.
httpd -V  | grep -q 'threaded:.*yes' && exit 1

%patch5 -p1 -b .includedir
%patch6 -p1 -b .embed
%patch7 -p1 -b .recode
%patch8 -p1 -b .libdb

%patch40 -p1 -b .dlopen
%patch42 -p1 -b .systzdata
%patch43 -p1 -b .headers
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%patch45 -p1 -b .ldap_r
%endif
%patch46 -p1 -b .fixheader
%patch47 -p1 -b .phpinfo

# upstream patches

# security patches

# Fixes for tests
%patch300 -p1 -b .datetests


# Prevent %%doc confusion over LICENSE files
cp Zend/LICENSE Zend/ZEND_LICENSE
cp TSRM/LICENSE TSRM_LICENSE
%if ! %{with_libgd}
cp ext/gd/libgd/README libgd_README
cp ext/gd/libgd/COPYING libgd_COPYING
%endif
cp sapi/fpm/LICENSE fpm_LICENSE
cp ext/mbstring/libmbfl/LICENSE libmbfl_LICENSE
cp ext/mbstring/oniguruma/COPYING oniguruma_COPYING
cp ext/mbstring/ucgendat/OPENLDAP_LICENSE ucgendat_LICENSE
cp ext/fileinfo/libmagic/LICENSE libmagic_LICENSE
cp ext/phar/LICENSE phar_LICENSE
cp ext/bcmath/libbcmath/COPYING.LIB libbcmath_COPYING

# Multiple builds for multiple SAPIs
mkdir build-cgi build-apache build-embedded \
%if %{with_zts}
    build-zts build-ztscli \
%endif
    build-fpm

# ----- Manage known as failed test -------
# affected by systzdata patch
rm ext/date/tests/timezone_location_get.phpt
rm ext/date/tests/timezone_version_get.phpt
rm ext/date/tests/timezone_version_get_basic1.phpt
# fails sometime
rm ext/sockets/tests/mcast_ipv?_recv.phpt
# cause stack exhausion
rm Zend/tests/bug54268.phpt
rm Zend/tests/bug68412.phpt

# Safety check for API version change.
pver=$(sed -n '/#define PHP_VERSION /{s/.* "//;s/".*$//;p}' main/php_version.h)
if test "x${pver}" != "x%{version}%{?rcver}"; then
   : Error: Upstream PHP version is now ${pver}, expecting %{version}%{?rcver}.
   : Update the version/rcver macros and rebuild.
   exit 1
fi

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

ver=$(sed -n '/#define PHP_JSON_VERSION /{s/.* "//;s/".*$//;p}' ext/json/php_json.h)
if test "$ver" != "%{jsonver}"; then
   : Error: Upstream JSON version is now ${ver}, expecting %{jsonver}.
   : Update the %{jsonver} macro and rebuild.
   exit 1
fi

# https://bugs.php.net/63362 - Not needed but installed headers.
# Drop some Windows specific headers to avoid installation,
# before build to ensure they are really not needed.
rm -f TSRM/tsrm_win32.h \
      TSRM/tsrm_config.w32.h \
      Zend/zend_config.w32.h \
      ext/mysqlnd/config-win.h \
      ext/standard/winver.h \
      main/win32_internal_function_disabled.h \
      main/win95nt.h

# Fix some bogus permissions
find . -name \*.[ch] -exec chmod 644 {} \;
chmod 644 README.*

# php-fpm configuration files for tmpfiles.d
echo "d /run/php-fpm 755 root root" >php-fpm.tmpfiles

# Some extensions have their own configuration file
cp %{SOURCE50} 10-opcache.ini

%ifarch x86_64
sed -e '/opcache.huge_code_pages/s/0/1/' -i 10-opcache.ini
%endif


%build
# aclocal workaround - to be improved
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >>aclocal.m4

# Force use of system libtool:
libtoolize --force --copy
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >build/libtool.m4

# Regenerate configure scripts (patches change config.m4's)
touch configure.in
./buildconf --force

CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign"
export CFLAGS

# Install extension modules in %{_libdir}/php/modules.
EXTENSION_DIR=%{_libdir}/php/modules; export EXTENSION_DIR

# Set PEAR_INSTALLDIR to ensure that the hard-coded include_path
# includes the PEAR directory even though pear is packaged
# separately.
PEAR_INSTALLDIR=%{_datadir}/pear; export PEAR_INSTALLDIR

# Shell function to configure and build a PHP tree.
build() {
# Old/recent bison version seems to produce a broken parser;
# upstream uses GNU Bison 2.3. Workaround:
mkdir Zend && cp ../Zend/zend_{language,ini}_{parser,scanner}.[ch] Zend

# Always static:
# date, ereg, filter, libxml, reflection, spl: not supported
# hash: for PHAR_SIG_SHA256 and PHAR_SIG_SHA512
# session: dep on hash, used by soap and wddx
# pcre: used by filter, zip
# pcntl, readline: only used by CLI sapi
# openssl: for PHAR_SIG_OPENSSL
# zlib: used by image

ln -sf ../configure
%configure \
    --cache-file=../config.cache \
    --with-libdir=%{_lib} \
    --with-config-file-path=%{_sysconfdir} \
    --with-config-file-scan-dir=%{_sysconfdir}/php.d \
    --disable-debug \
    --with-pic \
    --disable-rpath \
    --without-pear \
    --with-exec-dir=%{_bindir} \
    --with-freetype-dir=%{_prefix} \
    --with-png-dir=%{_prefix} \
    --with-xpm-dir=%{_prefix} \
    --enable-gd-native-ttf \
    --without-gdbm \
    --with-jpeg-dir=%{_prefix} \
    --with-openssl \
    --with-system-ciphers \
    --with-pcre-regex=%{_prefix} \
    --with-zlib \
    --with-layout=GNU \
    --with-kerberos \
    --with-libxml-dir=%{_prefix} \
    --with-system-tzdata \
    --with-mhash \
%if %{with_dtrace}
    --enable-dtrace \
%endif
    $*
if test $? != 0; then
  tail -500 config.log
  : configure failed
  exit 1
fi

make %{?_smp_mflags}
}

# Build /usr/bin/php-cgi with the CGI SAPI, and most shared extensions
pushd build-cgi

build --libdir=%{_libdir}/php \
      --enable-pcntl \
      --enable-opcache \
      --enable-opcache-file \
      --enable-phpdbg \
      --with-imap=shared --with-imap-ssl \
      --enable-mbstring=shared \
      --enable-mbregex \
%if %{with_libgd}
      --with-gd=shared,%{_prefix} \
%else
      --with-gd=shared \
%endif
      --with-gmp=shared \
      --enable-calendar=shared \
      --enable-bcmath=shared \
      --with-bz2=shared \
      --enable-ctype=shared \
      --enable-dba=shared --with-db4=%{_prefix} \
                          --with-tcadb=%{_prefix} \
      --enable-exif=shared \
      --enable-ftp=shared \
      --with-gettext=shared \
      --with-iconv=shared \
      --enable-sockets=shared \
      --enable-tokenizer=shared \
      --with-xmlrpc=shared \
      --with-ldap=shared --with-ldap-sasl \
      --enable-mysqlnd=shared \
      --with-mysqli=shared,mysqlnd \
      --with-mysql-sock=%{mysql_sock} \
%if %{with_firebird}
      --with-interbase=shared \
      --with-pdo-firebird=shared \
%endif
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-simplexml=shared \
      --enable-xml=shared \
      --enable-wddx=shared \
      --with-snmp=shared,%{_prefix} \
      --enable-soap=shared \
      --with-xsl=shared,%{_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared,%{_prefix} \
      --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_prefix} \
      --with-pdo-mysql=shared,mysqlnd \
      --with-pdo-pgsql=shared,%{_prefix} \
      --with-pdo-sqlite=shared,%{_prefix} \
      --with-pdo-dblib=shared,%{_prefix} \
      --with-sqlite3=shared,%{_prefix} \
      --enable-json=shared \
%if %{with_zip}
      --enable-zip=shared \
%if %{with_libzip}
      --with-libzip \
%endif
%endif
      --without-readline \
      --with-libedit \
      --with-pspell=shared \
      --enable-phar=shared \
      --with-mcrypt=shared,%{_prefix} \
      --with-tidy=shared,%{_prefix} \
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-shmop=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,%{_prefix} \
      --enable-fileinfo=shared \
      --enable-intl=shared \
      --with-icu-dir=%{_prefix} \
      --with-enchant=shared,%{_prefix} \
      --with-recode=shared,%{_prefix}
popd

without_shared="--without-gd \
      --disable-dom --disable-dba --without-unixODBC \
      --disable-opcache \
      --disable-json \
      --disable-xmlreader --disable-xmlwriter \
      --without-sqlite3 --disable-phar --disable-fileinfo \
      --without-pspell --disable-wddx \
      --without-curl --disable-posix --disable-xml \
      --disable-simplexml --disable-exif --without-gettext \
      --without-iconv --disable-ftp --without-bz2 --disable-ctype \
      --disable-shmop --disable-sockets --disable-tokenizer \
      --disable-sysvmsg --disable-sysvshm --disable-sysvsem"

# Build Apache module, and the CLI SAPI, /usr/bin/php
pushd build-apache
build --with-apxs2=%{_httpd_apxs} \
      --libdir=%{_libdir}/php \
      --without-mysqli \
      --disable-pdo \
      ${without_shared}
popd

# Build php-fpm
pushd build-fpm
build --enable-fpm \
      --with-fpm-acl \
      --with-fpm-systemd \
      --libdir=%{_libdir}/php \
      --without-mysqli \
      --disable-pdo \
      ${without_shared}
popd

# Build for inclusion as embedded script language into applications,
# /usr/lib[64]/libphp7.so
pushd build-embedded
build --enable-embed \
      --without-mysqli --disable-pdo \
      ${without_shared}
popd

%if %{with_zts}
# Build a special thread-safe (mainly for modules)
pushd build-ztscli

EXTENSION_DIR=%{_libdir}/php-zts/modules
build --includedir=%{_includedir}/php-zts \
      --libdir=%{_libdir}/php-zts \
      --enable-maintainer-zts \
      --program-prefix=zts- \
      --disable-cgi \
      --with-config-file-scan-dir=%{_sysconfdir}/php-zts.d \
      --enable-pcntl \
      --enable-opcache \
      --enable-opcache-file \
      --with-imap=shared --with-imap-ssl \
      --enable-mbstring=shared \
      --enable-mbregex \
%if %{with_libgd}
      --with-gd=shared,%{_prefix} \
%else
      --with-gd=shared \
%endif
      --with-gmp=shared \
      --enable-calendar=shared \
      --enable-bcmath=shared \
      --with-bz2=shared \
      --enable-ctype=shared \
      --enable-dba=shared --with-db4=%{_prefix} \
                          --with-tcadb=%{_prefix} \
      --with-gettext=shared \
      --with-iconv=shared \
      --enable-sockets=shared \
      --enable-tokenizer=shared \
      --enable-exif=shared \
      --enable-ftp=shared \
      --with-xmlrpc=shared \
      --with-ldap=shared --with-ldap-sasl \
      --enable-mysqlnd=shared \
      --with-mysqli=shared,mysqlnd \
      --with-mysql-sock=%{mysql_sock} \
      --enable-mysqlnd-threading \
%if %{with_firebird}
      --with-interbase=shared \
      --with-pdo-firebird=shared \
%endif
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-simplexml=shared \
      --enable-xml=shared \
      --enable-wddx=shared \
      --with-snmp=shared,%{_prefix} \
      --enable-soap=shared \
      --with-xsl=shared,%{_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared,%{_prefix} \
      --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_prefix} \
      --with-pdo-mysql=shared,mysqlnd \
      --with-pdo-pgsql=shared,%{_prefix} \
      --with-pdo-sqlite=shared,%{_prefix} \
      --with-pdo-dblib=shared,%{_prefix} \
      --with-sqlite3=shared,%{_prefix} \
      --enable-json=shared \
%if %{with_zip}
      --enable-zip=shared \
%if %{with_libzip}
      --with-libzip \
%endif
%endif
      --without-readline \
      --with-libedit \
      --with-pspell=shared \
      --enable-phar=shared \
      --with-mcrypt=shared,%{_prefix} \
      --with-tidy=shared,%{_prefix} \
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-shmop=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,%{_prefix} \
      --enable-fileinfo=shared \
      --enable-intl=shared \
      --with-icu-dir=%{_prefix} \
      --with-enchant=shared,%{_prefix} \
      --with-recode=shared,%{_prefix}
popd

# Build a special thread-safe Apache SAPI
pushd build-zts
build --with-apxs2=%{_httpd_apxs} \
      --includedir=%{_includedir}/php-zts \
      --libdir=%{_libdir}/php-zts \
      --enable-maintainer-zts \
      --with-config-file-scan-dir=%{_sysconfdir}/php-zts.d \
      --without-mysqli \
      --disable-pdo \
      ${without_shared}
popd

### NOTE!!! EXTENSION_DIR was changed for the -zts build, so it must remain
### the last SAPI to be built.
%endif


%check
%if %runselftest
cd build-apache

# Run tests, using the CLI SAPI
export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2
export SKIP_ONLINE_TESTS=1
unset TZ LANG LC_ALL
if ! make test; then
  set +x
  for f in $(find .. -name \*.diff -type f -print); do
    if ! grep -q XFAIL "${f/.diff/.phpt}"
    then
      echo "TEST FAILURE: $f --"
      cat "$f"
      echo -e "\n-- $f result ends."
    fi
  done
  set -x
  #exit 1
fi
unset NO_INTERACTION REPORT_EXIT_STATUS MALLOC_CHECK_
%endif

%install
%if %{with_zts}
# Install the extensions for the ZTS version
make -C build-ztscli install \
     INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# Install the version for embedded script language in applications + php_embed.h
make -C build-embedded install-sapi install-headers \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Install the php-fpm binary
make -C build-fpm install-fpm \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Install everything from the CGI SAPI build
make -C build-cgi install \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Install the default configuration file and icons
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/php.ini
install -m 755 -d $RPM_BUILD_ROOT%{_httpd_contentdir}/icons
install -m 644 php.gif $RPM_BUILD_ROOT%{_httpd_contentdir}/icons/php.gif

# For third-party packaging:
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/php

# install the DSO
install -m 755 -d $RPM_BUILD_ROOT%{_httpd_moddir}
install -m 755 build-apache/libs/libphp7.so $RPM_BUILD_ROOT%{_httpd_moddir}

%if %{with_zts}
# install the ZTS DSO
install -m 755 build-zts/libs/libphp7.so $RPM_BUILD_ROOT%{_httpd_moddir}/libphp7-zts.so
%endif

# Apache config fragment
# Dual config file with httpd >= 2.4 (fedora >= 18)
install -D -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{_httpd_modconfdir}/15-php.conf
%if %{with_zts}
cat %{SOURCE10} >>$RPM_BUILD_ROOT%{_httpd_modconfdir}/15-php.conf
%endif
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd_confdir}/php.conf

install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php.d
%if %{with_zts}
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d
%endif
install -m 755 -d $RPM_BUILD_ROOT%{_sharedstatedir}/php
install -m 755 -d $RPM_BUILD_ROOT%{_sharedstatedir}/php/peclxml
install -m 700 -d $RPM_BUILD_ROOT%{_sharedstatedir}/php/session
install -m 700 -d $RPM_BUILD_ROOT%{_sharedstatedir}/php/wsdlcache
install -m 700 -d $RPM_BUILD_ROOT%{_sharedstatedir}/php/opcache

install -m 755 -d $RPM_BUILD_ROOT%{_docdir}/pecl
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/tests/pecl

# PHP-FPM stuff
# Log
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/log/php-fpm
install -m 755 -d $RPM_BUILD_ROOT/run/php-fpm
# Config
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d/www.conf
mv $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf.default .
mv $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d/www.conf.default .
# tmpfiles.d
install -m 755 -d $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d
install -m 644 php-fpm.tmpfiles $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d/php-fpm.conf
# install systemd unit files and scripts for handling server startup
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/php-fpm.service.d
install -m 755 -d $RPM_BUILD_ROOT%{_unitdir}
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_unitdir}/
# LogRotate
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/php-fpm
# Nginx configuration
install -D -m 644 %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/php-fpm.conf
install -D -m 644 %{SOURCE14} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/default.d/php.conf

# Generate files lists and stub .ini files for each subpackage
for mod in pgsql odbc ldap snmp xmlrpc imap json \
    mysqlnd mysqli pdo_mysql \
    mbstring gd dom xsl soap bcmath dba xmlreader xmlwriter \
    simplexml bz2 calendar ctype exif ftp gettext gmp iconv \
    sockets tokenizer opcache \
    pdo pdo_pgsql pdo_odbc pdo_sqlite \
%if %{with_zip}
    zip \
%endif
%if %{with_firebird}
    interbase pdo_firebird \
%endif
    sqlite3 \
    enchant phar fileinfo intl \
    mcrypt tidy pdo_dblib pspell curl wddx \
    posix shmop sysvshm sysvsem sysvmsg recode xml \
    ; do
    case $mod in
      opcache)
        # Zend extensions
        ini=10-${mod}.ini;;
      pdo_*|mysqli|wddx|xmlreader|xmlrpc)
        # Extensions with dependencies on 20-*
        ini=30-${mod}.ini;;
      *)
        # Extensions with no dependency
        ini=20-${mod}.ini;;
    esac
    # some extensions have their own config file
    if [ -f ${ini} ]; then
      cp -p ${ini} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${ini}
      cp -p ${ini} $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/${ini}
    else
      cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${ini} <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
%if %{with_zts}
      cat > $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/${ini} <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
%endif
    fi
    cat > files.${mod} <<EOF
%attr(755,root,root) %{_libdir}/php/modules/${mod}.so
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/php.d/${ini}
%if %{with_zts}
%attr(755,root,root) %{_libdir}/php-zts/modules/${mod}.so
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/php-zts.d/${ini}
%endif
EOF
done

# The dom, xsl and xml* modules are all packaged in php-xml
cat files.dom files.xsl files.xml{reader,writer} files.wddx \
    files.simplexml >> files.xml

# mysqlnd
cat files.mysqli \
    files.pdo_mysql \
    >> files.mysqlnd

# Split out the PDO modules
cat files.pdo_pgsql >> files.pgsql
cat files.pdo_odbc >> files.odbc
%if %{with_firebird}
cat files.pdo_firebird >> files.interbase
%endif

# sysv* and posix in packaged in php-process
cat files.shmop files.sysv* files.posix > files.process

# Package sqlite3 and pdo_sqlite with pdo; isolating the sqlite dependency
# isn't useful at this time since rpm itself requires sqlite.
cat files.pdo_sqlite >> files.pdo
cat files.sqlite3 >> files.pdo

# Package zip, curl, phar and fileinfo in -common.
cat files.curl files.phar files.fileinfo \
    files.exif files.gettext files.iconv files.calendar \
    files.ftp files.bz2 files.ctype files.sockets \
    files.tokenizer > files.common
%if %{with_zip}
cat files.zip >> files.common
%endif

# The default Zend OPcache blacklist file
install -m 644 %{SOURCE51} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/opcache-default.blacklist
install -m 644 %{SOURCE51} $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/opcache-default.blacklist
sed -e '/blacklist_filename/s/php.d/php-zts.d/' \
    -i $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/10-opcache.ini

# Install the macros file:
sed -e "s/@PHP_APIVER@/%{apiver}%{isasuffix}/" \
    -e "s/@PHP_ZENDVER@/%{zendver}%{isasuffix}/" \
    -e "s/@PHP_PDOVER@/%{pdover}%{isasuffix}/" \
    -e "s/@PHP_VERSION@/%{version}/" \
%if ! %{with_zts}
    -e "/zts/d" \
%endif
    < %{SOURCE3} > macros.php
install -m 644 -D macros.php \
           $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.php

# Remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_libdir}/php/modules/*.a \
       $RPM_BUILD_ROOT%{_libdir}/php-zts/modules/*.a \
       $RPM_BUILD_ROOT%{_bindir}/{phptar} \
       $RPM_BUILD_ROOT%{_datadir}/pear \
       $RPM_BUILD_ROOT%{_libdir}/libphp7.la

# Remove irrelevant docs
rm -f README.{Zeus,QNX,CVS-RULES}


%post fpm
%systemd_post php-fpm.service

%preun fpm
%systemd_preun php-fpm.service

%postun fpm
%systemd_postun_with_restart php-fpm.service

%post embedded -p /sbin/ldconfig
%postun embedded -p /sbin/ldconfig

%files
%{_httpd_moddir}/libphp7.so
%if %{with_zts}
%{_httpd_moddir}/libphp7-zts.so
%endif
%attr(0770,root,apache) %dir %{_sharedstatedir}/php/session
%attr(0770,root,apache) %dir %{_sharedstatedir}/php/wsdlcache
%attr(0770,root,apache) %dir %{_sharedstatedir}/php/opcache
%config(noreplace) %{_httpd_confdir}/php.conf
%config(noreplace) %{_httpd_modconfdir}/15-php.conf
%{_httpd_contentdir}/icons/php.gif

%files common -f files.common
%doc CODING_STANDARDS CREDITS EXTENSIONS NEWS README*
%license LICENSE Zend/ZEND_* TSRM_LICENSE
%license libmagic_LICENSE
%license phar_LICENSE
%doc php.ini-*
%config(noreplace) %{_sysconfdir}/php.ini
%dir %{_sysconfdir}/php.d
%dir %{_libdir}/php
%dir %{_libdir}/php/modules
%if %{with_zts}
%dir %{_sysconfdir}/php-zts.d
%dir %{_libdir}/php-zts
%dir %{_libdir}/php-zts/modules
%endif
%dir %{_sharedstatedir}/php
%dir %{_sharedstatedir}/php/peclxml
%dir %{_datadir}/php
%dir %{_docdir}/pecl
%dir %{_datadir}/tests
%dir %{_datadir}/tests/pecl

%files cli
%{_bindir}/php
%if %{with_zts}
%{_bindir}/zts-php
%endif
%{_bindir}/php-cgi
%{_bindir}/phar.phar
%{_bindir}/phar
# provides phpize here (not in -devel) for pecl command
%{_bindir}/phpize
%{_mandir}/man1/php.1*
%{_mandir}/man1/zts-php.1*
%{_mandir}/man1/php-cgi.1*
%{_mandir}/man1/phar.1*
%{_mandir}/man1/phar.phar.1*
%{_mandir}/man1/phpize.1*
%doc sapi/cgi/README* sapi/cli/README

%files dbg
%doc sapi/phpdbg/{README.md,CREDITS}
%{_bindir}/phpdbg
%{_mandir}/man1/phpdbg.1*
%if %{with_zts}
%{_bindir}/zts-phpdbg
%{_mandir}/man1/zts-phpdbg.1*
%endif

%files fpm
%doc php-fpm.conf.default www.conf.default
%license fpm_LICENSE
%attr(0770,root,apache) %dir %{_sharedstatedir}/php/session
%attr(0770,root,apache) %dir %{_sharedstatedir}/php/wsdlcache
%attr(0770,root,apache) %dir %{_sharedstatedir}/php/opcache
%config(noreplace) %{_httpd_confdir}/php.conf
%config(noreplace) %{_sysconfdir}/php-fpm.conf
%config(noreplace) %{_sysconfdir}/php-fpm.d/www.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/php-fpm
%config(noreplace) %{_sysconfdir}/nginx/conf.d/php-fpm.conf
%config(noreplace) %{_sysconfdir}/nginx/default.d/php.conf
%{_prefix}/lib/tmpfiles.d/php-fpm.conf
%{_unitdir}/php-fpm.service
%{_sbindir}/php-fpm
%dir %{_sysconfdir}/systemd/system/php-fpm.service.d
%dir %{_sysconfdir}/php-fpm.d
# log owned by apache for log
%attr(770,apache,root) %dir %{_localstatedir}/log/php-fpm
%dir /run/php-fpm
%{_mandir}/man8/php-fpm.8*
%dir %{_datadir}/fpm
%{_datadir}/fpm/status.html

%files devel
%{_bindir}/php-config
%{_includedir}/php
%{_libdir}/php/build
%if %{with_zts}
%{_bindir}/zts-php-config
%{_bindir}/zts-phpize
%{_includedir}/php-zts
%{_libdir}/php-zts/build
%{_mandir}/man1/zts-php-config.1*
%{_mandir}/man1/zts-phpize.1*
%endif
%{_mandir}/man1/php-config.1*
%{_rpmconfigdir}/macros.d/macros.php

%files embedded
%{_libdir}/libphp7.so
%{_libdir}/libphp7-%{embed_version}.so

%files pgsql -f files.pgsql
%files odbc -f files.odbc
%files imap -f files.imap
%files ldap -f files.ldap
%files snmp -f files.snmp
%files xml -f files.xml
%files xmlrpc -f files.xmlrpc
%files mbstring -f files.mbstring
%license libmbfl_LICENSE
%license oniguruma_COPYING
%license ucgendat_LICENSE
%files gd -f files.gd
%if ! %{with_libgd}
%license libgd_README
%license libgd_COPYING
%endif
%files soap -f files.soap
%files bcmath -f files.bcmath
%license libbcmath_COPYING
%files gmp -f files.gmp
%files dba -f files.dba
%files pdo -f files.pdo
%files mcrypt -f files.mcrypt
%files tidy -f files.tidy
%files pdo-dblib -f files.pdo_dblib
%files pspell -f files.pspell
%files intl -f files.intl
%files process -f files.process
%files recode -f files.recode
%if %{with_firebird}
%files interbase -f files.interbase
%endif
%files enchant -f files.enchant
%files mysqlnd -f files.mysqlnd
%files opcache -f files.opcache
%config(noreplace) %{_sysconfdir}/php.d/opcache-default.blacklist
%config(noreplace) %{_sysconfdir}/php-zts.d/opcache-default.blacklist
%files json -f files.json


%changelog
