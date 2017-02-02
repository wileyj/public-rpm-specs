# needed for building on el6
%{?nodejs_find_provides_and_requires}

%define git_repo https://github.com/etsy/statsd
%define git_version %(echo `curl -s  %{git_repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">'`)
%global git_revision %(echo `git ls-remote %{git_repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define git_summary        %(echo `curl -s %{git_repo} | grep "<title>" | cut -f2 -d ":" | sed 's|</title>||'`)
%define rel_version 1
%define _prefix /opt/%{name}-%{version}

# filter provides and requires from examples directory RHBZ#1263969
%{?perl_default_filter}

%global enable_tests 1

%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
%bcond_without systemd
%endif

Name:       statsd
Version:    %{git_version}
Release:    7.%{?dist}
Summary:    %{git_summary}
License:    MIT
URL:        https://github.com/etsy/statsd/
#Source0:    https://github.com/etsy/%{name}/archive/v%{version}.tar.gz#/%{name}-v%{version}.tar.gz
Source1:    statsd.service
Source2:    statsd.sysvinit

BuildArch:      noarch
%if 0%{?fedora} >= 19
ExclusiveArch: %{nodejs_arches} noarch
%else
ExclusiveArch: %{ix86} x86_64 %{arm} noarch
%endif

BuildRequires:  dos2unix
BuildRequires:  nodejs-packaging
BuildRequires:  nodeunit
BuildRequires:  npm(temp)
BuildRequires:  npm(underscore)

Requires(pre):  shadow-utils

%if %{with systemd}
BuildRequires:      systemd
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
%else
Requires(post):     chkconfig
Requires(preun):    chkconfig
Requires(postun):   initscripts
%endif


%description
A network daemon that runs on the Node.js platform and listens for statistics, 
like counters and timers, sent over UDP or TCP and sends aggregates to one or 
more pluggable backend services (e.g., Graphite).


%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{git_repo} %{name}-%{version}
cd %{name}-%{version}

# fix end of line encodings
/usr/bin/dos2unix examples/go/statsd.go
/usr/bin/dos2unix examples/csharp_example.cs

# set Graphitehost to localhost in default config
sed -i 's/graphite\.example\.com/localhost/' exampleConfig.js


%build
cd %{name}-%{version}
#nothing to do


%install
cd %{name}-%{version}
%{__mkdir_p} %{buildroot}%{nodejs_sitelib}/%{name}
cp -pr package.json proxy.js stats.js utils %{buildroot}%{nodejs_sitelib}/%{name}
cp -pr backends lib bin %{buildroot}%{nodejs_sitelib}/%{name}

%{__mkdir_p} %{buildroot}%{_bindir}
ln -s %{nodejs_sitelib}/%{name}/bin/%{name} %{buildroot}%{_bindir}/%{name}

%{__mkdir_p} %{buildroot}%{_sysconfdir}/%{name}
cp -pr exampleConfig.js %{buildroot}%{_sysconfdir}/%{name}/config.js


%if %{with systemd}
%{__install} -Dp -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
%else
%{__install} -Dp -m 0755 %{SOURCE2} %{buildroot}%{_initddir}/%{name}
%endif

%nodejs_symlink_deps


%if 0%{?enable_tests}
%check
%nodejs_symlink_deps --check
./run_tests.sh
%endif


%pre
getent group statsd >/dev/null || groupadd -r statsd
getent passwd statsd >/dev/null || \
    useradd -r -g statsd -d / -s /sbin/nologin \
    -c "statsd daemon user" statsd
exit 0


%post
%if %{with systemd}
%systemd_post %{name}.service
%else
/sbin/chkconfig --add %{name}
%endif


%preun
%if %{with systemd}
%systemd_preun %{name}.service
%else
if [ $1 -eq 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi
%endif


%postun
%if %{with systemd}
%systemd_postun_with_restart %{name}.service
%else
if [ "$1" -ge "1" ] ; then
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi
%endif


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
# following macro is needed for el6
%{!?_licensedir:%global license %%doc}
%doc README.md CONTRIBUTING.md Changelog.md exampleConfig.js exampleProxyConfig.js docs/ examples/
%license LICENSE
%{nodejs_sitelib}/%{name}
%{_bindir}/statsd
%{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/config.js

%if %{with systemd}
%{_unitdir}/%{name}.service
%else
%{_initddir}/%{name}
%endif


%changelog
