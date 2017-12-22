%global _hardened_build 1
%global java_home /usr/java/current
%global __provides_exclude_from ^%{_libdir}/collectd/.*\\.so$

%define git_repo https://github.com/collectd/collectd
%define git_version %(echo `curl -s  %{git_repo}/releases | grep 'class="css-truncate-target"' | head -1 |  tr -d '\\-</span class="css-truncate-target">'`)
%global git_revision %(echo `git ls-remote %{git_repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define git_summary        %(echo `curl -s %{git_repo} | grep "<title>" | cut -f2 -d ":" | sed 's|</title>||'`)
%define rel_version 1
%define _prefix /opt/%{name}-%{version}
%define _includedir %{_prefix}/include
%define _libdir %{_prefix}/lib64

Summary: %{git_summary}
Name: collectd
Version: %{git_version}
Release: 1.%{?dist}
License: GPLv2
Group: System Environment/Daemons
URL: https://collectd.org/

#Source: https://collectd.org/files/%{name}-%{version}.tar.bz2
Source1: collectd-httpd.conf
Source2: collectd.service
Source91: apache.conf
Source92: email.conf
Source93: mysql.conf
Source94: nginx.conf
Source95: sensors.conf
Source96: snmp.conf
Source97: rrdtool.conf

Patch0: %{name}-include-collectd.d.patch

BuildRequires: libtool-ltdl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(ExtUtils::Embed)
BuildRequires: python-devel
BuildRequires: libgcrypt-devel
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description
collectd is a daemon which collects system performance statistics periodically
and provides mechanisms to store the values in a variety of ways,
for example in RRD files.

%package amqp
Summary:       AMQP plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: librabbitmq-devel
%description amqp
This plugin can be used to communicate with other instances of collectd
or third party applications using an AMQP message broker.


%package apache
Summary:       Apache plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
%description apache
This plugin collects data provided by Apache's 'mod_status'.


%package ascent
Summary:       Ascent plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: curl-devel
BuildRequires: libxml2-devel
%description ascent
This plugin collects data about an Ascent server,
a free server for the "World of Warcraft" game.


%package bind
Summary:       Bind plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: curl-devel
BuildRequires: libxml2-devel
%description bind
This plugin retrieves statistics from the BIND dns server.


%package ceph
Summary:       Ceph plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: yajl-devel
%description ceph
This plugin collects data from Ceph.


%package chrony
Summary:       Chrony plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
%description chrony
Chrony plugin for collectd


%package curl
Summary:       Curl plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: curl-devel
%description curl
This plugin reads webpages with curl


%package curl_json
Summary:       Curl JSON plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: curl-devel
BuildRequires: yajl-devel
%description curl_json
This plugin retrieves JSON data via curl.


%package curl_xml
Summary:       Curl XML plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: curl-devel
BuildRequires: libxml2-devel
%description curl_xml
This plugin retrieves XML data via curl.


%package dbi
Summary:       DBI plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: libdbi-devel
%description dbi
This plugin uses the dbi library to connect to various databases,
execute SQL statements and read back the results.


%package dns
Summary:       DNS traffic analysis plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: libpcap-devel
%description dns
This plugin collects DNS traffic data.


%package drbd
Summary:       DRBD plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
%description drbd
This plugin collects data from DRBD.


%package email
Summary:       Email plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
%description email
This plugin collects data provided by spamassassin.


%package generic-jmx
Summary:       Generic JMX plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
%description generic-jmx
This plugin collects data provided by JMX.


%package gmond
Summary:       Gmond plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: ganglia-devel
%description gmond
This plugin receives multicast traffic sent by gmond,
the statistics collection daemon of Ganglia.


%package gps
Summary:       GPS plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: gpsd-devel
%description gps
This plugin monitor gps related data through gpsd.

%package hugepages
Summary:       Hugepages plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
%description hugepages
This plugin collects statistics about hugepage usage.


%package ipmi
Summary:       IPMI plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: OpenIPMI-devel
%description ipmi
This plugin for collectd provides IPMI support.


%ifnarch aarch64
%package iptables
Summary:       Iptables plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: iptables-devel
%description iptables
This plugin collects data from iptables counters.
%endif


%package ipvs
Summary:       IPVS plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
%description ipvs
This plugin collects data from IPVS.


%package java
Summary:       Java bindings for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: jdk
#BuildRequires: jpackage-utils
%description java
These are the Java bindings for collectd.


%package lua
Summary:       Lua plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: lua-devel
%description lua
The Lua plugin embeds a Lua interpreter into collectd and exposes the
application programming interface (API) to Lua scripts.


%package lvm
Summary:       LVM plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: lvm2-devel
%description lvm
This plugin collects information from lvm


%package modbus
Summary:       Modbus plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: libmodbus-devel
%description modbus
This plugin connects to a Modbus "slave" via Modbus/TCP
and reads register values.


%package mqtt
Summary:       MQTT plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: mosquitto-devel
%description mqtt
The MQTT plugin publishes and subscribes to MQTT topics.


%package mysql
Summary:       MySQL plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: mysql-devel
%description mysql
MySQL querying plugin. This plugin provides data of issued commands,
called handlers and database traffic.


%package netlink
Summary:       Netlink plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: iproute-static, libmnl-devel
%description netlink
This plugin uses a netlink socket to query the Linux kernel
about statistics of various interface and routing aspects.


%package nginx
Summary:       Nginx plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
%description nginx
This plugin collects data provided by Nginx.


%package notify_desktop
Summary:       Notify desktop plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: libnotify-devel
%description notify_desktop
This plugin sends a desktop notification to a notification daemon,
as defined in the Desktop Notification Specification.


%package notify_email
Summary:       Notify email plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: libesmtp-devel
%description notify_email
This plugin uses the ESMTP library to send
notifications to a configured email address.


%ifnarch s390 s390x
%package nut
Summary:       Network UPS Tools plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: nut-devel
%description nut
This plugin for collectd provides Network UPS Tools support.
%endif


%package openldap
Summary:       OpenLDAP plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: openldap-devel
%description openldap
This plugin for collectd reads monitoring information
from OpenLDAP's cn=Monitor subtree.


%package -n perl-Collectd
Summary:       Perl bindings for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%description -n perl-Collectd
This package contains the Perl bindings and plugin for collectd.


%package pinba
Summary:       Pinba plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: protobuf-c-devel
%description pinba
This plugin receives profiling information from Pinba,
an extension for the PHP interpreter.


%package ping
Summary:       Ping plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: liboping-devel
%description ping
This plugin for collectd provides network latency statistics.


%package postgresql
Summary:       PostgreSQL plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: postgresql-devel
%description postgresql
PostgreSQL querying plugin. This plugins provides data of issued commands,
called handlers and database traffic.


%package redis
Summary:       Redis plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: hiredis-devel
%description redis
The Redis plugin connects to one or more instances of Redis, a key-value store,
and collects usage information using the hiredis library.


%package rrdcached
Summary:       RRDCacheD plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: rrdtool-devel
%description rrdcached
This plugin uses the RRDtool accelerator daemon, rrdcached(1),
to store values to RRD files in an efficient manner.


%package rrdtool
Summary:       RRDTool plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: rrdtool-devel
%description rrdtool
This plugin for collectd provides rrdtool support.


%ifnarch ppc sparc sparc64 aarch64
%package sensors
Summary:       Libsensors module for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: lm_sensors-devel
%description sensors
This plugin for collectd provides querying of sensors supported by
lm_sensors.
%endif


%package smart
Summary:       SMART plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: libatasmart-devel
%description smart
This plugin for collectd collects SMART statistics,
notably load cycle count, temperature and bad sectors.


%package snmp
Summary:       SNMP module for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: net-snmp-devel
%description snmp
This plugin for collectd provides querying of net-snmp.


%ifarch %ix86 x86_64
%package turbostat
Summary:       Turbostat module for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: libcap-devel
%description turbostat
This plugin for collectd reads CPU frequency and C-state residency
on modern Intel turbo-capable processors.
%endif


%package varnish
Summary:       Varnish plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: varnish-libs-devel
%description varnish
This plugin collects information about Varnish, an HTTP accelerator.


%ifnarch ppc ppc64 sparc sparc64 aarch64
%package virt
Summary:       Libvirt plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: libvirt-devel
BuildRequires: libxml2-devel
%description virt
This plugin collects information from virtualized guests.
%endif


%package web
Summary:       Contrib web interface to viewing rrd files
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      collectd-rrdtool = %{version}-%{release}
Requires:      perl-HTML-Parser, perl-Regexp-Common, rrdtool-perl, httpd
%description web
This package will allow for a simple web interface to view rrd files created by
collectd.

%package write_prometheus
Summary:       Prometheus output plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: libmicrohttpd-devel
%description write_prometheus
This plugin exposes collected values using an embedded HTTP
server, turning the collectd daemon into a Prometheus exporter.


%package write_redis
Summary:       Redis output plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: hiredis-devel
%description write_redis
This plugin can send data to Redis.


%package write_riemann
Summary:       Riemann output plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: riemann-c-client-devel
%description write_riemann
This plugin can send data to Riemann.


%package write_sensu
Summary:       Sensu output plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
%description write_sensu
This plugin can send data to Sensu.


%package write_tsdb
Summary:       OpenTSDB output plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
%description write_tsdb
This plugin can send data to OpenTSDB.


%package zookeeper
Summary:       Zookeeper plugin for collectd
Group:         System Environment/Daemons
Requires:      %{name}%{?_isa} = %{version}-%{release}
%description zookeeper
This is a collectd plugin that reads data from Zookeeper's MNTR command.



# recompile generated files
touch src/pinba.proto

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{git_repo} %{name}-%{version}

%build
cd %{name}-%{version}
sh build.sh
#export CXXFLAGS="-I/usr/java/current/include"
#export CPPFLAGS="-I/usr/java/current/include"
%configure CXXFLAGS="-I/usr/java/current/include" \
    --disable-dependency-tracking \
    --disable-silent-rules \
    --without-included-ltdl \
    --enable-all-plugins \
    --disable-static \
    --disable-apple_sensors \
    --disable-aquaero \
    --disable-dpdkevents \
    --disable-dpdkstat \
    --disable-barometer \
    --disable-grpc \
    --disable-intel_rdt \
    --disable-intel_pmu \
%ifarch aarch64
    --disable-iptables \
%endif
%ifarch ppc64 aarch64
    --disable-virt \
%endif
    --disable-lpar \
    --disable-memcachec \
    --disable-mic \
    --disable-netapp \
%ifarch s390 s390x
    --disable-nut \
%endif
    --disable-onewire \
    --disable-oracle \
    --disable-pf \
    --disable-routeros \
%ifarch ppc sparc sparc64 aarch64
    --disable-sensors \
%endif
    --disable-sigrok \
    --disable-tape \
    --disable-tokyotyrant \
%ifnarch %ix86 x86_64
    --disable-turbostat \
%endif
    --disable-write_kafka \
    --disable-write_mongodb \
    --disable-xencpu \
    --disable-xmms \
    --disable-zone \
    --with-java=%{java_home}/ \
    --with-python \
    --with-perl-bindings=INSTALLDIRS=vendor \
    --disable-werror

make %{?_smp_mflags}


%install
cd %{name}-%{version}
rm -rf contrib/SpamAssassin
make install DESTDIR="%{buildroot}"

install -Dp -m0644 src/collectd.conf %{buildroot}%{_sysconfdir}/collectd.conf
install -Dp -m0644 %{SOURCE2} %{buildroot}%{_unitdir}/collectd.service
install -d -m0755 %{buildroot}%{_localstatedir}/lib/collectd/rrd
install -d -m0755 %{buildroot}%{_datadir}/collectd/collection3/
install -d -m0755 %{buildroot}%{_sysconfdir}/httpd/conf.d/

find contrib/ -type f -exec chmod a-x {} \;

# Remove Perl hidden .packlist files.
find %{buildroot} -name .packlist -delete
# Remove Perl temporary file perllocal.pod
find %{buildroot} -name perllocal.pod -delete

# copy web interface
cp -ad contrib/collection3/* %{buildroot}%{_datadir}/collectd/collection3/
cp -pv %{buildroot}%{_datadir}/collectd/collection3/etc/collection.conf %{buildroot}%{_sysconfdir}/collection.conf
ln -rsf %{_sysconfdir}/collection.conf %{buildroot}%{_datadir}/collectd/collection3/etc/collection.conf
cp -pv %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/collectd.conf
chmod +x %{buildroot}%{_datadir}/collectd/collection3/bin/*.cgi

# Move the Perl examples to a separate directory.
#mkdir perl-examples
#find contrib -name '*.p[lm]' -exec mv {} perl-examples/ \;

# Move config contribs
mkdir -p %{buildroot}%{_sysconfdir}/collectd.d/
cp %{SOURCE91} %{buildroot}%{_sysconfdir}/collectd.d/apache.conf
cp %{SOURCE93} %{buildroot}%{_sysconfdir}/collectd.d/mysql.conf
cp %{SOURCE94} %{buildroot}%{_sysconfdir}/collectd.d/nginx.conf
cp %{SOURCE92} %{buildroot}%{_sysconfdir}/collectd.d/email.conf
cp %{SOURCE95} %{buildroot}%{_sysconfdir}/collectd.d/sensors.conf
cp %{SOURCE96} %{buildroot}%{_sysconfdir}/collectd.d/snmp.conf
cp %{SOURCE97} %{buildroot}%{_sysconfdir}/collectd.d/rrdtool.conf

# configs for subpackaged plugins
%ifnarch s390 s390x
for p in dns ipmi libvirt nut perl ping postgresql
%else
for p in dns ipmi libvirt perl ping postgresql
%endif
do
cat > %{buildroot}%{_sysconfdir}/collectd.d/$p.conf <<EOF
LoadPlugin $p
EOF
done

# *.la files shouldn't be distributed.
rm -f %{buildroot}/%{_libdir}/{collectd/,}*.la


%check
cd %{name}-%{version}
make check

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}



%post
/sbin/ldconfig
%systemd_post collectd.service


%preun
%systemd_preun collectd.service


%postun
/sbin/ldconfig
%systemd_postun_with_restart collectd.service


%files
%config(noreplace) %{_sysconfdir}/collectd.conf
%config(noreplace) %{_sysconfdir}/collectd.d/
%exclude %{_sysconfdir}/collectd.d/apache.conf
%exclude %{_sysconfdir}/collectd.d/dns.conf
%exclude %{_sysconfdir}/collectd.d/email.conf
%exclude %{_sysconfdir}/collectd.d/ipmi.conf
%exclude %{_sysconfdir}/collectd.d/libvirt.conf
%exclude %{_sysconfdir}/collectd.d/mysql.conf
%exclude %{_sysconfdir}/collectd.d/nginx.conf
%ifnarch s390 s390x
%exclude %{_sysconfdir}/collectd.d/nut.conf
%endif
%exclude %{_sysconfdir}/collectd.d/perl.conf
%exclude %{_sysconfdir}/collectd.d/ping.conf
%exclude %{_sysconfdir}/collectd.d/postgresql.conf
%exclude %{_datadir}/collectd/postgresql_default.conf
%exclude %{_sysconfdir}/collectd.d/rrdtool.conf
%exclude %{_sysconfdir}/collectd.d/sensors.conf
%exclude %{_sysconfdir}/collectd.d/snmp.conf

%{_unitdir}/collectd.service
%{_bindir}/collectd-nagios
%{_bindir}/collectdctl
%{_bindir}/collectd-tg
%{_sbindir}/collectd
%{_sbindir}/collectdmon
%dir %{_localstatedir}/lib/collectd/

%dir %{_libdir}/collectd

%{_libdir}/collectd/aggregation.so
%{_libdir}/collectd/apcups.so
%{_libdir}/collectd/battery.so
%{_libdir}/collectd/cgroups.so
%{_libdir}/collectd/conntrack.so
%{_libdir}/collectd/contextswitch.so
%{_libdir}/collectd/cpu.so
%{_libdir}/collectd/cpufreq.so
%{_libdir}/collectd/cpusleep.so
%{_libdir}/collectd/csv.so
%{_libdir}/collectd/df.so
%{_libdir}/collectd/disk.so
%{_libdir}/collectd/entropy.so
%{_libdir}/collectd/ethstat.so
%{_libdir}/collectd/exec.so
%{_libdir}/collectd/fhcount.so
%{_libdir}/collectd/filecount.so
%{_libdir}/collectd/fscache.so
%{_libdir}/collectd/hddtemp.so
%{_libdir}/collectd/interface.so
%{_libdir}/collectd/ipc.so
%{_libdir}/collectd/irq.so
%{_libdir}/collectd/load.so
%{_libdir}/collectd/log_logstash.so
%{_libdir}/collectd/logfile.so
%{_libdir}/collectd/madwifi.so
%{_libdir}/collectd/match_empty_counter.so
%{_libdir}/collectd/match_hashed.so
%{_libdir}/collectd/match_regex.so
%{_libdir}/collectd/match_timediff.so
%{_libdir}/collectd/match_value.so
%{_libdir}/collectd/mbmon.so
%{_libdir}/collectd/md.so
%{_libdir}/collectd/memcached.so
%{_libdir}/collectd/memory.so
%{_libdir}/collectd/multimeter.so
%{_libdir}/collectd/network.so
%{_libdir}/collectd/nfs.so
%{_libdir}/collectd/notify_nagios.so
%{_libdir}/collectd/ntpd.so
%{_libdir}/collectd/numa.so
%{_libdir}/collectd/olsrd.so
%{_libdir}/collectd/openvpn.so
%{_libdir}/collectd/powerdns.so
%{_libdir}/collectd/processes.so
%{_libdir}/collectd/protocols.so
%{_libdir}/collectd/python.so
%{_libdir}/collectd/serial.so
%{_libdir}/collectd/statsd.so
%{_libdir}/collectd/swap.so
%{_libdir}/collectd/syslog.so
%{_libdir}/collectd/table.so
%{_libdir}/collectd/tail.so
%{_libdir}/collectd/tail_csv.so
%{_libdir}/collectd/target_notification.so
%{_libdir}/collectd/target_replace.so
%{_libdir}/collectd/target_scale.so
%{_libdir}/collectd/target_set.so
%{_libdir}/collectd/target_v5upgrade.so
%{_libdir}/collectd/tcpconns.so
%{_libdir}/collectd/teamspeak2.so
%{_libdir}/collectd/ted.so
%{_libdir}/collectd/thermal.so
%{_libdir}/collectd/threshold.so
%{_libdir}/collectd/unixsock.so
%{_libdir}/collectd/uptime.so
%{_libdir}/collectd/users.so
%{_libdir}/collectd/uuid.so
%{_libdir}/collectd/vmem.so
%{_libdir}/collectd/vserver.so
%{_libdir}/collectd/wireless.so
%{_libdir}/collectd/write_graphite.so
%{_libdir}/collectd/write_http.so
%{_libdir}/collectd/write_log.so
%{_libdir}/collectd/zfs_arc.so

%{_datadir}/collectd/types.db

# collectdclient - TBD reintroduce -devel subpackage?
%{_libdir}/libcollectdclient.so
%{_libdir}/libcollectdclient.so.1
%{_libdir}/libcollectdclient.so.1.*
%{_libdir}/pkgconfig/libcollectdclient.pc
%{_includedir}/collectd/client.h
%{_includedir}/collectd/lcc_features.h
%{_includedir}/collectd/network.h
%{_includedir}/collectd/network_buffer.h

%doc %{_prefix}/share/man/man1/collectd.1*
%doc %{_prefix}/share/man/man1/collectdctl.1*
%doc %{_prefix}/share/man/man1/collectd-nagios.1*
%doc %{_prefix}/share/man/man1/collectd-tg.1*
%doc %{_prefix}/share/man/man1/collectdmon.1*
%doc %{_prefix}/share/man/man5/collectd.conf.5*
%doc %{_prefix}/share/man/man5/collectd-exec.5*
%doc %{_prefix}/share/man/man5/collectd-python.5*
%doc %{_prefix}/share/man/man5/collectd-threshold.5*
%doc %{_prefix}/share/man/man5/collectd-unixsock.5*
%doc %{_prefix}/share/man/man5/types.db.5*

%files amqp
%{_libdir}/collectd/amqp.so


%files apache
%{_libdir}/collectd/apache.so
%config(noreplace) %{_sysconfdir}/collectd.d/apache.conf


%files ascent
%{_libdir}/collectd/ascent.so


%files bind
%{_libdir}/collectd/bind.so


%files ceph
%{_libdir}/collectd/ceph.so


%files chrony
%{_libdir}/collectd/chrony.so


%files curl
%{_libdir}/collectd/curl.so


%files curl_json
%{_libdir}/collectd/curl_json.so


%files curl_xml
%{_libdir}/collectd/curl_xml.so


%files dbi
%{_libdir}/collectd/dbi.so


%files dns
%{_libdir}/collectd/dns.so
%config(noreplace) %{_sysconfdir}/collectd.d/dns.conf


%files drbd
%{_libdir}/collectd/drbd.so


%files email
%{_libdir}/collectd/email.so
%config(noreplace) %{_sysconfdir}/collectd.d/email.conf
%doc %{_prefix}/share/man/man5/collectd-email.5*


%files generic-jmx
%{_datadir}/collectd/java/generic-jmx.jar


%files gmond
%{_libdir}/collectd/gmond.so


%files gps
%{_libdir}/collectd/gps.so

%files hugepages
%{_libdir}/collectd/hugepages.so

%files ipmi
%{_libdir}/collectd/ipmi.so
%config(noreplace) %{_sysconfdir}/collectd.d/ipmi.conf


%ifnarch aarch64
%files iptables
%{_libdir}/collectd/iptables.so
%endif


%files ipvs
%{_libdir}/collectd/ipvs.so


%files java
%{_libdir}/collectd/java.so
%dir %{_datadir}/collectd/java/
%{_datadir}/collectd/java/collectd-api.jar
%doc %{_prefix}/share/man/man5/collectd-java.5*


%files lua
%{_prefix}/share/man/man5/collectd-lua*
%{_libdir}/collectd/lua.so


%files lvm
%{_libdir}/collectd/lvm.so


%files modbus
%{_libdir}/collectd/modbus.so


%files mqtt
%{_libdir}/collectd/mqtt.so


%files mysql
%{_libdir}/collectd/mysql.so
%config(noreplace) %{_sysconfdir}/collectd.d/mysql.conf


%files netlink
%{_libdir}/collectd/netlink.so


%files nginx
%{_libdir}/collectd/nginx.so
%config(noreplace) %{_sysconfdir}/collectd.d/nginx.conf


%files notify_desktop
%{_libdir}/collectd/notify_desktop.so


%files notify_email
%{_libdir}/collectd/notify_email.so


%ifnarch s390 s390x
%files nut
%{_libdir}/collectd/nut.so
%config(noreplace) %{_sysconfdir}/collectd.d/nut.conf
%endif


%files openldap
%{_libdir}/collectd/openldap.so


%files -n perl-Collectd
#%doc perl-examples/*
%{_libdir}/collectd/perl.so
%{perl_vendorlib}/Collectd.pm
%{perl_vendorlib}/Collectd/
%config(noreplace) %{_sysconfdir}/collectd.d/perl.conf
%doc %{_prefix}/share/man/man5/collectd-perl.5*
%doc /usr/share/man/man3/Collectd::Unixsock.3pm.gz
%doc /usr/share/perl5/vendor_perl/Collectd/Unixsock.pm

%files pinba
%{_libdir}/collectd/pinba.so


%files ping
%{_libdir}/collectd/ping.so
%config(noreplace) %{_sysconfdir}/collectd.d/ping.conf


%files postgresql
%{_libdir}/collectd/postgresql.so
%config(noreplace) %{_sysconfdir}/collectd.d/postgresql.conf
%{_datadir}/collectd/postgresql_default.conf


%files redis
%{_libdir}/collectd/redis.so


%files rrdcached
%{_libdir}/collectd/rrdcached.so


%files rrdtool
%{_libdir}/collectd/rrdtool.so
%config(noreplace) %{_sysconfdir}/collectd.d/rrdtool.conf


%ifnarch ppc sparc sparc64 aarch64
%files sensors
%{_libdir}/collectd/sensors.so
%config(noreplace) %{_sysconfdir}/collectd.d/sensors.conf
%endif


%files smart
%{_libdir}/collectd/smart.so


%files snmp
%{_libdir}/collectd/snmp.so
%config(noreplace) %{_sysconfdir}/collectd.d/snmp.conf
%doc %{_prefix}/share/man/man5/collectd-snmp.5*


%ifarch %ix86 x86_64
%files turbostat
%{_libdir}/collectd/turbostat.so
%endif


%files varnish
%{_libdir}/collectd/varnish.so


%ifnarch ppc ppc64 sparc sparc64 aarch64
%files virt
%{_libdir}/collectd/virt.so
%config(noreplace) %{_sysconfdir}/collectd.d/libvirt.conf
%endif


%files web
%{_datadir}/collectd/collection3/
%config(noreplace) %{_sysconfdir}/httpd/conf.d/collectd.conf
%config(noreplace) %{_sysconfdir}/collection.conf

%files write_prometheus
%{_libdir}/collectd/write_prometheus.so


%files write_redis
%{_libdir}/collectd/write_redis.so


%files write_riemann
%{_libdir}/collectd/write_riemann.so


%files write_sensu
%{_libdir}/collectd/write_sensu.so


%files write_tsdb
%{_libdir}/collectd/write_tsdb.so


%files zookeeper
%{_libdir}/collectd/zookeeper.so

   /opt/collectd-d5.6.3/include/collectd/network_parse.h
   /opt/collectd-d5.6.3/include/collectd/server.h
   /opt/collectd-d5.6.3/include/collectd/types.h
   /opt/collectd-d5.6.3/lib64/collectd/mcelog.so
   /opt/collectd-d5.6.3/lib64/collectd/ovs_events.so
   /opt/collectd-d5.6.3/lib64/collectd/ovs_stats.so
   /opt/collectd-d5.6.3/lib64/collectd/snmp_agent.so
   /opt/collectd-d5.6.3/lib64/collectd/synproxy.so


%changelog
