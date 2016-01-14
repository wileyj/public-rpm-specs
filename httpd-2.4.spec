%define contentdir /var/www
%define appuser apache
%define appgroup www
%define logdir /u/log/apache
%define realname apache
%define suexec_caller apache
%define mmn 20120211
%define major 2
%define minor 4
%define revision 17
%define vstring CentOS 
%define mpms worker prefork event
%define opt_apache /opt/apache%{major}.%{minor}

Summary: Apache HTTP Server
Name: httpd
Version: %{major}.%{minor}.%{revision}
Release: %{revision}.%{dist}
URL: http://httpd.apache.org/
Source0: %{name}-%{major}.%{minor}.x.tar.gz
Source1: apache-scripts.tar.gz
Source2: apache.init
Source3: apache-new.init
License: ASL 2.0
Vendor: %{vendor}
Packager: %{packager}
Group: System Environment/Daemons
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: autoconf, perl, pkgconfig, findutils expat-devel, svn, pcre, pcre-devel
BuildRequires: zlib-devel, libselinux-devel
BuildRequires: pcre, apr-devel >= 1.4.0, apr-util-devel >= 1.4.0, pcre-devel >= 5.0
Obsoletes: httpd-suexec
Requires(pre): shadow-utils
Requires(post): chkconfig
Provides: webserver
Provides: mod_dav = %{version}-%{release}, httpd-suexec = %{version}-%{release}
Provides: httpd-mmn = %{mmn}, %{name} = %{version}-%{release}
Obsoletes: secureweb, mod_dav, mod_gzip, stronghold-apache
Obsoletes: stronghold-htdocs, mod_put, mod_roaming
Conflicts: pcre < 4.0
Requires: %{name}-tools = %{version}-%{release}, apr-util-ldap,  perl-LDAP, mod_ssl
%description
The Apache HTTP Server is a powerful, efficient, and extensible
web server.

%package devel
Group: Development/Libraries
Summary: Development interfaces for the Apache HTTP server
Obsoletes: secureweb-devel, stronghold-apache-devel
Requires: apr-devel, apr-util-devel, pkgconfig
Requires: %{name} = %{version}-%{release}

%description devel
The httpd-devel package contains the APXS binary and other files
that you need to build Dynamic Shared Objects (DSOs) for the
Apache HTTP Server.

If you are installing the Apache HTTP server and you want to be
able to compile or develop additional modules for Apache, you need
to install this package.

%package manual
Group: Documentation
Summary: Documentation for the Apache HTTP server
Requires: %{name} = %{version}-%{release}
Obsoletes: secureweb-manual, httpd-manual
BuildArch: noarch

%description manual
The httpd-manual package contains the complete manual and
reference guide for the Apache HTTP server. The information can
also be found at http://httpd.apache.org/docs/%{major}.%{minor}/.

%package tools
Group: System Environment/Daemons
Summary: Tools for use with the Apache HTTP Server
Requires: %{name} = %{version}-%{release}
Obsoletes: apache-tools

%description tools
The httpd-tools package contains tools which can be used with 
the Apache HTTP Server.

%package -n mod_ssl
Group: System Environment/Daemons
Summary: SSL/TLS module for the Apache HTTP Server
#Epoch: 1
BuildRequires: openssl-devel
Requires: openssl >= 0.9.7f-4, /bin/cat
Requires: %{name} = %{version}-%{release}
Obsoletes: stronghold-mod_ssl

%description -n mod_ssl
The mod_ssl module provides strong cryptography for the Apache Web
server via the Secure Sockets Layer (SSL) and Transport Layer
Security (TLS) protocols.

%prep
%setup -q -n %{name}
git pull 
svn co http://svn.apache.org/repos/asf/apr/apr/branches/1.4.x srclib/apr
svn co http://svn.apache.org/repos/asf/apr/apr-util/branches/1.4.x srclib/apr-util
./buildconf

# Safety check: prevent build if defined MMN does not equal upstream MMN.
vmmn=`echo MODULE_MAGIC_NUMBER_MAJOR | cpp -include include/ap_mmn.h | sed -n '/^2/p'`
if test "x${vmmn}" != "x%{mmn}"; then
   : Error: Upstream MMN is now ${vmmn}, packaged MMN is %{mmn}.
   : Update the mmn macro and rebuild.
   exit 1
fi

: Building with MMN %{mmn} and vendor string '%{vstring}'

%build
# forcibly prevent use of bundled apr, apr-util, pcre
rm -rf srclib/{apr,apr-util,pcre}

# regenerate configure scripts
autoheader && autoconf || exit 1

# Before configure; fix location of build dir in generated apxs
%{__perl} -pi -e "s:\@exp_installbuilddir\@:%{opt_apache}/build:g" support/apxs.in

CFLAGS="$RPM_OPT_FLAGS -Wformat-security -fno-strict-aliasing"
SH_LDFLAGS="-Wl,-z,relro"
export CFLAGS SH_LDFLAGS

# Forcibly disable use of rsync to install (#557049)
export ac_cv_path_RSYNC=

# Hard-code path to links to avoid unnecessary builddep
export LYNX_PATH=/usr/bin/links

function mpmbuild()
{
mpm=$1; shift
mkdir $mpm; pushd $mpm
../configure \
	--with-pcre=%{_bindir}pcre-config  \
	--prefix=%{opt_apache} \
    	--includedir=%{opt_apache}/include \
	--with-mpm=$mpm \
	--enable-cache \
    	--enable-disk-cache \
    	--enable-mem-cache \
    	--enable-proxy \
    	--enable-proxy-connect \
    	--enable-proxy-ftp \
    	--enable-proxy-http \
    	--enable-speling \
    	--enable-cgi \
    	--enable-imap \
    	--enable-dav \
    	--enable-dav-fs \
    	--enable-logio \
    	--enable-file-cache \
    	--enable-so \
    	--enable-cgid \
    	--enable-auth-anon \
    	--enable-auth-dbm \
    	--enable-auth-digest \
    	--enable-ext-filter \
    	--enable-mime-magic \
    	--enable-cern-meta \
    	--enable-expires \
    	--enable-headers \
    	--enable-version \
    	--enable-info \
    	--enable-vhost-alias \
    	--enable-rewrite \
    	--with-ldap \
    	--enable-ldap \
    	--enable-auth-ldap \
    	--enable-deflate \
    	--enable-mods-shared=all \
    	--enable-ssl \
    	--enable-authn-alias \
    	--enable-authnz-ldap \
    	--enable-deflate \
        --with-apr=/usr/bin/apr-1-config \
	--with-apr-util=/usr/bin/apu-1-config \
        --enable-pie \
	--disable-suexec \
        --with-pcre=/usr/bin/pcre-config \
	$*

make %{?_smp_mflags} EXTRA_CFLAGS="-Werror-implicit-function-declaration"
popd
}

# Build everything and the kitchen sink with the prefork build
#mpmbuild prefork \
#        --enable-mods-shared=all \
#	--enable-ssl --with-ssl \
#	--enable-proxy \
#        --enable-cache \
#        --enable-disk-cache \
#        --enable-ldap --enable-authnz-ldap \
#        --enable-cgid \
#        --enable-authn-anon --enable-authn-alias \
#        --disable-imagemap
#
# For the other MPMs, just build httpd and no optional modules
for f in %{mpms}; do
   mpmbuild $f
done

%install
rm -rf $RPM_BUILD_ROOT

#pushd prefork
#make DESTDIR=$RPM_BUILD_ROOT install
#popd

pushd worker
make DESTDIR=$RPM_BUILD_ROOT install
popd


# install alternative MPMs
mkdir -pv $RPM_BUILD_ROOT%{opt_apache}/bin/
install -m 755 prefork/httpd $RPM_BUILD_ROOT%{opt_apache}/bin/httpd.prefork
install -m 775 event/httpd $RPM_BUILD_ROOT%{opt_apache}/bin/httpd.event

# remove manual sources
find $RPM_BUILD_ROOT%{contentdir}/manual \( \
    -name \*.xml -o -name \*.xml.* -o -name \*.ent -o -name \*.xsl -o -name \*.dtd \
    \) -print0 | xargs -0 rm -f

# Strip the manual down just to English and replace the typemaps with flat files:
set +x
for f in `find $RPM_BUILD_ROOT%{contentdir}/manual -name \*.html -type f`; do
   if test -f ${f}.en; then
      cp ${f}.en ${f}
      rm ${f}.*
   fi
done
set -x

# Remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.exp \
      $RPM_BUILD_ROOT/etc/httpd/conf/mime.types \
      $RPM_BUILD_ROOT%{_libdir}/httpd/modules/*.exp \
      $RPM_BUILD_ROOT%{_libdir}/httpd/build/config.nice \
      $RPM_BUILD_ROOT%{_bindir}/ap?-config \
      $RPM_BUILD_ROOT%{_sbindir}/{checkgid,dbmmanage,envvars*} \
      $RPM_BUILD_ROOT%{contentdir}/htdocs/* \
      $RPM_BUILD_ROOT%{_mandir}/man1/dbmmanage.* \
      $RPM_BUILD_ROOT%{contentdir}/cgi-bin/*

rm -rf $RPM_BUILD_ROOT/etc/httpd/conf/{original,extra}


# We don't care about this tuff
rm -frv $RPM_BUILD_ROOT%{opt_apache}/conf/httpd.conf
rm -frv $RPM_BUILD_ROOT%{opt_apache}/conf/extra
rm -frv $RPM_BUILD_ROOT%{opt_apache}/conf/original
rm -frv $RPM_BUILD_ROOT%{opt_apache}/build/config.nice
rm -frv $RPM_BUILD_ROOT%{opt_apache}/error/
rm -frv $RPM_BUILD_ROOT%{opt_apache}/htdocs/
rm -frv $RPM_BUILD_ROOT%{opt_apache}/manual/
rm -frv $RPM_BUILD_ROOT%{opt_apache}/modules/httpd.exp


# we need this dir
mkdir -pv $RPM_BUILD_ROOT%{opt_apache}/instances/
tar -C $RPM_BUILD_ROOT%{opt_apache} -xzvf %SOURCE1 

%{__mv} $RPM_BUILD_ROOT%{opt_apache}/apache-scripts/conf/*  $RPM_BUILD_ROOT%{opt_apache}/conf/
%{__mv} $RPM_BUILD_ROOT%{opt_apache}/apache-scripts/scripts  $RPM_BUILD_ROOT%{opt_apache}
%{__rm} -rf $RPM_BUILD_ROOT%{opt_apache}/apache-scripts

# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -P -o root -g root -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/apache
%{__install} -P -o root -g root -m 0755 %{SOURCE3} $RPM_BUILD_ROOT%{_initrddir}/apache-new



# Make suexec a+rw so it can be stripped.  %%files lists real permissions
#chmod 755 $RPM_BUILD_ROOT%{_sbindir}/suexec


#create symlinks for ease
ln -sf %{opt_apache}  %{buildroot}/opt/apache
ln -sf %{opt_apache}  %{buildroot}/etc/httpd
ln -sf %{opt_apache}/scripts/apache-instancectl  %{buildroot}%{_initrddir}/apache-instancectl

%pre
getent group %{appgroup} >/dev/null 2>&1 || groupadd -g 48 -r %{appgroup}  >/dev/null 2>&1
getent passwd %{appuser} >/dev/null 2>&1 || useradd -r -u 48 -g %{appgroup} -s /sbin/nologin -d %{contentdir} -c "Apache" %{appuser} >/dev/null 2>&1

%post
if [ ! -d /u/log/apache ]
then
	mkdir -p %{logdir}
	chown -R %{appuser}:%{appgroup} %{logdir}
fi

# Register the httpd service
/sbin/chkconfig --add %{realname}

%preun
if [ $1 = 0 ]; then
	/sbin/service %{realname} stop > /dev/null 2>&1
	/sbin/chkconfig --del %{realname}
fi

%postun
getent passwd %{appuser}  >/dev/null 2>&1
if [ $? -eq 0 ]
then
        userdel %{appuser}  >/dev/null 2>&1
fi
getent group %{appgroup}  >/dev/null 2>&1
if [  $? -eq 0 ]
then
        groupdel %{appgroup}  >/dev/null 2>&1
fi

%check
# Check the built modules are all PIC
if readelf -d $RPM_BUILD_ROOT%{_libdir}/httpd/modules/*.so | grep TEXTREL; then
   : modules contain non-relocatable code
   exit 1
fi

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root)
%dir %{opt_apache}
%dir %{opt_apache}/instances
#%dir %{opt_apache}/conf
%dir %{opt_apache}/icons
%dir %{opt_apache}/modules
%dir %{opt_apache}/man
%dir %{opt_apache}/man/man1
%dir %{opt_apache}/man/man8
%dir %{opt_apache}/bin
%dir %{opt_apache}/cgi-bin
/opt/apache
/etc/httpd
%{opt_apache}/bin
%{opt_apache}/modules/mod*.so
%exclude %{opt_apache}/modules/mod_ssl.so
%{opt_apache}/icons/*
%{opt_apache}/cgi-bin/printenv*
%{opt_apache}/cgi-bin/test-cgi*
%{opt_apache}/conf
%{opt_apache}/man/man8/*
%exclude %{opt_apache}/bin/ab
%exclude %{opt_apache}/bin/htdbm
%exclude %{opt_apache}/bin/logresolve
%exclude %{opt_apache}/bin/htpasswd
%exclude %{opt_apache}/bin/htdigest
%exclude %{opt_apache}/bin/dbmmanage
%exclude %{opt_apache}/bin/httxt2dbm
%{opt_apache}/scripts
%{_initrddir}/apache
%{_initrddir}/apache-new
%{_initrddir}/apache-instancectl

%files tools
%defattr(-,root,root)
%dir %{opt_apache}/bin/
%{opt_apache}/bin/ab
%{opt_apache}/bin/htdbm
%{opt_apache}/bin/logresolve
%{opt_apache}/bin/htpasswd
%{opt_apache}/bin/htdigest
%{opt_apache}/bin/dbmmanage
%{opt_apache}/bin/httxt2dbm
%{opt_apache}/man/man1/*

%files -n mod_ssl
%defattr(-,root,root)
%{opt_apache}/modules/mod_ssl.so

%files devel
%defattr(-,root,root)
%dir %{opt_apache}/include/
%dir %{opt_apache}/build
%{opt_apache}/include/*.h
%{opt_apache}/bin/apxs
%{opt_apache}/build/*.mk
%{opt_apache}/build/*.sh
