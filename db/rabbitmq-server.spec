%if 0%{?amzn} >= 1
%define python python27
BuildRequires: %{python} %{python}-rpm-macros %{python}-devel
Requires: %{python} %{python}-setuptools
%else
%define python python
BuildRequires: %{python} %{python}-rpm-macros %{python}-devel
Requires: %{python} %{python}-setuptools
%endif

%global shortname rabbitmq
%global erlang_minver R12B-3
%global _rabbit_libdir %{_exec_prefix}/lib/rabbitmq
%define filelist %{name}-%{version}-filelist

#%define rmq_mandir %{_mandir}
#%define rmq_prefix /usr
#%define rmq_rootdir %{rmq_prefix}/lib/%{shortname}
#%define rmq_bindir %{rmq_rootdir}/bin
#%define rmq_sbindir %{rmq_rootdir}/sbin
#%define rmq_libdir %{rmq_rootdir}/lib
#%define rmq_erlapp_dir %{rmq_libdir}/rabbitmq_server-%{VERSION}

Name: %{shortname}-server
Version: 3.6.1
Release: 2.%{?dist}
License: MPLv1.1
Group: Development/Libraries
Source: http://www.rabbitmq.com/releases/rabbitmq-server/v%{version}/%{name}-%{version}.tar.xz
Source1: %{name}.init
Source2: %{shortname}-script-wrapper
Source3: %{shortname}-server.logrotate
Source4: %{shortname}-server.ocf
Source5: %{shortname}-server.tmpfiles
URL: http://www.rabbitmq.com/
BuildArch: noarch
BuildRequires: erlang >= %{erlang_minver} %{python}-simplejson xmlto libxslt zip
BuildRequires: erlang-observer erlang-gs erlang-et erlang-jinterface erlang-epmd erlang-reltool erlang-src
Requires: logrotate erlang erlang-observer erlang-gs erlang-et erlang-jinterface erlang-epmd erlang-reltool erlang-src
Summary: The RabbitMQ server
Requires(pre): shadow-utils

Patch1: rabbitmq-common-0001-Use-ephemeral-port-for-probing.patch
Patch2: rabbitmq-server-0001-Make-slaves-wait-timeout-configurable-instead-of-har.patch

%description
RabbitMQ is an implementation of AMQP, the emerging standard for high
performance enterprise messaging. The RabbitMQ server is a robust and
scalable implementation of an AMQP broker.

%prep
%setup -q

cd deps/rabbit_common
%patch1 -p1 -b .ephemeral
cd -
%patch2 -p1 -b .slave_wait_timeout_configurable

%build
#USE_SPECS="true" USE_PROPER_QC="false" make %{?_smp_mflags}
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_localstatedir}/lib/%{shortname}
mkdir -p %{buildroot}%{_localstatedir}/log/%{shortname}

make install \
        DESTDIR=%{buildroot} \
        PREFIX=%{_prefix} \
        RMQ_ROOTDIR=%{_rabbit_libdir}

make install-bin \
        DESTDIR=%{buildroot} \
        PREFIX=%{_prefix} \
        RMQ_ROOTDIR=%{_rabbit_libdir}

make install-man \
        DESTDIR=%{buildroot} \
        PREFIX=%{_prefix} \
        RMQ_ROOTDIR=%{_rabbit_libdir}

mkdir -p %{buildroot}%{_localstatedir}/lib/rabbitmq
mkdir -p %{buildroot}%{_localstatedir}/log/rabbitmq
sed -i -e 's|/usr/lib/rabbitmq/bin|%{_rabbit_libdir}/lib/rabbitmq_server-%{version}/sbin|g' %{S:2}

install -p -D -m 0755 %{S:1} %{buildroot}%{_initrddir}/%{name}
install -p -D -m 0755 %{S:2} %{buildroot}%{_sbindir}/rabbitmqctl
install -p -D -m 0755 %{S:2} %{buildroot}%{_sbindir}/rabbitmq-server
install -p -D -m 0755 %{S:2} %{buildroot}%{_sbindir}/rabbitmq-plugins
install -p -D -m 0755 %{S:4} %{buildroot}%{_exec_prefix}/lib/ocf/resource.d/rabbitmq/rabbitmq-server
install -p -D -m 0644 %{S:3} %{buildroot}%{_sysconfdir}/logrotate.d/rabbitmq-server
install -p -D -m 0644 docs/rabbitmq.config.example %{buildroot}%{_sysconfdir}/rabbitmq/rabbitmq.config

rm %{buildroot}%{_rabbit_libdir}/lib/rabbitmq_server-%{version}/{LICENSE,LICENSE-*,INSTALL}


install -d %{buildroot}%{_localstatedir}/run/%{shortname}
install -p -D -m 0644 %{SOURCE5} %{buildroot}%{_prefix}/lib/tmpfiles.d/%{name}.conf

#Build the list of files
echo '%defattr(-,root,root, -)' >%{_builddir}/%{name}.files
find %{buildroot} -path %{buildroot}%{_sysconfdir} -prune -o '!' -type d -printf "/%%P\n" >>%{filelist}


%pre
if [ $1 -gt 1 ]; then
	/sbin/service %{name} stop
fi

if ! getent group %{shortname} >/dev/null; then
	groupadd -r %{shortname} 
fi

if ! getent passwd  %{shortname} >/dev/null; then
	useradd -r -g %{shortname} -d %{_localstatedir}/lib/%{shortname} %{shortname} -c "RabbitMQ messaging server"
fi

%post
/sbin/chkconfig --add %{name}
if [ -f %{_sysconfdir}/%{shortname}/%{shortname}.conf ] && [ ! -f %{_sysconfdir}/%{shortname}/%{shortname}-env.conf ]; then
	mv %{_sysconfdir}/%{shortname}/%{shortname}.conf %{_sysconfdir}/%{shortname}/%{shortname}-env.conf
fi

%preun
if [ $1 = 0 ]; then
 	/sbin/service %{name} stop
  	/sbin/chkconfig --del %{name}
fi

rm -rf %{_localstatedir}/lib/%{shortname}/plugins
for ext in rel script boot ; do
    rm -f %{_rabbit_libdir}/lib/rabbitmq_server-%{version}/ebin/rabbit.$ext
done


%postun

%triggerun -- %{name} < 3.5.7-3
/usr/bin/chown -R %{shortname}:%{shortname} %{_sysconfdir}/%{shortname}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files -f %{filelist}
%defattr(-,rabbitmq,rabbitmq)
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %attr(0644, rabbitmq, rabbitmq) %{_sysconfdir}/%{shortname}/%{shortname}.config
%{_initrddir}/%{name}
%dir %attr(0755, rabbitmq, rabbitmq) %{_localstatedir}/lib/%{shortname}
%dir %attr(0755, rabbitmq, rabbitmq) %{_localstatedir}/log/%{shortname}

#%files
#%dir %attr(0755, rabbitmq, rabbitmq) %{_sysconfdir}/%{shortname}
#%config(noreplace) %attr(0644, rabbitmq, rabbitmq) %{_sysconfdir}/%{shortname}/%{shortname}.config
#%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
#%dir %{_rabbit_libdir}
#%dir %{_rabbit_libdir}/lib
#%{_sbindir}/rabbitmqctl
#%{_sbindir}/%{name}
#%{_sbindir}/%{shortname}-plugins
#%{_rabbit_libdir}/bin/%{shortname}-defaults
#%{_rabbit_libdir}/bin/%{shortname}-env
#%{_rabbit_libdir}/bin/%{shortname}-plugins
#%{_rabbit_libdir}/bin/%{shortname}-server
#%{_rabbit_libdir}/bin/rabbitmqctl
#%{_rabbit_libdir}/lib/rabbitmq_server-%{version}/
#%{_initrddir}/%{name}
#%dir /usr/lib/ocf/resource.d/%{shortname}/
#/usr/lib/ocf/resource.d/%{shortname}/%{name}
#%{_prefix}/lib/tmpfiles.d/%{name}.conf
#%dir %attr(0750, rabbitmq, rabbitmq) %{_localstatedir}/lib/%{shortname}
#%dir %attr(0750, rabbitmq, rabbitmq) %{_localstatedir}/log/%{shortname}
#%dir %attr(0755, rabbitmq, rabbitmq) %{_localstatedir}/run/%{shortname}
#%doc LICENSE LICENSE-* docs/rabbitmq.config.example
#%{_mandir}/man1/rabbitmq-plugins.1*
#%{_mandir}/man1/rabbitmq-server.1*
#%{_mandir}/man1/rabbitmqctl.1*
#%{_mandir}/man5/rabbitmq-env.conf.5*

%changelog
