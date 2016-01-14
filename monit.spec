%define logmsg logger -t %{name}/rpm
Summary: Process monitor and restart utility
Name: monit
Version: 5.10
Release: 1.%{?dist}
License: GPLv3
Group: Applications/Internet
URL: http://mmonit.com/monit/

Source0: %{name}.tar.gz
Patch0: gitmodules.patch 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: binutils
BuildRequires: byacc
BuildRequires: flex
BuildRequires: gcc
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: perl
BuildRequires: /usr/bin/logger
BuildRequires: pam-devel

%description
Monit is an utility for monitoring daemons or similar programs running on
a Unix system. It will start specified programs if they are not running
and restart programs not responding.

%prep
%setup -q -n %{name}
%patch0 -p0
%{__perl} -pi.orig -e 's|\bmonitrc\b|monit.conf|' src/monit.h
%{__perl} -pi.orig -e 's|^#\s+(include .*)$|$1|' monitrc

# store id and state files in /var/monit
%{__perl} -pi.orig -e 's|^#(\s+)set (id\|state)file /var/\.monit\.(id\|state)$|set $2file /var/monit/$3|' monitrc

# fix config path in /etc/init.d/monit
%{__perl} -pi.orig -e 's|monitrc|monit.conf|' system/startup/rc.monit

%build
#ssh -o "StrictHostKeyChecking no" -o PasswordAuthentication=no bitbucket.org 2>&1 > /dev/null
#ssh-keyscan bitbucket.org >> ~/.ssh/known_hosts
git pull
%__rm -rf libmonit
git submodule init
git submodule update
./bootstrap

%configure \
	--with-ssl-lib-dir="%{_libdir}"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall \
	BINDIR="%{buildroot}%{_bindir}" \
	MANDIR="%{buildroot}%{_mandir}/man1/"

%{__install} -Dp -m0755 system/startup/rc.monit %{buildroot}%{_initrddir}/monit
%{__install} -Dp -m0600 monitrc %{buildroot}%{_sysconfdir}/monit.conf

%{__install} -d -m0755 %{buildroot}%{_sysconfdir}/monit.d/
%{__install} -d -m0755 %{buildroot}%{_localstatedir}/lib/monit/

# create folder where state and id are stored
%{__install} -d -m0755 %{buildroot}%{_localstatedir}/monit/

%pre
if ! /usr/bin/id monit &>/dev/null; then
	/usr/sbin/useradd -M -r -d %{_localstatedir}/lib/monit -s /bin/sh -c "monit daemon" monit || \
		%logmsg "Unexpected error adding user \"monit\". Aborting installation."
fi

%post
/sbin/chkconfig --add monit

# Moving old style configuration file to conf standard location
if [ -f %{_sysconfdir}/monitrc ]; then
    mv -f %{_sysconfdir}/monitrc %{_sysconfdir}/monit.conf
fi

%preun
if [ $1 -eq 0 ]; then
	service monit stop &>/dev/null || :
	/sbin/chkconfig --del monit
fi

%postun
/sbin/service monit condrestart &>/dev/null || :
if [ $1 -eq 0 ]; then
	/usr/sbin/userdel monit || %logmsg "User \"monit\" could not be deleted."
fi

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc CHANGES COPYING README*
%doc %{_mandir}/man?/*
%{_initrddir}/monit
%config %{_sysconfdir}/monit.d/
%config %{_localstatedir}/monit/
%{_localstatedir}/lib/monit/
%attr(0755, root, root) %{_bindir}/monit
%attr(0600, root, root) %config(noreplace) %{_sysconfdir}/monit.conf

%changelog
