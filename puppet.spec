%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7 || 0%{?amzn} >= 1
%global puppet_libdir   %(ruby -rrbconfig -e 'puts RbConfig::CONFIG["vendorlibdir"]')
%else
%global puppet_libdir   %(ruby -rrbconfig -e 'puts RbConfig::CONFIG["sitelibdir"]')
%endif
%global _with_systemd 0
%global realversion 4.3.0
%global rpmversion 4.3.0
%global puppet_bindir /opt/puppetlabs/bin
%global puppet_codedir /etc/puppetlabs/code
%global puppet_confdir /etc/puppetlabs/puppet

%global confdir ext/redhat
%global pending_upgrade_path %{_localstatedir}/lib/rpm-state/puppet
%global pending_upgrade_file %{pending_upgrade_path}/upgrade_pending

Name:           puppet
Version:        %{rpmversion}
Release:        1.%{dist}
Summary:        A network tool for managing many disparate systems
License:        ASL 2.0
Packager:       %{packager}
Vendor:         %{vendor}
URL:            http://puppetlabs.com
Source0:        %{name}.tar.gz
Group:          System Environment/Base
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  facter >= 1.7.0
BuildRequires:  ruby >= 1.8.7
BuildRequires:  hiera >= 2.0.0
BuildRequires:  git
BuildArch:      noarch
Requires:       ruby >= 1.8
Requires:       ruby-shadow
Requires:       rubygem-json
Requires:       facter >= 1.7.0
Requires:       hiera >= 2.0.0
Obsoletes:      hiera-puppet < 1.0.0
Provides:       hiera-puppet >= 1.0.0
Requires:       ruby-augeas
Requires:       shadow-utils

%if 0%{?_with_systemd}
Requires:       systemd
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
BuildRequires:  systemd
%else
BuildRequires:  systemd-units
%endif
%else
Requires:       chkconfig
# Required for %%preun and %%postun
Requires:       initscripts
%endif

%description
Puppet lets you centrally manage every important aspect of your system using a
cross-platform specification language that manages all the separate elements
normally aggregated in different files, like users, cron jobs, and hosts,
along with obviously discrete elements like packages, services, and files.

%package server
Group:          System Environment/Base
Summary:        Server for the puppet system management tool
Requires:       puppet = %{version}-%{release}

%description server
Provides the central puppet server daemon which provides manifests to clients.
The server can also function as a certificate authority and file server.

%prep
%setup -q -n %{name}

%build
git pull
for f in external/nagios.rb relationship.rb; do
  sed -i -e '1d' lib/puppet/$f
done

find examples/ -type f | xargs --no-run-if-empty chmod a-x

%install
rm -rf %{buildroot}
ruby install.rb --destdir=%{buildroot} --quick --no-rdoc --sitelibdir=%{puppet_libdir} --bindir=%{puppet_bindir}
%__mkdir_p %{buildroot}%{puppet_bindir}
%__mkdir_p %{buildroot}%{puppet_confdir}
%__mkdir_p %{buildroot}%{puppet_codedir}
install -d -m0755 %{buildroot}%{puppet_bindir}
install -d -m0755 %{buildroot}%{puppet_codedir}/environments/production/manifests
install -d -m0755 %{buildroot}%{puppet_codedir}/environments/dev/manifests
install -d -m0755 %{buildroot}%{puppet_codedir}/environments/staging/manifests
install -d -m0755 %{buildroot}%{puppet_codedir}/modules
install -d -m0755 %{buildroot}%{_localstatedir}/lib/puppet
install -d -m0755 %{buildroot}%{_localstatedir}/lib/puppet/state
install -d -m0755 %{buildroot}%{_localstatedir}/lib/puppet/reports
install -d -m0755 %{buildroot}%{_localstatedir}/run/puppet
install -d -m0750 %{buildroot}%{_localstatedir}/log/puppet

%if 0%{?_with_systemd}
%{__install} -d -m0755  %{buildroot}%{_unitdir}
install -Dp -m0644 ext/systemd/puppet.service %{buildroot}%{_unitdir}/puppet.service
ln -s %{_unitdir}/puppet.service %{buildroot}%{_unitdir}/puppetagent.service
install -Dp -m0644 ext/systemd/puppetmaster.service %{buildroot}%{_unitdir}/puppetmaster.service
%else
install -Dp -m0644 %{confdir}/client.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/puppet
install -Dp -m0755 %{confdir}/client.init %{buildroot}%{_initrddir}/puppet
install -Dp -m0644 %{confdir}/server.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/puppetmaster
install -Dp -m0755 %{confdir}/server.init %{buildroot}%{_initrddir}/puppetmaster
%endif

install -Dp -m0644 conf/auth.conf %{buildroot}%{puppet_confdir}
install -Dp -m0644 %{confdir}/fileserver.conf %{buildroot}%{puppet_confdir}/fileserver.conf
install -Dp -m0644 conf/puppet.conf %{buildroot}%{puppet_confdir}/puppet.conf
install -Dp -m0644 %{confdir}/logrotate %{buildroot}%{_sysconfdir}/logrotate.d/puppet

install -d %{buildroot}%{_datadir}/%{name}
cp -a ext/ %{buildroot}%{_datadir}/%{name}
rm -rf %{buildroot}%{_datadir}/%{name}/ext/{emacs,vim}
rm -rf %{buildroot}%{_datadir}/%{name}/ext/{gentoo,freebsd,solaris,suse,windows,osx,ips,debian}
rm -f %{buildroot}%{_datadir}/%{name}/ext/redhat/*.init
rm -f %{buildroot}%{_datadir}/%{name}/ext/{build_defaults.yaml,project_data.yaml}
chmod 755 %{buildroot}%{_datadir}/%{name}/ext/regexp_nodes/regexp_nodes.rb

emacsdir=%{buildroot}%{_datadir}/emacs/site-lisp
install -Dp -m0644 ext/emacs/puppet-mode.el $emacsdir/puppet-mode.el
install -Dp -m0644 ext/emacs/puppet-mode-init.el $emacsdir/site-start.d/puppet-mode-init.el

vimdir=%{buildroot}%{_datadir}/vim/vimfiles
install -Dp -m0644 ext/vim/ftdetect/puppet.vim $vimdir/ftdetect/puppet.vim
install -Dp -m0644 ext/vim/syntax/puppet.vim $vimdir/syntax/puppet.vim
install -Dp -m0644 ext/vim/indent/puppet.vim $vimdir/indent/puppet.vim
install -Dp -m0644 ext/vim/ftplugin/puppet.vim $vimdir/ftplugin/puppet.vim

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
    mkdir -p %{buildroot}%{_sysconfdir}/tmpfiles.d
    echo "D /var/run/%{name} 0755 %{name} %{name} -" > %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf
%endif

mkdir -p %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d
cp -pr ext/puppet-nm-dispatcher %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d/98-%{name}

# Fixed uid/gid were assigned in bz 472073 (Fedora), 471918 (RHEL-5),
# and 471919 (RHEL-4)
%pre
getent group puppet &>/dev/null || groupadd -r puppet -g 52 &>/dev/null
getent passwd puppet &>/dev/null || \
useradd -r -u 52 -g puppet -d %{_localstatedir}/lib/puppet -s /sbin/nologin \
    -c "Puppet" puppet &>/dev/null
# ensure that old setups have the right puppet home dir
if [ $1 -gt 1 ] ; then
  usermod -d %{_localstatedir}/lib/puppet puppet &>/dev/null
fi
exit 0

%post
%if 0%{?_with_systemd}
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ "$1" -ge 1 ]; then
  # The pidfile changed from 0.25.x to 2.6.x, handle upgrades without leaving
  # the old process running.
  oldpid="%{_localstatedir}/run/puppet/puppetd.pid"
  newpid="%{_localstatedir}/run/puppet/agent.pid"
  if [ -s "$oldpid" -a ! -s "$newpid" ]; then
    (kill $(< "$oldpid") && rm -f "$oldpid" && \
      /bin/systemctl start puppet.service) >/dev/null 2>&1 || :
  fi
fi
%else
/sbin/chkconfig --add puppet || :
if [ "$1" -ge 1 ]; then
  # The pidfile changed from 0.25.x to 2.6.x, handle upgrades without leaving
  # the old process running.
  oldpid="%{_localstatedir}/run/puppet/puppetd.pid"
  newpid="%{_localstatedir}/run/puppet/agent.pid"
  if [ -s "$oldpid" -a ! -s "$newpid" ]; then
    (kill $(< "$oldpid") && rm -f "$oldpid" && \
      /sbin/service puppet start) >/dev/null 2>&1 || :
  fi

  # If an old puppet process (one whose binary is located in /sbin) is running,
  # kill it and then start up a fresh with the new binary.
  if [ -e "$newpid" ]; then
    if ps aux | grep `cat "$newpid"` | grep -v grep | awk '{ print $12 }' | grep -q sbin; then
      (kill $(< "$newpid") && rm -f "$newpid" && \
        /sbin/service puppet start) >/dev/null 2>&1 || :
    fi
  fi
fi
%endif

%post server
%if 0%{?_with_systemd}
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ "$1" -ge 1 ]; then
  # The pidfile changed from 0.25.x to 2.6.x, handle upgrades without leaving
  # the old process running.
  oldpid="%{_localstatedir}/run/puppet/puppetmasterd.pid"
  newpid="%{_localstatedir}/run/puppet/master.pid"
  if [ -s "$oldpid" -a ! -s "$newpid" ]; then
    (kill $(< "$oldpid") && rm -f "$oldpid" && \
      /bin/systemctl start puppetmaster.service) > /dev/null 2>&1 || :
  fi
fi
%else
/sbin/chkconfig --add puppetmaster || :
if [ "$1" -ge 1 ]; then
  # The pidfile changed from 0.25.x to 2.6.x, handle upgrades without leaving
  # the old process running.
  oldpid="%{_localstatedir}/run/puppet/puppetmasterd.pid"
  newpid="%{_localstatedir}/run/puppet/master.pid"
  if [ -s "$oldpid" -a ! -s "$newpid" ]; then
    (kill $(< "$oldpid") && rm -f "$oldpid" && \
      /sbin/service puppetmaster start) >/dev/null 2>&1 || :
  fi
fi
%endif

%preun
%if 0%{?_with_systemd}
if [ "$1" -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable puppetagent.service > /dev/null 2>&1 || :
    /bin/systemctl --no-reload disable puppet.service > /dev/null 2>&1 || :
    /bin/systemctl stop puppetagent.service > /dev/null 2>&1 || :
    /bin/systemctl stop puppet.service > /dev/null 2>&1 || :
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

if [ "$1" == "1" ]; then
    /bin/systemctl is-enabled puppetagent.service > /dev/null 2>&1
    if [ "$?" == "0" ]; then
        /bin/systemctl --no-reload disable puppetagent.service > /dev/null 2>&1 ||:
        /bin/systemctl stop puppetagent.service > /dev/null 2>&1 ||:
        /bin/systemctl daemon-reload >/dev/null 2>&1 ||:
        if [ ! -d %{pending_upgrade_path} ]; then
            mkdir -p %{pending_upgrade_path}
        fi

        if [ ! -e %{pending_upgrade_file} ]; then
            touch %{pending_upgrade_file}
        fi
    fi
fi

%else
if [ "$1" = 0 ] ; then
    /sbin/service puppet stop > /dev/null 2>&1
    /sbin/chkconfig --del puppet || :
fi
%endif

%preun server
%if 0%{?_with_systemd}
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable puppetmaster.service > /dev/null 2>&1 || :
    /bin/systemctl stop puppetmaster.service > /dev/null 2>&1 || :
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
%else
if [ "$1" = 0 ] ; then
    /sbin/service puppetmaster stop > /dev/null 2>&1
    /sbin/chkconfig --del puppetmaster || :
fi
%endif

%postun
%if 0%{?_with_systemd}
if [ $1 -ge 1 ] ; then
    if [ -e %{pending_upgrade_file} ]; then
        /bin/systemctl --no-reload enable puppet.service > /dev/null 2>&1 ||:
        /bin/systemctl start puppet.service > /dev/null 2>&1 ||:
        /bin/systemctl daemon-reload >/dev/null 2>&1 ||:
        rm %{pending_upgrade_file}
    fi
    # Package upgrade, not uninstall
    /bin/systemctl try-restart puppetagent.service >/dev/null 2>&1 || :
fi
%else
if [ "$1" -ge 1 ]; then
    /sbin/service puppet condrestart >/dev/null 2>&1 || :
fi
%endif

%postun server
%if 0%{?_with_systemd}
    if [ $1 -ge 1 ] ; then
            # Package upgrade, not uninstall
            /bin/systemctl try-restart puppetmaster.service >/dev/null 2>&1 || :
    fi
%else
if [ "$1" -ge 1 ]; then
    /sbin/service puppetmaster condrestart >/dev/null 2>&1 || :
fi
%endif

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-, root, root, 0755)
%doc LICENSE README.md examples
%{puppet_bindir}/puppet
%{puppet_bindir}/extlookup2hiera
%{puppet_libdir}/*
%dir %{_sysconfdir}/NetworkManager
%dir %{_sysconfdir}/NetworkManager/dispatcher.d
%{_sysconfdir}/NetworkManager/dispatcher.d/98-puppet
%if 0%{?_with_systemd}
%{_unitdir}/puppet.service
%{_unitdir}/puppetagent.service
%else
%{_initrddir}/puppet
%config(noreplace) %{_sysconfdir}/sysconfig/puppet
%endif
%dir %{_sysconfdir}/puppetlabs
%dir %{puppet_codedir}/modules
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%endif
%config(noreplace) %{puppet_confdir}/puppet.conf
%config(noreplace) %{puppet_confdir}/auth.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/puppet
# We don't want to require emacs or vim, so we need to own these dirs
%{_datadir}/emacs
%{_datadir}/vim
%{_datadir}/%{name}
# man pages
%{_mandir}/man5/puppet.conf.5.gz
%{_mandir}/man8/puppet.8.gz
%{_mandir}/man8/puppet-agent.8.gz
%{_mandir}/man8/puppet-apply.8.gz
%{_mandir}/man8/puppet-catalog.8.gz
%{_mandir}/man8/puppet-describe.8.gz
%{_mandir}/man8/puppet-ca.8.gz
%{_mandir}/man8/puppet-cert.8.gz
%{_mandir}/man8/puppet-certificate.8.gz
%{_mandir}/man8/puppet-certificate_request.8.gz
%{_mandir}/man8/puppet-certificate_revocation_list.8.gz
%{_mandir}/man8/puppet-config.8.gz
%{_mandir}/man8/puppet-device.8.gz
%{_mandir}/man8/puppet-doc.8.gz
%{_mandir}/man8/puppet-facts.8.gz
%{_mandir}/man8/puppet-file.8.gz
%{_mandir}/man8/puppet-filebucket.8.gz
%{_mandir}/man8/puppet-help.8.gz
%{_mandir}/man8/puppet-inspect.8.gz
%{_mandir}/man8/puppet-key.8.gz
%{_mandir}/man8/puppet-epp.8.gz
%{_mandir}/man8/puppet-man.8.gz
%{_mandir}/man8/puppet-module.8.gz
%{_mandir}/man8/puppet-node.8.gz
%{_mandir}/man8/puppet-parser.8.gz
%{_mandir}/man8/puppet-plugin.8.gz
%{_mandir}/man8/puppet-report.8.gz
%{_mandir}/man8/puppet-resource.8.gz
%{_mandir}/man8/puppet-resource_type.8.gz
%{_mandir}/man8/puppet-status.8.gz
%{_mandir}/man8/extlookup2hiera.8.gz
# These need to be owned by puppet so the server can
# write to them. The separate %defattr's are required
# to work around RH Bugzilla 681540
%defattr(-, puppet, puppet, 0755)
%dir %{_localstatedir}/run/puppet
%defattr(-, puppet, puppet, 0750)
%dir %{_localstatedir}/log/puppet
%dir %{_localstatedir}/lib/puppet
%{_localstatedir}/lib/puppet/state
%{_localstatedir}/lib/puppet/reports
# Return the default attributes to 0755 to
# prevent incorrect permission assignment on EL6
%defattr(-, root, root, 0755)
%dir %{puppet_codedir}/environments
%dir %{puppet_codedir}/environments/production
%dir %{puppet_codedir}/environments/dev
%dir %{puppet_codedir}/environments/staging
%dir %{puppet_codedir}/environments/production/manifests
%dir %{puppet_codedir}/environments/dev/manifests
%dir %{puppet_codedir}/environments/staging/manifests

%files server
%defattr(-, root, root, 0755)
%if 0%{?_with_systemd}
%{_unitdir}/puppetmaster.service
%else
%{_initrddir}/puppetmaster
%config(noreplace) %{_sysconfdir}/sysconfig/puppetmaster
%endif
%config(noreplace) %{puppet_confdir}/fileserver.conf
%{_mandir}/man8/puppet-ca.8.gz
%{_mandir}/man8/puppet-master.8.gz

%changelog
