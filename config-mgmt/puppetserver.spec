%global realname puppetserver
%global realversion 2.4.0
%global rpmversion 2.4.0

# Application bin dir.
%global _app_bindir /opt/puppetlabs/server/apps/puppetserver/bin
# Bin dir where convenience symlinks go.
%global _sym_bindir /opt/puppetlabs/server/bin
# Bin dir the end user adds to their PATH
%global _ux_bindir /opt/puppetlabs/bin
# Log directory
%global _app_logdir /var/log/puppetlabs/puppetserver
# Run directory, PID files go here
%global _app_rundir /var/run/puppetlabs/puppetserver

# Puppet Installation Layout
# https://github.com/puppetlabs/puppet-specifications/blob/af82509/file_paths.md
%global _app_prefix /opt/puppetlabs/server/apps/puppetserver
%global _app_data /opt/puppetlabs/server/data/puppetserver
%global _projconfdir /etc/puppetlabs/puppetserver

# java 1.8.0 is available starting in fedora 20 and el 6
%if 0%{?fedora} >= 20 || 0%{?rhel} >= 6
%global open_jdk          jdk
%else
%global open_jdk          jdk
%endif

%global rubylibdir        /opt/puppetlabs/puppet/lib/ruby/vendor_ruby

%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%global _with_systemd 1
%else
%global _with_systemd 0
%endif

# Use the alternate locations for things.
%global _sysconfdir      /etc
%global _prefix          /opt/puppetlabs/server/apps/puppetserver
%global _rundir          /var/run

%define __jar_repack     0

Name:             puppetserver
Version:          2.4.0
Release:          1.%{?dist}
BuildRoot:        %{_tmppath}/%{realname}-%{version}-%{release}-root-%(%{__id_u} -n)

Summary:          Puppet Labs - puppetserver
Vendor:           Puppet Labs <info@puppetlabs.com>
License:          ASL 2.0

URL:              http://puppetlabs.com
Source0:          %{name}-%{realversion}.tar.gz

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

Requires:         %{open_jdk}
# net-tools is required for netstat usage in service unit file
# See: https://tickets.puppetlabs.com/browse/SERVER-338
Requires:         net-tools

Requires:         puppet-agent >= 1.5.0


%description
Puppet Server (clojure 1.7.0,puppetserver 2.4.0,trapperkeeper-webserver-jetty9 1.5.9)

%prep
%setup -q -n %{name}-%{realversion}

%build

%install

rm -rf $RPM_BUILD_ROOT

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


%clean
rm -rf $RPM_BUILD_ROOT

%pre
# Note: changes to this section of the spec may require synchronisation with the
# install.sh source based installation methodology.
#
# Add puppet group
getent group puppet > /dev/null || \
  groupadd -r puppet || :
# Add puppet user
if getent passwd puppet > /dev/null; then
  usermod --gid puppet --home %{_app_data} \
  --comment "puppetserver daemon" puppet || :
else
  useradd -r --gid puppet --home %{_app_data} --shell $(which nologin) \
    --comment "puppetserver daemon"  puppet || :
fi

%post
%{_app_prefix}/scripts/install.sh postinst_redhat
%if %{_with_systemd}
# Reload the systemd units
systemctl daemon-reload >/dev/null 2>&1 || :
%systemd_post puppetserver.service
%else
# If this is an install (as opposed to an upgrade)...
if [ "$1" = "1" ]; then
    # Register the puppetserver service
    /sbin/chkconfig --add %{name}
fi
%endif

%preun
%if %{_with_systemd}
%systemd_preun puppetserver.service
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
%systemd_postun_with_restart puppetserver.service
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

%files
%defattr(-, root, root)
%dir %attr(0700, puppet, puppet) %{_app_logdir}
%dir %attr(0750, puppet, puppet) %{_projconfdir}
%{_app_prefix}
%if %{_with_systemd}
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%else
%{_initrddir}/%{name}
%endif
%config(noreplace) %{_sysconfdir}/puppetlabs/%{realname}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_app_bindir}/puppetserver
%{_sym_bindir}/puppetserver
%{_ux_bindir}/puppetserver
%dir %attr(0770, puppet, puppet) %{_app_data}
%dir %attr(0755, puppet, puppet) %{_app_rundir}



%changelog
* Tue May 17 2016 Puppet Labs Release <info@puppetlabs.com> -  2.4.0-1
- Build for 2.4.0
