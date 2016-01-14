%global include_tests 0
%define use_systemd 0
%if 0%{?el6}
%include %{_rpmconfigdir}/macros.d/macros.python27
%global __python /usr/bin/python27
%global __python27 /usr/bin/python27
%else
%include %{_rpmconfigdir}/macros.d/macros.python
%global __python /usr/bin/python27
%global __python27 /usr/bin/python27
%endif

%define _salttesting SaltTesting
%define _salttesting_ver 2015.7.10

Name: salt
Version: 2015.5.5
Release: 1.%{?dist}
Summary: A parallel remote execution system
Group:   System Environment/Daemons
License: ASL 2.0
URL:     http://saltstack.org/
Source0: %{name}.tar.gz
Source1: https://pypi.python.org/packages/source/S/%{_salttesting}/%{_salttesting}-%{_salttesting_ver}.tar.gz
Source2: %{name}-master
Source3: %{name}-syndic
Source4: %{name}-minion
Source5: %{name}-api
Source6: %{name}-master.service
Source7: %{name}-syndic.service
Source8: %{name}-minion.service
Source9: %{name}-api.service
#Source10: README.fedora
Source11: logrotate.salt
Source12: salt.bash
#Patch0:  salt-%{version}-tests.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: dmidecode
Requires: pciutils
Requires: which
Requires: yum-utils
%if 0%{?el6}
Requires: python27-crypto
Requires: python27-jinja2
Requires: python27-m2crypto
Requires: python27-msgpack
Requires: python27-PyYAML
Requires: python27-requests
Requires: python27-pyzmq
BuildRequires: python27-devel
BuildRequires: python27-crypto
BuildRequires: python27-jinja2
BuildRequires: python27-msgpack
BuildRequires: python27-pip
BuildRequires: python27-pyzmq
BuildRequires: python27-PyYAML
BuildRequires: python27-requests
BuildRequires: python27-unittest2
BuildRequires: python27-mock
BuildRequires: python27-libcloud
BuildRequires: python27-argparse
BuildRequires: python27-devel
%else
Requires: python-crypto
Requires: python-jinja2
Requires: python-m2crypto
Requires: python-msgpack
Requires: python-PyYAML
Requires: python-requests
Requires: python-pyzmq
BuildRequires: python-devel
BuildRequires: python-crypto
BuildRequires: python-jinja2
BuildRequires: python-msgpack
BuildRequires: python-pip
BuildRequires: python-pyzmq
BuildRequires: python-PyYAML
BuildRequires: python-requests
BuildRequires: python-unittest2
BuildRequires: python-mock
BuildRequires: python-libcloud
BuildRequires: python-argparse
BuildRequires: python-devel
%endif

Requires: m2crypto
BuildRequires: m2crypto
BuildRequires: git
%if %{use_systemd}
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
BuildRequires: systemd-units
Requires:      systemd-python
%else
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(postun): initscripts
%endif

%description
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

%description master
The Salt master is the central server to which all minions connect.

%package minion
Summary: Client component for Salt, a parallel remote execution system 
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}

%description minion
The Salt minion is the agent component of Salt. It listens for instructions
from the master, runs jobs, and returns results back to the master.

%package syndic
Summary: Master-of-master component for Salt, a parallel remote execution system 
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}

%description syndic
The Salt syndic is a master daemon which can receive instruction from a
higher-level master, allowing for tiered organization of your Salt
infrastructure.

%package api
Summary: REST API for Salt, a parallel remote execution system
Group:   System administration tools
Requires: %{name}-master = %{version}-%{release}
Requires: python-cherrypy

%description api
salt-api provides a REST interface to the Salt master.

%package cloud
Summary: Cloud provisioner for Salt, a parallel remote execution system
Group:   System administration tools
Requires: %{name}-master = %{version}-%{release}
Requires: python-libcloud

%description cloud
The salt-cloud tool provisions new cloud VMs, installs salt-minion on them, and
adds them to the master's collection of controllable minions.

%package ssh
Summary: Agentless SSH-based version of Salt, a parallel remote execution system
Group:   System administration tools
Requires: %{name} = %{version}-%{release}

%description ssh
The salt-ssh tool can run remote execution functions and states without the use
of an agent (salt-minion) service.

%prep
%setup -q -n %{name}
#%patch0 -p1

%build
git pull

%install
rm -rf %{buildroot}
%{__python27} setup.py install -O1 --root %{buildroot}
install -d -m 0755 %{buildroot}%{_var}/cache/salt
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/cloud.conf.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/cloud.deploy.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/cloud.maps.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/cloud.profiles.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/cloud.providers.d
install -p -m 0640 conf/minion %{buildroot}%{_sysconfdir}/salt/minion
install -p -m 0640 conf/master %{buildroot}%{_sysconfdir}/salt/master
install -p -m 0640 conf/cloud %{buildroot}%{_sysconfdir}/salt/cloud
install -p -m 0640 conf/roster %{buildroot}%{_sysconfdir}/salt/roster

%if %{use_systemd}
mkdir -p %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE6} %{buildroot}%{_unitdir}/
install -p -m 0644 %{SOURCE7} %{buildroot}%{_unitdir}/
install -p -m 0644 %{SOURCE8} %{buildroot}%{_unitdir}/
install -p -m 0644 %{SOURCE9} %{buildroot}%{_unitdir}/
%else
mkdir -p %{buildroot}%{_initrddir}
install -p %{SOURCE2} %{buildroot}%{_initrddir}/
install -p %{SOURCE3} %{buildroot}%{_initrddir}/
install -p %{SOURCE4} %{buildroot}%{_initrddir}/
install -p %{SOURCE5} %{buildroot}%{_initrddir}/
%endif

sed -i 's#/usr/bin/python#/usr/bin/python2.7#g' %{buildroot}%{_bindir}/salt*
sed -i 's#/usr/bin/python#/usr/bin/python2.7#g' %{buildroot}%{_initrddir}/salt*

# Logrotate
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/
install -p -m 0644 %{SOURCE11} %{buildroot}%{_sysconfdir}/logrotate.d/salt

# Bash completion
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d/
install -p -m 0644 %{SOURCE12} %{buildroot}%{_sysconfdir}/bash_completion.d/salt.bash

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

# less than RHEL 8 / Fedora 16
%if %{use_systemd}
%preun master
if [ $1 -eq 0 ] ; then
/sbin/service salt-master stop >/dev/null 2>&1
/sbin/chkconfig --del salt-master
fi

%preun syndic
if [ $1 -eq 0 ] ; then
/sbin/service salt-syndic stop >/dev/null 2>&1
/sbin/chkconfig --del salt-syndic
fi

%preun minion
if [ $1 -eq 0 ] ; then
/sbin/service salt-minion stop >/dev/null 2>&1
/sbin/chkconfig --del salt-minion
fi

%post master
/sbin/chkconfig --add salt-master

%post minion
/sbin/chkconfig --add salt-minion

%postun master
if [ "$1" -ge "1" ] ; then
/sbin/service salt-master condrestart >/dev/null 2>&1 || :
fi

#%postun syndic
#  if [ "$1" -ge "1" ] ; then
#      /sbin/service salt-syndic condrestart >/dev/null 2>&1 || :
#  fi

%postun minion
if [ "$1" -ge "1" ] ; then
/sbin/service salt-minion condrestart >/dev/null 2>&1 || :
fi
%else
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
%endif

%files
%defattr(-,root,root,-)
%if 0%{?el6}
%{python27_sitelib}/%{name}/*
#%{python27_sitelib}/%{name}-%{version}-py?.?.egg-info
%{python27_sitelib}/%{name}*.egg-info
%else
%{python_sitelib}/%{name}/*
#%{python_sitelib}/%{name}-%{version}-py?.?.egg-info
%{python_sitelib}/%{name}*.egg-info
%endif

%{_sysconfdir}/logrotate.d/salt
%{_sysconfdir}/bash_completion.d/salt.bash
%{_var}/cache/salt

%files master
%defattr(-,root,root)
%doc %{_mandir}/man7/salt.7.*
%doc %{_mandir}/man1/salt-cp.1.*
%doc %{_mandir}/man1/salt-key.1.*
%doc %{_mandir}/man1/salt-master.1.*
%doc %{_mandir}/man1/salt-run.1.*
%doc %{_mandir}/man1/salt-unity.1.*
%{_bindir}/salt
%{_bindir}/salt-cp
%{_bindir}/salt-key
%{_bindir}/salt-master
%{_bindir}/salt-run
%{_bindir}/salt-unity
%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
%attr(0755, root, root) %{_initrddir}/salt-master
%else
%{_unitdir}/salt-master.service
%endif
%config(noreplace) %{_sysconfdir}/salt/master

%files minion
%defattr(-,root,root)
%doc %{_mandir}/man1/salt-call.1.*
%doc %{_mandir}/man1/salt-minion.1.*
%{_bindir}/salt-minion
%{_bindir}/salt-call
%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
%attr(0755, root, root) %{_initrddir}/salt-minion
%else
%{_unitdir}/salt-minion.service
%endif
%config(noreplace) %{_sysconfdir}/salt/minion
%{_bindir}/%{name}-proxy
%{_bindir}/spm
%doc %{_mandir}/man1/salt-proxy.1.gz
%doc %{_mandir}/man1/spm.1.gz

%files syndic
%doc %{_mandir}/man1/salt-syndic.1.*
%{_bindir}/salt-syndic
%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
%attr(0755, root, root) %{_initrddir}/salt-syndic
%else
%{_unitdir}/salt-syndic.service
%endif

%files api
%defattr(-,root,root)
%doc %{_mandir}/man1/salt-api.1.*
%{_bindir}/salt-api
%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
%attr(0755, root, root) %{_initrddir}/salt-api
%else
%{_unitdir}/salt-api.service
%endif

%files cloud
%doc %{_mandir}/man1/salt-cloud.1.*
%{_bindir}/salt-cloud
%{_sysconfdir}/salt/cloud.conf.d
%{_sysconfdir}/salt/cloud.deploy.d
%{_sysconfdir}/salt/cloud.maps.d
%{_sysconfdir}/salt/cloud.profiles.d
%{_sysconfdir}/salt/cloud.providers.d
%config(noreplace) %{_sysconfdir}/salt/cloud

%files ssh
%doc %{_mandir}/man1/salt-ssh.1.*
%{_bindir}/salt-ssh
%config(noreplace) %{_sysconfdir}/salt/roster

%changelog
