# https://github.com/utobi/prometheus-rpm
# https://github.com/prometheus/graphite_exporter


%define debug_package %{nil}

Name:		graphite-exporter
Version:	0.1.0
Release:	1%{?dist}
Summary:	Prometheus exporter for receiving graphite metrics.
Group:		System Environment/Daemons
License:	See the LICENSE file at github.
URL:		https://github.com/prometheus/graphite_exporter
Source0:        https://github.com/prometheus/graphite_exporter/releases/download/%{version}/graphite_exporter-%{version}.linux-amd64.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Requires(pre):  /usr/sbin/useradd
Requires:       daemonize
AutoReqProv:	No

%description

Prometheus exporter for machine metrics, written in Go with pluggable metric collectors.

%prep
%setup -q -n graphite_exporter-%{version}.linux-amd64

%build
echo

%install
mkdir -vp $RPM_BUILD_ROOT/var/log/prometheus/
mkdir -vp $RPM_BUILD_ROOT/var/run/prometheus
mkdir -vp $RPM_BUILD_ROOT/var/lib/prometheus
mkdir -vp $RPM_BUILD_ROOT/usr/bin
mkdir -vp $RPM_BUILD_ROOT/etc/init.d
mkdir -vp $RPM_BUILD_ROOT/etc/sysconfig
install -m 755 graphite_exporter $RPM_BUILD_ROOT/usr/bin/graphite_exporter
install -m 755 contrib/graphite_exporter.init $RPM_BUILD_ROOT/etc/init.d/graphite_exporter
install -m 644 contrib/graphite_exporter.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/graphite_exporter

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
/usr/bin/graphite_exporter
/etc/init.d/graphite_exporter
%config(noreplace) /etc/sysconfig/graphite_exporter
/var/run/prometheus
/var/log/prometheus
