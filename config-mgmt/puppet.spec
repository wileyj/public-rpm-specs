%global vendorname puppetlabs
%define repo https://github.com/puppetlabs/puppet
%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1

%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7 || 0%{?amzn} >= 1
%global rubylibdir   %(ruby -rrbconfig -e 'puts RbConfig::CONFIG["vendorlibdir"]')
%else
%global rubylibdir   %(ruby -rrbconfig -e 'puts RbConfig::CONFIG["sitelibdir"]')
%endif

%global _with_systemd 0
%global appname puppetlabs
%global vendor_dir /opt/%{vendorname}
%global app_dir %{_sysconfdir}/%{vendorname}
%global _projconfdir %{_sysconfdir}/%{vendorname}/%{name}
#%global _app_scriptdir  %{_sysconfdir}/%{vendorname}/scripts
%global _app_bindir  %{vendor_dir}/agent/bin
#%global _master_bindir  %{vendor_dir}/master/bin
#%global _app_codedir %{app_dir}/code
%global _sym_bindir %{vendor_dir}/bin
%global _hiera_dir %{_app_codedir}/hieradata
%global _fact_dir %{vendor_dir}/facter
%global _app_logdir %{_localstatedir}/log/%{name}
%global _app_rundir %{_localstatedir}/run/%{name}
%global _app_libdir %{_localstatedir}/lib/%{name}
%global _app_prefix %{vendor_dir}/agent/apps/%{name}
%global _app_data %{vendor_dir}/agent/data/%{name}
%global confdir ext/redhat
%global pending_upgrade_path %{_localstatedir}/lib/rpm-state/puppet
%global pending_upgrade_file %{pending_upgrade_path}/upgrade_pending

Name:           puppet
Version:        %{gitversion}
Release:        %{rel_version}.%{revision}.%{dist}
Summary:        A network tool for managing many disparate systems
License:        ASL 2.0
Packager:       %{packager}
Vendor:         %{vendor}
URL:            http://puppetlabs.com
Group:          System Environment/Base
BuildRequires:  ruby >= 2.2 git facter hiera
Requires:       ruby >= 2.2 rubygem-ruby-shadow rubygem-json facter >= 3.1 hiera >= 3.0.0 shadow-utils rubygem-ast rubygem-hashdiff rubygem-json-schema rubygem-metaclass rubygem-msgpack rubygem-powerpack rubygem-puppet-lint rubygem-rspec-support rubygem-racc rubygem-redcarpet rubygem-ruby-progressbar rubygem-ruby-prof rubygem-vcr rubygem-yard rubygem-puppet-syntax rubygem-parser rubygem-hiera rubygem-rdoc rubygem-mocha rubygem-astrolabe rubygem-webmock rubygem-rspec-collection_matchers rubygem-rspec-its rubygem-rspec rubygem-rubocop rubygem-rspec-puppet rubygem-rspec-legacy_formatters rubygem-yarjuf rubygem-puppetlabs_spec_helper rubygem-librarian-puppet ruby-augeas puppetdb-termini
BuildArch:      noarch
Source1:        puppet.conf
Source2:        puppetdb.conf
Source3:        routes.yaml
Source4:        run-puppet  
Source5:        run-puppet-dev  
Source6:        run-puppet-local  
Source7:        run-puppet-prod  
Source8:        run-puppet-staging
Source9:        hiera.yaml
#Source9:        hieradata.tar.gz
#Source10:        code.tar.gz

%if 0%{?_with_systemd}
Requires:       systemd
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
BuildRequires:  systemd
%else
BuildRequires:  systemd-units
%endif
%else
Requires:       chkconfig
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
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update

%build
cd %{name}-%{version}
for f in external/nagios.rb relationship.rb; do
  sed -i -e '1d' lib/%{name}/$f
done

find examples/ -type f | xargs --no-run-if-empty chmod a-x

%install
cd %{name}-%{version}
rm -rf %{buildroot}
ruby install.rb --destdir=%{buildroot} --quick --no-rdoc --sitelibdir=%{rubylibdir} --bindir=%{_app_bindir}
%__mkdir_p %{vendor_dir}

#install -d -m0755 %{buildroot}%{_projconfdir}
#install -d -m0755 %{buildroot}%{_app_codedir}
install -d -m0755 %{buildroot}%{_app_bindir}
#install -d -m0755 %{buildroot}%{_master_bindir}
install -d -m0755 %{buildroot}%{_bindir}
install -d -m0755 %{buildroot}%{_sym_bindir}
#install -d -m0755 %{buildroot}%{_app_scriptdir}
#install -d -m0755 %{buildroot}%{_hiera_dir}
#install -d -m0755 %{buildroot}%{_fact_dir}
#install -d -m0755 %{buildroot}%{_app_codedir}/environments/production/manifests
#install -d -m0755 %{buildroot}%{_app_codedir}/environments/dev/manifests
#install -d -m0755 %{buildroot}%{_app_codedir}/environments/staging/manifests
#install -d -m0755 %{buildroot}%{_app_codedir}/environments/qa/manifests
#install -d -m0755 %{buildroot}%{_app_codedir}/modules
install -d -m0755 %{buildroot}%{_app_libdir}
install -d -m0755 %{buildroot}%{_app_libdir}/state
install -d -m0755 %{buildroot}%{_app_libdir}/reports
install -d -m0755 %{buildroot}%{_app_rundir}
install -d -m0750 %{buildroot}%{_app_logdir}


%if 0%{?_with_systemd}
%{__install} -d -m0755  %{buildroot}%{_unitdir}
install -Dp -m0644 ext/systemd/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
ln -s %{_unitdir}/%{name}.service %{buildroot}%{_unitdir}/%{name}agent.service
install -Dp -m0644 ext/systemd/%{name}master.service %{buildroot}%{_unitdir}/%{name}master.service
%else
install -Dp -m0644 %{confdir}/client.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -Dp -m0755 %{confdir}/client.init %{buildroot}%{_initrddir}/%{name}
install -Dp -m0644 %{confdir}/server.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{name}master
install -Dp -m0755 %{confdir}/server.init %{buildroot}%{_initrddir}/%{name}master
#sed -i -e 's|{appname}|/var/run/%{appname}|g' %{buildroot}%{_initrddir}/%{name}master
#sed -i -e 's|/var/run/%{appname}|/var/run/%{appname}|g' %{buildroot}%{_initrddir}/%{name}
#sed -i -e 's|/opt/%{appname}/%{name}/bin|%{puppet_bindir}|g' %{buildroot}%{_initrddir}/%{name}
%endif

if [ -f %{buildroot}%{_projconfdir}/auth.conf ]; then
    rm %{buildroot}%{_projconfdir}/auth.conf
fi
if [ -f %{buildroot}%{_projconfdir}/fileserver.conf ]; then
    rm %{buildroot}%{_projconfdir}/fileserver.conf
fi
if [ -f %{buildroot}%{_projconfdir}/puppet.conf ]; then
    rm %{buildroot}%{_projconfdir}/puppet.conf
fi
#install -Dp -m0644 conf/auth.conf %{buildroot}%{_projconfdir}
install -Dp -m0644 %{confdir}/fileserver.conf %{buildroot}%{_projconfdir}/fileserver.conf
#install -Dp -m0644 conf/%{name}.conf %{buildroot}%{_projconfdir}/%{name}.conf
install -Dp -m0644 %{confdir}/logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

install -d %{buildroot}%{_datadir}/%{name}
cp -a ext/ %{buildroot}%{_datadir}/%{name}
rm -rf %{buildroot}%{_datadir}/%{name}/ext/{emacs,vim}
rm -rf %{buildroot}%{_datadir}/%{name}/ext/{gentoo,freebsd,solaris,suse,windows,osx,ips,debian}
rm -f %{buildroot}%{_datadir}/%{name}/ext/redhat/*.init
rm -f %{buildroot}%{_datadir}/%{name}/ext/{build_defaults.yaml,project_data.yaml}
chmod 755 %{buildroot}%{_datadir}/%{name}/ext/regexp_nodes/regexp_nodes.rb
%{__install} -d -m0755  %{buildroot}%{_bindir}
ln -s %{_app_bindir}/%{name} %{buildroot}%{_bindir}/%{name}
ln -s %{_app_bindir}/%{name} %{buildroot}%{_sym_bindir}/%{name}
#ln -s %{_app_bindir}/%{name} %{buildroot}%{_master_bindir}/%{name}

ln -s %{_app_bindir}/extlookup2hiera %{buildroot}%{_bindir}/extlookup2hiera
ln -s %{_app_bindir}/extlookup2hiera %{buildroot}%{_sym_bindir}/extlookup2hiera
#ln -s %{_app_bindir}/extlookup2hiera %{buildroot}%{_master_bindir}/extlookup2hiera

#emacsdir=%{buildroot}%{_datadir}/emacs/%{name}-site-lisp
#vimdir=%{buildroot}%{_datadir}/vim/vimfiles
#install -Dp -m0644 ext/emacs/%{name}-mode.el $emacsdir/%{name}-mode.el
#install -Dp -m0644 ext/emacs/%{name}-mode-init.el $emacsdir/site-start.d/%{name}-mode-init.el
#install -Dp -m0644 ext/vim/ftdetect/%{name}.vim $vimdir/ftdetect/%{name}.vim
#install -Dp -m0644 ext/vim/syntax/%{name}.vim $vimdir/syntax/%{name}.vim
#install -Dp -m0644 ext/vim/indent/%{name}.vim $vimdir/indent/%{name}.vim
#install -Dp -m0644 ext/vim/ftplugin/%{name}.vim $vimdir/ftplugin/%{name}.vim

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
    mkdir -p %{buildroot}%{_sysconfdir}/tmpfiles.d
    echo "D %{_app_rundir} 0755 %{name} %{name} -" > %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf
%endif


#mkdir -p %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d
#cp -pr ext/%{name}-nm-dispatcher %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d/98-%{name}

#install -Dp -m0644 %{SOURCE1} %{buildroot}%{_projconfdir}/%{name}.conf
#install -Dp -m0644 %{SOURCE2} %{buildroot}%{_projconfdir}/%{name}db.conf
#install -Dp -m0644 %{SOURCE3} %{buildroot}%{_projconfdir}/routes.yaml
#install -Dp -m0755 %{SOURCE9} %{buildroot}%{_app_codedir}/hiera.yaml
#install -Dp -m0755 %{SOURCE4} %{buildroot}%{_app_scriptdir}/run-puppet
#install -Dp -m0755 %{SOURCE5} %{buildroot}%{_app_scriptdir}/run-puppet-dev
#install -Dp -m0755 %{SOURCE6} %{buildroot}%{_app_scriptdir}/run-puppet-local
#install -Dp -m0755 %{SOURCE7} %{buildroot}%{_app_scriptdir}/run-puppet-prod
#install -Dp -m0755 %{SOURCE8} %{buildroot}%{_app_scriptdir}/run-puppet-staging

#rm -rf /var/tmp/%{name}
#cp -R $RPM_BUILD_ROOT /var/tmp/%{name}

%pre
getent group puppet &>/dev/null || groupadd -r puppet -g 52 &>/dev/null
getent passwd puppet &>/dev/null || useradd -r -u 52 -g puppet -d %{_app_libdir} -s /sbin/nologin -c "Puppet" puppet &>/dev/null
if [ $1 -gt 1 ] ; then
  usermod -d %{_app_libdir} %{name} &>/dev/null
fi
exit 0

%post
%if 0%{?_with_systemd}
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ "$1" -ge 1 ]; then
  oldpid="%{_app_rundir}/%{name}d.pid"
  newpid="%{_app_rundir}/agent.pid"
  if [ -s "$oldpid" -a ! -s "$newpid" ]; then
    (kill $(< "$oldpid") && rm -f "$oldpid" && \
      /bin/systemctl start %{name}.service) >/dev/null 2>&1 || :
  fi
fi
%else
/sbin/chkconfig --add %{name} || :
if [ "$1" -ge 1 ]; then
  oldpid="%{_app_rundir}/%{name}d.pid"
  newpid="%{_app_rundir}/agent.pid"
  if [ -s "$oldpid" -a ! -s "$newpid" ]; then
    (kill $(< "$oldpid") && rm -f "$oldpid" && \
      /sbin/service %{name} start) >/dev/null 2>&1 || :
  fi
  if [ -e "$newpid" ]; then
    if ps aux | grep `cat "$newpid"` | grep -v grep | awk '{ print $12 }' | grep -q sbin; then
      (kill $(< "$newpid") && rm -f "$newpid" && \
        /sbin/service %{name} start) >/dev/null 2>&1 || :
    fi
  fi
fi
%endif

%post server
%if 0%{?_with_systemd}
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ "$1" -ge 1 ]; then
  oldpid="%{_app_rundir}/%{name}masterd.pid"
  newpid="%{_app_rundir}/master.pid"
  if [ -s "$oldpid" -a ! -s "$newpid" ]; then
    (kill $(< "$oldpid") && rm -f "$oldpid" && \
      /bin/systemctl start %{name}master.service) > /dev/null 2>&1 || :
  fi
fi
%else
/sbin/chkconfig --add %{name}master || :
if [ "$1" -ge 1 ]; then
  # The pidfile changed from 0.25.x to 2.6.x, handle upgrades without leaving
  # the old process running.
  oldpid="%{_app_rundir}/%{name}masterd.pid"
  newpid="%{_app_rundir}/master.pid"
  if [ -s "$oldpid" -a ! -s "$newpid" ]; then
    (kill $(< "$oldpid") && rm -f "$oldpid" && \
      /sbin/service %{name}master start) >/dev/null 2>&1 || :
  fi
fi
%endif

%preun
%if 0%{?_with_systemd}
if [ "$1" -eq 0 ] ; then
    /bin/systemctl --no-reload disable %{name}agent.service > /dev/null 2>&1 || :
    /bin/systemctl --no-reload disable %{name}.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}agent.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}.service > /dev/null 2>&1 || :
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

if [ "$1" == "1" ]; then
    /bin/systemctl is-enabled %{name}agent.service > /dev/null 2>&1
    if [ "$?" == "0" ]; then
        /bin/systemctl --no-reload disable %{name}agent.service > /dev/null 2>&1 ||:
        /bin/systemctl stop %{name}agent.service > /dev/null 2>&1 ||:
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
    /sbin/service %{name} stop > /dev/null 2>&1
    /sbin/chkconfig --del %{name} || :
fi
%endif

%preun server
%if 0%{?_with_systemd}
if [ $1 -eq 0 ] ; then
    /bin/systemctl --no-reload disable %{name}master.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}master.service > /dev/null 2>&1 || :
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
%else
if [ "$1" = 0 ] ; then
    /sbin/service %{name}master stop > /dev/null 2>&1
    /sbin/chkconfig --del %{name}master || :
fi
%endif

%postun
%if 0%{?_with_systemd}
if [ $1 -ge 1 ] ; then
    if [ -e %{pending_upgrade_file} ]; then
        /bin/systemctl --no-reload enable %{name}.service > /dev/null 2>&1 ||:
        /bin/systemctl start %{name}.service > /dev/null 2>&1 ||:
        /bin/systemctl daemon-reload >/dev/null 2>&1 ||:
        rm %{pending_upgrade_file}
    fi
    # Package upgrade, not uninstall
    /bin/systemctl try-restart %{name}agent.service >/dev/null 2>&1 || :
fi
%else
if [ "$1" -ge 1 ]; then
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi
%endif

%postun server
%if 0%{?_with_systemd}
    if [ $1 -ge 1 ] ; then
            # Package upgrade, not uninstall
            /bin/systemctl try-restart %{name}master.service >/dev/null 2>&1 || :
    fi
%else
if [ "$1" -ge 1 ]; then
    /sbin/service %{name}master condrestart >/dev/null 2>&1 || :
fi
%endif

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-, root, root)
#%dir %{_app_scriptdir}
#%dir %{_projconfdir}
%{rubylibdir}/hiera
%{rubylibdir}/%{name}
%{rubylibdir}/hiera_puppet.rb
%{rubylibdir}/puppet.rb
%{rubylibdir}/puppet_x.rb
#%{rubylibdir}/semver.rb
%attr(0755, puppet, puppet) %{_app_bindir}/%{name}
#%attr(0755, puppet, puppet) %{_app_bindir}/extlookup2hiera
%attr(0755, puppet, puppet)  /etc/puppetlabs/puppet/hiera.yaml
%attr(0755, puppet, puppet)  /opt/puppetlabs/bin/extlookup2hiera
#%{_sym_bindir}/extlookup2hiera
%{_sym_bindir}/%{name}
%{_bindir}/%{name}
%{_bindir}/extlookup2hiera
%if 0%{?_with_systemd}
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}agent.service
%else
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%endif
%dir %{_sysconfdir}/%{appname}
#%dir %{_app_codedir}/modules
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%endif
#%config(noreplace) %{_projconfdir}/%{name}.conf
#%config(noreplace) %{_projconfdir}/auth.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
#%config(noreplace) %{_projconfdir}/puppetdb.conf
#%config(noreplace) %{_projconfdir}/routes.yaml
#%attr(0755, puppet, puppet) %{_app_scriptdir}/run-puppet
#%attr(0755, puppet, puppet) %{_app_scriptdir}/run-puppet-dev
#%attr(0755, puppet, puppet) %{_app_scriptdir}/run-puppet-local
#%attr(0755, puppet, puppet) %{_app_scriptdir}/run-puppet-prod
#%attr(0755, puppet, puppet) %{_app_scriptdir}/run-puppet-staging
%{_app_bindir}

##%{_datadir}/emacs
##%{_datadir}/vim
##%{_datadir}/emacs/%{name}-site-lisp/%{name}-mode.el
##%{_datadir}/emacs/%{name}-site-lisp/site-start.d/%{name}-mode-init.el
##%{_datadir}/vim/vimfiles/ftdetect/%{name}.vim
##%{_datadir}/vim/vimfiles/syntax/%{name}.vim
##%{_datadir}/vim/vimfiles/indent/%{name}.vim
##%{_datadir}/vim/vimfiles/ftplugin/%{name}.vim


%{_datadir}/%{name}
# man pages
%{_mandir}/man5/%{name}*
%{_mandir}/man8/%{name}*
#%{_mandir}/man8/extlookup2hiera.8.gz

# These need to be owned by puppet so the server can
# write to them. The separate %defattr's are required
# to work around RH Bugzilla 681540
%defattr(-, %{name}, %{name}, 0755)
%dir %{_app_rundir}

%defattr(-, %{name}, %{name}, 0750)
%dir %{_app_logdir}
%dir %{_app_libdir}
%dir %{_app_libdir}/state
%dir %{_app_libdir}/reports
#%dir %{_app_codedir}
#%config(noreplace) %{_app_codedir}/hiera.yaml
#%dir %{_app_codedir}/environments
#%dir %{_app_codedir}/environments/production
#%dir %{_app_codedir}/environments/dev
#%dir %{_app_codedir}/environments/staging
#%dir %{_app_codedir}/environments/qa
#%dir %{_app_codedir}/environments/production/manifests
#%dir %{_app_codedir}/environments/dev/manifests
#%dir %{_app_codedir}/environments/staging/manifests
#%dir %{_app_codedir}/environments/qa/manifests
%config(noreplace)  %{vendor_dir}/%{name}/share/locale/config.yaml
%{vendor_dir}/%{name}/share/locale/%{name}.pot

%files server
%defattr(-, puppet, puppet)
%if 0%{?_with_systemd}
%{_unitdir}/puppetmaster.service
%else
%{_initrddir}/puppetmaster
%config(noreplace) %{_sysconfdir}/sysconfig/puppetmaster
%endif
%config(noreplace) %{_projconfdir}/fileserver.conf
#%attr(0755, puppet, puppet) %{_master_bindir}/%{name}
#%attr(0755, puppet, puppet) %{_master_bindir}/extlookup2hiera
#%{_master_bindir}/%{name}
#%{_master_bindir}/extlookup2hiera
%{_mandir}/man8/puppet-ca.8.gz
%{_mandir}/man8/puppet-master.8.gz


