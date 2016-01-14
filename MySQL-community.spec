%define mysql_old_vendor        MySQL AB
%define mysql_vendor_2          Sun Microsystems, Inc.
%define mysql_vendor            Oracle and/or its affiliates
%define	mysql_major	5
%define	mysql_minor	6
%define mysql_rev	19
%define mysql_patch	67
%define mysqlversion   %{mysql_major}.%{mysql_minor}.%{mysql_rev}

%define redhatversion %(lsb_release -rs | awk -F. '{ print $1}')
%define majorversion 67
%define minorversion 0
%define compilation_comment_release MySQL Community Server (GPL)

%define mysqld_user     mysql
%define mysqld_group    mysql
%global mysql_root  /opt/mysql/product/%{mysqlversion}
%global mysqldatadir  %{mysql_root}/share
%global mysql_libdir %{mysql_root}/lib64
%global mysql_mandir %{mysql_root}/share/man
%global mysql_bindir %{mysql_root}/bin
%global mysql_sbindir %{mysql_root}/sbin
%global mysql_sysconfdir %{mysql_root}/etc
%global mysql_includedir %{mysql_root}/include
%global mysql_infodir %{mysql_root}/share/info
%define release         %{minorversion}.%{dist}
%define product_suffix      community
%define server_suffix %{product_suffix}


%undefine __perl_provides
%undefine __perl_requires

%if %{undefined src_base}
%define src_base mysql
%endif
%define src_dir %{src_base}-%{mysqlversion}
%define feature_set community

  %define generic_kernel %(uname -r | cut -d. -f1-2)
  %define distro_description            Generic Linux (kernel %{generic_kernel})
  %define distro_releasetag             linux%{generic_kernel}
  %define distro_buildreq               gcc-c++ gperf ncurses-devel perl readline-devel time zlib-devel libaio-devel bison cmake > 2.8.8, libtool < 2.2.10, gmock-devel, gmock, gtest, gtest-devel, git
  %define distro_requires               coreutils grep procps /sbin/chkconfig /usr/sbin/useradd /usr/sbin/groupadd

%if %{defined malloc_lib_target}
%define WITH_TCMALLOC 1
%else
%define WITH_TCMALLOC 0
%endif

##############################################################################
# Configuration based upon above user input, not to be set directly
##############################################################################

%define license_files_server    %{src_dir}/COPYING %{src_dir}/README
%define license_type            GPL

##############################################################################
# Main spec file section
##############################################################################

Name:           MySQL-%{product_suffix}
Summary:        MySQL: a very fast and reliable SQL database server
Group:          Applications/Databases
Version:        %{mysqlversion}
Release:        %{release}
Distribution:   %{distro_description}
License:        Copyright (c) 2000, 2010, %{mysql_vendor}.  All rights reserved.  Use is subject to license terms.  Under %{license_type} license as shown in the Description field.
Packager:	%{packager}
Vendor:		%{vendor}
Source:         mysql-%{mysqlversion}.tar.gz
Source1:	gmock-1.6.0.tar.gz
Source2:	HandlerSocket-Plugin-for-MySQL.tar.gz
Provides:       mysql-server
BuildRequires:  %{distro_buildreq}

# Think about what you use here since the first step is to
# run a rm -rf
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

# From the manual
%description
The MySQL Server software delivers a very fast, multi-threaded, multi-user,
and robust SQL (Structured Query Language) database server. MySQL Server
is intended for mission-critical, heavy-load production systems.


##############################################################################
# Sub package definition
##############################################################################

%package -n MySQL-%{product_suffix}-server
Summary:        MySQLServer: a very fast and reliable SQL database server
Group:          Applications/Databases
Requires:       %{distro_requires} MySQL-%{product_suffix}-shared
Provides:       mysql-server

%description -n MySQL-%{product_suffix}-server
The MySQL Server software delivers a very fast, multi-threaded, multi-user,
and robust SQL (Structured Query Language) database server. MySQLServer
is intended for mission-critical, heavy-load production systems.


This package includes the MySQLServer with XtraDB binary 
as well as related utilities to run and administer MySQLServer.

If you want to access and work with the database, you have to install
package "MySQL-%{product_suffix}-client" as well!

# ----------------------------------------------------------------------------
%package -n MySQL-%{product_suffix}-client
Summary:        MySQL Server - Client
Group:          Applications/Databases
Requires:      MySQL-%{product_suffix}-shared
Provides:       mysql-client MySQL-client

%description -n MySQL-%{product_suffix}-client
This package contains the standard MySQL Server client and administration tools.

# ----------------------------------------------------------------------------
%package -n MySQL-%{product_suffix}-test
Requires:       MySQL-%{product_suffix}-client perl
Summary:        MySQL Server - Test suite
Group:          Applications/Databases
Provides:       mysql-test
AutoReqProv:    no

%description -n MySQL-%{product_suffix}-test
This package contains the MySQL Server regression test suite.


# ----------------------------------------------------------------------------
%package -n MySQL-%{product_suffix}-devel
Summary:        MySQL Server - Development header files and libraries
Group:          Applications/Databases
Provides:       mysql-devel

%description -n MySQL-%{product_suffix}-devel
This package contains the development header files and libraries necessary
to develop MySQL Server client applications.


# ----------------------------------------------------------------------------
%package -n MySQL-%{product_suffix}-shared
Summary:        MySQL Server - Shared libraries
Group:          Applications/Databases
Provides:       mysql-shared

%description -n MySQL-%{product_suffix}-shared
This package contains the shared libraries (*.so*) which certain languages
and applications need to dynamically load and use MySQL Server.

##############################################################################
%prep
%setup -T -a 0 -c -n %{src_dir}
##############################################################################
%build

if [ ! -d $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/source_downloads ]
then
        mkdir -p $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/source_downloads
fi

cp %{SOURCE1} $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/source_downloads/gmock-1.6.0.tar.gz
tar -xzvf $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/source_downloads/gmock-1.6.0.tar.gz
t=`pwd`
cd $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/plugin
tar -xzvf  %{SOURCE2}
cd $t

# Be strict about variables, bail at earliest opportunity, etc.
set -u
BuildHandlerSocket(){
	cd $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/plugin/HandlerSocket-Plugin-for-MySQL
	git pull
	#sed -i -e 's/MYSQL_VERSION_PATCH=19/MYSQL_VERSION_PATCH=19-67.0/' $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/VERSION
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
	sed -i -e 's/$(handlersocket_la_LINK) -rpath $(pkgplugindir) $(handlersocket_la_OBJECTS) $(handlersocket_la_LIBADD) $(LIBS)/$(handlersocket_la_LINK) -rpath \/opt\/mysql\/product\/5.6.19\/HandlerSocket $( handlersocket_la_OBJECTS) $(handlersocket_la_LIBADD) $(LIBS)/' $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/plugin/HandlerSocket-Plugin-for-MySQL/handlersocket/Makefile
	make %{?_smp_mflags}
}

# Optional package files
touch optional-files-devel
export PATH=${MYSQL_BUILD_PATH:-$PATH}
export CC=${MYSQL_BUILD_CC:-${CC:-gcc}}
export CXX=${MYSQL_BUILD_CXX:-${CXX:-g++}}
export CFLAGS=${MYSQL_BUILD_CFLAGS:-${CFLAGS:-$RPM_OPT_FLAGS}}
export CXXFLAGS=${MYSQL_BUILD_CXXFLAGS:-${CXXFLAGS:-$RPM_OPT_FLAGS -felide-constructors -fno-exceptions -fno-rtti}}
export LDFLAGS=${MYSQL_BUILD_LDFLAGS:-${LDFLAGS:-}}
export CMAKE=${MYSQL_BUILD_CMAKE:-${CMAKE:-cmake}}
export MAKE_JFLAG=${MYSQL_BUILD_MAKE_JFLAG:-${MAKE_JFLAG:-}}
mkdir release
(
  cd release
  # XXX: MYSQL_UNIX_ADDR should be in cmake/* but mysqlversion is included before
  # XXX: install_layout so we can't just set it based on INSTALL_LAYOUT=RPM
 ${CMAKE} ../%{src_dir}                                       	\
	-DENABLE_DOWNLOADS=1					\
        -DCMAKE_BUILD_TYPE=RelWithDebInfo                       \
        -DBUILD_CONFIG=mysql_release                            \
        -DCOMPILATION_COMMENT="%{compilation_comment_release}"  \
        -DFEATURE_SET="%{feature_set}"                          \
        -DCMAKE_INSTALL_PREFIX=%{mysql_root}                    \
        -DCMAKE_MYSQL_DATADIR=%{mysqldatadir}                   \
        -DCMAKE_SYSCONFDIR=%{mysql_sysconfdir}                  \
        -DINSTALL_LAYOUT=RPM                                    \
        -DINSTALL_SCRIPTDIR=bin                                 \
        -DINSTALL_LIBDIR_RPM=%{_lib}                            \
        -DINSTALL_DOCDIR=%{mysql_root}/share/doc/mysql          \
        -DINSTALL_DOCREADMEDIR=%{mysql_root}/share/doc/mysql    \
        -DINSTALL_INCLUDEDIR=%{mysql_root}/include/mysql        \
        -DINSTALL_INFODIR=%{mysql_root}/share/info              \
        -DINSTALL_MANDIR=%{mysql_root}/share/man                \
        -DINSTALL_SBINDIR=%{mysql_root}/sbin                    \
        -DINSTALL_MYSQLDATADIR=%{mysqldatadir}                  \
        -DINSTALL_MYSQLSHAREDIR=%{mysql_root}/share/mysql       \
        -DINSTALL_MYSQLTESTDIR=%{mysql_root}/share/mysql/test   \
        -DINSTALL_PLUGINDIR=%{mysql_root}/%{_lib}/mysql/plugin  \
        -DINSTALL_SQLBENCHDIR=%{mysql_root}/share/mysql/bench   \
        -DINSTALL_SUPPORTFILESDIR=%{mysql_root}/share/mysql     \
        -DMYSQL_DATADIR=%{mysqldatadir}                         \
        -DMYSQL_UNIX_ADDR=/var/lib/mysql/mysql.sock             \
        -DSYSCONFDIR=%{mysql_sysconfdir}                        \
        -DWITH_PARTITION_STORAGE_ENGINE=OFF                     \
        -DWITH_PERFSCHEMA_STORAGE_ENGINE=OFF                    \
        -DWITH_EXTRA_CHARSETS=complex                           \
        -DWITH_LIBEVENT=system                                  \
        -DINSTALL_LIBDIR=%{_lib}                                \
        -DENABLED_LOCAL_INFILE=ON                               \
        -DENABLE_DTRACE=ON                                      \
        -DWITH_EMBEDDED_SERVER=OFF                              \
        -DWITH_READLINE=ON                                      \
        -DWITH_SSL=system                                       \
        -DWITH_ZLIB=system					\
	 -DWITH_UNIT_TESTS=off

  echo BEGIN_NORMAL_CONFIG ; egrep '^#define' include/config.h ; echo END_NORMAL_CONFIG
  make ${MAKE_JFLAG}
  cd ../%{src_dir}
  d="`pwd`"
  BuildHandlerSocket
  cd "$d"
)
# Use the build root for temporary storage of the shared libraries.
RBR=$RPM_BUILD_ROOT

# Clean up the BuildRoot first
[ "$RBR" != "/" ] && [ -d "$RBR" ] && rm -rf "$RBR";

# For gcc builds, include libgcc.a in the devel subpackage (BUG 4921).  This
# needs to be during build phase as $CC is not set during install.
if "$CC" -v 2>&1 | grep '^gcc.version' >/dev/null 2>&1
then
  libgcc=`$CC $CFLAGS --print-libgcc-file`
  if [ -f $libgcc ]
  then
    mkdir -p $RBR%{mysql_libdir}/mysql
    install -m 644 $libgcc $RBR%{mysql_libdir}/mysql/libmygcc.a
    echo "%{mysql_libdir}/mysql/libmygcc.a" >>optional-files-devel
  fi
fi

# Move temporarily the saved files to the BUILD directory since the BUILDROOT
# dir will be cleaned at the start of the install phase
mkdir -p "$(dirname $RPM_BUILD_DIR/%{mysql_libdir})"
mv $RBR%{mysql_libdir} $RPM_BUILD_DIR/%{mysql_libdir}
#sed -i -e 's/MYSQL_VERSION_PATCH=19-67.0/MYSQL_VERSION_PATCH=19/' $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/VERSION


##############################################################################
%install

RBR=$RPM_BUILD_ROOT
MBD=$RPM_BUILD_DIR/%{src_dir}

# Move back the libdir from BUILD dir to BUILDROOT
mkdir -p "$(dirname $RBR%{mysql_libdir})"
mv $RPM_BUILD_DIR/%{mysql_libdir} $RBR%{mysql_libdir}

# Ensure that needed directories exists
install -d $RBR%{mysql_sysconfdir}/{logrotate.d,init.d}
install -d $RBR%{mysqldatadir}/mysql
install -d $RBR%{mysqldatadir}/mysql-test
install -d $RBR%{mysqldatadir}/mysql/SELinux/RHEL4
install -d $RBR%{mysql_includedir}
install -d $RBR%{mysql_libdir}
install -d $RBR%{mysql_mandir}
install -d $RBR%{mysql_sbindir}
install -d $RBR%{mysql_libdir}/mysql/plugin
install -m 644 $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/plugin/HandlerSocket-Plugin-for-MySQL/handlersocket/*.la $RBR/%{mysql_libdir}/mysql/plugin
install -m 644 $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/plugin/HandlerSocket-Plugin-for-MySQL/handlersocket/*.lo $RBR/%{mysql_libdir}/mysql/plugin
install -m 644 $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/plugin/HandlerSocket-Plugin-for-MySQL/handlersocket/.libs/*.a $RBR/%{mysql_libdir}/mysql/plugin
install -m 644 $RPM_BUILD_DIR/%{src_dir}/%{src_dir}/plugin/HandlerSocket-Plugin-for-MySQL/handlersocket/.libs/*.so*  $RBR/%{mysql_libdir}/mysql/plugin

(
  cd $MBD/release
  make DESTDIR=$RBR benchdir_root=%{mysqldatadir} install
  d="`pwd`"
  cd $MBD/%{src_dir}/plugin/HandlerSocket-Plugin-for-MySQL
  make DESTDIR=$RBR benchdir_root=%{mysqldatadir} install
  cd "$d"
)

(
  d="`pwd`"
  cd $MBD/release
  make DESTDIR=$RBR benchdir_root=%{mysqldatadir} install
  cd "$d"
)

# Install all binaries
(
  cd $MBD/release
  make DESTDIR=$RBR install
)

# FIXME: at some point we should stop doing this and just install everything
# FIXME: directly into %{mysql_libdir}/mysql - perhaps at the same time as renaming
# FIXME: the shared libraries to use libmysql*-$major.$minor.so syntax
mv -v $RBR/%{mysql_libdir}/*.a $RBR/%{mysql_libdir}/mysql/

# Install logrotate and autostart
install -m 644 $MBD/release/support-files/mysql-log-rotate $RBR%{mysql_sysconfdir}/logrotate.d/mysql
install -m 755 $MBD/release/support-files/mysql.server $RBR%{mysql_sysconfdir}/init.d/mysql

# Create a symlink "rcmysql", pointing to the init.script. SuSE users
# will appreciate that, as all services usually offer this.
ln -s %{mysql_sysconfdir}/init.d/mysql $RBR%{mysql_sbindir}/rcmysql

# Touch the place where the my.cnf config file might be located
# Just to make sure it's in the file list and marked as a config file
touch $RBR%{mysql_sysconfdir}/my.cnf

# Install SELinux files in datadir
install -m 600 $MBD/%{src_dir}/support-files/RHEL4-SElinux/mysql.{fc,te} \
  $RBR%{mysqldatadir}/mysql/SELinux/RHEL4

%if %{WITH_TCMALLOC}
# Even though this is a shared library, put it under /usr/lib*/mysql, so it
# doesn't conflict with possible shared lib by the same name in /usr/lib*.  See
# `mysql_config --variable=pkglibdir` and mysqld_safe for how this is used.
install -m 644 "%{malloc_lib_source}" \
  "$RBR%{mysql_libdir}/mysql/%{malloc_lib_target}"
%endif

# Remove man pages we explicitly do not want to package, avoids 'unpackaged
# files' warning.
rm -f $RBR%{mysql_mandir}/man1/make_win_bin_dist.1*


# fix the paths since they're broken for some reason
#mkdir -p $RBR/etc/init.d/

for i in `find $RBR%{mysql_root} -type f -exec sh -c "file -i {} | grep -v binary >/dev/null" \; -print`
 do
 sed -i -e 's/\/opt\/mysql\/product\/5.6.19\/\//\//' $i
 done

##############################################################################
#  Post processing actions, i.e. when installed
##############################################################################

%pre -n MySQL-%{product_suffix}-server

%post -n MySQL-%{product_suffix}-server

mysql_datadir=%{mysqldatadir}
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
# echo "Analyzed: SERVER_TO_START=$SERVER_TO_START"
if [ ! -d $mysql_datadir/mysql ] ; then
	mkdir $mysql_datadir/mysql;
	echo "MySQL RPM installation of version $NEW_VERSION" >> $STATUS_FILE
else
	# If the directory exists, we may assume it is an upgrade.
	echo "MySQL RPM upgrade to version $NEW_VERSION" >> $STATUS_FILE
fi
if [ ! -d $mysql_datadir/test ] ; then mkdir $mysql_datadir/test; fi

# ----------------------------------------------------------------------
# Make MySQL start/shutdown automatically when the machine does it.
# ----------------------------------------------------------------------
# NOTE: This still needs to be debated. Should we check whether these links
# for the other run levels exist(ed) before the upgrade?
# use chkconfig on Enterprise Linux and newer SuSE releases
if [ -x /sbin/chkconfig ] ; then
        /sbin/chkconfig --add mysql
# use insserv for older SuSE Linux versions
elif [ -x /sbin/insserv ] ; then
        /sbin/insserv %{mysql_sysconfdir}/init.d/mysql
fi

# ----------------------------------------------------------------------
# Create a MySQL user and group. Do not report any problems if it already
# exists.
# ----------------------------------------------------------------------
groupadd -r %{mysqld_group} 2> /dev/null || true
useradd -M -r -d $mysql_datadir -s /bin/bash -c "MySQL server" \
  -g %{mysqld_group} %{mysqld_user} 2> /dev/null || true
# The user may already exist, make sure it has the proper group nevertheless
# (BUG#12823)
usermod -g %{mysqld_group} %{mysqld_user} 2> /dev/null || true

# ----------------------------------------------------------------------
# Change permissions so that the user that will run the MySQL daemon
# owns all database files.
# ----------------------------------------------------------------------
chown -R %{mysqld_user}:%{mysqld_group} $mysql_datadir
echo "ROJASJ %{mysql_libdir}"

# ----------------------------------------------------------------------
# Initiate databases if needed
# ----------------------------------------------------------------------
%{mysql_bindir}/mysql_install_db --rpm --user=%{mysqld_user}

# ----------------------------------------------------------------------
# Upgrade databases if needed would go here - but it cannot be automated yet
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# Change permissions again to fix any new files.
# ----------------------------------------------------------------------
chown -R %{mysqld_user}:%{mysqld_group} $mysql_datadir

# ----------------------------------------------------------------------
# Fix permissions for the permission database so that only the user
# can read them.
# ----------------------------------------------------------------------
chmod -R og-rw $mysql_datadir/mysql

# ----------------------------------------------------------------------
# install SELinux files - but don't override existing ones
# ----------------------------------------------------------------------
SETARGETDIR=/etc/selinux/targeted/src/policy
SEDOMPROG=$SETARGETDIR/domains/program
SECONPROG=$SETARGETDIR/file_contexts/program
if [ -f /etc/redhat-release ] \
 && (grep -q "Red Hat Enterprise Linux .. release 4" /etc/redhat-release \
 || grep -q "CentOS release 4" /etc/redhat-release) ; then
  echo
  echo
  echo 'Notes regarding SELinux on this platform:'
  echo '========================================='
  echo
  echo 'The default policy might cause server startup to fail because it is'
  echo 'not allowed to access critical files.  In this case, please update'
  echo 'your installation.'
  echo
  echo 'The default policy might also cause inavailability of SSL related'
  echo 'features because the server is not allowed to access /dev/random'
  echo 'and /dev/urandom. If this is a problem, please do the following:'
  echo
  echo '  1) install selinux-policy-targeted-sources from your OS vendor'
  echo '  2) add the following two lines to '$SEDOMPROG/mysqld.te':'
  echo '       allow mysqld_t random_device_t:chr_file read;'
  echo '       allow mysqld_t urandom_device_t:chr_file read;'
  echo '  3) cd to '$SETARGETDIR' and issue the following command:'
  echo '       make load'
  echo
  echo
fi

if [ -x sbin/restorecon ] ; then
  sbin/restorecon -R var/lib/mysql
fi

# Was the server running before the upgrade? If so, restart the new one.
if [ "$SERVER_TO_START" = "true" ] ; then
	# Restart in the same way that mysqld will be started normally.
	if [ -x %{mysql_sysconfdir}/init.d/mysql ] ; then
		%{mysql_sysconfdir}/init.d/mysql start
		echo "Giving mysqld 5 seconds to start"
		sleep 5
	fi
fi

echo "MySQL Server is distributed with several useful UDF (User Defined Function) from Maatkit."
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


#echo "Thank you for installing the MySQL Community Server! For Production
#systems, we recommend MySQL Enterprise, which contains enterprise-ready
#software, intelligent advisory services, and full production support with
#scheduled service packs and more.  Visit www.mysql.com/enterprise for more
#information."

%preun -n MySQL-%{product_suffix}-server

# Which '$1' does this refer to?  Fedora docs have info:
# " ... a count of the number of versions of the package that are installed.
#   Action                           Count
#   Install the first time           1
#   Upgrade                          2 or higher (depending on the number of versions installed)
#   Remove last version of package   0 "
#
#  http://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/RPM_Guide/ch09s04s05.html
 
if [ $1 = 0 ] ; then
        # Stop MySQL before uninstalling it
        if [ -x %{mysql_sysconfdir}/init.d/mysql ] ; then
                %{mysql_sysconfdir}/init.d/mysql stop > /dev/null
                # Remove autostart of MySQL
                # use chkconfig on Enterprise Linux and newer SuSE releases
                if [ -x /sbin/chkconfig ] ; then
                        /sbin/chkconfig --del mysql
                # For older SuSE Linux versions
                elif [ -x /sbin/insserv ] ; then
                        /sbin/insserv -r %{mysql_sysconfdir}/init.d/mysql
                fi
        fi
fi

# We do not remove the mysql user since it may still own a lot of
# database files.

%triggerpostun -n MySQL-%{product_suffix}-server --MySQL-server-community

# Setup: We renamed this package, so any existing "server-community"
#   package will be removed when this "server" is installed.
# Problem: RPM will first run the "pre" and "post" sections of this script,
#   and only then the "preun" of that old community server.
#   But this "preun" includes stopping the server and uninstalling the service,
#   "chkconfig --del mysql" which removes the symlinks to the start script.
# Solution: *After* the community server got removed, restart this server
#   and re-install the service.
#
# For information about triggers in spec files, see the Fedora docs:
#   http://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/RPM_Guide/ch10s02.html
# For all details of this code, see the "pre" and "post" sections.

mysql_datadir=%{mysqldatadir}
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
# use insserv for older SuSE Linux versions
elif [ -x /sbin/insserv ] ; then
        /sbin/insserv %{mysql_sysconfdir}/init.d/mysql
fi

# Was the server running before the upgrade? If so, restart the new one.
if [ "$SERVER_TO_START" = "true" ] ; then
	# Restart in the same way that mysqld will be started normally.
	if [ -x %{mysql_sysconfdir}/init.d/mysql ] ; then
		%{mysql_sysconfdir}/init.d/mysql start
		echo "Giving mysqld 5 seconds to start"
		sleep 5
	fi
fi

echo "Trigger 'postun --community' finished at `date`"        >> $STATUS_HISTORY
echo                                             >> $STATUS_HISTORY
echo "====="                                     >> $STATUS_HISTORY


# ----------------------------------------------------------------------
# Clean up the BuildRoot after build is done
# ----------------------------------------------------------------------
%clean
[ "$RPM_BUILD_ROOT" != "/" ] && [ -d $RPM_BUILD_ROOT ] \
  && rm -rf $RPM_BUILD_ROOT;

##############################################################################
#  Files section
##############################################################################

%files -n MySQL-%{product_suffix}-server
%defattr(-,root,root,0755)

%if %{defined license_files_server}
%doc %{license_files_server}
%endif

%doc release/Docs/INFO_BIN
%doc release/support-files/my-*.cnf

#%doc %attr(644, root, root) %{mysql_infodir}/mysql.info*

%doc %attr(644, root, man) %{mysql_mandir}/man1/innochecksum.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/my_print_defaults.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/myisam_ftdump.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/myisamchk.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/myisamlog.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/myisampack.1*
%attr(755, root, root) %{mysql_bindir}/mysql_config_editor
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

%attr(755, root, root) %{mysql_sbindir}/mysqld
%attr(755, root, root) %{mysql_sbindir}/rcmysql
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
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/validate_password.so

# HandlerSocket files
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/handlersocket*.a
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/handlersocket*.la
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/handlersocket*.so*
%attr(755, root, root) %{mysql_libdir}/mysql/plugin/handlersocket_la*

%if %{WITH_TCMALLOC}
%attr(755, root, root) %{mysql_libdir}/mysql/%{malloc_lib_target}
%endif

%attr(644, root, root) %config(noreplace,missingok) %{mysql_sysconfdir}/logrotate.d/mysql
%attr(755, root, root) %{mysql_sysconfdir}/init.d/mysql

%attr(755, root, root) %{mysqldatadir}/mysql/

# ----------------------------------------------------------------------------
%files -n MySQL-%{product_suffix}-client

%defattr(-, root, root, 0755)
%attr(755, root, root) %{mysql_bindir}/msql2mysql
%attr(755, root, root) %{mysql_bindir}/mysql
%attr(755, root, root) %{mysql_bindir}/mysql_find_rows
%attr(755, root, root) %{mysql_bindir}/mysql_waitpid
%attr(755, root, root) %{mysql_bindir}/mysqlaccess
# XXX: This should be moved to %{mysql_sysconfdir}
%attr(755, root, root) %{mysql_libdir}/libmysqlclient*.so
%attr(755, root, root) %{mysql_libdir}/libmysqlclient*.0
%attr(755, root, root) %{mysql_libdir}/libmysqlclient*.18
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
%dir %attr(755, root, root) %{mysql_includedir}/mysql
%dir %attr(755, root, root) %{mysql_libdir}/mysql
%{mysql_includedir}/mysql/*
%{mysql_includedir}/handlersocket
%{mysqldatadir}/aclocal/mysql.m4
%{mysql_libdir}/mysql/libmysqlclient.a
%{mysql_libdir}/mysql/libmysqlclient_r.a
%{mysql_libdir}/mysql/libmysqlservices.a
%{mysql_libdir}/mysql/libhsclient.a
%{mysql_libdir}/libhsclient.la

# ----------------------------------------------------------------------------
%files -n MySQL-%{product_suffix}-shared
%defattr(-, root, root, 0755)
# Shared libraries (omit for architectures that don't support them)
%{mysql_libdir}/libmysql*.so*
# Maatkit UDF libs
#%{mysql_libdir}/mysql/plugin/libfnv1a_udf.a
#%{mysql_libdir}/mysql/plugin/libfnv1a_udf.la
#%{mysql_libdir}/mysql/plugin/libfnv_udf.a
#%{mysql_libdir}/mysql/plugin/libfnv_udf.la
#%{mysql_libdir}/mysql/plugin/libmurmur_udf.a
#%{mysql_libdir}/mysql/plugin/libmurmur_udf.la

%post -n MySQL-%{product_suffix}-shared
echo "%{mysql_libdir}" > /etc/ld.so.conf.d/mysql.conf
/sbin/ldconfig

%postun -n MySQL-%{product_suffix}-shared
echo -n > /etc/ld.so.conf.d/mysql.conf
/sbin/ldconfig

%post -n MySQL-%{product_suffix}-client
echo "%{mysql_libdir}" > /etc/ld.so.conf.d/mysql.conf
/sbin/ldconfig

%postun -n MySQL-%{product_suffix}-client
echo -n > /etc/ld.so.conf.d/mysql.conf
/sbin/ldconfig
# ----------------------------------------------------------------------------
%files -n MySQL-%{product_suffix}-test
%defattr(-, root, root, 0755)
%attr(-, root, root) %{mysqldatadir}/mysql-test
%attr(755, root, root) %{mysql_bindir}/mysql_client_test
#%attr(755, root, root) %{mysql_bindir}/mysql_client_test_embedded
#%attr(755, root, root) %{mysql_bindir}/mysqltest_embedded
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysql_client_test.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysql-stress-test.pl.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysql-test-run.pl.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysql_client_test_embedded.1*
%doc %attr(644, root, man) %{mysql_mandir}/man1/mysqltest_embedded.1*

##############################################################################
# The spec file changelog only includes changes made to the spec file
# itself - note that they must be ordered by date (important when
# merging BK trees)
##############################################################################
%changelog
