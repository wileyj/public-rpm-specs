%define repo https://github.com/Graylog2/graylog2-server
%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="css-truncate-target"' | head -1 |  tr -d '\\-</span class="css-truncate-target">'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1

%define base_install_dir %{_javadir}{%name}
%define __jar_repack %{nil}
Name:           graylog2-server
Version:        0.20.2
Release:        1.%{dist}
Summary:        graylog2-server
Group:          System Environment/Daemons
License:        ASL 2.0
Vendor: %{vendor}
Packager: %{packager}
URL:            http://www.graylog2.org
Source0:        graylog2-server-0.20.2.tgz
Source1:        init.d-%{name}
Source2:        sysconfig-%{name}
Source3:        log4j.xml
Source4:	logrotate-%{name}
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Provides:	graylog graylog2
Requires:       jpackage-utils
Requires: 	logrotate

Requires(post): chkconfig initscripts
Requires(pre):  chkconfig initscripts
Requires(pre):  shadow-utils

%description
A distributed, highly available, RESTful search engine

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
%__rm -rf $RPM_BUILD_ROOT
# I know we can use -p to create the root directory, but this is more to
# keep track of the required dir
%__mkdir_p %{buildroot}/opt/graylog2/server
%__mkdir_p %{buildroot}/opt/graylog2/server/bin
%__install -p -m 755 graylog2-server.jar %{buildroot}/opt/graylog2/server
%__install -p -m 755 bin/graylog2ctl %{buildroot}/opt/graylog2/server/bin/

# config
%__mkdir_p %{buildroot}%{_sysconfdir}/graylog2
%__install -m 644 graylog2.conf.example %{buildroot}%{_sysconfdir}/graylog2/server.conf


# logs
%__mkdir_p %{buildroot}%{_localstatedir}/log/graylog2/web
%__mkdir_p %{buildroot}/opt/graylog2/server/log
%__install} -p -m 644 %{SOURCE3} %{buildroot}/opt/graylog2/server/log4j.xml

# plugins
%__mkdir_p %{buildroot}/opt/graylog2/server/plugin/alarm_callbacks
%__mkdir_p %{buildroot}/opt/graylog2/server/plugin/filters
%__mkdir_p %{buildroot}/opt/graylog2/server/plugin/initializers
%__mkdir_p %{buildroot}/opt/graylog2/server/plugin/inputs
%__mkdir_p %{buildroot}/opt/graylog2/server/plugin/ouput
%__mkdir_p %{buildroot}/opt/graylog2/server/plugin/transports

# sysconfig and init
%__mkdir_p %{buildroot}%{_sysconfdir}/sysconfig
%__mkdir_p %{buildroot}%{_sysconfdir}/init.d
%__mkdir_p %{buildroot}%{_sysconfdir}/logrotate.d
%__install -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/init.d/%{name}
%__install -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%__install -m 644 %{SOURCE4}  %{buildroot}%{_sysconfdir}/logrotate.d/%name

#Docs and other stuff
%__install -p -m 644 COPYING %{buildroot}/opt/graylog2/server
%__install -p -m 644 build_date %{buildroot}/opt/graylog2/server
%__install -p -m 644 README.markdown %{buildroot}/opt/graylog2/server
%__mkdir_p %{buildroot}/var/run/graylog2
%pre
# create graylog2 group
if ! getent group graylog2 >/dev/null; then
        groupadd -r graylog2
fi

# create graylog2 user
if ! getent passwd graylog2 >/dev/null; then
        useradd -r -g graylog2 -d %{_javadir}/%{name} \
            -s /sbin/nologin -c "Party Gorilla" graylog2
fi

%post
/sbin/chkconfig --add graylog2-server

%preun
if [ $1 -eq 0 ]; then
  /sbin/service/graylog2 stop >/dev/null 2>&1
  /sbin/chkconfig --del graylog2-server
fi

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root,-)
%{_sysconfdir}/init.d/graylog2-server
%config(noreplace) %{_sysconfdir}/sysconfig/graylog2-server
%dir /opt/graylog2/server
%dir /opt/graylog2/server/bin
%dir /opt/graylog2/server/log
%dir /opt/graylog2/server/plugin
%config(noreplace) %{_sysconfdir}/graylog2/server.conf
%config(noreplace) %{_sysconfdir}/graylog2
%config(noreplace) %{_sysconfdir}/logrotate.d/%name
%doc README.markdown
%defattr(-,graylog2,graylog2,-)
/opt/graylog2/server/graylog2-server.jar
/opt/graylog2/server/bin/graylog2ctl
/opt/graylog2/server/log4j.xml
/opt/graylog2/server/COPYING
/opt/graylog2/server/build_date
/opt/graylog2/server/README.markdown
/var/run/graylog2
%dir %{_localstatedir}/log/graylog2

%changelog
