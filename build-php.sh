#!/bin/sh

  RPM_SOURCE_DIR="/opt/rpmbuild/SOURCES"
  RPM_BUILD_DIR="/opt/rpmbuild/BUILD"
  RPM_OPT_FLAGS="-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1  -m64 -mtune=generic"
  RPM_LD_FLAGS="-Wl,-z,relro -specs=/usr/lib/rpm/redhat/redhat-hardened-ld"
  RPM_ARCH="x86_64"
  RPM_OS="linux"
  export RPM_SOURCE_DIR RPM_BUILD_DIR RPM_OPT_FLAGS RPM_LD_FLAGS RPM_ARCH RPM_OS
  RPM_DOC_DIR="/usr/share/doc"
  export RPM_DOC_DIR
  RPM_PACKAGE_NAME="php"
  RPM_PACKAGE_VERSION="5.6.29"
  RPM_PACKAGE_RELEASE="1mbot.el7"
  export RPM_PACKAGE_NAME RPM_PACKAGE_VERSION RPM_PACKAGE_RELEASE
  LANG=C
  export LANG
  unset CDPATH DISPLAY ||:
  RPM_BUILD_ROOT="/opt/rpmbuild/BUILDROOT/php-5.6.29-1mbot.el7.x86_64"
  export RPM_BUILD_ROOT
  
  PKG_CONFIG_PATH="${PKG_CONFIG_PATH}:/usr/lib64/pkgconfig:/usr/share/pkgconfig"
  export PKG_CONFIG_PATH
  
  set -x
  umask 022
  cd "/opt/rpmbuild/BUILD"
cd 'php-5.6.29'
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >>aclocal.m4

libtoolize --force --copy
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >build/libtool.m4

touch configure.in
./buildconf --force

CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign"
export CFLAGS

PEAR_INSTALLDIR=/opt/php-5.6.29/share/pear; export PEAR_INSTALLDIR
EXTENSION_DIR=/opt/php-5.6.29/lib/php/modules; export EXTENSION_DIR
PHP_MYSQLND_ENABLED=yes; export PHP_MYSQLND_ENABLED
SNMP_CONFIG=/usr/bin/net-snmp-config-x86_64 ; export SNMP_CONFIG

build() {
mkdir Zend && cp ../Zend/zend_{language,ini}_{parser,scanner}.[ch] Zend

ln -sf ../configure

  CFLAGS="${CFLAGS:--O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1  -m64 -mtune=generic}" ; export CFLAGS ; 
  CXXFLAGS="${CXXFLAGS:--O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1  -m64 -mtune=generic}" ; export CXXFLAGS ; 
  FFLAGS="${FFLAGS:--O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1  -m64 -mtune=generic -I/usr/lib64/gfortran/modules}" ; export FFLAGS ; 
  FCFLAGS="${FCFLAGS:--O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1  -m64 -mtune=generic -I/usr/lib64/gfortran/modules}" ; export FCFLAGS ; 
  LDFLAGS="${LDFLAGS:--Wl,-z,relro -specs=/usr/lib/rpm/redhat/redhat-hardened-ld}"; export LDFLAGS; 
  [ "1" == 1 ] && [ "x86_64" == ppc64le ] && /usr/lib/rpm/redhat/libtool-handle-ppc64le.sh ; 
  for i in $(find . -name config.guess -o -name config.sub) ; do 
      [ -f /usr/lib/rpm/redhat/$(basename $i) ] && /usr/bin/rm -f $i && /usr/bin/cp -fv /usr/lib/rpm/redhat/$(basename $i) $i ; 
  done ; 
  ./configure --build=x86_64-redhat-linux-gnu --host=x86_64-redhat-linux-gnu \
	--program-prefix= \
	--disable-dependency-tracking \
	--prefix=/usr \
	--exec-prefix=/usr \
	--bindir=/usr/bin \
	--sbindir=/usr/sbin \
	--sysconfdir=/etc \
	--datadir=/usr/share \
	--includedir=/usr/include \
	--libdir=/usr/lib64 \
	--libexecdir=/usr/libexec \
	--localstatedir=/var \
	--sharedstatedir=/var/lib \
	--mandir=/usr/share/man \
	--infodir=/usr/share/info \
    --enable-maintainer-zts \
    --prefix=/opt/php-5.6.29 \
    --bindir=/opt/php-5.6.29/bin \
    --sbindir=/opt/php-5.6.29/sbin \
    --includedir=/opt/php-5.6.29/include \
    --with-libdir=lib64 \
    --cache-file=../config.cache \
    --with-config-file-path=/opt/php-5.6.29/etc \
    --with-config-file-scan-dir=/opt/php-5.6.29/etc/mods_enabled \
    --disable-debug \
    --with-pic \
    --disable-rpath \
    --with-bz2 \
    --with-curl \
    --enable-exif \
    --with-exec-dir=/opt/php-5.6.29/bin \
    --with-freetype-dir=/usr \
    --with-png-dir=/usr \
    --with-xpm-dir=/usr \
    --with-gd \
    --enable-gd-native-ttf \
    --with-gettext \
    --with-gmp \
    --with-iconv \
    --with-jpeg-dir=/usr \
    --with-icu-dir=/usr \
    --enable-intl \
    --with-ldap=/usr \
    --with-mcrypt=/usr \
    --with-mhash \
    --with-mysql=mysqlnd \
    --with-mysqli=mysqlnd \
    --with-openssl \
    --without-pear \
    --enable-pdo \
    --with-pdo-mysql=mysqlnd \
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
    --with-tidy=/usr \
    --with-libxml-dir=/usr \
    --enable-xml \
    --with-xmlrpc \
    --with-xsl=/usr \
    --with-system-tzdata \
    --enable-zip \
    --enable-bcmath=shared \
    --enable-dba=shared --with-db4 \
    --enable-ftp=shared \
    --enable-pcntl=shared \
    --with-snmp=shared,/usr \
    --enable-wddx=shared \
    --without-gdbm \
    --with-system-ciphers \
    --with-pcre-regex=/usr \
    --with-kerberos \
    --enable-dtrace \
    $*
if test $? != 0; then
  tail -500 config.log
  : configure failed
  exit 1
fi

make -j4 -j2
}

# Build /usr/bin/php-cgi with the CGI SAPI, and most shared extensions
pushd build-cgi

build --libdir=/opt/php-5.6.29/lib \
      --enable-pcntl \
      --enable-opcache \
      --enable-phpdbg \
      --enable-mbstring=shared \
      --enable-mbregex \
      --with-gd=shared \
      --with-gmp=shared \
      --enable-calendar=shared \
      --enable-bcmath=shared \
      --with-bz2=shared \
      --enable-ctype=shared \
      --enable-dba=shared --with-db4=/usr \
      --with-tcadb=/usr \
      --enable-exif=shared \
      --enable-ftp=shared \
      --with-gettext=shared \
      --with-iconv=shared \
      --enable-sockets=shared \
      --enable-tokenizer=shared \
      --with-xmlrpc=shared \
      --with-ldap=shared --with-ldap-sasl \
      --enable-mysqlnd=shared \
      --with-mysql=shared,mysqlnd \
      --with-mysqli=shared,mysqlnd \
      --with-mysql-sock=/var/lib/mysql/mysql.sock \
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-simplexml=shared \
      --enable-xml=shared \
      --enable-wddx=shared \
      --with-snmp=shared,/usr \
      --enable-soap=shared \
      --with-xsl=shared,/usr \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared,/usr \
      --enable-pdo=shared \
	--enable-sqlite3 \
      --with-pdo-odbc=shared,unixODBC,/usr \
      --with-pdo-mysql=shared,mysqlnd \
      --with-pdo-pgsql=shared,/usr \
      --with-pdo-sqlite=shared,/usr \
      --with-pdo-dblib=shared,/usr \
      --with-sqlite3=shared,/usr \
      --without-readline \
      --with-libedit \
      --with-pspell=shared \
      --enable-phar=shared \
      --with-mcrypt=shared,/usr \
      --with-tidy=shared,/usr \
      --with-mssql=shared,/usr \
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-shmop=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,/usr \
      --enable-fileinfo=shared \
      --enable-intl=shared \
      --with-icu-dir=/usr \
      --with-enchant=shared,/usr \
      --with-recode=shared,/usr
popd

without_shared="--without-gd \
      --disable-dom --disable-dba --without-unixODBC \
      --disable-opcache \
      --disable-xmlreader --disable-xmlwriter \
	--enable-sqlite3 \
      --without-sqlite3 --disable-phar --disable-fileinfo \
      --without-pspell --disable-wddx \
      --without-curl --disable-posix --disable-xml \
      --disable-simplexml --disable-exif --without-gettext \
      --without-iconv --disable-ftp --without-bz2 --disable-ctype \
      --disable-shmop --disable-sockets --disable-tokenizer \
      --disable-sysvmsg --disable-sysvshm --disable-sysvsem"

# Build Apache module, and the CLI SAPI, /usr/bin/php
pushd build-apache
build --with-apxs2=/usr/bin/apxs \
      --libdir=/opt/php-5.6.29/lib \
      --without-mysql \
      --enable-pdo \
      ${without_shared}
popd

# Build php-fpm
pushd build-fpm
build --enable-fpm \
      --with-fpm-acl \
      --with-fpm-systemd \
      --libdir=/opt/php-5.6.29/lib \
      --without-mysql \
      --enable-pdo \
      ${without_shared}
popd

# Build for inclusion as embedded script language into applications,
# /usr/lib[64]/libphp5.so
pushd build-embedded
build --enable-embed \
      --without-mysql 
      --enable-pdo \
      ${without_shared}
popd

# Build a special thread-safe (mainly for modules)
pushd build-ztscli

EXTENSION_DIR=/opt/php-5.6.29/lib/php-zts/modules
build \
    --includedir=/usr/include/php-zts \
    --libdir=/opt/php-5.6.29/lib/php-zts \
    --enable-maintainer-zts \
    --program-prefix=zts- \
    --disable-cgi \
    --with-config-file-scan-dir=/opt/php-5.6.29/etc/php-zts.d \
    --enable-pcntl \
    --enable-opcache \
    --enable-mbstring=shared \
    --enable-mbregex \
    --with-gd=shared \
    --with-gmp=shared \
    --enable-calendar=shared \
    --enable-bcmath=shared \
    --with-bz2=shared \
    --enable-ctype=shared \
    --enable-dba=shared
    --with-db4=/usr \
    --with-tcadb=/usr \
    --with-gettext=shared \
    --with-iconv=shared \
    --enable-sockets=shared \
    --enable-tokenizer=shared \
    --enable-exif=shared \
    --enable-ftp=shared \
    --with-xmlrpc=shared \
    --with-ldap=shared --with-ldap-sasl \
    --enable-mysqlnd=shared \
    --with-mysql=shared,mysqlnd \
    --with-mysqli=shared,mysqlnd \
    --with-mysql-sock=/var/lib/mysql/mysql.sock \
    --enable-mysqlnd-threading \
    --enable-dom=shared \
    --with-pgsql=shared \
    --enable-simplexml=shared \
    --enable-xml=shared \
    --enable-wddx=shared \
    --with-snmp=shared,/usr \
    --enable-soap=shared \
    --with-xsl=shared,/usr \
    --enable-xmlreader=shared --enable-xmlwriter=shared \
    --with-curl=shared,/usr \
    --enable-pdo=shared \
	--enable-sqlite3 \
    --with-pdo-odbc=shared,unixODBC,/usr \
    --with-pdo-mysql=shared,mysqlnd \
    --with-pdo-pgsql=shared,/usr \
    --with-pdo-sqlite=shared,/usr \
    --with-pdo-dblib=shared,/usr \
    --with-sqlite3=shared,/usr \
    --without-readline \
    --with-libedit \
    --with-pspell=shared \
    --enable-phar=shared \
    --with-mcrypt=shared,/usr \
    --with-tidy=shared,/usr \
    --with-mssql=shared,/usr \
    --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
    --enable-shmop=shared \
    --enable-posix=shared \
    --with-unixODBC=shared,/usr \
    --enable-fileinfo=shared \
    --enable-intl=shared \
    --with-icu-dir=/usr \
    --with-enchant=shared,/usr \
    --with-recode=shared,/usr
popd

# Build a special thread-safe Apache SAPI
pushd build-zts
build \
    --with-apxs2=/usr/bin/apxs \
    --includedir=/usr/include/php-zts \
    --libdir=/opt/php-5.6.29/lib/php-zts \
    --enable-maintainer-zts \
    --with-config-file-scan-dir=/opt/php-5.6.29/etc/php-zts.d \
    --without-mysql \
    --enable-pdo=shared 
popd



exit 0
