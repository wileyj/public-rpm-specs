%define repo https://github.com/puppetlabs/marionette-collective
%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1

%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7 || 0%{?amzn} >= 1
%global mco_libdir   %(ruby -rrbconfig -e 'puts RbConfig::CONFIG["vendorlibdir"]')
%global _with_systemd 0
%else
%global mco_libdir   %(ruby -rrbconfig -e 'puts RbConfig::CONFIG["sitelibdir"]')
%global _with_systemd 1
%endif

%global mco_prefix /opt/mcollective
%global mco_bindir %{mco_prefix}/bin
%global mco_sbindir %{mco_prefix}/sbin
%global mco_confdir %{mco_prefix}/etc
%global mco_plugindir %{mco_prefix}/plugins

Summary:        Application Server for hosting Ruby code on any capable middleware
Name:           mcollective
Version:        %{gitversion}
Release: %{rel_version}.%{revision}.%{dist}
Group:          System Environment/Daemons
License:        ASL 2.0
URL:            http://puppetlabs.com/mcollective/introduction/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  ruby >= 1.8
Requires:       mcollective-common = %{version}-%{release}
Packager:       Puppet Labs <info@puppetlabs.com>
BuildArch:      noarch

%if 0%{?_with_systemd}
# Required for %%post, %%preun, %%postun
Requires:       systemd
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
BuildRequires:  systemd
%else
BuildRequires:  systemd-units
%endif
%else
# Required for %%post and %%preun
Requires:       chkconfig
# Required for %%preun and %%postun
Requires:       initscripts
%endif

%description
The Marionette Collective:

Server for the mcollective Application Server

%package common
Summary:        Common libraries for the mcollective clients and servers
Group:          System Environment/Libraries
Requires:       ruby >= 1.8
Requires:       rubygems >= 1.3.7
Requires:       rubygem-stomp
Requires:       rubygem-json

%description common
The Marionette Collective:

Common libraries for the mcollective clients and servers

%package client
Summary:        Client tools for the mcollective Application Server
Requires:       mcollective-common = %{version}-%{release}
Group:          Applications/System

%description client
The Marionette Collective:

Client tools for the mcollective Application Server

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
rm -rf %{buildroot}
%__mkdir_p %{buildroot}%{mco_bindir}
%__mkdir_p %{buildroot}%{mco_confdir}
%__mkdir_p %{buildroot}%{mco_codedir}
%__mkdir_p %{buildroot}%{_sbindir}
%__mkdir_p %{buildroot}%{_bindir}
ruby install.rb --destdir=%{buildroot} --no-rdoc --sitelibdir=%{mco_libdir} --plugindir=%{mco_plugindir} --configdir=%{mco_confdir} --bindir=%{mco_bindir} --sbindir=%{mco_sbindir}


%if 0%{?_with_systemd}
%{__install} -d -m0755  %{buildroot}%{_unitdir}
%{__install} -m0644 ext/redhat/mcollective.service %{buildroot}%{_unitdir}/mcollective.service
%else
%{__install} -d -m0755  %{buildroot}%{_initrddir}
%if 0%{?suse_version}
%{__install} -m0755 mcollective.init %{buildroot}%{_initrddir}/%{name}
%else
%{__install} -m0755 ext/redhat/mcollective.init %{buildroot}%{_initrddir}/%{name}
%endif
%endif

%{__install} -d -m0755  %{buildroot}%{mco_confdir}/plugin.d
%{__install} -d -m0755  %{buildroot}%{mco_confdir}/ssl/clients
%{__ln_s} %{mco_bindir}/mco %{buildroot}%{_bindir}/mco
%{__ln_s} %{mco_sbin}/mco %{buildroot}%{_sbindir}/mcollectived

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%post
%if 0%{?_with_systemd}
if [ $1 -eq 1 ] ; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
%else
/sbin/chkconfig --add mcollective || :
%endif

%postun
%if 0%{?_with_systemd}
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart mcollective.service >/dev/null 2>&1 || :
fi
%else
if [ "$1" -ge 1 ]; then
  /sbin/service mcollective condrestart &>/dev/null || :
fi
%endif

%preun
%if 0%{?_with_systemd}
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable mcollective.service > /dev/null 2>&1 || :
    /bin/systemctl stop mcollective.service > /dev/null 2>&1 || :
fi
%else
if [ "$1" = 0 ] ; then
  /sbin/service mcollective stop > /dev/null 2>&1
  /sbin/chkconfig --del mcollective || :
fi
%endif

%files common
%defattr(-, root, root, 0755)
%{mco_libdir}/mcollective.rb
%{mco_libdir}/mcollective
%dir %{mco_confdir}
%dir %{mco_confdir}/ssl
%config %{mco_confdir}/*.erb

%files client
%defattr(-, root, root, 0755)
%attr(0755, root, root)%{mco_bindir}/mco
%{_bindir}/mco
%config(noreplace)%{mco_confdir}/client.cfg

%files
%defattr(-, root, root, 0755)
%attr(0755, root, root)%{mco_sbindir}/mcollectived
%{_sbindir}/mcollectived
%if 0%{?_with_systemd}
%{_unitdir}/mcollective.service
%else
%{_initrddir}/%{name}
%endif
%config(noreplace)%{mco_confdir}/server.cfg
%config(noreplace)%{mco_confdir}/facts.yaml
%dir %{mco_confdir}/ssl/clients
%config(noreplace)%{mco_confdir}/plugin.d

%changelog

