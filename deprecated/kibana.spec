%define repo https://github.com/elastic/kibana
%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">' | cut -f1 -d "+" | sed 's/REL_//'`)
%define kibana_prefix /opt/%{name}
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1`)
%global release 1
%define kibana_prefix /opt/%{name}

Name:     kibana
Version:  %{gitversion}
Release:  %{release}.%{revision}.%{?dist}
Summary:  Explore & Visualize Your Data
Group:    Applications/Internet
License:  ASL 2.0
URL:      https://www.elastic.co/products/%{name}
Source1:  kibana-sysconfig
Source2:  kibana-logrotate
Source3:  kibana.service
BuildRequires: systemd
Requires: nodejs
Provides: kibana 
%{?systemd_requires}

%description
Explore & Visualize Your Data

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
%__rm -fr node

%install
cd %{name}-%{version}

%__mkdir_p %{buildroot}%{kibana_prefix}%{_sysconfdir}
%__mkdir_p %{buildroot}%{_sysconfdir}
%__mkdir_p %{buildroot}%{_sysconfdir}/sysconfig
%__mkdir_p %{buildroot}%{_localstatedir}/log/%{name}
%__mkdir_p %{buildroot}%{_unitdir}
%__mkdir_p %{buildroot}/var/log/%{name}

%__ln_s -f %{kibana_prefix} %{buildroot}%{_sysconfdir}/%{name}

%{__install} -m 644 config/kibana.yml %{buildroot}%{kibana_prefix}%{_sysconfdir}/%{name}.yml
%{__install} -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%{__install} -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service
%__cp -R * %{buildroot}%{kibana_prefix}/

%pre -p /bin/sh
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || useradd -r -g %{name} -d %{kibana_prefix} -s /sbin/nologin -c "Kibana User" %{name}

%post -p /bin/sh
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun -p /bin/sh
%systemd_postun_with_restart %{name}.service 
if [ $1 -eq 0 ] ; then
  getent passwd %{name} > /dev/null
  if [ "$?" == "0" ] ; then
    userdel %{name}
  fi

  getent group %{name} >/dev/null
  if [ "$?" == "0" ] ; then
    groupdel %{name}
  fi
fi

exit

%files
%defattr(-,%{name},%{name},-)
%dir %config(noreplace) %{_sysconfdir}/sysconfig
%dir %config(noreplace) %{kibana_prefix}%{_sysconfdir}
%dir %attr(0755, kibana, kibana) /var/log/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{kibana_prefix}%{_sysconfdir}/%{name}.yml
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%dir %{kibana_prefix}
%{kibana_prefix}/*
%{_sysconfdir}/%{name}
%{_unitdir}/%{name}.service
%{_sysconfdir}/%{name}

%changelog
