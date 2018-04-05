%define repo https://github.com/elastic/logstash
%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">' | cut -f1 -d "+" | sed 's/REL_//'`)
%define kibana_prefix /opt/%{name}
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define release_ver 1

%define logstash_prefix /opt/{%name}

%global bindir %{base_install_dir}/bin
%global confdir %{base_install_dir }/%{conf}
%global homedir %{base_install_dir}/com
%global lockfile /var/subsys/%{name}
%global logdir /var/log/%{name}
%global piddir %{_localstatedir}/run/%{name}
%global plugindir %{_datadir}/%{name}
%global sysconfigdir %{_sysconfdir}/sysconfig

Name:           logstash
Version:        %{gitversion}
Release:        %{release_ver}.%{revision}.%{dist}
Summary:        A tool for managing events and logs

Group:          System Environment/Daemons
License:        ASL 2.0
URL:            http://logstash.net
Source1:        logstash.wrapper
Source2:        logstash.logrotate
Source3:        logstash.init
Source4:        logstash.sysconfig

BuildRequires:	rake


%description
A tool for managing events and logs.

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}

%build
cd %{name}-%{version}
rake artifact:tar

%install
cd %{name}-%{version}/build
ls
read ans


%{__mkdir} -p %{buildroot}%{logstash_prefix}/conf
%{__mkdir} -p %{buildroot}%{plugindir}/inputs
%{__mkdir} -p %{buildroot}%{plugindir}/filters
%{__mkdir} -p %{buildroot}%{plugindir}/outputs
/bin/echo "Dummy file due to https://logstash.jira.com/browse/LOGSTASH-1555" >  %{buildroot}%{plugindir}/inputs/dummy.rb

# Wrapper script
%{__mkdir} -p %{buildroot}%{_bindir}
%{__install} -m 755 %{SOURCE1} %{buildroot}%{logstash_prefix}/bin
%{__sed} -i \
  -e "s|@@@NAME@@@|%{name}|g" \
  -e "s|@@@JARPATH@@@|%{jarpath}|g" \
  %{buildroot}%{bindir}/%{name}

# Logs
%{__mkdir} -p %{buildroot}%{logdir}
%{__install} -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Misc
%{__mkdir} -p %{buildroot}%{piddir}

# sysconfig and init
%{__mkdir} -p %{buildroot}%{_initddir}
%{__mkdir} -p %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -m 755 %{SOURCE3} %{buildroot}%{_initddir}/%{name}
%{__install} -m 644 %{SOURCE4} %{buildroot}%{sysconfigdir}/%{name}

# Using _datadir for PLUGINDIR because logstash expects a structure like logstash/{inputs,filters,outputs}
%{__sed} -i \
  -e "s|@@@NAME@@@|%{name}|g" \
  -e "s|@@@DAEMON@@@|%{bindir}|g" \
  -e "s|@@@CONFDIR@@@|%{confdir}|g" \
  -e "s|@@@LOCKFILE@@@|%{lockfile}|g" \
  -e "s|@@@LOGDIR@@@|%{logdir}|g" \
  -e "s|@@@PIDDIR@@@|%{piddir}|g" \
  -e "s|@@@PLUGINDIR@@@|%{_datadir}|g" \
  %{buildroot}%{_initddir}/%{name}

%{__sed} -i \
  -e "s|@@@NAME@@@|%{name}|g" \
  -e "s|@@@CONFDIR@@@|%{confdir}|g" \
  -e "s|@@@LOGDIR@@@|%{logdir}|g" \
  -e "s|@@@PLUGINDIR@@@|%{_datadir}|g" \
  %{buildroot}%{sysconfigdir}/%{name}

# Create Home directory
#   See https://github.com/lfrancke/logstash-rpm/issues/5
%{__mkdir} -p %{buildroot}%{homedir}

%pre
# create logstash group
if ! getent group logstash >/dev/null; then
  groupadd -r logstash
fi

# create logstash user
if ! getent passwd logstash >/dev/null; then
  useradd -r -g logstash -d %{homedir} -s /sbin/nologin -c "Logstash service user" logstash
fi

%post
/sbin/chkconfig --add logstash

%preun
if [ $1 -eq 0 ]; then
  /sbin/service logstash stop >/dev/null 2>&1
  /sbin/chkconfig --del logstash
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
# JAR file
%{_javadir}/%{name}.jar

# Config
%config(noreplace) %{confdir}/

# Plugin dir
%dir %{plugindir}/inputs
%dir %{plugindir}/filters
%dir %{plugindir}/outputs
%{plugindir}/inputs/dummy.rb

# Wrapper script
%{bindir}/*

# Logrotate
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

# Sysconfig and init
%{_initddir}/%{name}
%config(noreplace) %{sysconfigdir}/*

%defattr(-,%{name},%{name},-)
%dir %{logdir}/
%dir %{piddir}/

# Home directory
%dir %{homedir}/

%changelog
