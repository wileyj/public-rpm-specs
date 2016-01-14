Summary: Host-based tool to scan for rootkits, backdoors and local exploits
Name: rkhunter
Version: 1.4.2
Release: 1.%{dist}
License: GPL
Packager: %{packager}
Vendor: %{vendor}
Group: Applications/System
URL: http://www.rootkit.nl/projects/rootkit_hunter.html

Source: http://downloads.sourceforge.net/project/rkhunter/rkhunter/%{version}/rkhunter-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch: noarch
Requires: /bin/sh
Requires: binutils
Requires: coreutils
Requires: e2fsprogs
Requires: findutils
Requires: grep
Requires: iproute
Requires: lsof
Requires: mailx
Requires: mktemp
Requires: modutils
Requires: net-tools
Requires: perl
Requires: perl(IO::Socket)
Requires: perl(strict)
Requires: prelink
Requires: procps
Requires: wget

%description
Rootkit Hunter scans files and systems for known and unknown rootkits,
backdoors, and sniffers.  The package contains one shell script, a few
text-based databases, and optional Perl modules.  It should run on almost
every Unix clone.  This tool scans for rootkits, backdoors and local
exploits by running tests like: 

    MD5 hash compare,
    Look for default files used by rootkits,
    Wrong file permissions for binaries,
    Look for suspected strings in LKM and KLD modules,
    Look for hidden files,
    Optional scan within plaintext and binary files,
    Software version checks and
    Application tests

%prep
%setup

### FIXME: installer has /usr/local as default prefix for RPM
%{__perl} -pi.orig -e 's|PREFIX="\${RPM_BUILD_ROOT}/usr/local"|PREFIX="\${RPM_BUILD_ROOT}%{_prefix}"|g' installer.sh

%{__cat} <<EOF >rkhunter.logrotate
%{_localstatedir}/log/rkhunter.log {
    weekly
    notifempty
    create 640 root root
}
EOF

%build

%install
%{__rm} -rf %{buildroot}
RPM_BUILD_ROOT="%{buildroot}" ./installer.sh --layout RPM --install

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
%files
%defattr(-, root, root 0755)
%doc files/ACKNOWLEDGMENTS files/CHANGELOG files/FAQ files/LICENSE files/README 
%doc %{_mandir}/man8/rkhunter.8*
%config(noreplace) %{_sysconfdir}/rkhunter.conf
%{_bindir}/rkhunter
%{_libdir}/rkhunter/
%{_localstatedir}/lib/rkhunter/
%exclude %{_docdir}
 
%changelog
