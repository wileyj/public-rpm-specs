%if 0%{?amzn} >= 1
%define python python27
BuildRequires: %{python} %{python}-rpm-macros %{python}-devel
Requires: %{python} %{python}-setuptools
%else
%define python python
BuildRequires: %{python} %{python}-rpm-macros %{python}-devel
Requires: %{python} %{python}-setuptools
%endif

%define macro %{_rpmconfigdir}/macros.d/macros.python
%define repo https://github.com/saltstack/salt
#%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">v'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1
%define gitversion 2016.3.3

%global include_tests 0
%define use_systemd 0
#%define _salttesting SaltTesting
#%define _salttesting_ver 2015.7.10

Name: salt
Version: %{gitversion}
Release: %{rel_version}.%{revision}.%{?dist}
Summary: A parallel remote execution system
Group:   System Environment/Daemons
License: ASL 2.0
URL:     http://saltstack.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: dmidecode
Requires: pciutils
Requires: which
Requires: yum-utils
Requires: git
Requires: %{python}-tornado %{python}-singledispatch %{python}-backports_abc
Requires: %{python}-crypto %{python}-jinja2 %{python}-m2crypto %{python}-msgpack 
Requires: %{python}-PyYAML %{python}-requests %{python}-pyzmq

BuildRequires: git
BuildRequires: %{python}-devel %{python}-crypto %{python}-jinja2 %{python}-msgpack %{python}-pip %{python}-pyzmq %{python}-PyYAML %{python}-requests %{python}-unittest2 %{python}-mock %{python}-argparse %{python}-devel

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
Requires: %{python}-cherrypy

%description api
salt-api provides a REST interface to the Salt master.

%package cloud
Summary: Cloud provisioner for Salt, a parallel remote execution system
Group:   System administration tools
Requires: %{name}-master = %{version}-%{release}
Requires: %{python}-libcloud

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

rm -rf %{buildroot}
%{__python} setup.py install -O1 --root %{buildroot}
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
sed -i 's#/usr/bin/python#/usr/bin/python27#g' %{buildroot}%{_initrddir}/%{name}-*
%endif

#sed -i 's#/usr/bin/python#/usr/bin/python27#g' %{buildroot}%{_bindir}/%{name}*

# Logrotate
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/
install -p -m 0644 pkg/%{name}-common.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Bash completion
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d/
install -p -m 0644 pkg/%{name}.bash %{buildroot}%{_sysconfdir}/bash_completion.d/%{name}.bash

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

# less than RHEL 8 / Fedora 16
%if %{use_systemd}
%preun master
    if [ $1 -eq 0 ] ; then
        /sbin/service %{name}-master stop >/dev/null 2>&1
        /sbin/chkconfig --del %{name}-master
    fi

%preun syndic
    if [ $1 -eq 0 ] ; then
        /sbin/service %{name}-syndic stop >/dev/null 2>&1
        /sbin/chkconfig --del %{name}-syndic
    fi

%preun minion
    if [ $1 -eq 0 ] ; then
        /sbin/service %{name}-minion stop >/dev/null 2>&1
        /sbin/chkconfig --del %{name}-minion
    fi

%post master
    /sbin/chkconfig --add %{name}-master

%post minion
    /sbin/chkconfig --add %{name}-minion

%postun master
    if [ "$1" -ge "1" ] ; then
        /sbin/service %{name}-master condrestart >/dev/null 2>&1 || :
    fi

%postun minion
    if [ "$1" -ge "1" ] ; then
        /sbin/service %{name}-minion condrestart >/dev/null 2>&1 || :
    fi
%else
%preun master
    %if 0%{?systemd_preun:1}
        %systemd_preun %{name}-master.service
    %else
        if [ $1 -eq 0 ] ; then
            # Package removal, not upgrade
            /bin/systemctl --no-reload disable %{name}-master.service > /dev/null 2>&1 || :
            /bin/systemctl stop %{name}-master.service > /dev/null 2>&1 || :
        fi
    %endif
%preun syndic
%if 0%{?systemd_preun:1}
    %systemd_preun %{name}-syndic.service
%else
    if [ $1 -eq 0 ] ; then
        # Package removal, not upgrade
        /bin/systemctl --no-reload disable %{name}-syndic.service > /dev/null 2>&1 || :
        /bin/systemctl stop %{name}-syndic.service > /dev/null 2>&1 || :
    fi
%endif
%preun minion
%if 0%{?systemd_preun:1}
    %systemd_preun %{name}-minion.service
%else
if [ $1 -eq 0 ] ; then
# Package removal, not upgrade
/bin/systemctl --no-reload disable %{name}-minion.service > /dev/null 2>&1 || :
/bin/systemctl stop %{name}-minion.service > /dev/null 2>&1 || :
fi
%endif

%post master
%if 0%{?systemd_post:1}
    %systemd_post %{name}-master.service
%else
    /bin/systemctl daemon-reload &>/dev/null || :
%endif
%post minion
%if 0%{?systemd_post:1}
        %systemd_post %{name}-minion.service
%else
    /bin/systemctl daemon-reload &>/dev/null || :
%endif
%postun master
%if 0%{?systemd_post:1}
        %systemd_postun %{name}-master.service
%else
    /bin/systemctl daemon-reload &>/dev/null
    [ $1 -gt 0 ] && /bin/systemctl try-restart %{name}-master.service &>/dev/null || :
%endif
%postun syndic
%if 0%{?systemd_post:1}
        %systemd_postun %{name}-syndic.service
%else
    /bin/systemctl daemon-reload &>/dev/null
    [ $1 -gt 0 ] && /bin/systemctl try-restart %{name}-syndic.service &>/dev/null || :
%endif
%postun minion
%if 0%{?systemd_post:1}
    %systemd_postun %{name}-minion.service
%else
    /bin/systemctl daemon-reload &>/dev/null
    [ $1 -gt 0 ] && /bin/systemctl try-restart %{name}-minion.service &>/dev/null || :
%endif
%endif

%files
%defattr(-,root,root,-)
%{python_sitelib}/%{name}/*
%{python_sitelib}/%{name}*.egg-info

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
%if %{?use_systemd:1}%{!?use_systemd:0}
    %attr(0755, root, root) %{_initrddir}/%{name}-master
%else
    %{_unitdir}/%{name}-master.service
%endif
%config(noreplace) %{_sysconfdir}/%{name}/master

%files minion
%defattr(-,root,root)
%doc %{_mandir}/man1/%{name}-call.1.*
%doc %{_mandir}/man1/%{name}-minion.1.*
%{_bindir}/%{name}-minion
%{_bindir}/%{name}-call
%if %{?use_systemd:1}%{!?use_systemd:0}
    %attr(0755, root, root) %{_initrddir}/%{name}-minion
%else
    %{_unitdir}/%{name}-minion.service
%endif
%config(noreplace) %{_sysconfdir}/%{name}/minion
%{_bindir}/%{name}-proxy
%{_bindir}/spm
%doc %{_mandir}/man1/%{name}-proxy.1.gz
%doc %{_mandir}/man1/spm.1.gz

%files syndic
%doc %{_mandir}/man1/%{name}-syndic.1.*
%{_bindir}/%{name}-syndic
%if %{?use_systemd:1}%{!?use_systemd:0}
    %attr(0755, root, root) %{_initrddir}/%{name}-syndic
%else
    %{_unitdir}/%{name}-syndic.service
%endif

%files api
%defattr(-,root,root)
%doc %{_mandir}/man1/%{name}-api.1.*
%{_bindir}/%{name}-api
%if %{?use_systemd:1}%{!?use_systemd:0}
    %attr(0755, root, root) %{_initrddir}/%{name}-api
%else
    %{_unitdir}/%{name}-api.service
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

