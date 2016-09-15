%if 0%{?amzn} >= 1
%define python python27
BuildRequires: %{python} %{python}-rpm-macros %{python}-devel
Requires: %{python} %{python}-setuptools
%else
%define python python
BuildRequires: %{python} %{python}-rpm-macros %{python}-devel
Requires: %{python} %{python}-setuptools
%endif

%define macro %{_rpmconfigdir}/macros.d/macros.python

%define repo https://github.com/voxpupuli/puppetboard
%define gitversion %(echo `curl -s https://github.com/voxpupuli/puppetboard/releases | grep 'class="css-truncate-target"' | head -1 |  tr -d '\\-</span class="css-truncate-target">'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1`)
%define rel_version 1


%define filelist %{name}-%{version}-filelist

%global _docroots /u/docroots
%global _appdir %{_docroots}/%{name}
%global _logdir %{_localstatedir}/log/%{name}
%global _rundir %{_localstatedir}/run/%{name}
%global uid nginx
%global guid nginx

Name:           puppetboard
Version:        %{gitversion}
Release:        %{rel_version}.%{revision}.%{dist}
Summary:        Web frontend for PuppetDB
License:        ASL
Packager:       %{packager}
Vendor:         %{vendor}
URL:            https://github.com/voxpupuli/puppetboard
Group:          System Environment/Base
Requires:       puppetdb %{python} nginx
Requires:	%{python}-Flask %{python}-Flask-WTF %{python}-jinja2 %{python}-MarkupSafe 
Requires:	%{python}-WTForms %{python}-Werkzeug %{python}-itsdangerous %{python}-pypuppetdb 
Requires:	%{python}-requests %{python}-uwsgi %{python}-uwsgi_metrics %{name}-libs = %{version}-%{release}
BuildArch:      noarch
Source1:	%{name}.ini
Source2:	%{name}.init
Source3:	wsgi.py
Source4:	settings.py
Source5:	puppetboard.conf

%description
%{summary}

%package libs
Summary: python module for puppetboard
Group:  Development/Languages 
Requires: %{name} = %{version}-%{release} %{python}

%description libs
%{summary}



%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update
%{python} setup.py build

%install
cd %{name}-%{version}
rm -rf %{buildroot}

install -d -m0755 %{buildroot}%{_docroots}
install -d -m0755 %{buildroot}%{_logdir}
install -d -m0755 %{buildroot}%{_rundir}
install -d -m0755 %{buildroot}%{_initrddir}
install -d -m0755 %{buildroot}%{_docroots}/%{name}
install -d -m0755 %{buildroot}%{_localstatedir}/log/%{name}
install -d -m0755 %{buildroot}%{_localstatedir}/run/%{name}
install -d -m0755 %{buildroot}%{_sysconfdir}/nginx/sites-available

%{python} setup.py install --skip-build --root $RPM_BUILD_ROOT
rsync -avz --progress --delete * %{buildroot}%{_docroots}/%{name}
install -d -m0755 %{buildroot}%{_docroots}/%{name}/conf
install  -m0644 %{SOURCE1} %{buildroot}%{_docroots}/%{name}/conf/%{name}.ini
install  -m0755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}
install  -m0755 %{SOURCE3} %{buildroot}%{_docroots}/%{name}/wsgi.py
install  -m0755 %{SOURCE4} %{buildroot}%{_docroots}/%{name}/settings.py
install  -m0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/nginx/sites-available/%{name}.conf

rm -rf %{buildroot}%{_docroots}/%{name}/build
(
    cd %{buildroot}
    echo '%defattr(-,root,root,-)'
    find %{buildroot} -type d -not \( -path */u/* -o -path */u -o -path */etc -o -path */etc/* -o -path */var -o -path */var/* -prune \) -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot} -type f -not \( -path */u/* -o -path */u -o -path */etc -o -path */etc/* -o -path */var -o -path */var/* -prune \) -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    echo '%exclude "%{python_sitelib}/%{name}/*.pyo"'
    echo '%exclude "%{python_sitelib}/%{name}/*.pyc"'
) >  %{filelist}
sed -i -e 's|%dir ""||g' %{filelist}

%post
/sbin/chkconfig --add %{name} || :
if [ "$1" -ge 1 ]; then
  oldpid="%{_rundir}/%{name}d.pid"
  newpid="%{_rundir}/agent.pid"
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

%preun
if [ "$1" = 0 ] ; then
    /sbin/service %{name} stop > /dev/null 2>&1
    /sbin/chkconfig --del %{name} || :
fi

%postun
if [ "$1" -ge 1 ]; then
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-, %{uid}, %{guid})
%exclude %{_appdir}/*.pyc
%exclude %{_appdir}/*.pyo
%exclude %{_appdir}/test/*.pyo
%exclude %{_appdir}/test/*.pyc
%exclude %{_appdir}/%{name}/*.pyo
%exclude %{_appdir}/%{name}/*.pyc

%config(noreplace) %attr(0644, %{uid}, %{guid}) %{_appdir}/conf/%{name}.ini
%config(noreplace) %attr(0755, %{uid}, %{guid}) %{_appdir}/settings.py
%config(noreplace) %attr(0755, %{uid}, %{guid}) %{_appdir}/wsgi.py
%config(noreplace) %attr(0644, %{uid}, %{guid}) %{_sysconfdir}/nginx/sites-available/%{name}.conf
%attr(0755, %{uid}, %{guid}) %{_initrddir}/%{name}
%dir %{_appdir}
%dir %{_rundir}
%dir %{_logdir}
%{_appdir}/*

%files libs -f %{name}-%{version}/%{filelist}

