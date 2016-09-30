%define repo https://github.com/elastic/elasticsearch
%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">' | cut -f1 -d "+" | sed 's/REL_//'`)
%define kibana_prefix /opt/%{name}
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1
%define build_path distribution/rpm/build/packaging
%global es_prefix /opt/%{name}


Name:           elasticsearch
Version:        %{gitversion}
Release:        %{rel_version}.%{revision}.%{dist}
Summary:        A distributed, highly available, RESTful search engine

Group:          System Environment/Daemons
License:        ASL 2.0
URL:            http://www.elasticsearch.com
Source5:        init.d-elasticsearch
Source1:        logrotate.d-elasticsearch
Source2:        config-logging.yml
Source3:        sysconfig-elasticsearch
Source4:        tmpfiles.d-elasticsearch

BuildArch:      noarch
BuildRequires:	gradle213 jdk
Requires:       jdk
Requires:       lucene >= 4.10.4
Requires:       lucene-contrib >= 4.10.4

%description
A distributed, highly available, RESTful search engine

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
source /etc/profile
source /etc/profile.d/jdk.sh

%build
cd %{name}-%{version}
/opt/gradle213/bin/gradle assemble
/opt/gradle213/bin/gradle buildModules

%install
cd %{name}-%{version}
/opt/gradle213/bin/gradle installDist 

%__mkdir_p %{buildroot}%{_localstatedir}/log/%{name}
%__mkdir_p %{buildroot}%{_sysconfdir}/rc.d/init.d
%__mkdir_p %{buildroot}%{_sysconfdir}/sysconfig
%__mkdir_p %{buildroot}%{_localstatedir}/run/elasticsearch
%__mkdir_p %{buildroot}%{_localstatedir}/lock/subsys/elasticsearch


%__install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}/logging.yml
%__install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/elasticsearch
%__install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/elasticsearch
%__install -m 755 %{SOURCE5} %{buildroot}%{_sysconfdir}/rc.d/init.d/elasticsearch
%__install -m 755 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/elasticsearch
install -D -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/tmpfiles.d/elasticsearch.conf

%pre
# create elasticsearch group
if ! getent group elasticsearch >/dev/null; then
    groupadd -r elasticsearch
fi

# create elasticsearch user
if ! getent passwd elasticsearch >/dev/null; then
    useradd -r -g elasticsearch -d %{es_prefix}/%{name} -s /sbin/nologin -c "You know, for search" elasticsearch
fi

%post
/sbin/chkconfig --add elasticsearch

%preun
if [ $1 -eq 0 ]; then
  /sbin/service elasticsearch stop >/dev/null 2>&1
  /sbin/chkconfig --del elasticsearch
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_sysconfdir}/rc.d/init.d/elasticsearch
%config(noreplace) %{_sysconfdir}/sysconfig/elasticsearch
%{_sysconfdir}/logrotate.d/elasticsearch
%{_sysconfdir}/tmpfiles.d/elasticsearch.conf
%dir %{es_prefix}/elasticsearch
%{es_prefix}/elasticsearch/bin/*
%{es_prefix}/elasticsearch/lib/%{name}-1.5.2.redhat-1.jar
%dir %{es_prefix}/elasticsearch/plugins
%config(noreplace) %{_sysconfdir}/elasticsearch
%doc LICENSE.txt  NOTICE.txt  README.textile
%defattr(-,elasticsearch,elasticsearch,-)
%dir %{_localstatedir}/lib/elasticsearch
%{_localstatedir}/run/elasticsearch
%dir %{_localstatedir}/log/elasticsearch


%changelog
