%global with_python3 1
%global with_python2 0
%global with_git 1
%define repo https://github.com/rpm-software-management/mock
%global mockgid  135

%define git_summary %(echo `curl %{repo} | grep '<title' | sed 's/<title>//g'`)
%define git_version %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-nameo">'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1
%define git_release %{rel_version}.%{revision}.%{?dist}

%if %{with_python3}
%global python_sitelib %{python3_sitelib}
%else
%global python_sitelib %{python_sitelib}
%endif



Summary: %{git_summary}
Name: mock
Version: %{git_version}
Release: %{git_release}
License: GPLv2+
Vendor: %{vendor}
Packager: %{packager}
Group: Development/Tools
URL: %{repo}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
%if %{with_python3}
Requires: python3
Requires: python3-distro
Requires: python3-six >= 1.4.0
Requires: python3-requests
Requires: rpm-python3
BuildRequires: python3-devel
BuildRequires: python3-pylint
%else
Requires: pyliblzma
Requires: python-ctypes
Requires: python-distro
Requires: python-six >= 1.4.0
Requires: python-requests
Requires: python >= 2.6
Requires: rpm-python
BuildRequires: python-devel
%endif

Requires: createrepo
Requires: pigz
Requires: shadow-utils
Requires: tar
Requires: usermode
Requires: yum >= 2.4
Requires: yum-utils
Requires: createrepo_c
Requires(post): /etc/os-release
Requires(pre): shadow-utils
Requires(post): coreutils
BuildRequires: autoconf, automake
BuildRequires: bash-completion
Requires: systemd
Requires: btrfs-progs
BuildRequires: perl
Requires: util-linux
Requires: coreutils
Requires: procps-ng

%description
%{summary}

%package scm
Summary: Mock SCM integration module
Requires: %{name} = %{version}-%{release}
Requires: cvs
Requires: git
Requires: subversion
Requires: tar

%description scm
Mock SCM integration module.

%package lvm
Summary: LVM plugin for mock
Requires: %{name} = %{version}-%{release}
Requires: lvm2

%description lvm
Mock plugin that enables using LVM as a backend and support creating snapshots
of the buildroot.

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
if [ -d %{buildroot} ]; then
    rm -rf %{buildroot}
fi
git clone %{repo} %{name}-%{version}
cd $RPM_BUILD_DIR/%{name}-%{version}
git submodule init
git submodule update
%if %{with_python3}
for file in py/mock.py py/mockchain.py; do
  sed -i 1"s|#!/usr/bin/python |#!/usr/bin/python3 |" $file
done
%endif

%build
cd $RPM_BUILD_DIR/%{name}-%{version}
for i in py/mock.py py/mockchain.py; do
    perl -p -i -e 's|^__VERSION__\s*=.*|__VERSION__="%{version}"|' $i
    perl -p -i -e 's|^SYSCONFDIR\s*=.*|SYSCONFDIR="%{_sysconfdir}"|' $i
    perl -p -i -e 's|^PYTHONDIR\s*=.*|PYTHONDIR="%{python_sitelib}"|' $i
    perl -p -i -e 's|^PKGPYTHONDIR\s*=.*|PKGPYTHONDIR="%{python_sitelib}/mockbuild"|' $i
done
for i in docs/mockchain.1 docs/mock.1; do
    perl -p -i -e 's|@VERSION@|%{version}"|' $i
done

%install
cd $RPM_BUILD_DIR/%{name}-%{version}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_libexecdir}/mock
install py/mockchain.py %{buildroot}%{_bindir}/mockchain
install py/mock.py %{buildroot}%{_libexecdir}/mock/mock
ln -s consolehelper %{buildroot}%{_bindir}/mock

install -d %{buildroot}%{_sysconfdir}/pam.d
cp -a etc/pam/* %{buildroot}%{_sysconfdir}/pam.d/

install -d %{buildroot}%{_sysconfdir}/mock
cp -a etc/mock/* %{buildroot}%{_sysconfdir}/mock/

install -d %{buildroot}%{_sysconfdir}/security/console.apps/
cp -a etc/consolehelper/mock %{buildroot}%{_sysconfdir}/security/console.apps/%{name}

install -d %{buildroot}%{_datadir}/bash-completion/completions/
cp -a etc/bash_completion.d/* %{buildroot}%{_datadir}/bash-completion/completions/
ln -s mock %{buildroot}%{_datadir}/bash-completion/completions/mockchain

install -d %{buildroot}%{_sysconfdir}/pki/mock
cp -a etc/pki/* %{buildroot}%{_sysconfdir}/pki/mock/

install -d %{buildroot}%{python_sitelib}/
cp -a py/mockbuild %{buildroot}%{python_sitelib}/

install -d %{buildroot}%{_mandir}/man1
cp -a docs/mockchain.1 docs/mock.1 %{buildroot}%{_mandir}/man1/

install -d %{buildroot}/var/lib/mock
install -d %{buildroot}/var/cache/mock

# generate files section with config - there is many of them
echo "%defattr(0644, root, mock)" > %{name}.cfgs
find %{buildroot}%{_sysconfdir}/mock -name "*.cfg" \
    | sed -e "s|^%{buildroot}|%%config(noreplace) |" >> %{name}.cfgs
# just for %%ghosting purposes
ln -s fedora-rawhide-x86_64.cfg %{buildroot}%{_sysconfdir}/mock/default.cfg
# bash-completion
if [ -d %{buildroot}%{_datadir}/bash-completion ]; then
    echo %{_datadir}/bash-completion/completions/mock >> %{name}.cfgs
    echo %{_datadir}/bash-completion/completions/mockchain >> /%{name}.cfgs
elif [ -d %{buildroot}%{_sysconfdir}/bash_completion.d ]; then
    echo %{_sysconfdir}/bash_completion.d/mock >> %{name}.cfgs
fi



%pre
getent group mock > /dev/null || groupadd -f -g %mockgid -r mock
exit 0

%post
chmod 2775 %{_localstatedir}/cache/%{name}

if [ -s /etc/os-release ]; then
    # fedora and rhel7
    if grep -Fiq Rawhide /etc/os-release; then
        ver=rawhide
    else
        ver=$(source /etc/os-release && echo $VERSION_ID | cut -d. -f1 | grep -o '[0-9]\+')
    fi
else
    # rhel6 or something obsure, use buildtime version
    ver=%{?rhel}%{?fedora}
fi
mock_arch=$(python -c "import rpmUtils.arch; baseArch = rpmUtils.arch.getBaseArch(); print baseArch")
cfg=%{?fedora:fedora}%{?rhel:epel}-$ver-${mock_arch}.cfg
if [ -e %{_sysconfdir}/%{name}/$cfg ]; then
    if [ "$(readlink %{_sysconfdir}/%{name}/default.cfg)" != "$cfg" ]; then
        ln -s $cfg %{_sysconfdir}/%{name}/default.cfg 2>/dev/null || ln -s -f $cfg %{_sysconfdir}/%{name}/default.cfg.rpmnew
    fi
else
    echo "Warning: file %{_sysconfdir}/%{name}/$cfg does not exists."
    echo "         unable to update %{_sysconfdir}/%{name}/default.cfg"
fi
:

%check
# ignore the errors for now, just print them and hopefully somebody will fix it one day
pylint py/mockbuild/ py/*.py py/mockbuild/plugins/* || :

%files -f %{name}-%{version}/%{name}.cfgs
%defattr(-, root, root)

# executables
%{_bindir}/mock
%{_bindir}/mockchain
%{_libexecdir}/mock

# python stuff
%{python_sitelib}/*
%exclude %{python_sitelib}/mockbuild/scm.*
%exclude %{python_sitelib}/mockbuild/plugins/lvm_root.*

# config files
%dir  %{_sysconfdir}/%{name}
%ghost %config(noreplace,missingok) %{_sysconfdir}/%{name}/default.cfg
%config(noreplace) %{_sysconfdir}/%{name}/*.ini
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%{_datadir}/bash-completion/completions/*

# gpg keys
%dir %{_sysconfdir}/pki/mock
%config(noreplace) %{_sysconfdir}/pki/mock/*

# docs
%{_mandir}/man1/mock.1*
%{_mandir}/man1/mockchain.1*

# cache & build dirs
%defattr(0775, root, mock, 02775)
%dir %{_localstatedir}/cache/mock
%dir %{_localstatedir}/lib/mock

%files scm
%{python_sitelib}/mockbuild/scm.py*

%files lvm
%{python_sitelib}/mockbuild/scm.py*

%changelog

