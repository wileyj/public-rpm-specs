# spec from https://github.com/utobi/prometheus-rpm
%define repo https://github.com/prometheus/prometheus
%define common_repo https://github.com/prometheus/common
%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">v'`)
%define revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1
%define app_prefix /opt/%{name}



%define debug_package %{nil}

Name:		prometheus
Version:	1.1.3
Release:	%{rel_version}.%{revision}.%{dist}
Summary:	Prometheus is a systems and service monitoring system. It collects metrics from configured targets at given intervals, evaluates rule expressions, displays the results, and can trigger alerts if some condition is observed to be true.
Group:		System Environment/Daemons
License:	See the LICENSE file at github.
URL:		https://github.com/prometheus/prometheus
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Requires(pre):  /usr/sbin/useradd
Requires:       go
AutoReqProv:	No

%description
Prometheus is a systems and service monitoring system.
It collects metrics from configured targets at given intervals, evaluates
rule expressions, displays the results, and can trigger alerts if
some condition is observed to be true.


%prep
if [ -d %{name}-%{version} ];then
  rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
git clone %{common)repo} %{name}-common-%{version}
cd %{name}-%{version}
git submodule init
git submodule update

%build
cd %{name}-%{version}
make build

%__install -d %{buildroot}%{_localstatedir}/log/prometheus/
%__install -d %{buildroot}%{_localstatedir}/run/prometheus
%__install -d %{buildroot}%{_localstatedir}/lib/prometheus
%__install -d %{buildroot}%{_bindir}
%__install -d %{buildroot}%{_initddir}
%__install -d %{buildroot}%{_sysconfdir}/sysconfig
%__install -d %{buildroot}%{_sysconfdir}
%__install -d %{buildroot}%{app_prefix}
%__install -d %{buildroot}%{app_prefix}%{_sysconfdir}
%__install -d %{buildroot}%{app_prefix}/consoles
%__install -d %{buildroot}%{app_prefix}/console_libraries
%__ln_s -f %{app_prefix}%{_sysconfdir} %{buildroot}%{_sysconfdir}/%{name}

%install
cd %{name}-%{version}
%__install -m 755 contrib/prometheus.init %{buildroot}%{_initddir}
%__install -m 644 contrib/prometheus.rules %{buildroot}/etc/prometheus/prometheus.rules
%__install -m 644 contrib/prometheus.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%__install -m 644 contrib/prometheus.yaml %{buildroot}%{app_prefix}%{_sysconfdir}/%{name}.yaml
%__install -m 755 prometheus %{buildroot}%{_bindir}/%{name}
%__install -m 755 promtool %{buildroot}%{_bindir}/promtool
%__install -m 755 console_libraries/* %{buildroot}%{app_prefix}/console_libraries/
%__install -m 755 consoles/* %{buildroot}%{app_prefix}/consoles/

%clean

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -s /sbin/nologin \
    -d %{buildroot}/var/lib/prometheus/ -c "prometheus Daemons" prometheus
exit 0

%post
chgrp prometheus /var/run/prometheus
chmod 774 /var/run/prometheus
chown prometheus:prometheus /var/log/prometheus
chmod 744 /var/log/prometheus

%files
%defattr(-,root,root,-)
/usr/bin/prometheus
/usr/bin/promtool
%config(noreplace) /etc/prometheus/prometheus.yaml
%config(noreplace) /etc/prometheus/prometheus.rules
/etc/init.d/prometheus
%config(noreplace) /etc/sysconfig/prometheus
/usr/share/prometheus/consoles/aws_elasticache.html
/usr/share/prometheus/consoles/aws_elb.html
/usr/share/prometheus/consoles/aws_redshift-cluster.html
/usr/share/prometheus/consoles/aws_redshift.html
/usr/share/prometheus/consoles/blackbox.html
/usr/share/prometheus/consoles/cassandra.html
/usr/share/prometheus/consoles/cloudwatch.html
/usr/share/prometheus/consoles/haproxy-backend.html
/usr/share/prometheus/consoles/haproxy-backends.html
/usr/share/prometheus/consoles/haproxy-frontend.html
/usr/share/prometheus/consoles/haproxy-frontends.html
/usr/share/prometheus/consoles/haproxy.html
/usr/share/prometheus/consoles/index.html.example
/usr/share/prometheus/consoles/node-cpu.html
/usr/share/prometheus/consoles/node-disk.html
/usr/share/prometheus/consoles/node-overview.html
/usr/share/prometheus/consoles/node.html
/usr/share/prometheus/consoles/prometheus-overview.html
/usr/share/prometheus/consoles/prometheus.html
/usr/share/prometheus/consoles/snmp-overview.html
/usr/share/prometheus/consoles/snmp.html
/usr/share/prometheus/console_libraries/prom.lib
/usr/share/prometheus/console_libraries/menu.lib
%attr(755, prometheus, prometheus)/var/lib/prometheus
/var/run/prometheus
/var/log/prometheus

