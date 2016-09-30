%define repo https://bitbucket.org/sshguard/sshguard
#%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">db'`)
%define gitversion 1.5.0
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1

Name: sshguard
Summary: sshguard
Version: %{gitversion}
Release: %{rel_version}.%{revision}.%{dist}
License: MIT
URL: http://zsh.sourceforge.net/
Group: System Environment/Shells
BuildRequires: autoconf automake gcc libtool

%description
sshguard protects hosts from brute-force attacks against SSH and other services. It aggregates system logs and blocks repeat offenders using one of several firewall backends, including iptables, ipfw, and pf.
sshguard can read log messages from standard input (suitable for piping from syslog) or monitor one or more log files. Log messages are parsed, line-by-line, for recognized patterns. If an attack, such as several login failures within a few seconds, is detected, the offending IP is blocked. Offenders are unblocked after a set interval, but can be semi-permanently banned using the blacklist option.


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
libtoolize --force
aclocal
autoheader
automake --force-missing --add-missing
autoconf
%configure --with-firewall=iptables --prefix=$RPM_BUILD_ROOT 

%install
cd %{name}-%{version}
rm -rf $RPM_BUILD_ROOT
make DESTDIR=%{buildroot} INSTALL='install -p' install

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%attr(755,root,root) %{_sbindir}/%{name}
%attr(755,root,root) %{_libexecdir}/sshg-blocker
%attr(755,root,root) %{_libexecdir}/sshg-fw
%attr(755,root,root) %{_libexecdir}/sshg-logtail
%attr(755,root,root) %{_libexecdir}/sshg-parser
%{_mandir}/man8/%{name}.8.*


