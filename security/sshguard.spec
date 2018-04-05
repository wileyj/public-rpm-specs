# iptables -A INPUT -j sshguard
# iptables -N sshguard
# iptables -A INPUT -p tcp --dport 22 -j ACCEPT
# iptables -P INPUT DROP
# /etc/init.d/iptables save 
# /etc/init.d/iptables restart 

%global with_alinux 1
%define repo https://bitbucket.org/sshguard/sshguard
#%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">db'`)
%define gitversion 2.1.0
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1

Name: sshguard
Summary: sshguard
Version: %{gitversion}
Release: %{rel_version}%{dist}
License: MIT
URL: http://zsh.sourceforge.net/
Group: System Environment/Shells
BuildRequires: autoconf automake gcc libtool
Source1: %{name}.init
Source2: %{name}.conf
Source3: %{name}.service

%description
sshguard protects hosts from brute-force attacks against SSH and other services. It aggregates system logs and blocks repeat offenders using one of several firewall backends, including iptables, ipfw, and pf.
sshguard can read log messages from standard input (suitable for piping from syslog) or monitor one or more log files. Log messages are parsed, line-by-line, for recognized patterns. If an attack, such as several login failures within a few seconds, is detected, the offending IP is blocked. Offenders are unblocked after a set interval, but can be semi-permanently banned using the blacklist option.

%package -n %{name}-docs
Summary: sshguard
License: MIT
URL: http://zsh.sourceforge.net/
Group: System Environment/Shells
BuildRequires: autoconf automake gcc libtool

%description -n %{name}-docs
** %{name} manpages
%{description}

%if 0%{?with_alinux}
%package -n %{name}-alinux
Summary: sshguard
License: MIT
URL: http://zsh.sourceforge.net/
Group: System Environment/Shells
BuildRequires: autoconf automake gcc libtool

%description -n %{name}-alinux
** Amazon Linux %{name}
%{description}

%package -n %{name}-alinux-docs
Summary: sshguard
License: MIT
URL: http://zsh.sourceforge.net/
Group: System Environment/Shells
BuildRequires: autoconf automake gcc libtool

%description -n %{name}-alinux-docs
** %{name} manpages
%{description}

%endif

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
%{__install} -Dp -m0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}.conf
%{__mkdir_p} %{buildroot}%{_unitdir}
%{__install} -p -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service

%if 0%{?with_alinux}
%__mkdir_p %{buildroot}%{_initrddir}
%{__install} -Dp -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
%endif

%preun 
if [ $1 = 0 ] ; then
    if [ -x %{_unitdir}/%{name}.service ]; then
        service %{name} stop > /dev/null
    fi  
    /sbin/chkconfig --del %{name}
fi

%preun -n %{name}-alinux
if [ $1 = 0 ] ; then
    if [ -x %{_initrddir}/%{name}-client ] ; then
        %{_initrddir}/%{name}-client stop > /dev/null
    fi
    /sbin/chkconfig --del %{name}
fi

%post 
touch /etc/whitelist
mkdir /var/lib/sshguard/
/sbin/chkconfig --add %{name}

%post -n %{name}-alinux
touch /etc/whitelist
mkdir /var/lib/sshguard/
/sbin/chkconfig --add %{name}


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}


%files
%attr(755,root,root) %{_sbindir}/%{name}
%attr(755,root,root) %{_libexecdir}/sshg*
%attr(755,root,root) %{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_unitdir}/%{name}.service

%files -n %{name}-docs
%{_mandir}/man8/%{name}*
%{_mandir}/man7/%{name}*


%if 0%{?with_alinux}
%files -n %{name}-alinux
%attr(755,root,root) %{_sbindir}/%{name}
%attr(755,root,root) %{_libexecdir}/sshg*
%attr(755,root,root) %{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.conf

%files -n %{name}-alinux-docs
%{_mandir}/man8/%{name}*
%{_mandir}/man7/%{name}*
%endif
