%include %{_rpmconfigdir}/macros.d/macros.python27
%global srcname graphite-web

%define __touch    /bin/touch
%define __service  /sbin/service

Name:           python27-%{srcname}
Version:        0.9.10
Release:        3.%{dist}
Summary:        Enterprise scalable realtime graphing
Group:          Applications/Internet
License:        Apache License
URL:            https://launchpad.net/graphite
Vendor: %{vendor}
Packager: %{packager}
Source0:        https://github.com/downloads/graphite-project/%{srcname}/%{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{srcname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python27 python27-devel python27-setuptools
Requires:       Django django-tagging httpd mod_wsgi pycairo python27-simplejson
Requires: 	bitmap-fonts-compat

%description
Graphite consists of a storage backend and a web-based visualization frontend.
Client applications send streams of numeric time-series data to the Graphite
backend (called carbon), where it gets stored in fixed-size database files
similar in design to RRD. The web frontend provides 2 distinct user interfaces
for visualizing this data in graphs as well as a simple URL-based API for
direct graph generation.

Graphite's design is focused on providing simple interfaces (both to users and
applications), real-time visualization, high-availability, and enterprise
scalability.

%prep
%setup -q -n %{srcname}-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python27} -c 'import setuptools; execfile("setup.py")' build

%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}
%{__python27} -c 'import setuptools; execfile("setup.py")' install --skip-build --root %{buildroot}

# Create var directory with ghost files
%{__mkdir_p} %{buildroot}%{_localstatedir}/lib/%{srcname}
%{__touch} %{buildroot}%{_localstatedir}/lib/%{srcname}/graphite.db

# Create log directory with ghost files
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/%{srcname}
%{__touch} %{buildroot}%{_localstatedir}/log/%{srcname}/access.log
%{__touch} %{buildroot}%{_localstatedir}/log/%{srcname}/error.log
%{__touch} %{buildroot}%{_localstatedir}/log/%{srcname}/exception.log
%{__touch} %{buildroot}%{_localstatedir}/log/%{srcname}/info.log

# Create config directory and install configuration files
%{__mkdir_p} %{buildroot}%{_sysconfdir}/%{srcname}
%{__install} -Dp -m0644 conf/dashboard.conf.example %{buildroot}%{_sysconfdir}/%{srcname}/dashboard.conf
%{__install} -Dp -m0644 webapp/graphite/local_settings.py.example %{buildroot}%{_sysconfdir}/%{srcname}/local_settings.py

# Install the example wsgi controller and vhost configuration
%{__install} -Dp -m0755 conf/graphite.wsgi.example %{buildroot}/usr/share/graphite/%{srcname}.wsgi
%{__install} -Dp -m0644 examples/example-graphite-vhost.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/%{srcname}.conf

# Create local_settings symlink
%{__mkdir_p} %{buildroot}%{python27_sitelib}/graphite
%{__ln_s} %{_sysconfdir}/%{srcname}/local_settings.py %{buildroot}%{python27_sitelib}/graphite/local_settings.py

%post
# Initialize the database
%{__python27} %{python27_sitelib}/graphite/manage.py syncdb --noinput >/dev/null
%{__chown} apache:apache %{_localstatedir}/lib/%{srcname}/graphite.db

%posttrans
# TEMPORARY FIX
#
# The 0.9.8-x versions of this RPM symlinked local_settings.py in during %post
# and removed it during %preun. This was replaced in 0.9.9-1 with a standard
# %files entry.
#
# When upgrading from 0.9.8 to 0.9.9 the %preun action of the previous version
# removes the %files entry of the new version. This check reinstates the
# symlink. It does not affect fresh installs and can be removed in subsequent
# releases.
[ -e %{python27_sitelib}/graphite/local_settings.py ] || \
    %{__ln_s} %{_sysconfdir}/%{srcname}/local_settings.py %{python27_sitelib}/graphite/local_settings.py

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{srcname}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{srcname}-%{version}
[ "%{_builddir}/%{srcname}" != "/" ] && %__rm -rf %{_builddir}/%{srcname}

%files
%defattr(-,root,root,-)
%doc INSTALL LICENSE conf/* examples/*

%{python27_sitelib}/graphite
/opt/graphite/*
/usr/share/graphite
/etc/httpd/conf.d/%{srcname}.conf

%config %{_sysconfdir}/%{srcname}

%attr(775,root,apache) %dir %{_localstatedir}/log/%{srcname}
%ghost %{_localstatedir}/log/%{srcname}/access.log
%ghost %{_localstatedir}/log/%{srcname}/error.log
%ghost %{_localstatedir}/log/%{srcname}/exception.log
%ghost %{_localstatedir}/log/%{srcname}/info.log

%attr(775,root,apache) %dir %{_localstatedir}/lib/%{srcname}
%ghost %{_localstatedir}/lib/%{srcname}/graphite.db

%changelog
