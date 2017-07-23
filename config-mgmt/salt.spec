%define checkout remotes/origin/2016.11
%global with_python3 0
%global with_git 0
%global include_tests 0
%define use_systemd 1
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

Name:       %{pypi_name}
Version:    %{pypi_version}
Release:    %{pypi_release}
Summary:    %{pypi_summary}
Group:      System Environment/Daemons
License:    ASL 2.0
URL:        http://saltstack.org/
BuildArch: noarch
Provides:   %{pypi_name} = %{version}
BuildRequires:  systemd-units
BuildRequires:  git
Requires:       dmidecode
Requires:       systemd-python
Requires:	zeromq
%if 0%{?with_python3}
Provides:   python3-%{pypi_name} = %{version}
Provides:   %{pypi_name} = %{version}
BuildRequires: python3-M2Crypto
BuildRequires: python3-devel
BuildRequires: python3-pycrypto
BuildRequires: python3-Jinja2
BuildRequires: python3-msgpack
BuildRequires: python3-pip
BuildRequires: python3-pyzmq
BuildRequires: python3-PyYAML
BuildRequires: python3-requests
BuildRequires: python3-unittest2
BuildRequires: python3-mock
BuildRequires: python3-libcloud
BuildRequires: python3-argparse
BuildRequires:  python3-M2Crypto
Requires: python3-M2Crypto
Requires: python3-Jinja2
Requires: python3-msgpack
Requires: python3-PyYAML
Requires: python3-MarkupSafe
Requires: python3-requests
Requires: python3-paramiko
Requires: python3-tornado
Requires: python3-futures
Requires: python3-pycrypto
Requires: python3-pyzmq
Requires: python3-backports.ssl_match_hostname
Requires: python3-singledispatch
Requires: python3-certifi
Requires: python3-backports_abc
Requires: python3-six
Requires: python3-M2Crypto
Requires: python3-chardet >= 3.0.4
#Requires: python3-urllib3 >= 1.21.1
Requires: python3-idna

%else
Provides:   python-%{pypi_name} = %{version}
Provides:   %{pypi_name}2 = %{version}
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
Requires: python-M2Crypto
Requires: python-Jinja2
Requires: python-msgpack
Requires: python-PyYAML
Requires: python-MarkupSafe
Requires: python-requests
Requires: python-paramiko
Requires: python-tornado
Requires: python-futures
Requires: python-pycrypto
Requires: python-pyzmq
Requires: python-backports.ssl_match_hostname
Requires: python-singledispatch
Requires: python-certifi
Requires: python-backports_abc
Requires: python-six
Requires: python-M2Crypto
Requires: python-chardet >= 3.0.4
#Requires: python-urllib3 >= 1.21.1
Requires: python-idna

%endif
Requires: zeromq
BuildRequires: zeromq-devel

%if 0%{?systemd_preun:1}
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
Requires: systemd-python
Provides:   python-%{pypi_name}-master = %{version}
Provides:   %{pypi_name}-master = %{version}

%description master
The Salt master is the central server to which all minions connect.

%package minion
Summary: Client component for Salt, a parallel remote execution system
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires:   e2fsprogs 
Requires:   python-boto3
Requires:   python-pip
Provides:   python-%{pypi_name}-minion = %{version}
Provides:   %{pypi_name}-minion = %{version}

%description minion
The Salt minion is the agent component of Salt. It listens for instructions
from the master, runs jobs, and returns results back to the master.

%package syndic
Summary: Master-of-master component for Salt, a parallel remote execution system
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Provides:   python-%{pypi_name}-syndic = %{version}
Provides:   %{pypi_name}-syndic = %{version}

%description syndic
The Salt syndic is a master daemon which can receive instruction from a
higher-level master, allowing for tiered organization of your Salt
infrastructure.

%package api
Summary: REST API for Salt, a parallel remote execution system
Group:   System administration tools
Requires: %{name} = %{version}-%{release}
Provides:   python-%{pypi_name}-api = %{version}
Provides:   %{pypi_name}-api = %{version}

%description api
salt-api provides a REST interface to the Salt master.

%package cloud
Summary: Cloud provisioner for Salt, a parallel remote execution system
Group:   System administration tools
Requires: %{name} = %{version}-%{release}
Provides:   python-%{pypi_name}-cloud = %{version}
Provides:   %{pypi_name}-cloud = %{version}

%description cloud
The salt-cloud tool provisions new cloud VMs, installs salt-minion on them, and
adds them to the master's collection of controllable minions.

%package ssh
Summary: Agentless SSH-based version of Salt, a parallel remote execution system
Group:   System administration tools
Requires: %{name} = %{version}-%{release}
Provides:   python-%{pypi_name}-ssh = %{version}
Provides:   %{pypi_name}-ssh = %{version}

%description ssh
The salt-ssh tool can run remote execution functions and states without the use
of an agent (salt-minion) service.

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
if [ -d %{buildroot} ]; then
    rm -rf %{buildroot}
fi
%if 0%{?with_git}
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
git checkout %{checkout}

git submodule init
git submodule update
%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%else
rm -rf %{py2dir}
cp -a . %{py2dir}
%endif
%else
curl -o $RPM_SOURCE_DIR/%{name}.tar.gz `curl -s %{pypi_url} | grep tar.gz | cut -d '"' -f2 | cut -f1 -d "#" | tail -2 | grep 1`
tar -xzvf $RPM_SOURCE_DIR/%{name}.tar.gz
%__rm -f $RPM_SOURCE_DIR/%{name}.tar.gz
#mv %{_builddir}/%{pypi_name}-%{version} %{_builddir}/%{name}-%{version}
%endif


%build
cd $RPM_BUILD_DIR/%{name}-%{version}
%if 0%{?with_python3}
#pushd %{py3dir}
%{__python3} setup.py build
#popd
%else
#pushd %{py2dir}
%{__python2} setup.py build
#popd
%endif

%install
cd $RPM_BUILD_DIR/%{name}-%{version}


%if 0%{?with_python3}
#pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
find %{buildroot}%{_prefix} -type d -depth -exec rmdir {} \; 2>/dev/null
#popd
%else
#pushd %{py2dir}
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
find %{buildroot}%{_prefix} -type d -depth -exec rmdir {} \; 2>/dev/null
#popd
%endif

install -d -m 0755 %{buildroot}%{_var}/cache/%{name}
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}/cloud.conf.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}/cloud.deploy.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}/cloud.maps.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}/cloud.profiles.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}/cloud.providers.d
install -p -m 0640 conf/minion %{buildroot}%{_sysconfdir}/%{name}/minion
install -p -m 0640 conf/master %{buildroot}%{_sysconfdir}/%{name}/master
install -p -m 0640 conf/cloud %{buildroot}%{_sysconfdir}/%{name}/cloud
install -p -m 0640 conf/roster %{buildroot}%{_sysconfdir}/%{name}/roster

%if %{use_systemd}
mkdir -p %{buildroot}%{_unitdir}
install -p -m 0644 pkg/%{name}-master.service %{buildroot}%{_unitdir}/%{name}-master.service
install -p -m 0644 pkg/%{name}-syndic.service %{buildroot}%{_unitdir}/%{name}-syndic.service
install -p -m 0644 pkg/%{name}-minion.service %{buildroot}%{_unitdir}/%{name}-minion.service
install -p -m 0644 pkg/%{name}-api.service %{buildroot}%{_unitdir}/%{name}-api.service
%else
mkdir -p %{buildroot}%{_initrddir}
install -p pkg/rpm/%{name}-master %{buildroot}%{_initrddir}/%{name}-master
install -p pkg/rpm/%{name}-syndic %{buildroot}%{_initrddir}/%{name}-syndic
install -p pkg/rpm/%{name}-minion %{buildroot}%{_initrddir}/%{name}-minion
install -p pkg/rpm/%{name}-api %{buildroot}%{_initrddir}/%{name}-api
sed -i 's#/usr/bin/python#/usr/bin/env python#g' %{buildroot}%{_initrddir}/%{name}-*
%endif

#sed -i 's#/usr/bin/python#/usr/bin/env python#g' %{buildroot}%{_bindir}/%{name}*

# Logrotate
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/
install -p -m 0644 pkg/%{name}-common.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Bash completion
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d/
install -p -m 0644 pkg/%{name}.bash %{buildroot}%{_sysconfdir}/bash_completion.d/%{name}.bash

#pki
install -d -m 0700 %{buildroot}%{_sysconfdir}/%{name}/pki

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}


%preun master
%if 0%{?systemd_preun:1}
  %systemd_preun salt-master.service
%else
  if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable salt-master.service > /dev/null 2>&1 || :
    /bin/systemctl stop salt-master.service > /dev/null 2>&1 || :
  fi
%endif

%preun syndic
%if 0%{?systemd_preun:1}
  %systemd_preun salt-syndic.service
%else
  if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable salt-syndic.service > /dev/null 2>&1 || :
    /bin/systemctl stop salt-syndic.service > /dev/null 2>&1 || :
  fi
%endif

%preun minion
%if 0%{?systemd_preun:1}
  %systemd_preun salt-minion.service
%else
  if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable salt-minion.service > /dev/null 2>&1 || :
    /bin/systemctl stop salt-minion.service > /dev/null 2>&1 || :
  fi
%endif

%post master
%if 0%{?systemd_post:1}
  %systemd_post salt-master.service
%else
  /bin/systemctl daemon-reload &>/dev/null || :
%endif

%post minion
%if 0%{?systemd_post:1}
  %systemd_post salt-minion.service
%else
  /bin/systemctl daemon-reload &>/dev/null || :
%endif

%postun master
%if 0%{?systemd_post:1}
  %systemd_postun salt-master.service
%else
  /bin/systemctl daemon-reload &>/dev/null
  [ $1 -gt 0 ] && /bin/systemctl try-restart salt-master.service &>/dev/null || :
%endif

%postun syndic
%if 0%{?systemd_post:1}
  %systemd_postun salt-syndic.service
%else
  /bin/systemctl daemon-reload &>/dev/null
  [ $1 -gt 0 ] && /bin/systemctl try-restart salt-syndic.service &>/dev/null || :
%endif

%postun minion
%if 0%{?systemd_post:1}
  %systemd_postun salt-minion.service
%else
  /bin/systemctl daemon-reload &>/dev/null
  [ $1 -gt 0 ] && /bin/systemctl try-restart salt-minion.service &>/dev/null || :
%endif


%files
%defattr(-,root,root,-)
%if 0%{?with_python3}
%{python3_sitelib}/%{name}/*
%{python3_sitelib}/%{name}*.egg-info
%else
%{python_sitelib}/%{name}/*
%{python_sitelib}/%{name}*.egg-info
%endif
%{_sysconfdir}/logrotate.d/%{name}
%{_sysconfdir}/bash_completion.d/%{name}.bash
%dir %{_sysconfdir}/%{name}/pki

%{_var}/cache/%{name}
%{_mandir}/man1/salt.1.gz

%{_sysconfdir}/logrotate.d/%{name}
%{_sysconfdir}/bash_completion.d/%{name}.bash
%{_var}/cache/%{name}
%{_mandir}/man1/salt.1.gz

%files master
%defattr(-,root,root)
%doc %{_mandir}/man7/%{name}.7.*
%doc %{_mandir}/man1/%{name}-cp.1.*
%doc %{_mandir}/man1/%{name}-key.1.*
%doc %{_mandir}/man1/%{name}-master.1.*
%doc %{_mandir}/man1/%{name}-run.1.*
%doc %{_mandir}/man1/%{name}-unity.1.*
%{_bindir}/%{name}
%{_bindir}/%{name}-cp
%{_bindir}/%{name}-key
%{_bindir}/%{name}-master
%{_bindir}/%{name}-run
%{_bindir}/%{name}-unity
%config(noreplace) %{_sysconfdir}/%{name}/master
%if %{?use_systemd:1}%{!?use_systemd:0}
    %attr(0644, root, root) %{_unitdir}/%{name}-master.service
%else
    %attr(0755, root, root) %{_initrddir}/%{name}-master
%endif

%files minion
%defattr(-,root,root)
%doc %{_mandir}/man1/%{name}-call.1.*
%doc %{_mandir}/man1/%{name}-minion.1.*
%{_bindir}/%{name}-minion
%{_bindir}/%{name}-call
%{_bindir}/%{name}-proxy
%{_bindir}/spm
%config(noreplace) %{_sysconfdir}/%{name}/minion
%doc %{_mandir}/man1/%{name}-proxy.1.gz
%doc %{_mandir}/man1/spm.1.gz
%if %{?use_systemd:1}%{!?use_systemd:0}
    %attr(0644, root, root) %{_unitdir}/%{name}-minion.service
%else
    %attr(0755, root, root) %{_initrddir}/%{name}-minion
%endif


%files syndic
%doc %{_mandir}/man1/%{name}-syndic.1.*
%{_bindir}/%{name}-syndic
%if %{?use_systemd:1}%{!?use_systemd:0}
    %attr(0644, root, root) %{_unitdir}/%{name}-syndic.service
%else
    %attr(0755, root, root) %{_initrddir}/%{name}-syndic
%endif

%files api
%defattr(-,root,root)
%doc %{_mandir}/man1/%{name}-api.1.*
%{_bindir}/%{name}-api
%if %{?use_systemd:1}%{!?use_systemd:0}
    %attr(0644, root, root) %{_unitdir}/%{name}-api.service
%else
    %attr(0755, root, root) %{_initrddir}/%{name}-api
%endif

%files cloud
%doc %{_mandir}/man1/%{name}-cloud.1.*
%{_bindir}/%{name}-cloud
%{_sysconfdir}/%{name}/cloud.conf.d
%{_sysconfdir}/%{name}/cloud.deploy.d
%{_sysconfdir}/%{name}/cloud.maps.d
%{_sysconfdir}/%{name}/cloud.profiles.d
%{_sysconfdir}/%{name}/cloud.providers.d
%config(noreplace) %{_sysconfdir}/%{name}/cloud

%files ssh
%doc %{_mandir}/man1/%{name}-ssh.1.*
%{_bindir}/%{name}-ssh
%config(noreplace) %{_sysconfdir}/%{name}/roster

%changelog

