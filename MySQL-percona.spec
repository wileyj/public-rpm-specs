%define mysql_old_vendor        MySQL AB
%define mysql_vendor_2          Sun Microsystems, Inc.
%define mysql_vendor            Oracle and/or its affiliates
%define percona_server_vendor   Percona, Inc
%define mysql_major             5
%define mysql_minor             6
%define mysql_rev               21
%define mysql_patch             69
%define mysqlversion            %{mysql_major}.%{mysql_minor}.%{mysql_rev}
%define redhatversion           %(lsb_release -rs | awk -F. '{ print $1}')
%define majorversion            69
%define minorversion            0 
%define percona_server_version  %{majorversion}.%{minorversion}
%define mysqld_user             mysql
%define mysqld_group            dba
%global mysql_root              /opt/mysql/product/%{mysqlversion}
%global mysql_datadir           %{mysql_root}/share
%global mysql_libdir            %{mysql_root}/lib
%global mysql_mandir            %{mysql_root}/share/man
%global mysql_bindir            %{mysql_root}/bin
%global mysql_sbindir           %{mysql_root}/sbin
%global mysql_sysconfdir        %{mysql_root}/etc
%global mysql_includedir        %{mysql_root}/include
%global mysql_infodir           %{mysql_root}/share/info
%define release                 1
%define src_base                percona-server
%define src_dir                 %{src_base}-%{mysqlversion}-%{percona_server_version}
%define feature_set             community
%define compile_comment         Percona Server (GPL), Release rel%{majorversion}.%{minorversion}, Revision %{gotrevision}
%define product_suffix          percona
%define server_suffix           %{product_suffix}
%define server_suffix           %{nil}
%define generic_kernel          %(uname -r | cut -d. -f1-2)
%define distro_description      Generic Linux (kernel %{generic_kernel})
%define distro_releasetag       linux%{generic_kernel}
%define distro_buildreq         gcc-c++ gperf ncurses-devel perl readline-devel time zlib-devel libaio-devel bison cmake > 2.8.0, libtool < 2.2.10, openssl-static,  zlib-devel, zlib-static, boost, gmock, gmock-devel, gtest, gtest-devel
%define distro_requires         coreutils grep procps /sbin/chkconfig /usr/sbin/useradd /usr/sbin/groupadd
%define license_files_server    %{src_dir}/COPYING %{src_dir}/README
%define license_type            GPL
%undefine __perl_provides
%undefine __perl_requires
# ---------------------------------------------------------------------------- 

Name:           MySQL-%{product_suffix}
Summary:        Percona-Server: a very fast and reliable SQL database server
Group:          Applications/Databases
Version:        %{mysqlversion}
Release:        %{release}.%{dist}
Distribution:   %{distro_description}
License:        Copyright (c) 2000, 2010, %{mysql_vendor}.  All rights reserved.  Use is subject to license terms.  Under %{license_type} license as shown in the Description field.
Packager:	%{packager}
Vendor:		%{vendor}
Source:         http://www.percona.com/downloads/Percona-Server-5.5/Percona-Server-%{mysqlversion}-%{majorversion}.%{minorversion}/source/%{src_dir}.tar.gz
Source1:        gmock-1.6.0.zip
Source2:        mysql.init
Source3:        mysqlenv
Source4:        mysqlctl
URL:            http://www.percona.com/
Provides:       mysql-server
BuildRequires:  %{distro_buildreq}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
The Percona Server software delivers a very fast, multi-threaded, multi-user,
and robust SQL (Structured Query Language) database server. Percona Server
is intended for mission-critical, heavy-load production systems.

Percona recommends that all production deployments be protected with a support
contract (http://www.percona.com/mysql-suppport/) to ensure the highest uptime,
be eligible for hot fixes, and boost your team's productivity.
# ----------------------------------------------------------------------------

%package -n     MySQL-%{product_suffix}-server
Summary:        Percona Server: a very fast and reliable SQL database server
Group:          Applications/Databases
Requires:       %{distro_requires} MySQL-%{product_suffix}-shared
Provides:       mysql-server

%description -n MySQL-%{product_suffix}-server
The Percona Server software delivers a very fast, multi-threaded, multi-user,
and robust SQL (Structured Query Language) database server. Percona Server
is intended for mission-critical, heavy-load production systems.

Percona recommends that all production deployments be protected with a support
contract (http://www.percona.com/mysql-suppport/) to ensure the highest uptime,
be eligible for hot fixes, and boost your team's productivity.

This package includes the Percona Server with XtraDB binary 
as well as related utilities to run and administer Percona Server.

If you want to access and work with the database, you have to install
package "MySQL-%{product_suffix}-client" as well!
# ----------------------------------------------------------------------------

%package -n     MySQL-%{product_suffix}-client
Summary:        Percona Server - Client
Group:          Applications/Databases
Requires:       MySQL-%{product_suffix}-shared
Provides:       mysql-client MySQL-client

%description -n MySQL-%{product_suffix}-client
This package contains the standard Percona Server client and administration tools.
For a description of Percona Server see http://www.percona.com/software/percona-server/
# ----------------------------------------------------------------------------

%package -n     MySQL-%{product_suffix}-test
Requires:       MySQL-%{product_suffix}-client perl
Summary:        Percona Server - Test suite
Group:          Applications/Databases
Provides:       mysql-test
AutoReqProv:    no

%description -n MySQL-%{product_suffix}-test
This package contains the Percona Server regression test suite.
For a description of Percona Server see http://www.percona.com/software/percona-server/
# ----------------------------------------------------------------------------

%package -n     MySQL-%{product_suffix}-bench
Requires:       MySQL-%{product_suffix}-server 
Summary:        Percona Server - Benchmark suite
Group:          Applications/Databases
Provides:       mysql-bench
AutoReqProv:    no

%description -n MySQL-%{product_suffix}-bench
This package contains the Percona Server Benchmark suite.
For a description of Percona Server see http://www.percona.com/software/percona-server/
# ----------------------------------------------------------------------------

%package -n     MySQL-%{product_suffix}-devel
Summary:        Percona Server - Development header files and libraries
Group:          Applications/Databases
Provides:       mysql-devel

%description -n MySQL-%{product_suffix}-devel
This package contains the development header files and libraries necessary
to develop Percona Server client applications.
For a description of Percona Server see http://www.percona.com/software/percona-server/
# ----------------------------------------------------------------------------

%package -n MySQL-%{product_suffix}-shared
Summary:        Percona Server - Shared libraries
Group:          Applications/Databases
Provides:       mysql-shared

%description -n MySQL-%{product_suffix}-shared
This package contains the shared libraries (*.so*) which certain languages
and applications need to dynamically load and use Percona Server.
# ----------------------------------------------------------------------------

%prep
%setup -T -a 0 -c -n %{src_dir}
%build
if [ ! -d $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/source_downloads ]
then
        mkdir -p $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/source_downloads
fi

%{__cp} %{SOURCE1} $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/source_downloads/gmock-1.6.0.zip
unzip $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/source_downloads/gmock-1.6.0.zip

touch optional-files-devel
export PATH=${MYSQL_BUILD_PATH:-$PATH}
export CC=${MYSQL_BUILD_CC:-${CC:-gcc}}
export CXX=${MYSQL_BUILD_CXX:-${CXX:-g++}}
export CFLAGS=${MYSQL_BUILD_CFLAGS:-${CFLAGS:-$RPM_OPT_FLAGS}}
export CXXFLAGS=${MYSQL_BUILD_CXXFLAGS:-${CXXFLAGS:-$RPM_OPT_FLAGS -felide-constructors -fno-exceptions }}
export LDFLAGS=${MYSQL_BUILD_LDFLAGS:-${LDFLAGS:-}}
export CMAKE=${MYSQL_BUILD_CMAKE:-${CMAKE:-cmake}}
export MAKE_JFLAG=${MYSQL_BUILD_MAKE_JFLAG:-${MAKE_JFLAG:-}}

%{__mkdir} release && cd release && cmake ../%{src_dir}         \
        -DBUILD_CONFIG=mysql_release                            \
        -DCMAKE_BUILD_TYPE=RelWithDebInfo                       \
        -DCMAKE_INSTALL_PREFIX=%{mysql_root}                    \
        -DCOMPILATION_COMMENT='%{compile_comment}'              \
        -DDEFAULT_CHARSET=utf8                                  \
        -DDEFAULT_COLLATION=utf8_unicode_ci                     \
        -DENABLED_LOCAL_INFILE=ON                               \
        -DENABLED_LOCAL_INFILE=TRUE                             \
        -DENABLED_PROFILING=ON                                  \
        -DENABLE_DTRACE=ON                                      \
        -DFEATURE_SET=community                                 \
        -DCMAKE_INSTALL_PREFIX=%{mysql_root}                    \
        -DMYSQL_MAINTAINER_MODE=OFF                             \
        -DMYSQL_UNIX_ADDR=/var/lib/mysql/mysql.sock             \
        -DWITH_ARCHIVE_STORAGE_ENGINE=1                         \
        -DWITH_BLACKHOLE_STORAGE_ENGINE=1                       \
        -DWITH_DEBUG=OFF                                        \
        -DWITH_EMBEDDED_SERVER=OFF                              \
        -DWITH_EXTRA_CHARSETS=complex                           \
        -DWITH_FEDERATED_STORAGE_ENGINE=1                       \
        -DWITH_PARTITION_STORAGE_ENGINE=OFF                     \
        -DWITH_PERFSCHEMA_STORAGE_ENGINE=OFF                    \
        -DWITH_SSL=system                                       \
        -DWITH_UNIT_TESTS=off                                   \
        -DWITH_ZLIB=system                                                 
%{__make} %{?_smp_mflags}

cd $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/plugin/HandlerSocket-Plugin-for-MySQL
sed -i -e 's/MYSQL_VERSION_PATCH=21/MYSQL_VERSION_PATCH=21-69.0/' $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/VERSION
bash -x ./autogen.sh
echo "Configuring HandlerSocket"
CXX="${HS_CXX:-g++}" \
CXXFLAGS="$CXXFLAGS -I$RPM_BUILD_DIR/%{src_dir}/release/include" \
./configure \
        --with-mysql-source=$RPM_BUILD_DIR/%{src_dir}/%{src_dir} \
        --with-mysql-bindir=$RPM_BUILD_DIR/%{src_dir}/release/scripts \
        --with-mysql-plugindir=%{mysql_libdir}/mysql/plugin \
        --libdir=%{mysql_libdir} \
        --prefix=%{mysql_root}
sed -i -e 's/$(handlersocket_la_LINK) -rpath $(pkgplugindir) $(handlersocket_la_OBJECTS) $(handlersocket_la_LIBADD) $(LIBS)/$(handlersocket_la_LINK) -rpath \/opt\/mysql\/product\/5.6.21\/HandlerSocket $( handlersocket_la_OBJECTS) $(handlersocket_la_LIBADD) $(LIBS)/' $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/plugin/HandlerSocket-Plugin-for-MySQL/handlersocket/Makefile
%{__make} %{?_smp_mflags}

echo BEGIN_NORMAL_CONFIG ; egrep '^#define' $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/plugin/HandlerSocket-Plugin-for-MySQL/config.h ; echo END_NORMAL_CONFIG
sed -i -e 's/MYSQL_VERSION_PATCH=21-69.0/MYSQL_VERSION_PATCH=21/' $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/VERSION

%install
RBR=$RPM_BUILD_ROOT
MBD=$RPM_BUILD_DIR/%{src_dir}
%{__mkdir_p} "$(dirname $RBR%{mysql_libdir})"
%{__install} -d $RBR%{mysql_sysconfdir}/{logrotate.d,init.d}
%{__install} -d $RBR%{mysql_datadir}/mysql
%{__install} -d $RBR%{mysql_datadir}/mysql/SELinux/RHEL4
%{__install} -d $RBR%{mysql_includedir}
%{__install} -d $RBR%{mysql_libdir}
%{__install} -d $RBR%{mysql_mandir}
%{__install} -d $RBR%{mysql_libdir}/mysql/plugin
%{__install} -d $RBR%{mysql_datadir}/info
%{__install} -d $RBR%{mysql_datadir}/man/man1
%{__install} -d $RBR%{mysql_datadir}/man/man8
%{__install} -d $RBR%{mysql_datadir}/test/
%{__install} -m 644 $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/plugin/HandlerSocket-Plugin-for-MySQL/handlersocket/*.la $RBR/%{mysql_libdir}/mysql/plugin
%{__install} -m 644 $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/plugin/HandlerSocket-Plugin-for-MySQL/handlersocket/*.lo $RBR/%{mysql_libdir}/mysql/plugin
%{__install} -m 644 $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/plugin/HandlerSocket-Plugin-for-MySQL/handlersocket/.libs/*.a $RBR/%{mysql_libdir}/mysql/plugin
%{__install} -m 644 $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/plugin/HandlerSocket-Plugin-for-MySQL/handlersocket/.libs/*.so*  $RBR/%{mysql_libdir}/mysql/plugin

(
  cd $MBD/release
  %{__make} DESTDIR=$RBR benchdir_root=%{mysql_datadir} install
  d="`pwd`"
  #cd $MBD/%{src_dir}/storage/HandlerSocket-Plugin-for-MySQL
  cd $MBD/%{src_dir}/plugin/HandlerSocket-Plugin-for-MySQL
  %{__make} DESTDIR=$RBR benchdir_root=%{mysql_datadir} install
  cd "$d"
)

# Install all binaries
(
  cd $MBD/release
  %{__make} DESTDIR=$RBR install
)

#symlink new libperconaserverclient libraries to the expected libmysqlclient names
a=`pwd`
cd $RBR%{mysql_libdir}
%{__ln_s} libperconaserverclient.so.18.1.0  libmysqlclient.so
%{__ln_s} libperconaserverclient.so.18.1.0  libmysqlclient.so.18
%{__ln_s} libperconaserverclient.so.18.1.0  libmysqlclient.so.0
%{__ln_s} libperconaserverclient.a          libmysqlclient.a 
%{__ln_s} libperconaserverclient.a          libmysqlclient_r.a 

cd $a

%{__install} -m 644 $MBD/release/support-files/mysql-log-rotate $RBR%{mysql_sysconfdir}/logrotate.d/mysql
touch $RBR%{mysql_sysconfdir}/my.cnf
%{__install} -m 600 $MBD/%{src_dir}/support-files/RHEL4-SElinux/mysql.{fc,te} $RBR%{mysql_datadir}/mysql/SELinux/RHEL4
%{__rm} -rf $RBR%{mysql_mandir}/man1/make_win_bin_dist.1*
%{__mkdir_p} -m 0755 $RBR%{_sysconfdir}/init.d
%{__mkdir_p} -m 0755 $RBR%{_bindir}
%{__install} -m 0755 %{SOURCE2} $RBR%{_sysconfdir}/init.d/mysql 
%{__install} -m 0755 %{SOURCE2} $RBR%{mysql_sysconfdir}/init.d/mysql 
%{__install} -m 0755 %{SOURCE3} $RBR%{_bindir}/mysqlenv
%{__install} -m 0755 %{SOURCE4} $RBR%{_bindir}/mysqlctl

#cleanup
%{__mv} -v $RBR%{mysql_root}/scripts/mysql_install_db $RBR%{mysql_bindir}/mysql_install_db
%{__mv} -v $RBR%{mysql_root}/docs/* $RBR%{mysql_datadir}/info/
%{__mv} -v $RBR%{mysql_root}/INSTALL-BINARY $RBR%{mysql_datadir}/info/
%{__mv} -v $RBR%{mysql_root}/COPYING $RBR%{mysql_datadir}/info/
%{__mv} -v $RBR%{mysql_root}/README.MySQL $RBR%{mysql_datadir}/info/
%{__mv} -v $RBR%{mysql_root}/man/man1/* $RBR%{mysql_datadir}/man/man1/
%{__mv} -v $RBR%{mysql_root}/man/man8/* $RBR%{mysql_datadir}/man/man8/
%{__mv} -v $RBR/%{mysql_root}/mysql-test/* $RBR%{mysql_datadir}/test/
%{__mv} -v $RBR%{mysql_root}/support-files/my-default.cnf $RBR%{mysql_sysconfdir}/my.cnf
%{__rm} -rf $RBR%{mysql_root}/scripts
%{__rm} -rf $RBR/%{mysql_root}/docs
%{__rm} -rf $RBR/%{mysql_root}/man/
%{__rm} -rf  $RBR%{mysql_root}/mysql-test

%pre -n MySQL-%{product_suffix}-server
%post -n MySQL-%{product_suffix}-server
mysql_datadir=%{mysql_datadir}
NEW_VERSION=%{mysqlversion}-%{release}
STATUS_FILE=$mysql_datadir/RPM_UPGRADE_MARKER

# ----------------------------------------------------------------------
# Create data directory if needed, check whether upgrade or install
# ----------------------------------------------------------------------
if [ ! -d $mysql_datadir ] ; then mkdir -m 755 $mysql_datadir; fi
if [ -f $STATUS_FILE ] ; then
    SERVER_TO_START=`grep '^SERVER_TO_START=' $STATUS_FILE | cut -c17-`
else
    SERVER_TO_START=''
fi
if [ ! -d $mysql_datadir/mysql ] ; then
    mkdir $mysql_datadir/mysql;
    echo "MySQL RPM installation of version $NEW_VERSION" >> $STATUS_FILE
else
    # If the directory exists, we may assume it is an upgrade.
    echo "MySQL RPM upgrade to version $NEW_VERSION" >> $STATUS_FILE
fi
if [ ! -d $mysql_datadir/test ] ; then mkdir $mysql_datadir/test; fi

if [ -x /sbin/chkconfig ] ; then
        /sbin/chkconfig --add mysql
# use insserv for older SuSE Linux versions
elif [ -x /sbin/insserv ] ; then
        /sbin/insserv %{_sysconfdir}/init.d/mysql
fi

groupadd -r %{mysqld_group} 2> /dev/null || true
#useradd -M -r -d $mysql_datadir -s /bin/bash -c "MySQL server" -g %{mysqld_group} %{mysqld_user} 2> /dev/null || true
useradd -m -r -d /home/%{mysqld_user} -s /bin/bash -c "MySQL server" -g %{mysqld_group} %{mysqld_user} 2> /dev/null || true
usermod -g %{mysqld_group} %{mysqld_user} 2> /dev/null || true
chown -R %{mysqld_user}:%{mysqld_group} $mysql_datadir
chown -R %{mysqld_user}:%{mysqld_group} /home/%{mysqld_user}
echo "export PATH=\$PATH:%{mysql_bindir}" >> /home/%{mysqld_user}/.bash_profile
chmod 644 /home/%{mysqld_user}/.bash_profile
chmod -R og-rw $mysql_datadir/mysql

SETARGETDIR=/etc/selinux/targeted/src/policy
SEDOMPROG=$SETARGETDIR/domains/program
SECONPROG=$SETARGETDIR/file_contexts/program
if [ -x sbin/restorecon ] ; then
  sbin/restorecon -R var/lib/mysql
fi

# Was the server running before the upgrade? If so, restart the new one.
if [ "$SERVER_TO_START" = "true" ] ; then
    # Restart in the same way that mysqld will be started normally.
    if [ -x %{_sysconfdir}/init.d/mysql ] ; then
        %{_sysconfdir}/init.d/mysql start
        echo "Giving mysqld 5 seconds to start"
        sleep 5
    fi
fi

echo "Percona Server is distributed with several useful UDF (User Defined Function) from Maatkit."
echo "Run the following commands to create these functions:"
echo "mysql -e \"CREATE FUNCTION fnv1a_64 RETURNS INTEGER SONAME 'libfnv1a_udf.so'\""
echo "mysql -e \"CREATE FUNCTION fnv_64 RETURNS INTEGER SONAME 'libfnv_udf.so'\""
echo "mysql -e \"CREATE FUNCTION murmur_hash RETURNS INTEGER SONAME 'libmurmur_udf.so'\""
echo "See http://code.google.com/p/maatkit/source/browse/trunk/udf for more details"

# Collect an upgrade history ...
echo "Upgrade/install finished at `date`"        >> $STATUS_FILE
echo                                             >> $STATUS_FILE
echo "====="                                     >> $STATUS_FILE
STATUS_HISTORY=$mysql_datadir/RPM_UPGRADE_HISTORY
cat $STATUS_FILE >> $STATUS_HISTORY
mv -f  $STATUS_FILE ${STATUS_FILE}-LAST  # for "triggerpostun"

%preun -n MySQL-%{product_suffix}-server

if [ $1 = 0 ] ; then
        # Stop MySQL before uninstalling it
        if [ -x %{_sysconfdir}/init.d/mysql ] ; then
                %{_sysconfdir}/init.d/mysql stop > /dev/null
                # Remove autostart of MySQL
                # use chkconfig on Enterprise Linux and newer SuSE releases
                if [ -x /sbin/chkconfig ] ; then
                        /sbin/chkconfig --del mysql
                # For older SuSE Linux versions
                elif [ -x /sbin/insserv ] ; then
                        /sbin/insserv -r %{_sysconfdir}/init.d/mysql
                fi
        fi
fi
%triggerpostun -n MySQL-%{product_suffix}-server --MySQL-server-community
mysql_datadir=%{mysql_datadir}
NEW_VERSION=%{mysqlversion}-%{release}
STATUS_FILE=$mysql_datadir/RPM_UPGRADE_MARKER-LAST  # Note the difference!
STATUS_HISTORY=$mysql_datadir/RPM_UPGRADE_HISTORY

if [ -f $STATUS_FILE ] ; then
    SERVER_TO_START=`grep '^SERVER_TO_START=' $STATUS_FILE | cut -c17-`
else
    # This should never happen, but let's be prepared
    SERVER_TO_START=''
fi
echo "Analyzed: SERVER_TO_START=$SERVER_TO_START"

if [ -x /sbin/chkconfig ] ; then
        /sbin/chkconfig --add mysql
elif [ -x /sbin/insserv ] ; then
        /sbin/insserv %{_sysconfdir}/init.d/mysql
fi
if [ "$SERVER_TO_START" = "true" ] ; then
    # Restart in the same way that mysqld will be started normally.
    if [ -x %{_sysconfdir}/init.d/mysql ] ; then
        %{_sysconfdir}/init.d/mysql start
        echo "Giving mysqld 5 seconds to start"
        sleep 5
    fi
fi
# remove user 
if  getent passwd %{mysqld_user} >/dev/null; then
    /usr/sbin/userdel %{mysqld_user}
    if [ -d "/home/%{mysqld_user}" ]; then
        rm -rf /home/%{mysqld_user}
    fi
fi
#remove group
if  getent group %{mysqld_group} >/dev/null; then
    /usr/sbin/groupdel %{mysqld_group} 
fi


echo "Trigger 'postun' finished at `date`"        >> $STATUS_HISTORY
echo                                             >> $STATUS_HISTORY
echo "====="                                     >> $STATUS_HISTORY
%clean
[ "$RPM_BUILD_ROOT" != "/" ] && [ -d $RPM_BUILD_ROOT ] && rm -rf $RPM_BUILD_ROOT;

%files -n MySQL-%{product_suffix}-server
%defattr(-,root,root,0755)
%doc release/Docs/INFO_BIN
%doc release/support-files/my-*.cnf
%doc %{mysql_infodir}/COPYING
%doc %{mysql_infodir}/INFO_BIN
%doc %{mysql_infodir}/INFO_SRC
%doc %{mysql_infodir}/INSTALL-BINARY
%doc %{mysql_infodir}/mysql.info
%doc %{mysql_infodir}/README.MySQL
%doc %attr(644, root, man) %{mysql_mandir}/man1/innochecksum.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/my_print_defaults.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/myisam_ftdump.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/myisamchk.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/myisamlog.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/myisampack.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysql_convert_table_format.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysql_fix_extensions.1*
%doc %attr(644, root, man) %{mysql_mandir}/man8/mysqld.8*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysqld_multi.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysqld_safe.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysqldumpslow.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysql_install_db.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysql_secure_installation.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysql_setpermission.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysql_upgrade.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysqlhotcopy.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysqlman.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysql.server.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysqltest.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysql_tzinfo_to_sql.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysql_zap.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysqlbug.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/perror.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/replace.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/resolve_stack_dump.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/resolveip.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysql_plugin.1*
%ghost %config(noreplace,missingok) %{mysql_sysconfdir}/my.cnf
%attr(755, root, root) %{mysql_bindir}/innochecksum
%attr(755, root, root) %{mysql_bindir}/my_print_defaults
%attr(755, root, root) %{mysql_bindir}/myisam_ftdump
%attr(755, root, root) %{mysql_bindir}/myisamchk
%attr(755, root, root) %{mysql_bindir}/myisamlog
%attr(755, root, root) %{mysql_bindir}/myisampack
%attr(755, root, root) %{mysql_bindir}/mysql_config_editor
%attr(755, root, root) %{mysql_bindir}/mysql_convert_table_format
%attr(755, root, root) %{mysql_bindir}/mysql_fix_extensions
%attr(755, root, root) %{mysql_bindir}/mysql_install_db
%attr(755, root, root) %{mysql_bindir}/mysql_secure_installation
%attr(755, root, root) %{mysql_bindir}/mysql_setpermission
%attr(755, root, root) %{mysql_bindir}/mysql_tzinfo_to_sql
%attr(755, root, root) %{mysql_bindir}/mysql_upgrade
%attr(755, root, root) %{mysql_bindir}/mysql_plugin
%attr(755, root, root) %{mysql_bindir}/mysql_zap
%attr(755, root, root) %{mysql_bindir}/mysqlbug
%attr(755, root, root) %{mysql_bindir}/mysqld_multi
%attr(755, root, root) %{mysql_bindir}/mysqld_safe
%attr(755, root, root) %{mysql_bindir}/mysqldumpslow
%attr(755, root, root) %{mysql_bindir}/mysqlhotcopy
%attr(755, root, root) %{mysql_bindir}/mysqltest
%attr(755, root, root) %{mysql_bindir}/perror
%attr(755, root, root) %{mysql_bindir}/replace
%attr(755, root, root) %{mysql_bindir}/resolve_stack_dump
%attr(755, root, root) %{mysql_bindir}/resolveip
%attr(755, root, root) %{_bindir}/mysqlctl
%attr(755, root, root) %{_bindir}/mysqlenv
%attr(755, root, root) %{mysql_bindir}/mysqld
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/daemon_example.ini
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/adt_null.so
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/libdaemon_example.so
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/mypluglib.so
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/semisync_master.so
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/semisync_slave.so
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/auth.so
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/auth_socket.so
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/auth_test_plugin.so
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/qa_auth_client.so
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/qa_auth_interface.so
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/qa_auth_server.so
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/libfnv1a_udf.so
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/libfnv_udf.so
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/libmurmur_udf.so
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/scalability_metrics.so
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/validate_password.so
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/audit_log.so
%{mysql_datadir}/*.sql
%{mysql_datadir}/charsets
%{mysql_datadir}/*/errmsg.sys
%{mysql_root}/support-files/binary-configure
%{mysql_root}/support-files/magic
%{mysql_root}/support-files/mysql-log-rotate
%{mysql_root}/support-files/mysql.server
%{mysql_root}/support-files/mysqld_multi.server
%{mysql_datadir}/dictionary.txt
%{mysql_datadir}/errmsg-utf8.txt
# HandlerSocket files
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/handlersocket*.a
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/handlersocket*.la
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/handlersocket*.so*
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/handlersocket_la*
%attr(644, root, root) %config(noreplace,missingok) %{mysql_sysconfdir}/logrotate.d/mysql
%attr(755, root, root) %{_sysconfdir}/init.d/mysql
%attr(755, root, root) %{mysql_sysconfdir}/init.d/mysql
%attr(755, root, root) %{mysql_datadir}/mysql/
# ----------------------------------------------------------------------------

%files -n MySQL-%{product_suffix}-client
%defattr(-, root, root, 0755)
%attr(755, root, root) %{mysql_bindir}/msql2mysql
%attr(755, root, root) %{mysql_bindir}/mysql
%attr(755, root, root) %{mysql_bindir}/mysql_find_rows
%attr(755, root, root) %{mysql_bindir}/mysql_waitpid
%attr(755, root, root) %{mysql_bindir}/mysqlaccess
%attr(755, root, root) %{mysql_libdir}/libmysqlclient*.so
%attr(755, root, root) %{mysql_libdir}/libmysqlclient*.0
%attr(755, root, root) %{mysql_libdir}/libmysqlclient*.18
%attr(755, root, root) %{mysql_libdir}/libperconaserverclient*.so
%attr(755, root, root) %{mysql_libdir}/libperconaserverclient*.0
%attr(755, root, root) %{mysql_libdir}/libperconaserverclient*.18
%attr(644, root, root) %{mysql_bindir}/mysqlaccess.conf
%attr(755, root, root) %{mysql_bindir}/mysqladmin
%attr(755, root, root) %{mysql_bindir}/mysqlbinlog
%attr(755, root, root) %{mysql_bindir}/mysqlcheck
%attr(755, root, root) %{mysql_bindir}/mysqldump
%attr(755, root, root) %{mysql_bindir}/mysqlimport
%attr(755, root, root) %{mysql_bindir}/mysqlshow
%attr(755, root, root) %{mysql_bindir}/mysqlslap
%attr(755, root, root) %{mysql_bindir}/hsclient
%doc %attr(644, root, man) %{mysql_mandir}/man1/msql2mysql.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysql.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysql_find_rows.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysql_waitpid.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysqlaccess.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysqladmin.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysqlbinlog.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysqlcheck.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysqldump.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysqlimport.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysqlshow.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysqlslap.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysql_config_editor.1*


# ----------------------------------------------------------------------------
%files -n MySQL-%{product_suffix}-devel -f optional-files-devel
%defattr(-, root, root, 0755)
%doc %attr(644, root, man) %{mysql_mandir}/man1/comp_err.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysql_config.1*
%attr(755, root, root) %{mysql_bindir}/mysql_config
#%dir %attr(755, root, root) %{mysql_includedir}/mysql
%dir %attr(755, root, root) %{mysql_libdir}/mysql
%{mysql_includedir}/*
%{mysql_datadir}/aclocal/mysql.m4
%{mysql_libdir}/libmysqlclient.a
%{mysql_libdir}/libmysqlclient_r.a
%{mysql_libdir}/libperconaserverclient.a
%{mysql_libdir}/libperconaserverclient_r.a
%{mysql_libdir}/libmysqlservices.a
%{mysql_libdir}/libhsclient.a
%{mysql_libdir}/libhsclient.la

# ----------------------------------------------------------------------------

%files -n MySQL-%{product_suffix}-shared
%defattr(-, root, root, 0755)
# Shared libraries (omit for architectures that don't support them)
%{mysql_libdir}/libmysql*.so*
%{mysql_libdir}/mysql/plugin/query_response_time.so

# ----------------------------------------------------------------------------
 
%files -n MySQL-%{product_suffix}-test
%defattr(-, root, root, 0755)
%attr(-, root, root) %{mysql_datadir}/test
%attr(755, root, root) %{mysql_bindir}/mysql_client_test
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysql_client_test.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysql-stress-test.pl.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysql-test-run.pl.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysql_client_test_embedded.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysqltest_embedded.1*
%{mysql_root}/data/test/db.opt
# ----------------------------------------------------------------------------

%files -n MySQL-%{product_suffix}-bench
%defattr(-, root, root, 0755)
%attr(-, root, root) %{mysql_root}/sql-bench
%changelog

%post -n MySQL-%{product_suffix}-shared
echo "%{mysql_libdir}" > /etc/ld.so.conf.d/mysql-percona.conf
/sbin/ldconfig

%postun -n MySQL-%{product_suffix}-shared
echo -n > /etc/ld.so.conf.d/mysql-percona.conf
/sbin/ldconfig

%post -n MySQL-%{product_suffix}-client
echo "%{mysql_libdir}" > /etc/ld.so.conf.d/mysql-percona.conf
/sbin/ldconfig

%postun -n MySQL-%{product_suffix}-client
echo -n > /etc/ld.so.conf.d/mysql-percona.conf
/sbin/ldconfig

%changelog
* Tue Sep 23 2014 Jesse Wiley <jesse.wiley@remedyhealthmedia.com>
- updated init file to allow bind_address setting for db init function 

* Tue Sep 9 2014 Jesse Wiley <jesse.wiley@remedyhealthmedia.com>
- Initial Build for repo
