%define repo https://github.com/elastic/beats
%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">' | cut -f1 -d "+" | sed 's/REL_//'`)
%define kibana_prefix /opt/%{name}
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)

%define _binaries_in_noarch_packages_terminate_build 0
%global _binaries_in_noarch_packages_terminate_build 0

Name:           filebeat
Version:        1.0.1
Release:        10.1
Summary:        A tool for managing events and logs
License:        Apache-2.0
Group:          System/Monitoring
URL:            https://github.com/elastic/filebeat
#Source:         https://download.elastic.co/beats/filebeat/filebeat-%{version}-x86_64.tar.gz
Source:         filebeat-%{version}-x86_64.tar.bz2
Source1:        filebeat.service
Source2:        filebeat.init
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       logrotate
Requires(pre):  pwdutils

# needed for brp-check-bytecode-version (jar, fastjar would do as well)
BuildRequires:	unzip

%if 0%{?suse_version} >= 1210
BuildRequires:  systemd-rpm-macros
%{?systemd_requires}
%bcond_without  systemd
%else
%bcond_with     systemd
%endif

%description
Filebeat is a log data shipper initially based on the Logstash-Forwarder source code. 
Installed as an agent on your servers, Filebeat monitors the log directories or specific 
log files, tails the files, and forwards them either to Logstash for parsing or directly 
to Elasticsearch for indexing.

%prep
%setup -q -n %{name}-%{version}-x86_64

%build


%install
export NO_BRP_CHECK_BYTECODE_VERSION=true

## usr
%{__install} -d -m 755 %{buildroot}%{_sbindir}/
%{__install} -d -m 755 %{buildroot}%{_bindir}/
%{__install} -m 755 filebeat %{buildroot}%{_bindir}/
%{__install} -d -m 755 %{buildroot}/usr/share/%{name}/
%{__install} -m 644 filebeat.template.json %{buildroot}/usr/share/%{name}/

## etc
%{__install} -d -m 755 %{buildroot}%{_sysconfdir}/%{name}/
%{__install} -m 644 filebeat.yml %{buildroot}%{_sysconfdir}/%{name}/

## var
%{__install} -d -m 755 %{buildroot}/var/lib/%{name}/

## service (systemd or sysVinit)
%if %{with systemd}
%{__mkdir} -p %{buildroot}%{_unitdir}
%{__install} -m 444 %{S:1} %{buildroot}%{_unitdir}/%{name}.service
ln -sf /usr/sbin/service %{buildroot}%{_sbindir}/rc%{name}
%else
%{__install} -D -m 755 %{S:2} %{buildroot}%{_initrddir}/%{name}
%{__mkdir} -p %{buildroot}%{_sbindir}
ln -sf %{_initrddir}/%{name} %{buildroot}%{_sbindir}/rc%{name}
%endif



%pre
## Register service systemd
%if %{with systemd}
%service_add_pre %{name}.service
%endif

%post
## fill up sysconfig file
%{fillup_and_insserv -n -y %{name}}

## Register service systemd
%if %{with systemd}
%service_add_post %{name}.service
%endif


cat <<EOF

================================================================================
Please edit filebeat config in:
    /etc/filebeat/filebeat.yml

If you use elasticsearch as output, load the index template before startup filebeat:
curl -XPUT 'http://localhost:9200/_template/filebeat?pretty' -d@/usr/share/filebeat/filebeat.template.json
================================================================================

EOF


%preun
## Stop service (systemd or sysVinit)
%if %{with systemd}
%service_del_preun %{name}.service
%else
%stop_on_removal
%endif


%postun
## no auto restart on update
export DISABLE_RESTART_ON_UPDATE=1

## Unregister service (systemd or sysVinit)
%if %{with systemd}
%service_del_postun %{name}.service
%else
%insserv_cleanup
%endif


%files
%defattr(-,root,root)

%if %{with systemd}
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif

%{_sbindir}/rc%{name}
%{_bindir}/%{name}
%dir /etc/%{name}/
%config(noreplace) /etc/%{name}/filebeat.yml
%dir /usr/share/%{name}
%doc /usr/share/%{name}/*
%dir /var/lib/%{name}


%changelog
