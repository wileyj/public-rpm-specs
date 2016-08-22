%define name psad
%define version 2.4.3
%define release 1
%define psadsbindir /opt/%{name}/sbin
%define psadbindir /opt/%{name}/bin
%define psadsysconfdir /opt/%{name}/etc
%define psadlogdir /var/log/%{name}
%define psadrundir /var/run/%{name}
%define psadvarlibdir /var/lib/%{name}

Summary: psad analyzes iptables log messages for suspect traffic
Name: %name
Version: %version
Release: %release.%{dist}
License: GPL
Vendor: %{vendor}
Packager: %{packager}
Group: Applications/Internet
Url: http://www.cipherdyne.org/psad/
Source: %name-%version.tar.gz
BuildRoot: %_tmppath/%{name}-buildroot
Requires: iptables
#Prereq: rpm-helper

%description
Port Scan Attack Detector (psad) is a collection of three lightweight
system daemons written in Perl and in C that are designed to work with Linux
iptables firewalling code to detect port scans and other suspect traffic.  It
features a set of highly configurable danger thresholds (with sensible
defaults provided), verbose alert messages that include the source,
destination, scanned port range, begin and end times, tcp flags and
corresponding nmap options, reverse DNS info, email and syslog alerting,
automatic blocking of offending ip addresses via dynamic configuration of
iptables rulesets, and passive operating system fingerprinting.  In addition,
psad incorporates many of the tcp, udp, and icmp signatures included in the
snort intrusion detection system (http://www.snort.org) to detect highly
suspect scans for various backdoor programs (e.g. EvilFTP, GirlFriend,
SubSeven), DDoS tools (mstream, shaft), and advanced port scans (syn, fin,
xmas) which are easily leveraged against a machine via nmap.  psad can also
alert on snort signatures that are logged via fwsnort
(http://www.cipherdyne.org/fwsnort/), which makes use of the
iptables string match module to detect application layer signatures.


%prep
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%setup -q

%build
### build psad binaries (kmsgsd and psadwatchd)
make OPTS="$RPM_OPT_FLAGS"

%install
### config directory
#mkdir -p $RPM_BUILD_ROOT%psadetcdir
### log directory
mkdir -p $RPM_BUILD_ROOT%psadlogdir
### dir for psadfifo
mkdir -p $RPM_BUILD_ROOT%psadvarlibdir
### dir for pidfiles
mkdir -p $RPM_BUILD_ROOT%psadrundir

mkdir -p $RPM_BUILD_ROOT%_bindir
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%_sbindir
### psad config
mkdir -p $RPM_BUILD_ROOT%_sysconfdir/%name
### psad init script
mkdir -p $RPM_BUILD_ROOT%_initrddir

### the 700 permissions mode is fixed in the
### %post phase
install -m 700 psad $RPM_BUILD_ROOT%_sbindir/
install -m 700 kmsgsd $RPM_BUILD_ROOT%_sbindir/
install -m 700 psadwatchd $RPM_BUILD_ROOT%_sbindir/
install -m 500 fwcheck_psad.pl $RPM_BUILD_ROOT%_sbindir/fwcheck_psad
install -m 755 nf2csv $RPM_BUILD_ROOT/usr/bin/nf2csv
install -m 755 init-scripts/psad-init.redhat $RPM_BUILD_ROOT%_initrddir/psad
install -m 644 psad.conf $RPM_BUILD_ROOT%_sysconfdir/%name/
install -m 644 signatures $RPM_BUILD_ROOT%_sysconfdir/%name/
install -m 644 protocols $RPM_BUILD_ROOT%_sysconfdir/%name/
install -m 644 icmp_types $RPM_BUILD_ROOT%_sysconfdir/%name/
install -m 644 icmp6_types $RPM_BUILD_ROOT%_sysconfdir/%name/
install -m 644 ip_options $RPM_BUILD_ROOT%_sysconfdir/%name/
install -m 644 auto_dl $RPM_BUILD_ROOT%_sysconfdir/%name/
install -m 644 snort_rule_dl $RPM_BUILD_ROOT%_sysconfdir/%name/
install -m 644 pf.os $RPM_BUILD_ROOT%_sysconfdir/%name/
install -m 644 posf $RPM_BUILD_ROOT%_sysconfdir/%name/
install -m 644 *.8 $RPM_BUILD_ROOT%{_mandir}/man8/
install -m 644 nf2csv.1 $RPM_BUILD_ROOT%{_mandir}/man1/

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%pre
#if [ ! -p /var/lib/psad/psadfifo ];
#then [ -e /var/lib/psad/psadfifo ] && /bin/rm -f /var/lib/psad/psadfifo
#fi
#/bin/mknod -m 600 /var/lib/psad/psadfifo p
#chown root.root /var/lib/psad/psadfifo
#chmod 0600 /var/lib/psad/psadfifo

%post
### put the current hostname into the psad C binaries
### (kmsgsd and psadwatchd).
perl -p -i -e 'use Sys::Hostname; my $hostname = hostname(); s/HOSTNAME(\s+)_?CHANGE.?ME_?/HOSTNAME${1}$hostname/' %_sysconfdir/%name/psad.conf

/bin/touch %psadlogdir/fwdata
chown root.root %psadlogdir/fwdata
chmod 0500 %_sbindir/psad
chmod 0500 %_sbindir/kmsgsd
chmod 0500 %_sbindir/psadwatchd
chmod 0600 %psadlogdir/fwdata
if [ ! -p %psadvarlibdir/psadfifo ];
then [ -e %psadvarlibdir/psadfifo ] && /bin/rm -f %psadvarlibdir/psadfifo
/bin/mknod -m 600 %psadvarlibdir/psadfifo p
fi
chown root.root %psadvarlibdir/psadfifo
chmod 0600 %psadvarlibdir/psadfifo
### make psad start at boot
/sbin/chkconfig --add psad
if grep -q "EMAIL.*root.*localhost" /etc/psad/psad.conf;
then
echo "[+] You can edit the EMAIL_ADDRESSES variable in /etc/psad/psad.conf"
echo "    to have email alerts sent to an address other than root\@localhost"
fi

if grep -q "HOME_NET.*CHANGEME" /etc/psad/psad.conf;
then
echo "[+] Be sure to edit the HOME_NET variable in /etc/psad/psad.conf"
echo "    to define the internal network(s) attached to your machine."
fi

%preun
#%_preun_service psad

%files
%defattr(-,root,root)
%dir %psadlogdir
%dir %psadvarlibdir
%dir %psadrundir
%_initrddir/*
%_sbindir/*
%_bindir/*
%{_mandir}/man8/*
%{_mandir}/man1/*

%dir %_sysconfdir/%name
%config(noreplace) %_sysconfdir/%name/*.conf
%config(noreplace) %_sysconfdir/%name/signatures
%config(noreplace) %_sysconfdir/%name/protocols
%config(noreplace) %_sysconfdir/%name/auto_dl
%config(noreplace) %_sysconfdir/%name/ip_options
%config(noreplace) %_sysconfdir/%name/snort_rule_dl
%config(noreplace) %_sysconfdir/%name/posf
%config(noreplace) %_sysconfdir/%name/pf.os
%config(noreplace) %_sysconfdir/%name/icmp_types
%config(noreplace) %_sysconfdir/%name/icmp6_types
