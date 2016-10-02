%define repo https://github.com/draios/flame-ui
#%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">v'`)
%define gitversion %(echo `date +%s`)
%define name ansible
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1

%define docroot /u/docroot
%define logdir /u/logs
%define debug_package %{nil}
%{?nodejs_find_provides_and_requires}
%{?nodejs_default_filter}

Summary: A nodejs app with a systemd daemon
Name:     flame-ui
Provides: sysdig-ui
Group:   Monitoring/Tools
Version: %{gitversion}
Release: %{rel_version}.%{revision}.%{dist}
License: MIT
URL:     %{repo}
Vendor: %{vendor}
Packager: %{packager}
BuildArch: noarch
Requires: systemd
Requires: nodejs
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
A nodejs app that installs as a systemd service

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

%install
cd %{name}-%{version}
rm -rf $RPM_BUILD_ROOT

%__install -d  %{buildroot}%{docroot}/%{name}
%__install -d  %{buildroot}%{logdir}/%{name}
%__ln_s -f %{docroot}/%{name} %{buildroot}%{docroot}/sysdig-ui
%__ln_s -f %{logdir}/%{name} %{buildroot}%{logdir}/sysdig-ui
%__install -d %{buildroot}%{_unitdir}/

%__cp -pa * %{buildroot}%{docroot}/%{name}/
cat << __EOF > %{buildroot}%{_unitdir}/myappd.service
[Unit]
Description=MyApp provides the best API
Documentation=man:myapp.service(8)

[Service]
Type=simple
ExecStart=/usr/sbin/myappd

[Install]
WantedBy=multi-user.target
__EOF

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root)
%dir %{logdir}/%{name}
%dir %{docroot}/%{name}
%{logdir}/sysdig-ui
%{docroot}/sysdig-ui
%{docroot}/%{name}/*
%{_unitdir}/myappd.service

