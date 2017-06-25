%define repo https://github.com/rpm-software-management/dnf
%define gitversion %(echo `curl -s  %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1

%global hawkey_version 0.7.1
%global librepo_version 1.7.19
%global libcomps_version 0.1.8
%global rpm_version 4.13.0-0.rc1.29
%global min_plugins_core 0.1.13
%global dnf_langpacks_ver 0.15.1-6
%global confdir %{_sysconfdir}/%{name}
%global pluginconfpath %{confdir}/plugins
%global py2pluginpath %{python2_sitelib}/%{name}-plugins
%bcond_with python3
%global py3pluginpath %{python3_sitelib}/%{name}-plugins

# Use the same directory of the main package for subpackage licence and docs
%global _docdir_fmt %{name}

Name:           dnf
Version:        %{gitversion}
Release:        %{rel_version}.%{revision}.%{dist}
Summary:        Package manager forked from Yum, using libsolv as a dependency resolver
# For a breakdown of the licensing, see PACKAGE-LICENSING
License:        GPLv2+ and GPLv2 and GPL
URL:            https://github.com/rpm-software-management/dnf
#Source0:        %{url}/archive/%{name}-%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  cmake
BuildRequires:  gettext
BuildRequires:  python-bugzilla
BuildRequires:  python-sphinx
BuildRequires:  systemd
BuildRequires:  bash-completion
Requires:       python3-%{name} = %{version}-%{release}
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
Provides:       dnf-command(autoremove)
Provides:       dnf-command(check-update)
Provides:       dnf-command(clean)
Provides:       dnf-command(distro-sync)
Provides:       dnf-command(downgrade)
Provides:       dnf-command(group)
Provides:       dnf-command(history)
Provides:       dnf-command(info)
Provides:       dnf-command(install)
Provides:       dnf-command(list)
Provides:       dnf-command(makecache)
Provides:       dnf-command(mark)
Provides:       dnf-command(provides)
Provides:       dnf-command(reinstall)
Provides:       dnf-command(remove)
Provides:       dnf-command(repolist)
Provides:       dnf-command(repoquery)
Provides:       dnf-command(repository-packages)
Provides:       dnf-command(search)
Provides:       dnf-command(updateinfo)
Provides:       dnf-command(upgrade)
Provides:       dnf-command(upgrade-to)
Conflicts:      python2-dnf-plugins-core < %{min_plugins_core}
Conflicts:      python3-dnf-plugins-core < %{min_plugins_core}

# dnf-langpacks package is retired in F25
# to have clean upgrade path for dnf-langpacks
Obsoletes:      dnf-langpacks < %{dnf_langpacks_ver}

%description
Package manager forked from Yum, using libsolv as a dependency resolver.

%package conf
Summary:        Configuration files for DNF
Requires:       libreport-filesystem
# dnf-langpacks package is retired in F25
# to have clean upgrade path for dnf-langpacks
Obsoletes:      dnf-langpacks-conf < %{dnf_langpacks_ver}

%description conf
Configuration files for DNF.

%package yum
Conflicts:      yum < 3.4.3-505
Requires:       %{name} = %{version}-%{release}
Summary:        As a Yum CLI compatibility layer, supplies /usr/bin/yum redirecting to DNF

%description yum
As a Yum CLI compatibility layer, supplies /usr/bin/yum redirecting to DNF.

%package -n python2-%{name}
Summary:        Python 2 interface to DNF
%{?python_provide:%python_provide python2-%{name}}
BuildRequires:  python2-devel
BuildRequires:  python-hawkey >= %{hawkey_version}
BuildRequires:  python-iniparse
BuildRequires:  python-libcomps >= %{libcomps_version}
BuildRequires:  python-librepo >= %{librepo_version}
BuildRequires:  python-nose
%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:  pygpgme
%else
BuildRequires:  python2-pygpgme
%endif
BuildRequires:  pyliblzma
BuildRequires:  rpm-python >= %{rpm_version}
Requires:       pyliblzma
Requires:       %{name}-conf = %{version}-%{release}
Requires:       deltarpm
Requires:       python-hawkey >= %{hawkey_version}
Requires:       python-iniparse
Requires:       python-libcomps >= %{libcomps_version}
Requires:       python-librepo >= %{librepo_version}
%if 0%{?rhel} && 0%{?rhel} <= 7
Requires:       pygpgme
%else
Requires:       python2-pygpgme
%endif
Requires:       rpm-plugin-systemd-inhibit
Requires:       rpm-python >= %{rpm_version}
# dnf-langpacks package is retired in F25
# to have clean upgrade path for dnf-langpacks
Obsoletes:      python-dnf-langpacks < %{dnf_langpacks_ver}

%description -n python2-%{name}
Python 2 interface to DNF.

%if %{with python3}
%package -n python3-%{name}
Summary:        Python 3 interface to DNF.
%{?system_python_abi}
%{?python_provide:%python_provide python3-%{name}}
BuildRequires:  python3-devel
BuildRequires:  python3-hawkey >= %{hawkey_version}
BuildRequires:  python3-iniparse
BuildRequires:  python3-libcomps >= %{libcomps_version}
BuildRequires:  python3-librepo >= %{librepo_version}
BuildRequires:  python3-nose
BuildRequires:  python3-pygpgme
BuildRequires:  rpm-python3 >= %{rpm_version}
Requires:       %{name}-conf = %{version}-%{release}
Requires:       deltarpm
Requires:       python3-hawkey >= %{hawkey_version}
Requires:       python3-iniparse
Requires:       python3-libcomps >= %{libcomps_version}
Requires:       python3-librepo >= %{librepo_version}
Requires:       python3-pygpgme
Requires:       rpm-plugin-systemd-inhibit
Requires:       rpm-python3 >= %{rpm_version}
# dnf-langpacks package is retired in F25
# to have clean upgrade path for dnf-langpacks
Obsoletes:      python3-dnf-langpacks < %{dnf_langpacks_ver}

%description -n python3-%{name}
Python 3 interface to DNF.
%endif

%package automatic
Summary:        Alternative CLI to "dnf upgrade" suitable for automatic, regular execution.
BuildRequires:  systemd
Requires:       %{name} = %{version}-%{release}
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description automatic
Alternative CLI to "dnf upgrade" suitable for automatic, regular execution.

%prep
if [ -d %{name}-%{version} ];then
  rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
mkdir build
mkdir build-py3

%build
cd %{name}-%{version}
pushd build
  %cmake ..
  %make_build
  make doc-man
popd
%if %{with python3}
pushd build-py3
  %cmake .. -DPYTHON_DESIRED:str=3 -DWITH_MAN=0
  %make_build
popd
%endif

%install
cd %{name}-%{version}
pushd build
  %make_install
popd
%if %{with python3}
pushd build-py3
  %make_install
popd
%endif
%find_lang %{name}

mkdir -p %{buildroot}%{pluginconfpath}/
mkdir -p %{buildroot}%{py2pluginpath}/
%if %{with python3}
mkdir -p %{buildroot}%{py3pluginpath}/__pycache__/
%endif
mkdir -p %{buildroot}%{_localstatedir}/log/
mkdir -p %{buildroot}%{_var}/cache/dnf/
touch %{buildroot}%{_localstatedir}/log/%{name}.log
%if %{with python3}
%{?system_python_abi:sed -i 's|#!%{__python3}|#!%{_libexecdir}/system-python|' %{buildroot}%{_bindir}/{dnf-3,yum}}
ln -sr %{buildroot}%{_bindir}/dnf-3 %{buildroot}%{_bindir}/dnf
mv %{buildroot}%{_bindir}/dnf-automatic-3 %{buildroot}%{_bindir}/dnf-automatic
%else
ln -sr %{buildroot}%{_bindir}/dnf-2 %{buildroot}%{_bindir}/dnf
mv %{buildroot}%{_bindir}/dnf-automatic-2 %{buildroot}%{_bindir}/dnf-automatic
%endif
rm -vf %{buildroot}%{_bindir}/dnf-automatic-*

%check
pushd build
  ctest -VV
popd
%if %{with python3}
pushd build-py3
  ctest -VV
popd
%endif

%post
%systemd_post dnf-makecache.timer

%preun
%systemd_preun dnf-makecache.timer

%postun
%systemd_postun_with_restart dnf-makecache.timer

%post automatic
%systemd_post dnf-automatic-notifyonly.timer
%systemd_post dnf-automatic-download.timer
%systemd_post dnf-automatic-install.timer

%preun automatic
%systemd_preun dnf-automatic-notifyonly.timer
%systemd_preun dnf-automatic-download.timer
%systemd_preun dnf-automatic-install.timer

%postun automatic
%systemd_postun_with_restart dnf-automatic-notifyonly.timer
%systemd_postun_with_restart dnf-automatic-download.timer
%systemd_postun_with_restart dnf-automatic-install.timer

%files -f %{name}.lang
%{_bindir}/%{name}
%if 0%{?rhel} && 0%{?rhel} <= 7
%{_sysconfdir}/bash_completion.d/%{name}
%else
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/%{name}
%endif
%{_mandir}/man8/%{name}.8*
%{_mandir}/man8/yum2dnf.8*
%{_unitdir}/%{name}-makecache.service
%{_unitdir}/%{name}-makecache.timer
%{_var}/cache/%{name}/

%files conf
%license COPYING PACKAGE-LICENSING
%doc AUTHORS README.rst
%dir %{confdir}
%dir %{pluginconfpath}
%dir %{confdir}/protected.d
%config(noreplace) %{confdir}/%{name}.conf
%config(noreplace) %{confdir}/protected.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%ghost %{_localstatedir}/log/hawkey.log
%ghost %{_localstatedir}/log/%{name}.log
%ghost %{_localstatedir}/log/%{name}.librepo.log
%ghost %{_localstatedir}/log/%{name}.rpm.log
%ghost %{_localstatedir}/log/%{name}.plugin.log
%ghost %{_sharedstatedir}/%{name}
%ghost %{_sharedstatedir}/%{name}/groups.json
%ghost %{_sharedstatedir}/%{name}/yumdb
%ghost %{_sharedstatedir}/%{name}/history
%{_mandir}/man5/%{name}.conf.5.gz
%{_tmpfilesdir}/%{name}.conf
%{_sysconfdir}/libreport/events.d/collect_dnf.conf

%files yum
%{_bindir}/yum
%{_mandir}/man8/yum.8.gz

%files -n python2-%{name}
%{_bindir}/%{name}-2
%exclude %{python2_sitelib}/%{name}/automatic
%{python2_sitelib}/%{name}/
%dir %{py2pluginpath}

%if %{with python3}
%files -n python3-%{name}
%{_bindir}/%{name}-3
%exclude %{python3_sitelib}/%{name}/automatic
%{python3_sitelib}/%{name}/
%dir %{py3pluginpath}
%dir %{py3pluginpath}/__pycache__
%endif

%files automatic
%{_bindir}/%{name}-automatic
%config(noreplace) %{confdir}/automatic.conf
%{_mandir}/man8/%{name}.automatic.8.gz
%{_unitdir}/%{name}-automatic-notifyonly.service
%{_unitdir}/%{name}-automatic-notifyonly.timer
%{_unitdir}/%{name}-automatic-download.service
%{_unitdir}/%{name}-automatic-download.timer
%{_unitdir}/%{name}-automatic-install.service
%{_unitdir}/%{name}-automatic-install.timer
%if %{with python3}
%{python3_sitelib}/%{name}/automatic/
%else
%{python2_sitelib}/%{name}/automatic/
%endif

%changelog
