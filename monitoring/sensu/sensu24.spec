%global gem_name sensu
%global __chown /bin/chown
%global __rm /bin/rm
%global __chown /bin/chown
%global ruby_ver 24
%global alinux_ruby 2.4
%global remoteversion %(echo `gem list ^%{gem_name}$ -r |  grep %{gem_name} | cut -f2 -d" " | tr -d '()' | tr -d ','`)

%global         upstart     0
%global         systemd     1
%global         gem_bin     /usr/bin/gem
%global         app_dir     /opt/%{gem_name}
%define         conf_dir    %{_sysconfdir}/%{gem_name}
%global         extensions  %{conf_dir}/extensions
%global         metrics     %{conf_dir}/metrics
%global         mutators    %{conf_dir}/mutators
%global         handlers    %{conf_dir}/handlers
%global         ext_mutators    %{extensions}/mutators
%global         ext_handlers    %{extensions}/handlers
%global         confd       %{conf_dir}/conf.d
%global         c_plugins     %{confd}/plugins
%global         c_checks      %{confd}/checks
%global         c_services    %{confd}/services
%global         c_handlers    %{confd}/handlers
%define         user    sensu
%define         group   monitoring
%define         uid   487
%define         gid   487

Name:           %{gem_name}%{ruby_ver}
Version:        %{remoteversion}
Release:        1.%{dist}
Summary:        A monitoring framework that aims to be simple, malleable, and scalable.
License:        GPLv2
Packager:       %{packager}
Vendor:         %{vendor}
URL:            https://github.com/%{gem_name}/%{gem_name}
AutoReqProv:    no
Source2:        %{gem_name}-service.init
Source3:        %{gem_name}-server.init
Source4:        %{gem_name}-client.init
Source5:        %{gem_name}-api.init
Source6:        %{gem_name}-server.upstart
Source7:        %{gem_name}-runsvdir.upstart
Source8:        %{gem_name}-client.upstart
Source9:        %{gem_name}-api.upstart
Source10:       %{gem_name}-server.systemd
Source11:       %{gem_name}-runsvdir.systemd
Source12:       %{gem_name}-client.systemd
Source13:       %{gem_name}-api.systemd
Source14:       %{gem_name}-runsvdir.sh
Source15:       %{gem_name}-sv-log.sh
Source16:       %{gem_name}-sv-run.sh.erb
Source17:       %{gem_name}-server.rb
Source18:       %{gem_name}-ctl.rb
Source19:       %{gem_name}-client.rb
Source20:       %{gem_name}-api.rb
Source21:       %{gem_name}.logrotate
Source22:       %{gem_name}.default
Source23:       utmpset
Source24:       svlogd
Source25:       sv
Source26:       runsvdir
Source27:       runsv
Source28:       chpst
Source29:       %{gem_name}-name.erb
Source30:       config.json
Source31:       relay.rb
Source32:       metrics.rb
Source33:       check_cron.json
Source34:       check_sshd.json
Source35:       check_swapio.json
Source36:       check_vmstat.json
Source37:       client.json
Source38:       api.json
Source39:       config_relay.json
Source40:       rabbitmq.json
Source41:       redis.json
Source42:       email.json
Source43:       file.json
Source44:       handlers.json


%description
A monitoring framework that aims to be simple, malleable, and scalable.

#-----------------------------------------------------------------------

%package -n     %{gem_name}%{ruby_ver}-server
Summary:        A monitoring server
License:        GPLv2
#AutoReqProv:   no
BuildRequires:  ruby
Requires:       autoconf openssl openssl-devel openssl-perl ruby%{ruby_ver} ruby%{ruby_ver}-devel runit rubygems%{ruby_ver} ruby%{ruby_ver}-irb ruby%{ruby_ver}-libs zlib-devel zlib libyaml-devel libyaml
Requires:       sensu%{ruby_ver}-api  sensu%{ruby_ver}-configs  sensu%{ruby_ver} sensu%{ruby_ver}-server = %{version}
Requires:       rubygem%{ruby_ver}-sensu-extension  rubygem%{ruby_ver}-amqp rubygem%{ruby_ver}-childprocess
Requires:       rubygem%{ruby_ver}-em-worker rubygem%{ruby_ver}-sensu rubygem%{ruby_ver}-sensu-extension
Requires:       rubygem%{ruby_ver}-sensu-extensions  rubygem%{ruby_ver}-sensu-logger rubygem%{ruby_ver}-sensu-plugin rubygem%{ruby_ver}-sensu-settings rubygem%{ruby_ver}-sensu-spawn rubygem%{ruby_ver}-sensu-transport rubygem%{ruby_ver}-bigdecimal

%description -n %{gem_name}%{ruby_ver}-server
server for sensu
#-----------------------------------------------------------------------

%package -n     %{gem_name}%{ruby_ver}-client
Summary:        A monitoring client for sensu server
License:        GPLv2
#AutoReqProv:   no
Requires:       ruby%{ruby_ver} rubygem%{ruby_ver}-sensu ruby rubygem%{ruby_ver}-sensu rubygem%{ruby_ver}-sensu-logger rubygem%{ruby_ver}-sensu-transport rubygem%{ruby_ver}-sensu-spawn sensu%{ruby_ver} rubygem%{ruby_ver}-bigdecimal
Provides:       sensu%{ruby_ver}-client = %{version}

%description -n %{gem_name}%{ruby_ver}-client
Client for the sensu server
#-----------------------------------------------------------------------

%package -n     %{gem_name}%{ruby_ver}-api
Summary:        API service for sensu server
License:        GPLv2
#AutoReqProv:   no
Requires:       sensu%{ruby_ver}-server rubygem%{ruby_ver}-sensu rubygem%{ruby_ver}-sensu-extension
Provides:       sensu%{ruby_ver}-api = %{version}

%description -n %{gem_name}%{ruby_ver}-api
API for the sensu server
#-----------------------------------------------------------------------

%package -n     %{gem_name}%{ruby_ver}-configs
Summary:        Configs for sensu server
License:        GPLv2
#AutoReqProv:   no
Requires:       %{gem_name}-server
Provides:       %{gem_name}-configs = %{version}

%description -n %{gem_name}%{ruby_ver}-configs
Configs for the sensu server
#-----------------------------------------------------------------------

%package -n     %{gem_name}%{ruby_ver}-client-configs
Summary:        client configs for sensu client
License:        GPLv2
#AutoReqProv:   no
Requires:       sensu%{ruby_ver}-client rubygem%{ruby_ver}-sensu rubygem%{ruby_ver}-sensu-extension
Provides:       sensu%{ruby_ver}-client-configs = %{version}

%description -n %{gem_name}%{ruby_ver}-client-configs
Generic Configs for the sensu client
#-----------------------------------------------------------------------

%prep
export GEM_HOME=%{buildroot}%{gemdir}
%{__mkdir_p} $GEM_HOME

DIRS=" %{_var}/log/%{gem_name} %{app_dir} %{app_dir}/sv %{app_dir}/bin %{app_dir}/service %{conf_dir} %{ext_mutators} %{_sysconfdir}/default %{metrics} %{conf_dir} %{extensions} %{mutators} %{confd} %{c_plugins} %{checks} %{c_services} %{handlers} %{c_checks} %{ext_handlers} %{c_handlers} %{conf_dir}/ssl"
for dir in $DIRS
do
    %{__mkdir_p} -m 0755 %{buildroot}/$dir
done

#%{__sed} -i -e 's/\/opt\/%{gem_name}\/bin\/ruby/\/usr\/bin\/ruby%{alinux_ruby}/g'  %{SOURCE19}
#%{__sed} -i -e 's/\/opt\/%{gem_name}\/bin\/ruby/\/usr\/bin\/ruby%{alinux_ruby}/g'  %{SOURCE20}
#%{__sed} -i -e 's/\/opt\/%{gem_name}\/bin\/ruby/\/usr\/bin\/ruby%{alinux_ruby}/g'  %{SOURCE29}
#%{__sed} -i -e 's/\/opt\/%{gem_name}\/bin\/ruby/\/usr\/bin\/ruby%{alinux_ruby}/g'  %{SOURCE18}
#%{__sed} -i -e 's/\/opt\/%{gem_name}\/bin\/ruby/\/usr\/bin\/ruby%{alinux_ruby}/g'  %{SOURCE17}

%{__install} -p -m 0755 %{SOURCE23} %{buildroot}%{app_dir}/bin/utmpset
%{__install} -p -m 0755 %{SOURCE24} %{buildroot}%{app_dir}/bin/svlogd
%{__install} -p -m 0755 %{SOURCE25} %{buildroot}%{app_dir}/bin/sv
%{__install} -p -m 0755 %{SOURCE26} %{buildroot}%{app_dir}/bin/runsvdir
%{__install} -p -m 0755 %{SOURCE27} %{buildroot}%{app_dir}/bin/runsv
%{__install} -p -m 0755 %{SOURCE28} %{buildroot}%{app_dir}/bin/chpst

for f in utmpset svlogd sv runsvdir runsv chpst
do
    %{__ln_s} -f /sbin/$f %{buildroot}%{app_dir}/bin/$f
done

%{__install} -p -m 0755 %{SOURCE14} %{buildroot}%{app_dir}/bin/%{gem_name}-runsvdir
%{__install} -p -m 0755 %{SOURCE17} %{buildroot}%{app_dir}/bin/%{gem_name}-server
%{__install} -p -m 0755 %{SOURCE18} %{buildroot}%{app_dir}/bin/%{gem_name}-ctl
%{__install} -p -m 0755 %{SOURCE19} %{buildroot}%{app_dir}/bin/%{gem_name}-client
%{__install} -p -m 0755 %{SOURCE20} %{buildroot}%{app_dir}/bin/%{gem_name}-api

%{__install} -p -m 0644 %{SOURCE30} %{buildroot}%{conf_dir}/config.json
%{__install} -p -m 0755 %{SOURCE31} %{buildroot}%{ext_handlers}/relay.rb
%{__install} -p -m 0755 %{SOURCE32} %{buildroot}%{ext_mutators}/metrics.rb
%{__install} -p -m 0644 %{SOURCE33} %{buildroot}%{c_checks}/check_cron.json
%{__install} -p -m 0644 %{SOURCE34} %{buildroot}%{c_checks}/check_sshd.json
%{__install} -p -m 0644 %{SOURCE35} %{buildroot}%{c_checks}/check_swapio.json
%{__install} -p -m 0644 %{SOURCE36} %{buildroot}%{c_checks}/check_vmstat.json
%{__install} -p -m 0644 %{SOURCE37} %{buildroot}%{confd}/client.json
%{__install} -p -m 0644 %{SOURCE38} %{buildroot}%{c_services}/api.json
%{__install} -p -m 0644 %{SOURCE39} %{buildroot}%{c_services}/config_relay.json
%{__install} -p -m 0644 %{SOURCE40} %{buildroot}%{c_services}/rabbitmq.json
%{__install} -p -m 0644 %{SOURCE41} %{buildroot}%{c_services}/redis.json
%{__install} -p -m 0644 %{SOURCE42} %{buildroot}%{c_handlers}/email.json
%{__install} -p -m 0644 %{SOURCE43} %{buildroot}%{c_handlers}/file.json
%{__install} -p -m 0644 %{SOURCE44} %{buildroot}%{c_handlers}/handlers.json


for d in client server api
do
    %{__mkdir_p} -m 0755 %{buildroot}%{app_dir}/sv/%{gem_name}-$d/supervise
    %{__mkdir_p} -m 0755 %{buildroot}%{app_dir}/sv/%{gem_name}-$d/log/main
    %{__install} -p -m 0755 %{SOURCE15}  %{buildroot}%{app_dir}/sv/%{gem_name}-$d/log/run
    %{__install} -p -m 0755 %{SOURCE16}  %{buildroot}%{app_dir}/sv/%{gem_name}-$d/run
done
%{__mkdir_p} %{buildroot}%{_var}/run/%{gem_name}

%{__sed} -i -e 's/prog="%{gem_name}-<%= @sv %>"/prog="%{gem_name}-client"/' %{buildroot}%{app_dir}/sv/%{gem_name}-client/run
%{__sed} -i -e 's/prog="%{gem_name}-<%= @sv %>"/prog="%{gem_name}-api"/' %{buildroot}%{app_dir}/sv/%{gem_name}-api/run
%{__sed} -i -e 's/prog="%{gem_name}-<%= @sv %>"/prog="%{gem_name}-server"/' %{buildroot}%{app_dir}/sv/%{gem_name}-server/run

for f in %{gem_name}-api %{gem_name}-server
do
    %{__install} -p -m 0755 %{SOURCE29}  %{buildroot}%{app_dir}/bin/$f
    %{__sed} -i -e 's/\/opt\/%{gem_name}\/embedded\/bin\/ruby/\/usr\/bin\/ruby%{alinux_ruby}/' %{buildroot}%{app_dir}/bin/$f
done

%{__sed} -i -e 's/<%= @name %>/%{gem_name}-client/' %{buildroot}%{app_dir}/bin/%{gem_name}-client
%{__sed} -i -e 's/<%= @name %>/%{gem_name}-api/' %{buildroot}%{app_dir}/bin/%{gem_name}-api
%{__sed} -i -e 's/<%= @name %>/%{gem_name}-server/' %{buildroot}%{app_dir}/bin/%{gem_name}-server
%{__sed} -i -e 's/\/opt\/%{gem_name}\/embedded\/bin\/runsvdir/\/opt\/%{gem_name}\/bin\/runsvdir/' %{buildroot}%{app_dir}/bin/%{gem_name}-runsvdir
%{__sed} -i -e 's/\/opt\/%{gem_name}\/embedded\/bin\/runsvdir/\/opt\/%{gem_name}\/bin\/runsvdir/' %{buildroot}%{app_dir}/bin/%{gem_name}-ctl


#site specific configs:
%{__mkdir_p} -m 0755 %{buildroot}%{_initrddir}
%{__mkdir_p} -m 0755 %{buildroot}%{_sysconfdir}/logrotate.d
%{__mkdir_p} -m 0755 %{buildroot}%{_datadir}/%{gem_name}
%{__install} -p -m 0755 %{SOURCE21} %{buildroot}%{_sysconfdir}/logrotate.d/%{gem_name}
%{__install} -p -m 0755 %{SOURCE22} %{buildroot}%{_sysconfdir}/default/%{gem_name}

# init
%{__install} -p -m 0755 %{SOURCE2} %{buildroot}%{_initrddir}/%{gem_name}-service
%{__install} -p -m 0755 %{SOURCE3} %{buildroot}%{_initrddir}/%{gem_name}-server
%{__install} -p -m 0755 %{SOURCE4} %{buildroot}%{_initrddir}/%{gem_name}-client
%{__install} -p -m 0755 %{SOURCE5} %{buildroot}%{_initrddir}/%{gem_name}-api

# systemd
#%{__mkdir_p} %{buildroot}%{_unitdir}
#%{__install} -p -m 0644 %{SOURCE10} %{buildroot}%{_unitdir}/%{gem_name}-server.service
#%{__install} -p -m 0644 %{SOURCE11} %{buildroot}%{_unitdir}/%{gem_name}-runsvdir.service
#%{__install} -p -m 0644 %{SOURCE12} %{buildroot}%{_unitdir}/%{gem_name}-client.service
#%{__install} -p -m 0644 %{SOURCE13} %{buildroot}%{_unitdir}/%{gem_name}-api.service

# replace all lines in files that used the embedded files, since we're using custom built ruby
#for i in `find  %{buildroot} -type f | xargs grep "%{app_dir}/embedded/bin" |grep "\bPATH" | cut -f1 -d ":"`
#do
#    %{__sed} -i -e 's/PATH=\/opt\/%{gem_name}\/embedded\/bin:/PATH=/usr/bin/ruby%{alinux_ruby}/g' $i
#done

#for i in `find  %{buildroot} -type f | xargs grep "%{app_dir}/embedded/lib/ruby/gems/2.0.0" |grep "\bGEM_PATH" | cut -f1 -d ":"`
#do
#    %{__sed} -i -e 's/GEM_PATH=\/opt\/%{gem_name}\/embedded\/lib\/ruby\/gems\/2.0.0:/GEM_PATH=/g' $i
#done

#for i in `find  %{buildroot} -type f | xargs grep "%{app_dir}/embedded/bin/chpst" |grep "\bexec" | cut -f1 -d ":"`
#do
#    %{__sed} -i -e 's/\/opt\/%{gem_name}\/embedded\/bin\/chpst/\/opt\/%{gem_name}\/bin\/chpst/g' $i
#done

# one-offs
%{__sed} -i -e 's/\#!\/opt\/%{gem_name}\/embedded\/bin\/ruby/\#\!\/usr\/bin\/ruby/g' %{buildroot}%{app_dir}/bin/%{gem_name}-ctl
%{__sed} -i -e 's/\/opt\/%{gem_name}\/embedded\/bin\/sv/\/opt\/%{gem_name}\/bin\/sv/g' %{buildroot}%{app_dir}/bin/%{gem_name}-ctl
%{__sed} -i -e 's/\/opt\/%{gem_name}\/embedded\/bin\/%{gem_name}-runsvdir/\/opt\/%{gem_name}\/bin\/sv/g' %{buildroot}%{app_dir}/bin/%{gem_name}-ctl
%{__sed} -i -e 's/\/opt\/%{gem_name}\/embedded\/bin\/%{gem_name}-runsvdir/\/opt\/%{gem_name}\/bin\/%{gem_name}-runsvdir/g' %{buildroot}%{app_dir}/bin/%{gem_name}-runsvdir
%{__sed} -i -e 's/\/opt\/%{gem_name}\/embedded\/bin\/runsvdir/\/opt\/%{gem_name}\/bin\/runsvdir/g' %{buildroot}%{app_dir}/bin/%{gem_name}-runsvdir

# replace all files that reference '/usr/bin/ruby' with '/usr/bin/ruby<version>'
for file in `find %{buildroot} -type f`; do
    %{__sed} -i -e 's|/opt/%{gem_name}/bin/ruby|/usr/bin/ruby%{alinux_ruby}|g' $file
    %{__sed} -i -e 's|/usr/bin/ruby|/usr/bin/ruby%{alinux_ruby}|' $file
    %{__sed} -i -e 's|/opt/%{gem_name}/embedded/bin/chpst|/opt/%{gem_name}/bin/chpst|g' $file
    %{__sed} -i -e 's|GEM_PATH=/opt/%{gem_name}/embedded/lib/ruby/gems/2.0.0:|GEM_PATH=|g' $file
    %{__sed} -i -e 's|PATH=/opt/%{gem_name}/embedded/bin:|PATH=/usr/bin/ruby%{alinux_ruby}|g' $file
done

%pre
%{_bindir}/getent group %{group}|| %{_sbindir}/groupadd -r -g %{gid} %{group}
%{_bindir}/getent passwd %{user}|| %{_sbindir}/useradd -r -g %{group} -d %{app_dir} -s /bin/bash -c "Sensu User" -u %{uid} %{user}

%preun -n %{gem_name}%{ruby_ver}-client
if [ $1 = 0 ] ; then
    if [ -x %{_initrddir}/%{gem_name}-client ] ; then
        %{_initrddir}/%{gem_name}-client stop > /dev/null
        /sbin/chkconfig --del %{gem_name}-client
    fi
fi

%preun -n %{gem_name}%{ruby_ver}-server
if [ $1 = 0 ] ; then
    if [ -x %{_initrddir}/%{gem_name}-server ] ; then
        %{_initrddir}/%{gem_name}-server stop > /dev/null
        /sbin/chkconfig --del %{gem_name}-server
    fi
fi

%preun -n %{gem_name}%{ruby_ver}-api
if [ $1 = 0 ] ; then
    if [ -x %{_initrddir}/%{gem_name}-api ] ; then
        %{_initrddir}/%{gem_name}-client api > /dev/null
        /sbin/chkconfig --del %{gem_name}-api
    fi
fi

%triggerpostun -- %{gem_name}%{ruby_ver}
if  getent passwd %{user} >/dev/null; then
    %{_sbindir}/userdel %{user}
    if [ -d %{app_dir} ]; then
        %__rm -rf %{app_dir}
    fi
    if [ -d  %{_var}/run/%{gem_name} ]; then
        %__rm -rf  %{_var}/run/%{gem_name}
    fi
fi
#remove group
if  getent group %{group} >/dev/null; then
    if  ! getent passwd uchiwa >/dev/null; then
        %{_sbindir}/groupdel %{group}
    fi
fi

%post -n %{gem_name}%{ruby_ver}
%__chown -R %{user}:%{group} %{_var}/run/%{gem_name}
%__chown -R %{user}:%{group} %{_sysconfdir}/%{gem_name}
%__chown -R %{user}:%{group} %{_var}/log/%{gem_name}
%__chown -R %{user}:%{group} %{app_dir}
%__chown -R %{user}:%{group} %{app_dir}

%post -n %{gem_name}%{ruby_ver}-server
/sbin/chkconfig --add %{gem_name}-server
/sbin/chkconfig %{gem_name}-server on

%post -n %{gem_name}%{ruby_ver}-client
/sbin/chkconfig --add %{gem_name}-client
/sbin/chkconfig %{gem_name}-client on

%post -n %{gem_name}%{ruby_ver}-api
/sbin/chkconfig --add %{gem_name}-api
/sbin/chkconfig %{gem_name}-api on


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{gem_name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{gem_name}-%{version}
[ "%{_builddir}/%{gem_name}" != "/" ] && %__rm -rf %{_builddir}/%{gem_name}

%files -n %{gem_name}%{ruby_ver}
%attr(755, %{user}, %{group})
%dir %{extensions}
%dir %{ext_mutators}
%dir %{ext_handlers}
%dir %{c_plugins}
%dir %{metrics}
%dir %{conf_dir}/mutators
%dir %{conf_dir}/handlers
%dir %{conf_dir}/ssl
%dir %{app_dir}/sv
%dir %{_var}/run/%{gem_name}
%{_var}/log/%{gem_name}
%{_sysconfdir}/default/%{gem_name}
%{_initrddir}/%{gem_name}-service

%files -n %{gem_name}%{ruby_ver}-server
%attr(755, %{user}, %{group})
%{_initrddir}/%{gem_name}-server
#%{_initrddir}/%{gem_name}-runsvdir
%attr(0644, %{user}, %{group})%{_sysconfdir}/logrotate.d/%{gem_name}
%{app_dir}/bin/%{gem_name}-api
%{app_dir}/bin/%{gem_name}-ctl
%{app_dir}/bin/%{gem_name}-server
%{app_dir}/service
%{app_dir}/sv/%{gem_name}-server/log/main
%{app_dir}/sv/%{gem_name}-server/log/run
%{app_dir}/sv/%{gem_name}-server/run
%{app_dir}/sv/%{gem_name}-server/supervise
%{app_dir}/bin/chpst
%{app_dir}/bin/runsv
%{app_dir}/bin/runsvdir
%{app_dir}/bin/sv
%{app_dir}/bin/svlogd
%{app_dir}/bin/utmpset
%{app_dir}/bin/%{gem_name}-runsvdir
%{extensions}/handlers/relay.rb
%{extensions}/mutators/metrics.rb



%files -n %{gem_name}%{ruby_ver}-api
%attr(755, %{user}, %{group})
%{_initrddir}/%{gem_name}-api
%{app_dir}/sv/%{gem_name}-api/log/main
%{app_dir}/sv/%{gem_name}-api/log/run
%{app_dir}/sv/%{gem_name}-api/run
%{app_dir}/sv/%{gem_name}-api/supervise

%files -n %{gem_name}%{ruby_ver}-configs
%attr(755, %{user}, %{group})
%{conf_dir}/config.json
%{conf_dir}/conf.d/client.json

%files -n %{gem_name}%{ruby_ver}-client
%attr(755, %{user}, %{group})
%dir %{confd}
%{_initrddir}/%{gem_name}-client
%{app_dir}/bin/%{gem_name}-client
%{app_dir}/sv/%{gem_name}-client/log/main
%{app_dir}/sv/%{gem_name}-client/log/run
%{app_dir}/sv/%{gem_name}-client/run
%{app_dir}/sv/%{gem_name}-client/supervise
%{c_checks}/check_cron.json
%{c_checks}/check_sshd.json
%{c_checks}/check_swapio.json
%{c_checks}/check_vmstat.json
%{c_services}/api.json
%{c_services}/config_relay.json
%{c_services}/rabbitmq.json
%{c_services}/redis.json
%{c_handlers}/email.json
%{c_handlers}/file.json
%{c_handlers}/handlers.json
