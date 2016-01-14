%include %{_rpmconfigdir}/macros.d/macros.python27
%global srcname carbon

%define __getent   /usr/bin/getent
%define __useradd  /usr/sbin/useradd
%define __userdel  /usr/sbin/userdel
%define __groupadd /usr/sbin/groupadd
%define __touch    /bin/touch
%define __service  /sbin/service

Name:           python27-%{srcname}
Version:        0.9.10
Release:        1.%{dist}
Summary:        Metrics collection for graphite
Group:          Applications/Internet
License:        Apache Software License 2.0
URL:            https://launchpad.net/graphite
Vendor: %{vendor}
Packager: %{packager}
Source0:        https://github.com/downloads/graphite-project/%{srcname}/%{srcname}-%{version}.tar.gz
Patch1:         %{srcname}-config.patch
Source1:        %{srcname}-cache.init
Source2:        %{srcname}-cache.sysconfig
Source3:        %{srcname}-relay.init
Source4:        %{srcname}-relay.sysconfig
Source5:        %{srcname}-aggregator.init
Source6:        %{srcname}-aggregator.sysconfig
BuildRoot:      %{_tmppath}/%{srcname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python27 python27-devel python27-setuptools
Requires:       python27 python27-whisper
Requires:       python27-twisted-core >= 8.0

%description
Carbon is one of the components of Graphite, and is responsible for receiving metrics over the network and writing them down to disk using a storage backend.

%prep
%setup -q -n %{srcname}-%{version}
#%patch0 -p1
%patch1 -p1

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python27} -c 'import setuptools; execfile("setup.py")' build

%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}
%{__python27} -c 'import setuptools; execfile("setup.py")' install --skip-build --root %{buildroot}

# Create log and var directories
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/%{srcname}-cache
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/%{srcname}-relay
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/%{srcname}-aggregator
%{__mkdir_p} %{buildroot}%{_localstatedir}/lib/%{srcname}

# Install system configuration and init scripts
%{__install} -Dp -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{srcname}-cache
%{__install} -Dp -m0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{srcname}-cache
%{__install} -Dp -m0755 %{SOURCE3} %{buildroot}%{_initrddir}/%{srcname}-relay
%{__install} -Dp -m0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/%{srcname}-relay
%{__install} -Dp -m0755 %{SOURCE5} %{buildroot}%{_initrddir}/%{srcname}-aggregator
%{__install} -Dp -m0644 %{SOURCE6} %{buildroot}%{_sysconfdir}/sysconfig/%{srcname}-aggregator

# Install default configuration files
%{__mkdir_p} %{buildroot}%{_sysconfdir}/%{srcname}
%{__install} -Dp -m0644 conf/carbon.conf.example %{buildroot}%{_sysconfdir}/%{srcname}/carbon.conf
%{__install} -Dp -m0644 conf/storage-schemas.conf.example %{buildroot}%{_sysconfdir}/%{srcname}/storage-schemas.conf

# Create transient files in buildroot for ghosting
%{__mkdir_p} %{buildroot}%{_localstatedir}/lock/subsys
%{__touch} %{buildroot}%{_localstatedir}/lock/subsys/%{srcname}-cache
%{__touch} %{buildroot}%{_localstatedir}/lock/subsys/%{srcname}-relay
%{__touch} %{buildroot}%{_localstatedir}/lock/subsys/%{srcname}-aggregator

%{__mkdir_p} %{buildroot}%{_localstatedir}/run
%{__touch} %{buildroot}%{_localstatedir}/run/%{srcname}-cache.pid
%{__touch} %{buildroot}%{_localstatedir}/run/%{srcname}-relay.pid
%{__touch} %{buildroot}%{_localstatedir}/run/%{srcname}-aggregator.pid

%pre
%{__getent} group %{srcname} >/dev/null || %{__groupadd} -r %{srcname}
%{__getent} passwd %{srcname} >/dev/null || \
    %{__useradd} -r -g %{srcname} -d %{_localstatedir}/lib/%{srcname} \
    -s /sbin/nologin -c "Carbon cache daemon" %{srcname}
exit 0

%preun
%{__service} %{srcname} stop
exit 0

%postun
if [ $1 = 0 ]; then
  %{__getent} passwd %{srcname} >/dev/null && \
      %{__userdel} -r %{srcname} 2>/dev/null
fi
exit 0

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{srcname}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{srcname}-%{version}
[ "%{_builddir}/%{srcname}" != "/" ] && %__rm -rf %{_builddir}/%{srcname}

%files
%defattr(-,root,root,-)
%doc LICENSE conf/*

/opt/graphite/lib
/opt/graphite/bin
/opt/graphite/conf
%{_initrddir}/%{srcname}-cache
%{_initrddir}/%{srcname}-relay
%{_initrddir}/%{srcname}-aggregator

%config %{_sysconfdir}/%{srcname}
%config %{_sysconfdir}/sysconfig/%{srcname}-cache
%config %{_sysconfdir}/sysconfig/%{srcname}-relay
%config %{_sysconfdir}/sysconfig/%{srcname}-aggregator

%attr(-,%srcname,%srcname) %{_localstatedir}/lib/%{srcname}
%attr(-,%srcname,%srcname) %{_localstatedir}/log/%{srcname}-cache
%attr(-,%srcname,%srcname) %{_localstatedir}/log/%{srcname}-relay
%attr(-,%srcname,%srcname) %{_localstatedir}/log/%{srcname}-aggregator

%ghost %{_localstatedir}/lock/subsys/%{srcname}-cache
%ghost %{_localstatedir}/run/%{srcname}-cache.pid
%ghost %{_localstatedir}/lock/subsys/%{srcname}-relay
%ghost %{_localstatedir}/run/%{srcname}-relay.pid
%ghost %{_localstatedir}/lock/subsys/%{srcname}-aggregator
%ghost %{_localstatedir}/run/%{srcname}-aggregator.pid

%changelog
