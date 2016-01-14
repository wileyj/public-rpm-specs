%define couchdb_user couchdb
%define couchdb_group couchdb
%define couchdb_home /opt/couchdb

Name:       couchdb
Version:    1.6.1
Release:    1.%{dist}
Summary:    A document database server, accessible via a RESTful JSON API

Group:      Applications/Databases
License:    ASL 2.0
Vendor: %{vendor}
Packager: %{packager}
URL:        http://couchdb.apache.org/
Source0:    http://www.apache.org/dist/%{name}/source/%{version}/apache-%{name}-%{version}.tar.gz
Source2:    %{name}.init
Source3:    %{name}.service
Source4:    %{name}.tmpfiles.conf
Patch1:     couchdb-0001-Do-not-gzip-doc-files-and-do-not-install-installatio.patch
Patch2:     couchdb-0002-Install-docs-into-versioned-directory.patch
Patch3:     couchdb-0003-More-directories-to-search-for-place-for-init-script.patch
Patch4:     couchdb-0004-Install-into-erllibdir-by-default.patch

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  autoconf
BuildRequires:  autoconf-archive
BuildRequires:  automake
BuildRequires:  curl-devel >= 7.18.0
BuildRequires:  erlang-asn1
BuildRequires:  erlang-erts >= R13B
BuildRequires:  openssl-devel
# For building mochiweb
BuildRequires:  erlang-eunit
BuildRequires:  erlang-os_mon
BuildRequires:  erlang-xmerl
BuildRequires:  help2man
BuildRequires:  js-devel >= 1.8.5
BuildRequires:  libicu-devel
BuildRequires:  libtool
# For /usr/bin/prove
BuildRequires:  perl(Test::Harness)

Requires:    erlang-asn1%{?_isa}
Requires:    erlang-erts%{?_isa} >= R13B
Requires:    erlang-os_mon%{?_isa}
Requires:    erlang-xmerl%{?_isa}
Requires:    openssl

#Initscripts
%if 0%{?fedora} > 16
Requires(post): systemd info
Requires(preun): systemd info
Requires(postun): systemd
%else
Requires(post): chkconfig info
Requires(preun): chkconfig initscripts info
%endif

# Users and groups
Requires(pre): shadow-utils


%description
Apache CouchDB is a distributed, fault-tolerant and schema-free
document-oriented database accessible via a RESTful HTTP/JSON API.
Among other features, it provides robust, incremental replication
with bi-directional conflict detection and resolution, and is
queryable and indexable using a table-oriented view engine with
JavaScript acting as the default view definition language.


%prep
%setup -q -n apache-%{name}-%{version}
%patch1 -p1 -b .dont_gzip
%patch2 -p1 -b .use_versioned_docdir
%patch3 -p1 -b .more_init_dirs
%patch4 -p1 -b .install_into_erllibdir

# More verbose tests
sed -i -e "s,prove,prove -v,g" test/etap/run.tpl


%build
autoreconf -ivf
%configure --with-erlang=%{_libdir}/erlang/usr/include
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Install our custom couchdb initscript
%if 0%{?fedora} > 16
# Install /etc/tmpfiles.d entry
install -D -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf
# Install systemd entry
install -D -m 755 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service
rm -rf %{buildroot}/%{_sysconfdir}/rc.d/
rm -rf %{buildroot}%{_sysconfdir}/default/
%else
# Use /etc/sysconfig instead of /etc/default
mv %{buildroot}%{_sysconfdir}/{default,sysconfig}
install -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}
%endif

# Remove *.la files
find %{buildroot} -type f -name "*.la" -delete

# Remove generated info files
rm -f %{buildroot}%{_infodir}/dir


%check
#make check


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%pre
getent group %{couchdb_group} >/dev/null || groupadd -r %{couchdb_group}
getent passwd %{couchdb_user} >/dev/null || \
useradd -r -g %{couchdb_group} -d %{couchdb_home} -s /bin/bash \
-c "Couchdb Database Server" %{couchdb_user}
exit 0


%post
%if 0%{?fedora} > 16
if [ $1 -eq 1 ] ; then
    # Initial installation
    /usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
%else
/sbin/chkconfig --add couchdb
%endif
/sbin/install-info %{_infodir}/CouchDB.gz %{_infodir}/dir || :


%preun
%if 0%{?fedora} > 16
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /usr/bin/systemctl --no-reload disable %{name}.service > /dev/null 2>&1 || :
    /usr/bin/systemctl stop %{name}.service > /dev/null 2>&1 || :
fi
%else
if [ $1 = 0 ] ; then
    /sbin/service couchdb stop >/dev/null 2>&1
    /sbin/chkconfig --del couchdb
fi
%endif
/sbin/install-info --delete %{_infodir}/CouchDB.gz %{_infodir}/dir || :


%postun
%if 0%{?fedora} > 16
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /usr/bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :
fi
%endif


%if 0%{?fedora} > 16
%triggerun -- couchdb < 1.0.3-5
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply httpd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save couchdb >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del couchdb >/dev/null 2>&1 || :
/bin/systemctl try-restart couchdb.service >/dev/null 2>&1 || :
%endif


%files
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/local.d
%dir %{_sysconfdir}/%{name}/default.d
%config(noreplace) %attr(0644, %{couchdb_user}, %{couchdb_group}) %{_sysconfdir}/%{name}/default.ini
%config(noreplace) %attr(0644, %{couchdb_user}, %{couchdb_group}) %{_sysconfdir}/%{name}/local.ini
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%if 0%{?fedora} > 16
%{_sysconfdir}/tmpfiles.d/%{name}.conf
%{_unitdir}/%{name}.service
%else
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_initrddir}/%{name}
%endif
%{_bindir}/%{name}
%{_bindir}/couch-config
%{_bindir}/couchjs
%{_libdir}/erlang/lib/couch-%{version}/
%{_libdir}/erlang/lib/couch_index-0.1/
%{_libdir}/erlang/lib/couch_mrview-0.1/
%{_libdir}/erlang/lib/couch_replicator-0.1/
%{_libdir}/erlang/lib/couch_dbupdates-0.1/
%{_libdir}/erlang/lib/couch_plugins-0.1/
%{_libdir}/erlang/lib/ejson-0.1.0/
%{_libdir}/erlang/lib/etap/
%{_libdir}/erlang/lib/erlang-oauth/
%{_libdir}/erlang/lib/ibrowse-2.2.0/
%{_libdir}/erlang/lib/mochiweb-1.4.1/
%{_libdir}/erlang/lib/snappy-1.0.5/
%{_datadir}/%{name}
%{_mandir}/man1/%{name}.1.*
%{_mandir}/man1/couchjs.1.*
%{_infodir}/CouchDB.gz
%{_datadir}/doc/%{name}-%{version}
%dir %attr(0755, %{couchdb_user}, %{couchdb_group}) %{_localstatedir}/log/%{name}
%dir %attr(0755, %{couchdb_user}, %{couchdb_group}) %{_localstatedir}/run/%{name}
%dir %attr(0755, %{couchdb_user}, %{couchdb_group}) %{_localstatedir}/lib/%{name}


%changelog
