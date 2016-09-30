%if 0%{?amzn} >= 1
%define python python27
BuildRequires: %{python} %{python}-rpm-macros %{python}-devel
Requires: %{python} %{python}-setuptools
%else
%define python python
BuildRequires: %{python} %{python}-rpm-macros %{python}-devel
Requires: %{python} %{python}-setuptools
%endif

%define pkgname fail2ban

%define repo https://github.com/fail2ban/fail2ban
%define gitversion %(echo `curl -s https://github.com/fail2ban/fail2ban/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">db'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1

Summary: Scan logfiles and ban ip addresses with too many password failures
Name:           %{pkgname}
Version:        %{gitversion}
Release:        %{rel_version}.%{revision}.%{dist}
License: GPL
Group: System Environment/Daemons
URL: http://fail2ban.sourceforge.net/
Packager:       %{packager}
Vendor:         %{vendor}
Group:          System Environment/Base
BuildArch:      noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: dos2unix
#Requires: gamin-python
Requires: iptables
Requires: %{python}-fail2ban
Requires: tcp_wrappers

%description
Fail2Ban monitors log files like /var/log/pwdfail or /var/log/apache/error_log
and bans failure-prone addresses. It updates firewall rules to reject the IP
address or executes user defined commands.

%package -n %{python}-fail2ban
Summary: fail2ban %{python} modules
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}

%description -n %{python}-fail2ban
%{summary}


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
%{__perl} -pi -e 's|^# chkconfig:.+$|# chkconfig: 345 92 08|' files/redhat-initd
%{__perl} -pi -e 's|/tmp/fail2ban.sock|/var/run/fail2ban/fail2ban.sock|g;' files/redhat-initd

%{__cat} <<EOF >fail2ban.logrotate
/var/log/fail2ban.log {
    missingok
    notifempty
    size 30k
    create 0600 root root
    postrotate
        /usr/bin/fail2ban-client reload 2> /dev/null || true
    endscript
}
EOF

#%build
#cd %{name}-%{version}
%{__python} setup.py build

%install
cd %{name}-%{version}
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root="%{buildroot}" --prefix="%{_prefix}"
%{__install} -Dp -m0755 files/redhat-initd %{buildroot}%{_initrddir}/fail2ban
%{__install} -Dp -m0644 fail2ban.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/fail2ban
%{__install} -Dp -m0644 man/fail2ban-client.1 %{buildroot}%{_mandir}/man1/fail2ban-client.1
%{__install} -Dp -m0644 man/fail2ban-regex.1 %{buildroot}%{_mandir}/man1/fail2ban-regex.1
%{__install} -Dp -m0644 man/fail2ban-server.1 %{buildroot}%{_mandir}/man1/fail2ban-server.1
%{__install} -d %{buildroot}%{_var}/run/fail2ban
%{__install} -d %{buildroot}%{_datadir}/fail2ban


%clean
%{__rm} -rf %{buildroot}

%post
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add fail2ban
fi

%preun
if [ $1 -eq 0 ]; then
    /sbin/service fail2ban stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del fail2ban
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service fail2ban condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-, root, root, 0755)
%doc %{_mandir}/man1/fail2ban-client.1*
%doc %{_mandir}/man1/fail2ban-regex.1*
%doc %{_mandir}/man1/fail2ban-server.1*
%config(noreplace) %{_sysconfdir}/fail2ban/
%config(noreplace) %{_sysconfdir}/logrotate.d/fail2ban
%config %{_initrddir}/fail2ban
%{_bindir}/fail2ban-client
%{_bindir}/fail2ban-regex
%{_bindir}/fail2ban-server
%{_datadir}/fail2ban/
%dir %{_var}/run/fail2ban


%files -n %{python}-fail2ban
%dir %{python_sitelib}/%{name}
%{python_sitelib}/%{name}/*
%dir %{python_sitelib}/%{name}-*.egg-info
%{python_sitelib}/%{name}-*.egg-info/*
%{_bindir}/fail2ban-%{python}
%{_bindir}/fail2ban-testcases
%dir %{_datadir}/doc/%{name}
%{_datadir}/doc/%{name}/*

%changelog
