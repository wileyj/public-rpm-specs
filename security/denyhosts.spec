%if 0%{?amzn} >= 1
%define python python27
BuildRequires: %{python} %{python}-rpm-macros %{python}-devel
Requires: %{python} %{python}-setuptools
%else
%define python python
BuildRequires: %{python} %{python}-rpm-macros %{python}-devel
Requires: %{python} %{python}-setuptools
%endif

BuildRequires: git

%define prefix /opt/denyhosts
%define real_name DenyHosts

Summary: Scan ssh server logs and block hosts
Name: denyhosts
Version: 2.6
Release: 5.%{dist}
License: GPL
Vendor: %{vendor}
Packager: %{packager}
Group: Applications/Internet
URL: http://denyhosts.sourceforge.net/
Source: http://downloads.sourceforge.net/%{name}/%{real_name}-%{version}.tar.gz
Source1: reset-blocked-ip.pl
Patch0: denyhosts-2.6-regex.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Buildarch: noarch
Obsoletes: DenyHosts <= %{version}

%description
DenyHosts is a script intended to help Linux system administrators thwart
ssh server attacks. DenyHosts scans an ssh server log, updates
/etc/hosts.deny after a configurable number of failed attempts from a
rogue host is determined, and alerts the administrator of any suspicious
logins.

%prep
%setup -n %{real_name}-%{version}
%patch0 -p1

%build
/usr/bin/%{python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -c -O2 --exec-prefix="%{prefix}/bin" --install-data="%{prefix}/data" --install-lib="%{python_sitearch}" --root="%{buildroot}" --prefix="%{prefix}" 
#%{__python} setup.py install --install-headers --install-scripts --install-data --compile --install-lib="%{python_sitearch}" --root="%{buildroot}" --prefix="%{prefix}" 
%{__rm} -Rf %{buildroot}%{_datadir}/%{name}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/init.d
%{__cp} daemon-control-dist %{buildroot}%{_sysconfdir}/init.d/%{name}
%{__mkdir_p} %{buildroot}%{prefix}/etc
%{__cp} denyhosts.cfg-dist %{buildroot}%{prefix}/etc/%{name}.cfg
%{__install} -m 755 %{SOURCE1} %{buildroot}%{prefix}/bin/
%{__mkdir_p} %{buildroot}%{_bindir}
%{__ln_s} %{prefix}/bin/%{name}.py %{buildroot}%{_bindir}/%{name}.py 
%{__sed} -i -e 's@^DENYHOSTS_CFG   =.*@DENYHOSTS_CFG   = "%{prefix}/etc/%{name}.cfg"@g' %{buildroot}%{_sysconfdir}/init.d/%{name}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%post
if [ -x %{_initrddir}/%{name} ]; then
  /sbin/chkconfig --add %{name}
fi

%preun
if [ "$1" = 0 ]; then
  if [ -x %{_initrddir}/%{name} ]; then
    %{_initrddir}/%{name} stop
    /sbin/chkconfig --del %{name}
  fi
fi

%files
%defattr(-, root, root, 0755)
%doc CHANGELOG.txt daemon-control-dist %{name}.cfg-dist LICENSE.txt README.txt
%{prefix}/bin/%{name}.py*
%{prefix}/bin/reset-blocked-ip.pl
%{python_sitearch}/DenyHosts/
%{python_sitearch}/DenyHosts*.egg-info
%{prefix}/data
%config (noreplace) %{prefix}/etc/%{name}.cfg
/etc/init.d/%{name}
%{_bindir}/%{name}.py


%changelog
