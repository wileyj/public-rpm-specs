%include %{_rpmconfigdir}/macros.d/macros.rubygems
%global srcname sensu
%global remoteversion %(echo `gem list ^%{srcname}$ -r |  grep %{srcname} | cut -f2 -d" " | tr -d '()' | tr -d ','`)

%include        %{_rpmconfigdir}/macros.d/macros.rubygems
%global         upstart     0
%global         systemd     0
%global         gem_bin     /usr/bin/gem
%global         app_dir     /opt/%{srcname}
%define         conf_dir    %{_sysconfdir}/%{srcname}
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
%define         group   sensu

Name:           %{srcname}
Version:        %{remoteversion}
Release:        1.%{dist}
Summary:        A monitoring framework that aims to be simple, malleable, and scalable.
Group:          Monitoring    
License:        GPLv2
Packager:       %{packager} 
Vendor:         %{vendor} 
URL:            https://github.com/%{name}/%{name}
AutoReqProv:    no
Source2:        %{name}-service.init
Source3:        %{name}-server.init
Source4:        %{name}-client.init
Source5:        %{name}-api.init
Source6:        %{name}-server.upstart
Source7:        %{name}-runsvdir.upstart
Source8:        %{name}-client.upstart
Source9:        %{name}-api.upstart
Source10:       %{name}-server.systemd
Source11:       %{name}-runsvdir.systemd
Source12:       %{name}-client.systemd
Source13:       %{name}-api.systemd
Source14:       %{name}-runsvdir.sh
Source15:       %{name}-sv-log.sh
Source16:       %{name}-sv-run.sh.erb
Source17:       %{name}-server.rb
Source18:       %{name}-ctl.rb
Source19:       %{name}-client.rb
Source20:       %{name}-api.rb
Source21:       %{name}.logrotate
Source22:       %{name}.default
Source23:       utmpset
Source24:       svlogd
Source25:       sv
Source26:       runsvdir
Source27:       runsv
Source28:       chpst
Source29:       %{name}-name.erb
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

%package -n     %{name}-server
Summary:        A monitoring server
Group:          Monitoring
License:        GPLv2
#AutoReqProv:   no
BuildRequires:  runit ruby
Requires:       autoconf openssl openssl-devel openssl-perl ruby ruby-devel runit rubygems ruby-irb ruby-libs zlib-devel zlib libyaml-devel libyaml
Requires:       sensu-api  sensu-configs  sensu sensu-server = %{version} 
Requires:       rubygem-sensu-extension  rubygem-amqp  rubygem-async_sinatra rubygem-childprocess rubygem-daemons  rubygem-em-http-request 
Requires:       rubygem-em-redis-unified rubygem-em-worker  rubygem-ffi rubygem-rspec  rubygem-sensu  rubygem-sensu-em  rubygem-sensu-extension 
Requires:       rubygem-sensu-extensions  rubygem-sensu-logger rubygem-sensu-plugin rubygem-sensu-settings rubygem-sensu-spawn rubygem-sensu-transport 

%description -n %{name}-server
server for sensu 
#-----------------------------------------------------------------------

%package -n     %{name}-client
Summary:        A monitoring client for sensu server
Group:          Monitoring    
License:        GPLv2
#AutoReqProv:   no
Requires:       ruby rubygem-sensu ruby rubygem-sensu rubygem-sensu-logger rubygem-sensu-em rubygem-sensu-transport rubygem-sensu-spawn sensu 
Provides:       sensu-client = %{version}

%description client
Client for the sensu server
#-----------------------------------------------------------------------

%package -n     %{name}-api 
Summary:        API service for sensu server
Group:          Monitoring
License:        GPLv2
#AutoReqProv:   no
Requires:       sensu-server rubygem-sensu rubygem-sensu-em rubygem-sensu-extension
Provides:       sensu-api = %{version}

%description -n %{name}-api
API for the sensu server
#-----------------------------------------------------------------------

%package -n     %{name}-configs
Summary:        Configs for sensu server
Group:          Monitoring
License:        GPLv2
#AutoReqProv:   no
Requires:       %{name}-server
Provides:       %{name}-configs = %{version}

%description -n %{name}-configs
Configs for the sensu server
#-----------------------------------------------------------------------

%package -n     %{name}-client-configs
Summary:        client configs for sensu client
Group:          Monitoring
License:        GPLv2
#AutoReqProv:   no
Requires:       sensu-client rubygem-sensu-em rubygem-sensu rubygem-sensu-extension
Provides:       sensu-client-configs = %{version}

%description -n %{name}-client-configs
Generic Configs for the sensu client
#-----------------------------------------------------------------------

%prep
export GEM_HOME=%{buildroot}%{gemdir}
%{__mkdir_p} $GEM_HOME

DIRS=" %{_var}/log/%{name} %{app_dir} %{app_dir}/sv %{app_dir}/bin %{app_dir}/service %{conf_dir} %{ext_mutators} %{_sysconfdir}/default %{metrics} %{conf_dir} %{extensions} %{mutators} %{confd} %{c_plugins} %{checks} %{c_services} %{handlers} %{c_checks} %{ext_handlers} %{c_handlers} %{conf_dir}/ssl"
for dir in $DIRS
do
    %{__mkdir_p} -m 0755 %{buildroot}/$dir
done

%{__sed} -i -e 's/\/opt\/%{name}\/bin\/ruby/\/usr\/bin\/ruby/g'  %{SOURCE19}
%{__sed} -i -e 's/\/opt\/%{name}\/bin\/ruby/\/usr\/bin\/ruby/g'  %{SOURCE20}
%{__sed} -i -e 's/\/opt\/%{name}\/bin\/ruby/\/usr\/bin\/ruby/g'  %{SOURCE29}
%{__sed} -i -e 's/\/opt\/%{name}\/bin\/ruby/\/usr\/bin\/ruby/g'  %{SOURCE18}
%{__sed} -i -e 's/\/opt\/%{name}\/bin\/ruby/\/usr\/bin\/ruby/g'  %{SOURCE17}

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

%{__install} -p -m 0755 %{SOURCE14} %{buildroot}%{app_dir}/bin/%{name}-runsvdir
%{__install} -p -m 0755 %{SOURCE17} %{buildroot}%{app_dir}/bin/%{name}-server
%{__install} -p -m 0755 %{SOURCE18} %{buildroot}%{app_dir}/bin/%{name}-ctl
%{__install} -p -m 0755 %{SOURCE19} %{buildroot}%{app_dir}/bin/%{name}-client
%{__install} -p -m 0755 %{SOURCE20} %{buildroot}%{app_dir}/bin/%{name}-api

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
    %{__mkdir_p} -m 0755 %{buildroot}%{app_dir}/sv/%{name}-$d/supervise
    %{__mkdir_p} -m 0755 %{buildroot}%{app_dir}/sv/%{name}-$d/log/main
    %{__install} -p -m 0755 %{SOURCE15}  %{buildroot}%{app_dir}/sv/%{name}-$d/log/run
    %{__install} -p -m 0755 %{SOURCE16}  %{buildroot}%{app_dir}/sv/%{name}-$d/run
done 
%{__mkdir_p} %{buildroot}%{_var}/run/%{name}

%{__sed} -i -e 's/prog="%{name}-<%= @sv %>"/prog="%{name}-client"/' %{buildroot}%{app_dir}/sv/%{name}-client/run
%{__sed} -i -e 's/prog="%{name}-<%= @sv %>"/prog="%{name}-api"/' %{buildroot}%{app_dir}/sv/%{name}-api/run
%{__sed} -i -e 's/prog="%{name}-<%= @sv %>"/prog="%{name}-server"/' %{buildroot}%{app_dir}/sv/%{name}-server/run

for f in %{name}-api %{name}-server
do
    %{__install} -p -m 0755 %{SOURCE29}  %{buildroot}%{app_dir}/bin/$f
    %{__sed} -i -e 's/\/opt\/%{name}\/embedded\/bin\/ruby/\/usr\/bin\/ruby/' %{buildroot}%{app_dir}/bin/$f
done

%{__sed} -i -e 's/<%= @name %>/%{name}-client/' %{buildroot}%{app_dir}/bin/%{name}-client
%{__sed} -i -e 's/<%= @name %>/%{name}-api/' %{buildroot}%{app_dir}/bin/%{name}-api
%{__sed} -i -e 's/<%= @name %>/%{name}-server/' %{buildroot}%{app_dir}/bin/%{name}-server
%{__sed} -i -e 's/\/opt\/%{name}\/embedded\/bin\/runsvdir/\/opt\/%{name}\/bin\/runsvdir/' %{buildroot}%{app_dir}/bin/%{name}-runsvdir
%{__sed} -i -e 's/\/opt\/%{name}\/embedded\/bin\/runsvdir/\/opt\/%{name}\/bin\/runsvdir/' %{buildroot}%{app_dir}/bin/%{name}-ctl


#site specific configs:
%{__mkdir_p} -m 0755 %{buildroot}%{_initrddir}
%{__mkdir_p} -m 0755 %{buildroot}%{_sysconfdir}/logrotate.d
%{__mkdir_p} -m 0755 %{buildroot}%{_datadir}/%{name}
%{__install} -p -m 0755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}-service
%{__install} -p -m 0755 %{SOURCE3} %{buildroot}%{_initrddir}/%{name}-server
%{__install} -p -m 0755 %{SOURCE4} %{buildroot}%{_initrddir}/%{name}-client
%{__install} -p -m 0755 %{SOURCE5} %{buildroot}%{_initrddir}/%{name}-api
%{__install} -p -m 0755 %{SOURCE21} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%{__install} -p -m 0755 %{SOURCE22} %{buildroot}%{_sysconfdir}/default/%{name}

# systemd
#%{__install} -p -m 0755 %{SOURCE6} %{buildroot}%{_datadir}/%{name}/%{name}-server
#%{__install} -p -m 0755 %{SOURCE7} %{buildroot}%{_datadir}/%{name}/%{name}-runsvdir
#%{__install} -p -m 0755 %{SOURCE8} %{buildroot}%{_datadir}/%{name}/%{name}-client
#%{__install} -p -m 0755 %{SOURCE9} %{buildroot}%{_datadir}/%{name}/%{name}-api 

# upstart
#%{__install} -p -m 0755 %{SOURCE10} %{buildroot}%{_unitdir}/%{name}-server.service
#%{__install} -p -m 0755 %{SOURCE11} %{buildroot}%{_unitdir}/%{name}-runsvdir.service
#%{__install} -p -m 0755 %{SOURCE12} %{buildroot}%{_unitdir}/%{name}-client.service
#%{__install} -p -m 0755 %{SOURCE13} %{buildroot}%{_unitdir}/%{name}-api.service

# replace all lines in files that used the embedded files, since we're using custom built ruby
for i in `find  %{buildroot} -type f | xargs grep "%{app_dir}/embedded/bin" |grep "\bPATH" | cut -f1 -d ":"`
do
    %{__sed} -i -e 's/PATH=\/opt\/%{name}\/embedded\/bin:/PATH=/g' $i
done

for i in `find  %{buildroot} -type f | xargs grep "%{app_dir}/embedded/lib/ruby/gems/2.0.0" |grep "\bGEM_PATH" | cut -f1 -d ":"`
do
    %{__sed} -i -e 's/GEM_PATH=\/opt\/%{name}\/embedded\/lib\/ruby\/gems\/2.0.0:/GEM_PATH=/g' $i
done

for i in `find  %{buildroot} -type f | xargs grep "%{app_dir}/embedded/bin/chpst" |grep "\bexec" | cut -f1 -d ":"`
do
    %{__sed} -i -e 's/\/opt\/%{name}\/embedded\/bin\/chpst/\/opt\/%{name}\/bin\/chpst/g' $i
done

# one-offs
%{__sed} -i -e 's/\#!\/opt\/%{name}\/embedded\/bin\/ruby/\#\!\/usr\/bin\/ruby/g' %{buildroot}%{app_dir}/bin/%{name}-ctl
%{__sed} -i -e 's/\/opt\/%{name}\/embedded\/bin\/sv/\/opt\/%{name}\/bin\/sv/g' %{buildroot}%{app_dir}/bin/%{name}-ctl
%{__sed} -i -e 's/\/opt\/%{name}\/embedded\/bin\/%{name}-runsvdir/\/opt\/%{name}\/bin\/sv/g' %{buildroot}%{app_dir}/bin/%{name}-ctl
%{__sed} -i -e 's/\/opt\/%{name}\/embedded\/bin\/%{name}-runsvdir/\/opt\/%{name}\/bin\/%{name}-runsvdir/g' %{buildroot}%{app_dir}/bin/%{name}-runsvdir
%{__sed} -i -e 's/\/opt\/%{name}\/embedded\/bin\/runsvdir/\/opt\/%{name}\/bin\/runsvdir/g' %{buildroot}%{app_dir}/bin/%{name}-runsvdir


%pre
%{_bindir}/getent group %{group}|| %{_sbindir}/groupadd -r %{group}
%{_bindir}/getent passwd %{user}|| %{_sbindir}/useradd -r -g %{group} -d %{app_dir} -s /bin/bash -c "Sensu User" %{user} 

%preun -n %{name}-client
if [ $1 = 0 ] ; then
    if [ -x %{_initrddir}/%{name}-client ] ; then
        %{_initrddir}/%{name}-client stop > /dev/null
        /sbin/chkconfig --del %{name}-client
    fi
fi

%preun -n %{name}-server
if [ $1 = 0 ] ; then
    if [ -x %{_initrddir}/%{name}-server ] ; then
        %{_initrddir}/%{name}-server stop > /dev/null
        /sbin/chkconfig --del %{name}-server
    fi
fi

%preun -n %{name}-api
if [ $1 = 0 ] ; then
    if [ -x %{_initrddir}/%{name}-api ] ; then
        %{_initrddir}/%{name}-client api > /dev/null
        /sbin/chkconfig --del %{name}-api
    fi
fi

%triggerpostun -- %{name}
if  getent passwd %{user} >/dev/null; then
    %{_bindir}/userdel %{user}
    if [ -d %{app_dir} ]; then
        %__rm -rf %{app_dir}
    fi
    if [ -d  %{_var}/run/%{name} ]; then
        %__rm -rf  %{_var}/run/%{name}
    fi
fi
#remove group
if  getent group %{group} >/dev/null; then
    if  ! getent passwd uchiwa >/dev/null; then
        %{_sbindir}/groupdel %{group}
    fi
fi

%post
%__chown -R %{user}:%{group} %{_var}/run/%{name}
%__chown -R %{user}:%{group} %{_sysconfdir}/%{name}
%__chown -R %{user}:%{group} %{_var}/log/%{name}
%__chown -R %{user}:%{group} %{app_dir}
%__chown -R %{user}:%{group} %{app_dir}

%post -n %{name}-server
/sbin/chkconfig --add %{name}-server
/sbin/chkconfig %{name}-server on

%post -n %{name}-client
/sbin/chkconfig --add %{name}-client
/sbin/chkconfig %{name}-client on

%post -n %{name}-api
/sbin/chkconfig --add %{name}-api
/sbin/chkconfig %{name}-api on


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
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
%dir %{_var}/run/%{name}
%{_var}/log/%{name}
%{_sysconfdir}/default/%{name}
%{_initrddir}/%{name}-service

%files server
%attr(755, %{user}, %{group})
%{_initrddir}/%{name}-server
%{_sysconfdir}/logrotate.d/%{name}
%{app_dir}/bin/%{name}-api
%{app_dir}/bin/%{name}-ctl
%{app_dir}/bin/%{name}-server
%{app_dir}/service
%{app_dir}/sv/%{name}-server/log/main
%{app_dir}/sv/%{name}-server/log/run
%{app_dir}/sv/%{name}-server/run
%{app_dir}/sv/%{name}-server/supervise
%{app_dir}/bin/chpst
%{app_dir}/bin/runsv
%{app_dir}/bin/runsvdir
%{app_dir}/bin/sv
%{app_dir}/bin/svlogd
%{app_dir}/bin/utmpset
%{app_dir}/bin/%{name}-runsvdir
%{extensions}/handlers/relay.rb
%{extensions}/mutators/metrics.rb



%files api 
%attr(755, %{user}, %{group})
%{_initrddir}/%{name}-api
%{app_dir}/sv/%{name}-api/log/main
%{app_dir}/sv/%{name}-api/log/run
%{app_dir}/sv/%{name}-api/run
%{app_dir}/sv/%{name}-api/supervise

%files configs
%attr(755, %{user}, %{group})
%{conf_dir}/config.json
%{conf_dir}/conf.d/client.json

%files client
%attr(755, %{user}, %{group})
%dir %{confd}
%{_initrddir}/%{name}-client
%{app_dir}/bin/%{name}-client
%{app_dir}/sv/%{name}-client/log/main
%{app_dir}/sv/%{name}-client/log/run
%{app_dir}/sv/%{name}-client/run
%{app_dir}/sv/%{name}-client/supervise
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


