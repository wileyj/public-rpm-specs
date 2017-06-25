%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%define repo https://github.com/statsite/statsite
%define gitversion %(echo `curl %{repo}/releases | grep 'span class="css-truncate-target"' | head -1 |  tr -d '\\-</span class="css-truncate-target">v'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1

Name: statsite
Summary: C Implementation of statsd
Version: %{gitversion}
Release: %{rel_version}.%{revision}.%{?dist}
License: GPLv3
Group: Applications/Internet
URL: %{repo}

BuildRequires: gcc
BuildRequires: make

%description
C implementation of statsd http://armon.github.io/statsite


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
#./bootstrap.sh
./autogen.sh
./configure
make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
cd %{name}-%{version}
%__mkdir -vp %{buildroot}%{_sbindir}
%__mkdir -vp %{buildroot}%{_initrddir}
%__mkdir -vp %{buildroot}%{_sysconfdir}/%{name}
%__mkdir -vp %{buildroot}%{_sysconfdir}/tmpfiles.d
%__mkdir -vp %{buildroot}%{_libexecdir}/%{name}
%__mkdir -vp %{buildroot}%{_var}/run/%{name}
%__mkdir -vp %{buildroot}%{_var}/lib/%{name}

%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7 || 0%{?amzn} >= 1
    %__mkdir -vp %{buildroot}/%{_unitdir}
    %__install -m 644 rpm/%{name}.service %{buildroot}/%{_unitdir}
    %__install -m 644 rpm/%{name}.tmpfiles.conf %{buildroot}/%{_sysconfdir}/tmpfiles.d/%{name}.conf
%else
    %__install -m 755 rpm/%{name}.initscript %{buildroot}%{_initrddir}/%{name}
%endif

%__install -m 755 %{name} %{buildroot}%{_sbindir}
%__install -m 644 rpm/%{name}.conf.example %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
%__cp -pa sinks %{buildroot}%{_libexecdir}/%{name}


%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd  %{name}  >/dev/null || useradd -r -g  %{name} -d /var/lib/%{name} -s /sbin/nologin -c "Statsite user" %{name} 
exit 0

%post
if [ "$1" = 1 ] ; then
    %if 0%{?fedora} >= 17 || 0%{?rhel} >= 7 || 0%{?amzn} >= 1
        %{_sbindir}/systemctl daemon-reload
    %else
        %{_sbindir}/chkconfig --add %{name}
        %{_sbindir}/chkconfig %{name} off
    %endif
fi
exit 0

%postun
if [ "$1" = 1 ] ; then
    %if 0%{?fedora} >= 17 || 0%{?rhel} >= 7 || 0%{?amzn} >= 1
        %{_sbindir}/systemctl restart %{name}.service
    %else
        %{_sbindir}/service %{name} restart
    %endif
    if [ $1 -eq 0 ]; then
        %{_sbindir}/userdel %{name}
    if
fi
exit 0


%preun
if [ $1 -eq 0 ]; then
    %{_sbindir}/service %{name} stop &>/dev/null || :
    %{_sbindir}/chkconfig --del %{name}
fi

%clean
#[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
#[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
#[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
#[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-, root, root, 0755)
%config %{_sysconfdir}/%{name}/%{name}.conf
%attr(755, root, root) %{_sbindir}/%{name}
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7 || 0%{?amzn} >= 1
    %attr(644, root, root) %{_unitdir}/%{name}.service
    %dir /etc/tmpfiles.d
    %attr(644, root, root) /etc/tmpfiles.d/%{name}.conf
%else
    %attr(755, root, root) %{_initrddir}/%{name}
%endif
%dir %{_libexecdir}/%{name}
%dir %{_libexecdir}/%{name}/sinks
%attr(755, %[name}, %{name}) %{_var}/run/%{name}
%attr(755, %{name}, %{name}) %{_var}/lib/%{name}
%attr(755, root, root) %{_libexecdir}/%{name}/sinks/*.py
%attr(755, root, root) %{_libexecdir}/%{name}/sinks/*.rb
%attr(755, root, root) %{_libexecdir}/%{name}/sinks/*.sh
%attr(755, root, root) %{_libexecdir}/%{name}/sinks/*.js

%changelog
