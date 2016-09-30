# https://github.com/utobi/prometheus-rpm
# https://github.com/prometheus/pushgateway
%define debug_package %{nil}

Name:		pushgateway
Version:	0.3.0
Release:	1%{?dist}
Summary:	The pushgateway handles alerts sent by client applications such as the Prometheus server.
Group:		System Environment/Daemons
License:	See the LICENSE file at github.
URL:		https://github.com/prometheus/pushgateway
Source0:	https://github.com/prometheus/pushgateway/releases/download/%{version}/pushgateway-%{version}.linux-amd64.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Requires(pre):  /usr/sbin/useradd
Requires:       daemonize
AutoReqProv:	No

%description

The pushgateway handles alerts sent by client applications such as the Prometheus server. 
It takes care of deduplicating, grouping, and routing them to the correct receiver integration such as email, PagerDuty, or OpsGenie. 
It also takes care of silencing and inhibition of alerts.

%prep
%setup -q -n %{name}-%{version}.linux-amd64

%build
echo

%install
mkdir -vp $RPM_BUILD_ROOT/var/log/prometheus/
mkdir -vp $RPM_BUILD_ROOT/var/run/prometheus
mkdir -vp $RPM_BUILD_ROOT/var/lib/prometheus
mkdir -vp $RPM_BUILD_ROOT/usr/bin
mkdir -vp $RPM_BUILD_ROOT/etc/init.d
mkdir -vp $RPM_BUILD_ROOT/etc/prometheus
mkdir -vp $RPM_BUILD_ROOT/etc/sysconfig

install -m 755 contrib/pushgateway.init $RPM_BUILD_ROOT/etc/init.d/pushgateway
install -m 644 contrib/pushgateway.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/pushgateway
install -m 755 pushgateway-%{version}.linux-amd64/pushgateway $RPM_BUILD_ROOT/usr/bin/pushgateway

%clean

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -s /sbin/nologin \
    -d $RPM_BUILD_ROOT/var/lib/prometheus/ -c "prometheus Daemons" prometheus
exit 0

%post
chgrp prometheus /var/run/prometheus
chmod 774 /var/run/prometheus
chown prometheus:prometheus /var/log/prometheus
chmod 744 /var/log/prometheus

%files
%defattr(-,root,root,-)
/usr/bin/pushgateway
/etc/init.d/pushgateway
%config(noreplace) /etc/sysconfig/pushgateway
