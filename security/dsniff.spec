%define prefix /opt/%{name}

Summary:	Tools for network auditing and penetration testing
Name:		dsniff
Version:	2.4
Release:	1.%{?dist}
License:	BSD
Group:		Applications/Internet
URL:		http://www.monkey.org/~dugsong/%{name}/
Source:		http://www.monkey.org/~dugsong/%{name}/beta/%{name}-%{version}b1.tar.gz
Patch0:		dsniff-2.4-time_h.patch
Patch1:		dsniff-2.4-mailsnarf_corrupt.patch
Patch2:		dsniff-2.4-pcap_read_dump.patch
Patch3:		dsniff-2.4-multiple_intf.patch
Patch4:		dsniff-2.4-amd64_fix.patch
Patch5:		dsniff-2.4-urlsnarf_zeropad.patch
Patch6:		dsniff-2.4-libnet_11.patch
Patch7:		dsniff-2.4-checksum.patch
Patch8:		dsniff-2.4-openssl_098.patch
Patch9:		dsniff-2.4-sshcrypto.patch
Patch10:	dsniff-2.4-sysconf_clocks.patch
Patch11:	dsniff-2.4-urlsnarf_escape.patch
Patch12:	dsniff-2.4-string_header.patch
Patch13:	dsniff-2.4-arpa_inet_header.patch
Patch14:	dsniff-2.4-pop_with_version.patch
Patch15:	dsniff-2.4-obsolete_time.patch
Patch16:	dsniff-2.4-checksum_libnids.patch
Patch17:	dsniff-2.4-fedora_dirs.patch
Patch18:	dsniff-2.4-glib2.patch
Patch19:	dsniff-2.4-link_layer_offset.patch
Patch20:	dsniff-2.4-tds_decoder.patch
Patch21:	dsniff-2.4-msgsnarf_segfault.patch
Patch22:	dsniff-2.4-urlsnarf_timestamp.patch
Patch23:	dsniff-2.4-arpspoof_reverse.patch
Patch24:	dsniff-2.4-arpspoof_multiple.patch
Patch25:	dsniff-2.4-arpspoof_hwaddr.patch
Patch26:	dsniff-2.4-modernize_pop.patch
Patch27:	dsniff-2.4-libnet_name2addr4.patch
Patch28:	dsniff-2.4-pntohl_shift.patch
Patch29:	dsniff-2.4-rpc_segfault.patch
BuildRequires:	libnet-devel, openssl-devel, libnids-devel, glib2-devel, %{_includedir}/pcap.h
BuildRequires:	db4-devel
BuildRequires:	libXmu-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
A collection of tools for network auditing and penetration testing. Dsniff,
filesnarf, mailsnarf, msgsnarf, urlsnarf and webspy allow to passively monitor
a network for interesting data (passwords, e-mail, files). Arpspoof, dnsspoof
and macof facilitate the interception of network traffic normally unavailable
to an attacker (e.g, due to layer-2 switching). Sshmitm and webmitm implement
active monkey-in-the-middle attacks against redirected SSH and HTTPS sessions
by exploiting weak bindings in ad-hoc PKI.

%prep
%setup -q
%patch0 -p1 -b .time_h
%patch1 -p1 -b .mailsnarf
%patch2 -p1 -b .pcap_dump
%patch3 -p1 -b .multiple_intf
%patch4 -p1 -b .amd64_fix
%patch5 -p1 -b .urlsnarf_zeropad
%patch6 -p1 -b .libnet_11
%patch7 -p1 -b .checksum
%patch8 -p1 -b .openssl_098
%patch9 -p1 -b .sshcrypto
%patch10 -p1 -b .sysconf_clocks
%patch11 -p1 -b .urlsnarf_escape
%patch12 -p1 -b .string_header
%patch13 -p1 -b .arpa_inet_header
%patch14 -p1 -b .pop_with_version
%patch15 -p1 -b .obsolete_time
%patch16 -p1 -b .checksum_libnids
%patch17 -p1 -b .fedora_dirs
%patch18 -p1 -b .glib2
%patch19 -p1 -b .link_layer_offset
%patch20 -p1 -b .tds_decoder
%patch21 -p1 -b .msgsnarf_segfault
%patch22 -p1 -b .urlsnarf_timestamp
%patch23 -p1 -b .arpspoof_reverse
%patch24 -p1 -b .arpspoof_multiple
%patch25 -p1 -b .arpspoof_hwaddr
%patch26 -p1 -b .modernize_pop
%patch27 -p1 -b .libnet_name2addr4
%patch28 -p1 -b .pntohl_shift
%patch29 -p1 -b .rpc_segfault

%build
%configure --sbindir=%{prefix}/sbin --sysconfdir=%{prefix}/etc

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%__mkdir_p %{buildroot}%{prefix}
%__mkdir_p %{buildroot}%{prefix}/etc
%__mkdir_p %{buildroot}%{prefix}/sbin
%__mkdir_p %{buildroot}%{_sbindir}

make install_prefix=$RPM_BUILD_ROOT INSTALL='install -p' install

ln -sf %{prefix}/sbin/arpspoof %{buildroot}%{_sbindir}/arpspoof
ln -sf %{prefix}/sbin/dnsspoof %{buildroot}%{_sbindir}/dnsspoof
ln -sf %{prefix}/sbin/%{name} %{buildroot}%{_sbindir}/%{name}
ln -sf %{prefix}/sbin/filesnarf %{buildroot}%{_sbindir}/filesnarf
ln -sf %{prefix}/sbin/macof %{buildroot}%{_sbindir}/macof
ln -sf %{prefix}/sbin/mailsnarf %{buildroot}%{_sbindir}/mailsnarf
ln -sf %{prefix}/sbin/msgsnarf %{buildroot}%{_sbindir}/msgsnarf
ln -sf %{prefix}/sbin/sshmitm %{buildroot}%{_sbindir}/sshmitm
ln -sf %{prefix}/sbin/sshow %{buildroot}%{_sbindir}/sshow
ln -sf %{prefix}/sbin/tcpkill %{buildroot}%{_sbindir}/tcpkill
ln -sf %{prefix}/sbin/tcpnice %{buildroot}%{_sbindir}/tcpnice
ln -sf %{prefix}/sbin/urlsnarf %{buildroot}%{_sbindir}/urlsnarf
ln -sf %{prefix}/sbin/webmitm %{buildroot}%{_sbindir}/webmitm
ln -sf %{prefix}/sbin/webspy %{buildroot}%{_sbindir}/webspy

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE README TODO
%dir %{prefix}
%dir %{prefix}%{_sysconfdir}
%dir %{prefix}/sbin
%config(noreplace) %{prefix}%{_sysconfdir}/*
%{prefix}/sbin/arpspoof
%{prefix}/sbin/dnsspoof
%{prefix}/sbin/%{name}
%{prefix}/sbin/filesnarf
%{prefix}/sbin/macof
%{prefix}/sbin/mailsnarf
%{prefix}/sbin/msgsnarf
%{prefix}/sbin/sshmitm
%{prefix}/sbin/sshow
%{prefix}/sbin/tcpkill
%{prefix}/sbin/tcpnice
%{prefix}/sbin/urlsnarf
%{prefix}/sbin/webmitm
%{prefix}/sbin/webspy

%{_sbindir}/arpspoof
%{_sbindir}/dnsspoof
%{_sbindir}/%{name}
%{_sbindir}/filesnarf
%{_sbindir}/macof
%{_sbindir}/mailsnarf
%{_sbindir}/msgsnarf
%{_sbindir}/sshmitm
%{_sbindir}/sshow
%{_sbindir}/tcpkill
%{_sbindir}/tcpnice
%{_sbindir}/urlsnarf
%{_sbindir}/webmitm
%{_sbindir}/webspy

%{_mandir}/man8/arpspoof.8*
%{_mandir}/man8/dnsspoof.8*
%{_mandir}/man8/%{name}.8*
%{_mandir}/man8/filesnarf.8*
%{_mandir}/man8/macof.8*
%{_mandir}/man8/mailsnarf.8*
%{_mandir}/man8/msgsnarf.8*
%{_mandir}/man8/sshmitm.8*
%{_mandir}/man8/sshow.8*
%{_mandir}/man8/tcpkill.8*
%{_mandir}/man8/tcpnice.8*
%{_mandir}/man8/urlsnarf.8*
%{_mandir}/man8/webmitm.8*
%{_mandir}/man8/webspy.8*

%changelog
