%global vendorname puppetlabs
%global realversion 4.1.2
%global rpmversion 4.1.2
%global user puppet
%global group puppet

%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7 || 0%{?amzn} >= 1
%global rubylibdir   %(ruby -rrbconfig -e 'puts RbConfig::CONFIG["vendorlibdir"]')
%else
%global rubylibdir   %(ruby -rrbconfig -e 'puts RbConfig::CONFIG["sitelibdir"]')
%endif

%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%global _with_systemd 1
%else
%global _with_systemd 0
%endif

%global vendor_dir /opt/%{vendorname}
%global _app_bindir %{vendor_dir}/server/apps/%{name}/bin
%global _sym_bindir %{vendor_dir}/server/bin
%global _ux_bindir %{vendor_dir}/bin
%global _app_logdir %{_localstatedir}/log/%{name}
%global _app_rundir %{_localstatedir}/run/%{name}
%global _app_libdir %{_localstatedir}/lib/%{name}
%global _app_prefix %{vendor_dir}/server/apps/%{name}
%global _app_data %{vendor_dir}/server/data/%{name}
%global _projconfdir %{_sysconfdir}/%{vendorname}/%{name}


%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%global _with_systemd 1
%else
%global _with_systemd 0
%endif

# Use the alternate locations for things.
%define __jar_repack     0
Name:             puppetdb
Version:          4.1.2
Release:          1.%{?dist}
Summary:          Puppet Labs - puppetdb
Vendor:           Puppet Labs <info@puppetlabs.com>
License:          ASL 2.0
URL:              http://puppetlabs.com
Source0:          %{name}-%{realversion}.tar.gz
Source1:	  %{name}-logback.xml
Source2:          %{name}-request-logging.xml
Source3:          %{name}-config.ini
Source4:          %{name}-database.ini
Source5:          %{name}-jetty.ini
Source6:          %{name}-repl.ini
Group:            System Environment/Daemons
BuildArch:        noarch
BuildRequires:    ruby
BuildRequires:    /usr/sbin/useradd
%if %{_with_systemd}
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
BuildRequires:    systemd
%else
Requires:         chkconfig
%endif
Requires:         jdk 
Requires:	      postgresql95-libs postgresql95 postgresql95-contrib postgresql95-server
Requires:         net-tools
Requires:         puppet >= 3.8.1
Requires:         puppet < 5.0.0


%description
Puppet-integrated catalog and fact storage (puppetdb 4.1.2)
%package termini
Group: Development/Libraries
Summary: Termini for puppetdb
Requires: puppet

%description termini
Termini for puppetdb
Contains terminus for:
  puppetdb (version 4.1.2)

%prep
%setup -q -n %{name}-%{realversion}

%build

%install

rm -rf $RPM_BUILD_ROOT
install -d -m0755 %{buildroot}%{vendor_dir}
install -d -m0755 %{buildroot}%{_app_bindir}
install -d -m0755 %{buildroot}%{_sym_bindir}
install -d -m0755 %{buildroot}%{_ux_bindir}
install -d -m0755 %{buildroot}%{_app_logdir}
install -d -m0755 %{buildroot}%{_app_rundir}
install -d -m0755 %{buildroot}%{_app_libdir}
install -d -m0755 %{buildroot}%{_app_prefix}
install -d -m0755 %{buildroot}%{_app_data}
install -d -m0755 %{buildroot}%{_projconfdir}
install -d -m0755 %{buildroot}%{_bindir}

sed -i -e 's|/var/log/puppetlabs/puppetdb/|/var/log/puppetdb/|g' $RPM_BUILD_DIR/%{name}-%{version}/ext/redhat/init
sed -i -e 's|/var/run/puppetlabs/puppetdb/|/var/run/puppetdb/|g' $RPM_BUILD_DIR/%{name}-%{version}/ext/redhat/init

env EZ_VERBOSE=1 DESTDIR=%{buildroot} prefix=%{_prefix} app_prefix=%{_app_prefix} app_data=%{_app_data} confdir=%{_sysconfdir} bindir=%{_app_bindir} symbindir=%{_sym_bindir} rundir=%{_app_rundir} rubylibdir=%{rubylibdir} bash install.sh install_redhat
%if %{_with_systemd}
env EZ_VERBOSE=1 DESTDIR=%{buildroot} prefix=%{_prefix} app_prefix=%{_app_prefix} app_data=%{_app_data} confdir=%{_sysconfdir} bindir=%{_app_bindir} symbindir=%{_sym_bindir} rundir=%{_app_rundir} defaultsdir=%{_sysconfdir}/sysconfig unitdir=%{_unitdir} bash install.sh systemd_redhat
%else
env EZ_VERBOSE=1 DESTDIR=%{buildroot} prefix=%{_prefix} app_prefix=%{_app_prefix} app_data=%{_app_data} confdir=%{_sysconfdir} bindir=%{_app_bindir} symbindir=%{_sym_bindir} rundir=%{_app_rundir} defaultsdir=%{_sysconfdir}/sysconfig initdir=%{_initrddir} bash install.sh sysv_init_redhat
%endif

%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7 || 0%{?sles_version} >= 12
env EZ_VERBOSE=1 DESTDIR=%{buildroot} confdir=%{_sysconfdir} bash install.sh logrotate
%else
env EZ_VERBOSE=1 DESTDIR=%{buildroot} confdir=%{_sysconfdir} bash install.sh logrotate_legacy
%endif
env EZ_VERBOSE=1 DESTDIR=%{buildroot} rubylibdir=%{rubylibdir} prefix=%{_prefix} bash install.sh termini

install -m0644 %{SOURCE1} %{buildroot}%{_projconfdir}/logback.xml
install -m0644 %{SOURCE2} %{buildroot}%{_projconfdir}/request-logging.xml
install -m0644 %{SOURCE3} %{buildroot}%{_projconfdir}/conf.d/config.ini
install -m0644 %{SOURCE4} %{buildroot}%{_projconfdir}/conf.d/database.ini
install -m0644 %{SOURCE5} %{buildroot}%{_projconfdir}/conf.d/jetty.ini
install -m0644 %{SOURCE6} %{buildroot}%{_projconfdir}/conf.d/repl.ini
%__ln_s %{_app_bindir}%{name} %{buildroot}%{_bindir}/%{name}
sed -i -e 's|/opt/puppetlabs/server/bin/puppetdb ssl-setup|#/opt/puppetlabs/server/bin/puppetdb ssl-setup|g' %{buildroot}%{_app_prefix}/scripts/install.sh

rm -rf /var/tmp/%{name}
cp -R $RPM_BUILD_ROOT /var/tmp/%{name}


%clean
rm -rf $RPM_BUILD_ROOT

%pre
# Note: changes to this section of the spec may require synchronisation with the
# install.sh source based installation methodology.
#
# Add puppetdb group
getent group puppetdb > /dev/null || \
  groupadd -r puppetdb || :
# Add puppetdb user
if getent passwd puppetdb > /dev/null; then
  usermod --gid puppetdb --home %{_app_data} \
  --comment "puppetdb daemon" puppetdb || :
else
  useradd -r --gid puppetdb --home %{_app_data} --shell $(which nologin) \
    --comment "puppetdb daemon"  puppetdb || :
fi
if rpm -q puppetdb | grep ^puppetdb-2.* > /dev/null && [ $1 -eq 2 ] ; then tar -czf /tmp/puppetdb-upgrade-config-files.tgz -C /etc/puppetdb/conf.d config.ini database.ini jetty.ini ; fi

%preun
%if %{_with_systemd}
%systemd_preun puppetdb.service
%else
# If this is an uninstall (as opposed to an upgrade) then
#  we want to shut down and disable the service.
if [ "$1" = "0" ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi
%endif

%postun
%if %{_with_systemd}
%systemd_postun_with_restart puppetdb.service
%else
# Remove the rundir if this is an uninstall (as opposed to an upgrade)...
if [ "$1" = "0" ]; then
    rm -rf %{_app_rundir} || :
fi

# Only restart it if it is running
if [ "$1" = "1" ] ; then
    /sbin/service %{name} condrestart >/dev/null 2>&1
fi
%endif

%post
%{_app_prefix}/scripts/install.sh postinst_redhat
%if %{_with_systemd}
# Reload the systemd units
systemctl daemon-reload >/dev/null 2>&1 || :
%systemd_post puppetdb.service
%else
# If this is an install (as opposed to an upgrade)...
if [ "$1" = "1" ]; then
    # Register the puppetdb service
    /sbin/chkconfig --add %{name}
fi
%endif
%{_chown} -R %{name}:%{group} %{vendor_dir}
%{_chown} -R %{name}:%{group} %{_app_bindir}
%{_chown} -R %{name}:%{group} %{_sym_bindir}
%{_chown} -R %{name}:%{group} %{_ux_bindir}
%{_chown} -R %{name}:%{group} %{_app_logdir}
%{_chown} -R %{name}:%{group} %{_app_rundir}
%{_chown} -R %{name}:%{group} %{_app_libdir}



%files
%defattr(-, root, root)
%dir %{_projconfdir}
%doc ext/docs
%dir %{_app_prefix}
%if %{_with_systemd}
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%else
%{_initrddir}/%{name}
%endif
%dir %{_sysconfdir}/%{vendorname}/%{name}
%dir %{_sysconfdir}/%{vendorname}/%{name}/conf.d
%config(noreplace) %{_sysconfdir}/%{vendorname}/%{name}/bootstrap.cfg
%config(noreplace) %{_sysconfdir}/%{vendorname}/%{name}/logback.xml
%config(noreplace) %{_sysconfdir}/%{vendorname}/%{name}/request-logging.xml
%config(noreplace) %{_sysconfdir}/%{vendorname}/%{name}/conf.d/config.ini
%config(noreplace) %{_sysconfdir}/%{vendorname}/%{name}/conf.d/database.ini
%config(noreplace) %{_sysconfdir}/%{vendorname}/%{name}/conf.d/jetty.ini
%config(noreplace) %{_sysconfdir}/%{vendorname}/%{name}/conf.d/repl.ini
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_app_bindir}/%{name}
%{_app_prefix}
%{_sym_bindir}/%{name}
%{_ux_bindir}/%{name}
%{_bindir}/%{name}

%defattr(-, %{name}, %{name}, 0755)
%dir %attr(0770, %{name}, %{name}) %{_app_logdir}
%dir %attr(0770, %{name}, %{name}) %{_app_libdir}
%dir %attr(0770, %{name}, %{name}) %{_app_rundir}
%dir %attr(0770, %{name}, %{name}) %{_app_data}

%files termini
%defattr(-, root, root)
%{rubylibdir}/puppet/indirector/node/puppetdb.rb
%{rubylibdir}/puppet/indirector/facts/puppetdb_apply.rb
%{rubylibdir}/puppet/indirector/facts/puppetdb.rb
%{rubylibdir}/puppet/indirector/catalog/puppetdb.rb
%{rubylibdir}/puppet/indirector/resource/puppetdb.rb
%{rubylibdir}/puppet/util/puppetdb/command.rb
%{rubylibdir}/puppet/util/puppetdb/command_names.rb
%{rubylibdir}/puppet/util/puppetdb/config.rb
%{rubylibdir}/puppet/util/puppetdb/http.rb
%{rubylibdir}/puppet/util/puppetdb/char_encoding.rb
%{rubylibdir}/puppet/util/puppetdb/atom.rb
%{rubylibdir}/puppet/util/puppetdb.rb
%{rubylibdir}/puppet/reports/puppetdb.rb
%{rubylibdir}/puppet/face/node/deactivate.rb
%{rubylibdir}/puppet/face/node/status.rb
%{rubylibdir}/puppet/functions/puppetdb_query.rb
