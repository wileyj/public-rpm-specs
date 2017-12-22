%define checkout remotes/origin/2016.11
%global with_git 0
%global include_tests 0
%define use_systemd 0
%define pypi_name salt

%define pypi_version_test %(echo `curl -s https://pypi.python.org/pypi/%{pypi_name} | grep "<title>" | awk '{print $2}'`)
%if "%{?pypi_version_test:%{pypi_version_test}}%{!?pypi_version_test:0}" == "of"
%define pypi_version %(echo `curl -s https://pypi.python.org/pypi/%{pypi_name} | sed -n -e '/<table class="list">/{n;n;n;n;n;n;n;n;p;};h' | cut -d'"' -f2 | cut -d'/' -f4`)
%define pypi_url https://pypi.python.org/pypi/%{pypi_name}/%{pypi_version}
%define url https://pypi.python.org/pypi/%{pypi_name}/%{pypi_version}
%else
%define pypi_version %{pypi_version_test}
%define pypi_url https://pypi.python.org/pypi/%{pypi_name}
%endif
%define repo https://pypi.python.org/pypi/%{pypi_name}
%define revision 1
%define pypi_release %{revision}.%{?dist}

%global pypi_summary %(echo `curl -s %{pypi_url} | grep '<meta name="description" content=' | cut -d'"' -f4`)

%if 0%{?with_git}
%define repo https://github.com/saltstack/%{pypi_name}
%define pypi_version %(echo `curl -s %{repo}/releases | grep 'class="css-truncate-target"' | head -1 |  tr -d '\\-</span class="css-truncate-target">'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1
%define build_time %(echo `date +%s`)
%define pypi_release git.%{build_time}.%{revision}.%{?dist}
%endif

Name:       %{pypi_name}27
Version:    %{pypi_version}
Release:    %{pypi_release}
Summary:    %{pypi_summary}
Group:      System Environment/Daemons
License:    ASL 2.0
URL:        http://saltstack.org/
BuildArch: noarch
Provides:   %{pypi_name} = %{version}
%if %{use_systemd}
BuildRequires:  systemd-units
Requires:       systemd-python
%endif
BuildRequires:  git
Requires:       dmidecode
Requires:	zeromq
Provides:   python27-%{pypi_name} = %{version}
Provides:   %{name}2 = %{version}
BuildRequires: python-M2Crypto
BuildRequires: python-devel
BuildRequires: python-pycrypto
BuildRequires: python-Jinja2
BuildRequires: python-msgpack
BuildRequires: python-pip
BuildRequires: python-pyzmq
BuildRequires: python-PyYAML
BuildRequires: python-requests
BuildRequires: python-unittest2
BuildRequires: python-mock
BuildRequires: python-libcloud
BuildRequires: python-argparse
BuildRequires:  python-M2Crypto
Requires: python27-M2Crypto
Requires: python27-Jinja2
Requires: python27-msgpack
Requires: python27-PyYAML
Requires: python27-MarkupSafe
Requires: python27-requests
Requires: python27-paramiko
Requires: python27-tornado
Requires: python27-futures
Requires: python27-pycrypto
Requires: python27-pyzmq
Requires: python27-backports.ssl_match_hostname
Requires: python27-singledispatch
Requires: python27-certifi
Requires: python27-backports_abc
Requires: python27-six
Requires: python27-M2Crypto
Requires: python27-chardet >= 3.0.4
#Requires: python27-urllib3 >= 1.21.1
Requires: python27-idna

Requires: zeromq
BuildRequires: zeromq-devel

%if %{use_systemd}
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%endif

%description
Python 3 Build
Salt is a distributed remote execution system used to execute commands and
query data. It was developed in order to bring the best solutions found in
the world of remote execution together and make them better, faster and more
malleable. Salt accomplishes this via its ability to handle larger loads of
information, and not just dozens, but hundreds or even thousands of individual
servers, handle them quickly and through a simple and manageable interface.


%package master
Summary: Management component for salt, a parallel remote execution system
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}
%if %{use_systemd}
Requires: systemd-python
%endif
Provides:   python27-%{pypi_name}-master = %{version}
Provides:   %{name}-master = %{version}

%description master
The Salt master is the central server to which all minions connect.

%package minion
Summary: Client component for Salt, a parallel remote execution system
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires:   e2fsprogs 
#Requires:   python-boto3
Requires:   python27-pip
Provides:   python27-%{pypi_name}-minion = %{version}
Provides:   %{name}-minion = %{version}

%description minion
The Salt minion is the agent component of Salt. It listens for instructions
from the master, runs jobs, and returns results back to the master.

%package syndic
Summary: Master-of-master component for Salt, a parallel remote execution system
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Provides:   python27-%{pypi_name}-syndic = %{version}
Provides:   %{name}-syndic = %{version}

%description syndic
The Salt syndic is a master daemon which can receive instruction from a
higher-level master, allowing for tiered organization of your Salt
infrastructure.

%package api
Summary: REST API for Salt, a parallel remote execution system
Group:   System administration tools
Requires: %{name} = %{version}-%{release}
Provides:   python27-%{pypi_name}-api = %{version}
Provides:   %{name}-api = %{version}

%description api
salt-api provides a REST interface to the Salt master.

%package cloud
Summary: Cloud provisioner for Salt, a parallel remote execution system
Group:   System administration tools
Requires: %{name} = %{version}-%{release}
Provides:   python27-%{pypi_name}-cloud = %{version}
Provides:   %{name}-cloud = %{version}

%description cloud
The salt-cloud tool provisions new cloud VMs, installs salt-minion on them, and
adds them to the master's collection of controllable minions.

%package ssh
Summary: Agentless SSH-based version of Salt, a parallel remote execution system
Group:   System administration tools
Requires: %{name} = %{version}-%{release}
Provides:   python27-%{pypi_name}-ssh = %{version}
Provides:   %{name}-ssh = %{version}

%description ssh
The salt-ssh tool can run remote execution functions and states without the use
of an agent (salt-minion) service.

%prep
if [ -d %{pypi_name}-%{version} ];then
    rm -rf %{pypi_name}-%{version}
fi
if [ -d %{buildroot} ]; then
    rm -rf %{buildroot}
fi
%if 0%{?with_git}
git clone %{repo} %{pypi_name}-%{version}
cd %{pypi_name}-%{version}
git checkout %{checkout}

git submodule init
git submodule update
rm -rf %{py2dir}
cp -a . %{py2dir}
%else
curl -o $RPM_SOURCE_DIR/%{pypi_name}.tar.gz `curl -s %{pypi_url} | grep tar.gz | cut -d '"' -f2 | cut -f1 -d "#" | tail -2 | grep 1`
tar -xzvf $RPM_SOURCE_DIR/%{pypi_name}.tar.gz
%__rm -f $RPM_SOURCE_DIR/%{pypi_name}.tar.gz
#mv %{_builddir}/%{pypi_name}-%{version} %{_builddir}/%{pypi_name}-%{version}
%endif


%build
cd $RPM_BUILD_DIR/%{pypi_name}-%{version}
%{__python27} setup.py build

%install
cd $RPM_BUILD_DIR/%{pypi_name}-%{version}
%{__python27} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
find %{buildroot}%{_prefix} -type d -depth -exec rmdir {} \; 2>/dev/null

install -d -m 0755 %{buildroot}%{_var}/cache/%{pypi_name}
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{pypi_name}
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{pypi_name}/cloud.conf.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{pypi_name}/cloud.deploy.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{pypi_name}/cloud.maps.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{pypi_name}/cloud.profiles.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{pypi_name}/cloud.providers.d
install -p -m 0640 conf/minion %{buildroot}%{_sysconfdir}/%{pypi_name}/minion
install -p -m 0640 conf/master %{buildroot}%{_sysconfdir}/%{pypi_name}/master
install -p -m 0640 conf/cloud %{buildroot}%{_sysconfdir}/%{pypi_name}/cloud
install -p -m 0640 conf/roster %{buildroot}%{_sysconfdir}/%{pypi_name}/roster

%if %{use_systemd}
mkdir -p %{buildroot}%{_unitdir}
install -p -m 0644 pkg/%{pypi_name}-master.service %{buildroot}%{_unitdir}/%{pypi_name}-master.service
install -p -m 0644 pkg/%{pypi_name}-syndic.service %{buildroot}%{_unitdir}/%{pypi_name}-syndic.service
install -p -m 0644 pkg/%{pypi_name}-minion.service %{buildroot}%{_unitdir}/%{pypi_name}-minion.service
install -p -m 0644 pkg/%{pypi_name}-api.service %{buildroot}%{_unitdir}/%{pypi_name}-api.service
%else
mkdir -p %{buildroot}%{_initrddir}
install -p pkg/rpm/%{pypi_name}-master %{buildroot}%{_initrddir}/%{pypi_name}-master
install -p pkg/rpm/%{pypi_name}-syndic %{buildroot}%{_initrddir}/%{pypi_name}-syndic
install -p pkg/rpm/%{pypi_name}-minion %{buildroot}%{_initrddir}/%{pypi_name}-minion
install -p pkg/rpm/%{pypi_name}-api %{buildroot}%{_initrddir}/%{pypi_name}-api
sed -i 's#/usr/bin/python#/usr/bin/env python#g' %{buildroot}%{_initrddir}/%{pypi_name}-*
%endif

#sed -i 's#/usr/bin/python#/usr/bin/env python#g' %{buildroot}%{_bindir}/%{pypi_name}*

# Logrotate
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/
install -p -m 0644 pkg/%{pypi_name}-common.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{pypi_name}

# Bash completion
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d/
install -p -m 0644 pkg/%{pypi_name}.bash %{buildroot}%{_sysconfdir}/bash_completion.d/%{pypi_name}.bash

#pki
install -d -m 0700 %{buildroot}%{_sysconfdir}/%{pypi_name}/pki

#%clean
#[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
#[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
#[ "%{_builddir}/%{pypi_name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{pypi_name}-%{version}
#[ "%{_builddir}/%{pypi_name}" != "/" ] && %__rm -rf %{_builddir}/%{pypi_name}


%preun master
%if %{use_systemd}
  %systemd_preun salt-master.service
%else
  if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable salt-master.service > /dev/null 2>&1 || :
    /bin/systemctl stop salt-master.service > /dev/null 2>&1 || :
  fi
%endif

%preun syndic
%if %{use_systemd}
  %systemd_preun salt-syndic.service
%else
  if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable salt-syndic.service > /dev/null 2>&1 || :
    /bin/systemctl stop salt-syndic.service > /dev/null 2>&1 || :
  fi
%endif

%preun minion
%if %{use_systemd}
  %systemd_preun salt-minion.service
%else
  if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable salt-minion.service > /dev/null 2>&1 || :
    /bin/systemctl stop salt-minion.service > /dev/null 2>&1 || :
  fi
%endif

%post master
%if %{use_systemd}
  %systemd_post salt-master.service
%else
  /bin/systemctl daemon-reload &>/dev/null || :
%endif

%post minion
%if %{use_systemd}
  %systemd_post salt-minion.service
%else
  /bin/systemctl daemon-reload &>/dev/null || :
%endif

%postun master
%if %{use_systemd}
  %systemd_postun salt-master.service
%else
  /bin/systemctl daemon-reload &>/dev/null
  [ $1 -gt 0 ] && /bin/systemctl try-restart salt-master.service &>/dev/null || :
%endif

%postun syndic
%if %{use_systemd}
  %systemd_postun salt-syndic.service
%else
  /bin/systemctl daemon-reload &>/dev/null
  [ $1 -gt 0 ] && /bin/systemctl try-restart salt-syndic.service &>/dev/null || :
%endif

%postun minion
%if %{use_systemd}
  %systemd_postun salt-minion.service
%else
  /bin/systemctl daemon-reload &>/dev/null
  [ $1 -gt 0 ] && /bin/systemctl try-restart salt-minion.service &>/dev/null || :
%endif


%files
%defattr(-,root,root,-)
%{python_sitelib}/%{pypi_name}/*
%{python_sitelib}/%{pypi_name}*.egg-info
%{_sysconfdir}/logrotate.d/%{pypi_name}
%{_sysconfdir}/bash_completion.d/%{pypi_name}.bash
%dir %{_sysconfdir}/%{pypi_name}/pki

%{_var}/cache/%{pypi_name}
%{_mandir}/man1/salt.1.gz

%{_sysconfdir}/logrotate.d/%{pypi_name}
%{_sysconfdir}/bash_completion.d/%{pypi_name}.bash
%{_var}/cache/%{pypi_name}
%{_mandir}/man1/salt.1.gz

%files master
%defattr(-,root,root)
%doc %{_mandir}/man7/%{pypi_name}.7.*
%doc %{_mandir}/man1/%{pypi_name}-cp.1.*
%doc %{_mandir}/man1/%{pypi_name}-key.1.*
%doc %{_mandir}/man1/%{pypi_name}-master.1.*
%doc %{_mandir}/man1/%{pypi_name}-run.1.*
%doc %{_mandir}/man1/%{pypi_name}-unity.1.*
%{_bindir}/%{pypi_name}
%{_bindir}/%{pypi_name}-cp
%{_bindir}/%{pypi_name}-key
%{_bindir}/%{pypi_name}-master
%{_bindir}/%{pypi_name}-run
%{_bindir}/%{pypi_name}-unity
%config(noreplace) %{_sysconfdir}/%{pypi_name}/master
%if %{use_systemd}
#%if %{?use_systemd:1}%{!?use_systemd:0}
    %attr(0644, root, root) %{_unitdir}/%{pypi_name}-master.service
%else
    %attr(0755, root, root) %{_initrddir}/%{pypi_name}-master
%endif

%files minion
%defattr(-,root,root)
%doc %{_mandir}/man1/%{pypi_name}-call.1.*
%doc %{_mandir}/man1/%{pypi_name}-minion.1.*
%{_bindir}/%{pypi_name}-minion
%{_bindir}/%{pypi_name}-call
%{_bindir}/%{pypi_name}-proxy
%{_bindir}/spm
%config(noreplace) %{_sysconfdir}/%{pypi_name}/minion
%doc %{_mandir}/man1/%{pypi_name}-proxy.1.gz
%doc %{_mandir}/man1/spm.1.gz
%if %{use_systemd}
#%if %{?use_systemd:1}%{!?use_systemd:0}
    %attr(0644, root, root) %{_unitdir}/%{pypi_name}-minion.service
%else
    %attr(0755, root, root) %{_initrddir}/%{pypi_name}-minion
%endif


%files syndic
%doc %{_mandir}/man1/%{pypi_name}-syndic.1.*
%{_bindir}/%{pypi_name}-syndic
%if %{use_systemd}
##%if %{?use_systemd:1}%{!?use_systemd:0}
    %attr(0644, root, root) %{_unitdir}/%{pypi_name}-syndic.service
%else
    %attr(0755, root, root) %{_initrddir}/%{pypi_name}-syndic
%endif

%files api
%defattr(-,root,root)
%doc %{_mandir}/man1/%{pypi_name}-api.1.*
%{_bindir}/%{pypi_name}-api
%if %{use_systemd}
#%if %{?use_systemd:1}%{!?use_systemd:0}
    %attr(0644, root, root) %{_unitdir}/%{pypi_name}-api.service
%else
    %attr(0755, root, root) %{_initrddir}/%{pypi_name}-api
%endif

%files cloud
%doc %{_mandir}/man1/%{pypi_name}-cloud.1.*
%{_bindir}/%{pypi_name}-cloud
%{_sysconfdir}/%{pypi_name}/cloud.conf.d
%{_sysconfdir}/%{pypi_name}/cloud.deploy.d
%{_sysconfdir}/%{pypi_name}/cloud.maps.d
%{_sysconfdir}/%{pypi_name}/cloud.profiles.d
%{_sysconfdir}/%{pypi_name}/cloud.providers.d
%config(noreplace) %{_sysconfdir}/%{pypi_name}/cloud

%files ssh
%doc %{_mandir}/man1/%{pypi_name}-ssh.1.*
%{_bindir}/%{pypi_name}-ssh
%config(noreplace) %{_sysconfdir}/%{pypi_name}/roster

%changelog

