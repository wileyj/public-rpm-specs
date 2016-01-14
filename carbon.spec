%if 0%{?el6}
    %define macro %{_rpmconfigdir}/macros.d/macros.python27
    %global __python /usr/bin/python27
%else
    %define macro %{_rpmconfigdir}/macros.d/macros.python
    %global __python /usr/bin/python
%endif

%include %{macro}

%define __getent   /usr/bin/getent
%define __useradd  /usr/sbin/useradd
%define __userdel  /usr/sbin/userdel
%define __groupadd /usr/sbin/groupadd
%define __touch    /bin/touch
%define __service  /sbin/service

Name:           carbon
Version:        0.9.10
Release:        1.%{dist}
Summary:        Backend data caching and persistence daemon for Graphite
Group:          Applications/Internet
License:        Apache Software License 2.0
URL:            https://launchpad.net/graphite
Vendor: %{vendor}
Packager: %{packager}
Source0:        https://github.com/downloads/graphite-project/%{name}/%{name}-%{version}.tar.gz
#Patch0:         %{name}-setup.patch
Patch1:         %{name}-config.patch
Source1:        %{name}-cache.init
Source2:        %{name}-cache.sysconfig
Source3:        %{name}-relay.init
Source4:        %{name}-relay.sysconfig
Source5:        %{name}-aggregator.init
Source6:        %{name}-aggregator.sysconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if 0%{?el6}
BuildRequires:  python27 python27-devel python27-setuptools
Requires:       python27 whisper python27-twisted-core >= 8.0
%else
BuildRequires:  python python-devel python-setuptools
Requires:       python whisper
%endif

%description
The backend for Graphite. Carbon is a data collection and storage agent.  

%prep
%setup -q
#%patch0 -p1
%patch1 -p1

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python27} -c 'import setuptools; execfile("setup.py")' build

%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}
%{__python27} -c 'import setuptools; execfile("setup.py")' install --skip-build --root %{buildroot}

# Create log and var directories
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/%{name}-cache
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/%{name}-relay
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/%{name}-aggregator
%{__mkdir_p} %{buildroot}%{_localstatedir}/lib/%{name}

# Install system configuration and init scripts
%{__install} -Dp -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}-cache
%{__install} -Dp -m0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}-cache
%{__install} -Dp -m0755 %{SOURCE3} %{buildroot}%{_initrddir}/%{name}-relay
%{__install} -Dp -m0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/%{name}-relay
%{__install} -Dp -m0755 %{SOURCE5} %{buildroot}%{_initrddir}/%{name}-aggregator
%{__install} -Dp -m0644 %{SOURCE6} %{buildroot}%{_sysconfdir}/sysconfig/%{name}-aggregator

# Install default configuration files
%{__mkdir_p} %{buildroot}%{_sysconfdir}/%{name}
%{__install} -Dp -m0644 conf/carbon.conf.example %{buildroot}%{_sysconfdir}/%{name}/carbon.conf
%{__install} -Dp -m0644 conf/storage-schemas.conf.example %{buildroot}%{_sysconfdir}/%{name}/storage-schemas.conf

# Create transient files in buildroot for ghosting
%{__mkdir_p} %{buildroot}%{_localstatedir}/lock/subsys
%{__touch} %{buildroot}%{_localstatedir}/lock/subsys/%{name}-cache
%{__touch} %{buildroot}%{_localstatedir}/lock/subsys/%{name}-relay
%{__touch} %{buildroot}%{_localstatedir}/lock/subsys/%{name}-aggregator

%{__mkdir_p} %{buildroot}%{_localstatedir}/run
%{__touch} %{buildroot}%{_localstatedir}/run/%{name}-cache.pid
%{__touch} %{buildroot}%{_localstatedir}/run/%{name}-relay.pid
%{__touch} %{buildroot}%{_localstatedir}/run/%{name}-aggregator.pid

%pre
%{__getent} group %{name} >/dev/null || %{__groupadd} -r %{name}
%{__getent} passwd %{name} >/dev/null || \
    %{__useradd} -r -g %{name} -d %{_localstatedir}/lib/%{name} \
    -s /sbin/nologin -c "Carbon cache daemon" %{name}
exit 0

%preun
%{__service} %{name} stop
exit 0

%postun
if [ $1 = 0 ]; then
  %{__getent} passwd %{name} >/dev/null && \
      %{__userdel} -r %{name} 2>/dev/null
fi
exit 0

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%doc LICENSE conf/*

/opt/graphite/lib
/opt/graphite/bin
/opt/graphite/conf
%{_initrddir}/%{name}-cache
%{_initrddir}/%{name}-relay
%{_initrddir}/%{name}-aggregator

%config %{_sysconfdir}/%{name}
%config %{_sysconfdir}/sysconfig/%{name}-cache
%config %{_sysconfdir}/sysconfig/%{name}-relay
%config %{_sysconfdir}/sysconfig/%{name}-aggregator

%attr(-,%name,%name) %{_localstatedir}/lib/%{name}
%attr(-,%name,%name) %{_localstatedir}/log/%{name}-cache
%attr(-,%name,%name) %{_localstatedir}/log/%{name}-relay
%attr(-,%name,%name) %{_localstatedir}/log/%{name}-aggregator

%ghost %{_localstatedir}/lock/subsys/%{name}-cache
%ghost %{_localstatedir}/run/%{name}-cache.pid
%ghost %{_localstatedir}/lock/subsys/%{name}-relay
%ghost %{_localstatedir}/run/%{name}-relay.pid
%ghost %{_localstatedir}/lock/subsys/%{name}-aggregator
%ghost %{_localstatedir}/run/%{name}-aggregator.pid

%changelog
