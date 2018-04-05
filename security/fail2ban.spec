%global _python_bytecompile_errors_terminate_build 0
%global with_python3 1
%define pkgname fail2ban

%define repo https://github.com/fail2ban/%{pkgname}
%define git_summary %(echo `curl %{repo} | grep '<title' | sed 's/<title>//g'`)
%define git_version %(echo `curl -s %{repo}/releases | grep 'class="css-truncate-target"' | head -1 |  tr -d '\\-</span class="css-truncate-target">'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1
%define build_time %(echo `date +%s`)
%define git_release git.%{build_time}.%{revision}.%{?dist}

Summary: %{git_summary}
Name:           %{pkgname}
Version:        %{git_version}
Release:        %{git_release}
License: GPL
Group: System Environment/Daemons
URL: http://fail2ban.sourceforge.net/
Packager:       %{packager}
Vendor:         %{vendor}
Group:          System Environment/Base
BuildArch:      noarch
BuildRequires: dos2unix
Requires: iptables tcp_wrappers
Requires: gamin
Requires: gamin-python
Requires: python-inotify
%if 0%{?with_python3}
Requires: python3-fail2ban
BuildRequires:  python3-devel python2-rpm-macros python-srpm-macros
%endif
Requires: python-fail2ban
BuildRequires:  python-devel python2-rpm-macros python-srpm-macros
Requires: iptables tcp_wrappers
Requires: gamin
Requires: gamin-python3
Requires: python3-inotify

%description
%{git_summary}

%package -n python-fail2ban
Summary: fail2ban python modules
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}

%description -n python-fail2ban
%{summary}

%if 0%{?with_python3}
%package -n python3-fail2ban
Summary: fail2ban python3 modules
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Obsoletes: python-fail2ban

%description -n python3-fail2ban
%{summary}
%endif

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
if [ -d %{buildroot} ];then
    rm -rf %{buildroot}
fi
git clone %{repo} %{name}-%{version}
cd $RPM_BUILD_DIR/%{name}-%{version}
git submodule init
git submodule update
%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif
rm -rf %{py2dir}
cp -a . %{py2dir}

%build
cd $RPM_BUILD_DIR/%{name}-%{version}
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

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

pushd %{py2dir}
%{__python2} setup.py build
popd

%install
cd $RPM_BUILD_DIR/%{name}-%{version}
pushd %{py2dir}
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
%__cp %{buildroot}%{_bindir}/fail2ban-testcases %{buildroot}%{_bindir}/fail2ban-testcases%{python_version}
%__cp %{buildroot}%{_bindir}/fail2ban-client %{buildroot}%{_bindir}/fail2ban-client%{python_version}
%__cp %{buildroot}%{_bindir}/fail2ban-regex  %{buildroot}%{_bindir}/fail2ban-regex%{python_version}
%__cp %{buildroot}%{_bindir}/fail2ban-server %{buildroot}%{_bindir}/fail2ban-server%{python_version}

find %{buildroot}%{_prefix} -type d -depth -exec rmdir {} \; 2>/dev/null
popd

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
%__cp %{buildroot}%{_bindir}/fail2ban-testcases %{buildroot}%{_bindir}/fail2ban-testcases%{python3_version}
%__cp %{buildroot}%{_bindir}/fail2ban-client %{buildroot}%{_bindir}/fail2ban-client%{python3_version}
%__cp %{buildroot}%{_bindir}/fail2ban-regex  %{buildroot}%{_bindir}/fail2ban-regex%{python3_version}
%__cp %{buildroot}%{_bindir}/fail2ban-server %{buildroot}%{_bindir}/fail2ban-server%{python3_version}
find %{buildroot}%{_prefix} -type d -depth -exec rmdir {} \; 2>/dev/null
popd
%endif

%__rm %{buildroot}%{_bindir}/fail2ban-python
%__rm -f %{buildroot}%{_bindir}/fail2ban-testcases
%__rm -f %{buildroot}%{_bindir}/fail2ban-client
%__rm -f %{buildroot}%{_bindir}/fail2ban-regex
%__rm -f %{buildroot}%{_bindir}/fail2ban-server

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

%post -n python-fail2ban
%__ln_s %{_bindir}/fail2ban-testcases%{python_version} %{_bindir}/fail2ban-testcases
%__ln_s %{_bindir}/fail2ban-client%{python_version} %{_bindir}/fail2ban-client
%__ln_s %{_bindir}/fail2ban-regex%{python_version} %{_bindir}/fail2ban-regex
%__ln_s %{_bindir}/fail2ban-server%{python_version} %{_bindir}/fail2ban-server
%__ln_s %__python3 %{_bindir}/fail2ban-python


%postun -n python-fail2ban
%__rm -f %{_bindir}/fail2ban-testcases
%__rm -f %{_bindir}/fail2ban-client
%__rm -f %{_bindir}/fail2ban-regex
%__rm -f %{_bindir}/fail2ban-server
%__rm %{_bindir}/fail2ban-python

%if 0%{?with_python3}
%post -n python3-fail2ban
%__ln_s %{_bindir}/fail2ban-testcases%{python3_version} %{_bindir}/fail2ban-testcases
%__ln_s %{_bindir}/fail2ban-client%{python3_version} %{_bindir}/fail2ban-client
%__ln_s %{_bindir}/fail2ban-regex%{python3_version} %{_bindir}/fail2ban-regex
%__ln_s %{_bindir}/fail2ban-server%{python3_version} %{_bindir}/fail2ban-server
%__ln_s %__python3 %{_bindir}/fail2ban-python

%postun -n python3-fail2ban
%__rm -f %{_bindir}/fail2ban-testcases
%__rm -f %{_bindir}/fail2ban-client
%__rm -f %{_bindir}/fail2ban-regex
%__rm -f %{_bindir}/fail2ban-server
%__rm %{_bindir}/fail2ban-python
%endif

%files
%defattr(-, root, root, 0755)
%doc %{_mandir}/man1/fail2ban-client.1*
%doc %{_mandir}/man1/fail2ban-regex.1*
%doc %{_mandir}/man1/fail2ban-server.1*
%config(noreplace) %{_sysconfdir}/fail2ban/
%config(noreplace) %{_sysconfdir}/logrotate.d/fail2ban
%config %{_initrddir}/fail2ban
%{_datadir}/fail2ban/
%dir %{_var}/run/fail2ban
%dir %{_datadir}/doc/%{name}
%{_datadir}/doc/%{name}/*


%files -n python-fail2ban
%{python_sitelib}/*
%{_bindir}/fail2ban-testcases%{python_version}
%{_bindir}/fail2ban-client%{python_version}
%{_bindir}/fail2ban-regex%{python_version}
%{_bindir}/fail2ban-server%{python_version}

%if 0%{?with_python3}
%files -n python3-fail2ban
%{python3_sitelib}/*
%{_bindir}/fail2ban-testcases%{python3_version}
%{_bindir}/fail2ban-client%{python3_version}
%{_bindir}/fail2ban-regex%{python3_version}
%{_bindir}/fail2ban-server%{python3_version}
%endif

%changelog

