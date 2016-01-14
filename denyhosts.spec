%if 0%{?el6}
    %define macro %{_rpmconfigdir}/macros.d/macros.python27
    %global __python /usr/bin/python27
%else
    %define macro %{_rpmconfigdir}/macros.d/macros.python
    %global __python /usr/bin/python
%endif

%include %{macro}

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
%if 0%{?el6}
BuildRequires: python27-devel >= 2.7
Requires: python27
%else
BuildRequires: python-devel >= 2.7
Requires: python
%endif

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
/usr/bin/python2.7 setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -c -O2 --exec-prefix="%{prefix}/bin" --install-data="%{prefix}/data" --install-lib="%{python_sitearch}/site-packages" --root="%{buildroot}" --prefix="%{prefix}" 
#%{__python} setup.py install --install-headers --install-scripts --install-data --compile --install-lib="%{python_sitearch}/site-packages" --root="%{buildroot}" --prefix="%{prefix}" 
%{__rm} -Rf %{buildroot}%{_datadir}/denyhosts
%{__mkdir_p} %{buildroot}%{_sysconfdir}/init.d
%{__cp} daemon-control-dist %{buildroot}%{_sysconfdir}/init.d/denyhosts
%{__mkdir_p} %{buildroot}%{prefix}/etc
%{__cp} denyhosts.cfg-dist %{buildroot}%{prefix}/etc/denyhosts.cfg
%{__install} -m 755 %{SOURCE1} %{buildroot}%{prefix}/bin/
%{__sed} -i -e 's@^DENYHOSTS_CFG   =.*@DENYHOSTS_CFG   = "%{prefix}/etc/denyhosts.cfg"@g' %{buildroot}%{_sysconfdir}/init.d/denyhosts

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

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
%doc CHANGELOG.txt daemon-control-dist denyhosts.cfg-dist LICENSE.txt README.txt
%{prefix}/bin/denyhosts.py*
%{prefix}/bin/reset-blocked-ip.pl
%{python_sitearch}/site-packages/DenyHosts/
%{python_sitearch}/site-packages/DenyHosts-2.6.egg-info
%{prefix}/data
%config (noreplace) %{prefix}/etc/denyhosts.cfg
/etc/init.d/denyhosts

%changelog
