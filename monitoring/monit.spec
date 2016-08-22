%define repo https://bitbucket.org/tildeslash/monit.git
%define logmsg logger -t %{name}/rpm
Summary: Process monitor and restart utility
Name: monit
Version: 5.17
Release: 1.%{?dist}
License: GPLv3
Group: Applications/Internet
URL: http://mmonit.com/monit/

Source0: %{name}.tar.gz
#Patch0: gitmodules.patch 
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

%setup -q -c -T

%prep
if [ -d %{name}-%{version} ];then
     rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update
#%{__perl} -pi.orig -e 's|\bmonitrc\b|monit.conf|' src/monit.h
#%{__perl} -pi.orig -e 's|^#\s+(include .*)$|$1|' monitrc
#%{__perl} -pi.orig -e 's|^#(\s+)set (id\|state)file /var/\.monit\.(id\|state)$|set $2file /var/monit/$3|' monitrc
#%{__perl} -pi.orig -e 's|monitrc|monit.conf|' system/startup/rc.monit

%build
cd %{name}-%{version}
./bootstrap
./configure \
	--enable-shared \
  	--enable-optimized \
  	--bindir=%{buildroot}%{_bindir} \
  	--libdir=%{buildroot}%{_libdir} \
  	--mandir=%{buildroot}%{_mandir} \
	--with-ssl-lib-dir="%{buildroot}%{_libdir}"
make
make install DESTDIR=%{buildroot}

%install
cd %{name}-%{version}
%{__rm} -rf %{buildroot}
#make install
#%makeinstall \
#	BINDIR="%{buildroot}%{_bindir}" \
#	MANDIR="%{buildroot}%{_mandir}/man1/"

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
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-, root, root, 0755)
%doc %{_mandir}/man?/*
%{_initrddir}/monit
%config %{_sysconfdir}/monit.d/
%config %{_localstatedir}/monit/
%{_localstatedir}/lib/monit/
%attr(0755, root, root) %{_bindir}/monit
%attr(0600, root, root) %config(noreplace) %{_sysconfdir}/monit.conf

%changelog
