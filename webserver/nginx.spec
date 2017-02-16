%define repo https://github.com/nginx/nginx
%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">r'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1

%define nginx_home %{_localstatedir}/cache/nginx
%define nginx_user nginx
%define nginx_group nginx
%define prefix /opt/nginx
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)

Summary: High performance web server
Name: nginx
Version: %{gitversion}
Release: %{rel_version}.%{revision}.%{dist}
URL: http://nginx.org/
Group: System Environment/Daemons
Source1: logrotate
Source2: nginx.init
Source3: nginx.sysconf
Source4: nginx.conf
Source5: nginx.vh.default.conf
Source6: nginx.vh.example_ssl.conf
Source7: nginx.suse.init
Source8: nginx.service
Source9: nginx.upgrade.sh
Source10: logging.conf
Source11: status.conf
Source12: virtual.conf
License: 2-clause BSD-like license
Vendor: %{vendor}
Packager: %{packager}
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
Requires: openssl >= 1.0.1
BuildRequires: openssl-devel >= 1.0.1
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: zlib-devel
BuildRequires: pcre-devel GeoIP-devel
Provides: webserver

%if 0%{?rhel}  == 7
Group: System Environment/Daemons
Requires(pre): shadow-utils
Requires: systemd
Requires: openssl >= 1.0.1
BuildRequires: systemd
BuildRequires: openssl-devel >= 1.0.1
%endif

%description
nginx [engine x] is an HTTP and reverse proxy server, as well as
a mail proxy server.

#%package debug
#Summary: debug version of nginx
#Group: System Environment/Daemons
#Requires: nginx
#%description debug
#Not stripped version of nginx built with the debugging log support.

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
find examples/ -type f | xargs --no-run-if-empty chmod a-x
./auto/configure \
        --prefix=%{prefix} \
        --sbin-path=%{_sbindir}/%{name} \
        --conf-path=%{prefix}/nginx.conf \
        --error-log-path=%{_localstatedir}/log/nginx/error.log \
        --http-log-path=%{_localstatedir}/log/nginx/access.log \
        --pid-path=%{_localstatedir}/run/nginx.pid \
        --lock-path=%{_localstatedir}/run/nginx.lock \
        --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp \
        --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp \
        --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp \
        --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp \
        --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp \
        --user=%{nginx_user} \
        --group=%{nginx_group} \
        --with-http_ssl_module \
        --with-http_realip_module \
        --with-http_addition_module \
        --with-http_sub_module \
        --with-http_dav_module \
        --with-http_flv_module \
        --with-http_mp4_module \
        --with-http_gunzip_module \
        --with-http_gzip_static_module \
        --with-http_random_index_module \
        --with-http_secure_link_module \
        --with-http_stub_status_module \
        --with-http_auth_request_module \
        --with-http_geoip_module \
        --with-http_v2_module \
        --with-http_realip_module \
        --with-mail \
        --with-mail_ssl_module \
        --with-file-aio \
        --with-ipv6 \
        --with-stream \
        --with-stream_ssl_module \
        --with-threads \
        --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
        $*
make %{?_smp_mflags}

%install
cd %{name}-%{version}
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install

%{__rm} -f $RPM_BUILD_ROOT%{prefix}/*.default
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/run/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/cache/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{prefix}/conf.d
%{__mkdir} -p $RPM_BUILD_ROOT%{prefix}/sites-available
%{__mkdir} -p $RPM_BUILD_ROOT%{prefix}/sites-enabled
%{__rm} $RPM_BUILD_ROOT%{prefix}/nginx.conf
%{__install} -m 644 -p %{SOURCE4} $RPM_BUILD_ROOT%{prefix}/nginx.conf
#%{__install} -m 644 -p %{SOURCE5} $RPM_BUILD_ROOT%{prefix}/conf.d/default.conf
#%{__install} -m 644 -p %{SOURCE6} $RPM_BUILD_ROOT%{prefix}/conf.d/example_ssl.conf
%{__install} -m 644 -p %{SOURCE10} $RPM_BUILD_ROOT%{prefix}/conf.d/logging.conf
%{__install} -m 644 -p %{SOURCE11} $RPM_BUILD_ROOT%{prefix}/conf.d/status.conf
%{__install} -m 644 -p %{SOURCE12} $RPM_BUILD_ROOT%{prefix}/conf.d/virtual.conf
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -m 644 -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/nginx

%if %{use_systemd}
    %{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
    %{__install} -m644 %SOURCE8 $RPM_BUILD_ROOT%{_unitdir}/nginx.service
    %{__mkdir} -p $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/nginx
    %{__install} -m755 %SOURCE9 $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/nginx/upgrade
%else
    %{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
    %{__install} -m755 %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/nginx
%endif
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -m 644 -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/nginx
#%{__install} -m644 %{_builddir}/%{name}/objs/nginx.debug $RPM_BUILD_ROOT%{_sbindir}/nginx.debug


ln -s %{prefix} %{buildroot}%{_sysconfdir}/%{name}

%pre
getent group %{nginx_group} >/dev/null || groupadd -r %{nginx_group}
getent passwd %{nginx_user} >/dev/null || \
    useradd -r -g %{nginx_group} -s /sbin/nologin \
    -d %{nginx_home} -c "nginx user"  %{nginx_user}
exit 0

%post
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset nginx.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add nginx
%endif
    # print site info
    cat <<BANNER
----------------------------------------------------------------------

Thanks for using nginx!

Please find the official documentation for nginx here:
* http://nginx.org/en/docs/

Commercial subscriptions for nginx are available on:
* http://nginx.com/products/

----------------------------------------------------------------------
BANNER

    # Touch and set permisions on default log files on installation

    if [ -d %{_localstatedir}/log/nginx ]; then
        if [ ! -e %{_localstatedir}/log/nginx/access.log ]; then
            touch %{_localstatedir}/log/nginx/access.log
            %{__chmod} 640 %{_localstatedir}/log/nginx/access.log
            %{__chown} nginx:adm %{_localstatedir}/log/nginx/access.log
        fi

        if [ ! -e %{_localstatedir}/log/nginx/error.log ]; then
            touch %{_localstatedir}/log/nginx/error.log
            %{__chmod} 640 %{_localstatedir}/log/nginx/error.log
            %{__chown} nginx:adm %{_localstatedir}/log/nginx/error.log
        fi
    fi
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable nginx.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop nginx.service >/dev/null 2>&1 ||:
%else
    /sbin/service nginx stop > /dev/null 2>&1
    /sbin/chkconfig --del nginx
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service nginx status  >/dev/null 2>&1 || exit 0
    /sbin/service nginx upgrade >/dev/null 2>&1 || echo \
        "Binary upgrade failed, please check nginx's error.log"
fi

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name} 

%files
%defattr(-,root,root)
%{_sbindir}/%{name}
%dir %{prefix}/conf.d
%dir %{prefix}/sites-available
%dir %{prefix}/sites-enabled
%config(noreplace) %{prefix}/%{name}.conf
%config(noreplace) %{prefix}/conf.d/virtual.conf
%config(noreplace) %{prefix}/conf.d/logging.conf
%config(noreplace) %{prefix}/conf.d/status.conf
#%config(noreplace) %{prefix}/conf.d/example_ssl.conf
%config(noreplace) %{prefix}/conf.d/logging.conf
%config(noreplace) %{prefix}/mime.types
%config(noreplace) %{prefix}/fastcgi_params
%config(noreplace) %{prefix}/fastcgi.conf
%config(noreplace) %{prefix}/scgi_params
%config(noreplace) %{prefix}/uwsgi_params
%config(noreplace) %{prefix}/koi-utf
%config(noreplace) %{prefix}/koi-win
%config(noreplace) %{prefix}/win-utf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{prefix}/html/*
%if %{use_systemd}
%{_unitdir}/nginx.service
%dir %{_libexecdir}/initscripts/legacy-actions/%{name}
%{_libexecdir}/initscripts/legacy-actions/%{name}/*
%else
%{_initrddir}/%{name}
%endif
%attr(0755,root,root) %dir %{_localstatedir}/cache/%{name}
%attr(0755,root,root) %dir %{_localstatedir}/log/%{name}
%attr(0755,root,root) %dir %{prefix}/html
%{_sysconfdir}/%{name}

%changelog
