#%global with_python3  0
%define pypi_name DenyHosts
%define pypi_alternate denyhosts
%define prefix /opt/denyhosts

%define repo https://github.com/denyhosts/denyhosts
%define git_version %(echo `curl -s %{repo}/releases | grep 'class="css-truncate-target"' | head -1 |  tr -d '\\-</span class="css-truncate-target">v'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1
%define build_time %(echo `date +%s`)
%global pypi_summary %(echo `curl -s %{pypi_url} | grep '<meta name="description" content=' | cut -d'"' -f4`)

Name:           %{pypi_alternate}
Version:        %{git_version}
Release:        %{rel_version}.%{?dist}
Summary:        "%{pypi_summary}"
Group:          Development/Languages
License:        MIT
URL:            %{repo}
Source1: 	reset-blocked-ip.pl
Source2: 	reset-blocked.py
BuildArch: noarch

%if 0%{?with_python3}

Provides:       python3-%{pypi_name} = %{version}-%{release}
Provides:       python3-%{pypi_alternate} = %{version}-%{release}
Provides:       %{pypi_alternate} = %{version}-%{release}
Provides:       %{pypi_name} = %{version}-%{release}
Obsoletes:      python3-%{pypi_name} < %{version}-%{release}
Obsoletes:      python3-%{pypi_alternate} < %{version}-%{release}
Obsoletes:      %{pypi_alternate} < %{version}-%{release}
Obsoletes:      %{pypi_name} < %{version}-%{release}
BuildRequires:  python3-devel python3-rpm-macros python-srpm-macros
BuildRequires:	python3-ipaddr
Requires:       python3-six python3-ipaddr
%else
Provides:       python-%{pypi_name} = %{version}-%{release}
Provides:       python-%{pypi_alternate} = %{version}-%{release}
Provides:       %{pypi_alternate} = %{version}-%{release}
Provides:       %{pypi_name} = %{version}-%{release}
Obsoletes:      python-%{pypi_name} < %{version}-%{release}
Obsoletes:      python-%{pypi_alternate} < %{version}-%{release}
Obsoletes:      %{pypi_alternate} < %{version}-%{release}
Obsoletes:      %{pypi_name} < %{version}-%{release}
BuildRequires:  python-devel python2-rpm-macros python-srpm-macros
BuildRequires:  python-ipaddr
Requires:       python-six python-ipaddr
%endif

%description
%{summary} for Python

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
if [ -d %{buildroot} ];then
    rm -rf %{buildroot}
fi

git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update

%if 0%{?with_python3}
%__sed -i -e 's|import ipaddr|import ipaddress|g' DenyHosts/util.py
rm -rf %{py3dir}
cp -a . %{py3dir}
%else
rm -rf %{py2dir}
cp -a . %{py2dir}
%endif

%build
cd $RPM_BUILD_DIR/%{name}-%{version}
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%else
pushd %{py2dir}
%{__python2} setup.py build
popd
%endif

%install
cd $RPM_BUILD_DIR/%{name}-%{version}
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -c -O2 --exec-prefix="%{prefix}/bin" --install-data="%{prefix}/data" --install-lib="%{python3_sitearch}" --root="%{buildroot}" --prefix="%{prefix}"
find %{buildroot}%{_prefix} -type d -depth -exec rmdir {} \; 2>/dev/null
popd
%else
pushd %{py2dir}
%{__python2} setup.py install -c -O2 --exec-prefix="%{prefix}/bin" --install-data="%{prefix}/data" --install-lib="%{python_sitearch}" --root="%{buildroot}" --prefix="%{prefix}"
find %{buildroot}%{_prefix} -type d -depth -exec rmdir {} \; 2>/dev/null
popd
%endif


%{__rm} -Rf %{buildroot}%{_datadir}/%{pypi_alternate}
%{__mkdir_p} %{buildroot}%{_initrddir}
%{__cp} daemon-control-dist %{buildroot}%{_initrddir}/%{pypi_alternate}
%{__mkdir_p} %{buildroot}%{prefix}/etc
%{__cp} denyhosts.conf %{buildroot}%{prefix}/etc/%{pypi_alternate}.conf
%{__install} -m 755 %{SOURCE1} %{buildroot}%{prefix}/bin/
%{__install} -m 755 %{SOURCE2} %{buildroot}%{prefix}/bin/
%{__mkdir_p} %{buildroot}%{_bindir}
%{__ln_s} %{prefix}/bin/%{name}.py %{buildroot}%{_bindir}/%{pypi_alternate}.py
%{__ln_s} %{prefix}/bin/%{name}.py %{buildroot}%{_bindir}/%{pypi_alternate}
%__rm -f  %{buildroot}%{_sysconfdir}/%{pypi_alternate}.conf
%{__ln_s} %{prefix}/etc/%{pypi_alternate}.conf  %{buildroot}%{_sysconfdir}/%{pypi_alternate}.conf
%{__sed} -i -e 's@^DENYHOSTS_CFG   =.*@DENYHOSTS_CFG   = "%{prefix}/etc/%{pypi_alternate}.conf"@g' %{buildroot}%{_initrddir}/%{pypi_alternate}


%post
if [ -x %{_initrddir}/%{pypi_alternate} ]; then
  /sbin/chkconfig --add %{pypi_alternate}
fi

%preun
if [ "$1" = 0 ]; then
  if [ -x %{_initrddir}/%{pypi_alternate} ]; then
    %{_initrddir}/%{pypi_alternate} stop
    /sbin/chkconfig --del %{pypi_alternate}
  fi
fi


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
[ "%{_builddir}/python-%{pypi_name}-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python-python-%{pypi_name}-%{version}-%{release}
[ "%{_builddir}/python2-%{pypi_name}-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python2-python-%{pypi_name}-%{version}-%{release}
[ "%{_builddir}/python3-%{pypi_name}-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python3-python-%{pypi_name}-%{version}-%{release}



%files
%{prefix}/bin/%{pypi_alternate}*
%{prefix}/bin/daemon-control-dist
%{_bindir}/%{pypi_alternate}
%{prefix}/bin/reset-blocked-ip.pl
%{prefix}/bin/reset-blocked.py
%{prefix}/data
%{_sysconfdir}/%{pypi_alternate}.conf
%config (noreplace) %{prefix}/etc/%{pypi_alternate}*
%{_initrddir}/%{pypi_alternate}
%{_bindir}/%{pypi_alternate}.py
%if 0%{?with_python3}
%{python3_sitearch}/*
%else
%{python_sitearch}/*
%endif

%{_mandir}/man8/*

