%define repo https://github.com/xelerance/xl2tpd
%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |sed 's/TOMCAT.//' | tr '_' '.' |  tr -d '\\-</span class="tag-name">vr'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1

Summary: Layer 2 Tunnelling Protocol Daemon (RFC 2661)
Name: xl2tpd
Version: %{gitversion}
Release: %{rel_version}.%{revision}.%{?dist}
License: GPLv2
Url: http://www.xelerance.com/software/xl2tpd/
Group: System Environment/Daemons
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ppp 
BuildRequires: kernel-headers => 2.6.23
%if 0%{?el3}%{?el4}
BuildRequires: libpcap
%else
BuildRequires: libpcap-devel
%endif
Obsoletes: l2tpd <= 0.69-0.6.20051030.fc6
Provides: l2tpd = 0.69-0.6.20051030.fc7
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
 
%description
xl2tpd is an implementation of the Layer 2 Tunnelling Protocol (RFC 2661).
L2TP allows you to tunnel PPP over UDP. Some ISPs use L2TP to tunnel user
sessions from dial-in servers (modem banks, ADSL DSLAMs) to back-end PPP
servers. Another important application is Virtual Private Networks where
the IPsec protocol is used to secure the L2TP connection (L2TP/IPsec,
RFC 3193). The L2TP/IPsec protocol is mainly used by Windows and
Mac OS X clients. On Linux, xl2tpd can be used in combination with IPsec
implementations such as Openswan.
Example configuration files for such a setup are included in this RPM.

xl2tpd works by opening a pseudo-tty for communicating with pppd.
It runs completely in userspace but supports kernel mode L2TP.

xl2tpd supports IPsec SA Reference tracking to enable overlapping internak
NAT'ed IP's by different clients (eg all clients connecting from their
linksys internal IP 192.168.1.101) as well as multiple clients behind
the same NAT router.

xl2tpd supports the pppol2tp kernel mode operations on 2.6.23 or higher,
or via a patch in contrib for 2.4.x kernels.

Xl2tpd is based on the 0.69 L2TP by Jeff McAdams <jeffm@iglou.com>
It was de-facto maintained by Jacco de Leeuw <jacco2@dds.nl> in 2002 and 2003.


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
# Customer test case proved the first make line failed, the second one worked
# the failing one had incoming l2tp packets, but never got a tunnel up.
#make DFLAGS="$RPM_OPT_FLAGS -g -DDEBUG_PPPD -DDEBUG_CONTROL -DDEBUG_ENTROPY"
make DFLAGS="-g -DDEBUG_HELLO -DDEBUG_CLOSE -DDEBUG_FLOW -DDEBUG_PAYLOAD -DDEBUG_CONTROL -DDEBUG_CONTROL_XMIT -DDEBUG_FLOW_MORE -DDEBUG_MAGIC -DDEBUG_ENTROPY -DDEBUG_HIDDEN -DDEBUG_PPPD -DDEBUG_AAA -DDEBUG_FILE -DDEBUG_FLOW -DDEBUG_HELLO -DDEBUG_CLOSE -DDEBUG_ZLB -DDEBUG_AUTH"

%install
cd %{name}-%{version}
rm -rf %{buildroot}
make DESTDIR=%{buildroot} PREFIX=%{_prefix} install
install -p -D -m644 examples/xl2tpd.conf %{buildroot}%{_sysconfdir}/xl2tpd/xl2tpd.conf
install -p -D -m644 examples/ppp-options.xl2tpd %{buildroot}%{_sysconfdir}/ppp/options.xl2tpd
install -p -D -m600 doc/l2tp-secrets.sample %{buildroot}%{_sysconfdir}/xl2tpd/l2tp-secrets
install -p -D -m600 examples/chapsecrets.sample %{buildroot}%{_sysconfdir}/ppp/chap-secrets.sample
install -p -D -m755 packaging/fedora/xl2tpd.init %{buildroot}%{_initrddir}/xl2tpd
install -p -D -m755 -d %{buildroot}%{_localstatedir}/run/xl2tpd


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%post
/sbin/chkconfig --add xl2tpd
# if we migrate from l2tpd to xl2tpd, copy the configs
if [ -f /etc/l2tpd/l2tpd.conf ]; then
  echo "Old /etc/l2tpd configuration found, migrating to /etc/xl2tpd"
  mv /etc/xl2tpd/xl2tpd.conf /etc/xl2tpd/xl2tpd.conf.rpmsave
  cat /etc/l2tpd/l2tpd.conf | sed "s/options.l2tpd/options.xl2tpd/" > /etc/xl2tpd/xl2tpd.conf
  mv /etc/ppp/options.xl2tpd /etc/ppp/options.xl2tpd.rpmsave
  mv /etc/ppp/options.l2tpd /etc/ppp/options.xl2tpd
  mv /etc/xl2tpd/l2tp-secrets /etc/xl2tpd/l2tpd-secrets.rpmsave
  cp -pa /etc/l2tpd/l2tp-secrets /etc/xl2tpd/l2tp-secret
fi

%preun
if [ ( -eq 0 ]; then
  /sbin/service xl2tpd stop > /dev/null 2>&1
  /sbin/chkconfig --del xl2tpd
fi
                                                
%postun
if [ ( -ge 1 ]; then
  /sbin/service xl2tpd condrestart 2>&1 >/dev/null
fi
                                                      
%files
%defattr(-,root,root)
%attr(0755,root,root) %{_sbindir}/xl2tpd
%attr(0755,root,root) %{_sbindir}/xl2tpd-control
%attr(0755,root,root) %{_bindir}/pfc
%{_mandir}/*/*
%dir %{_sysconfdir}/xl2tpd
%config(noreplace) %{_sysconfdir}/xl2tpd/*
%config(noreplace) %{_sysconfdir}/ppp/*
%attr(0755,root,root)  %{_initrddir}/xl2tpd
%dir %{_localstatedir}/run/xl2tpd
%ghost %attr(0600,root,root) %{_localstatedir}/run/xl2tpd/l2tp-control
                                                      
