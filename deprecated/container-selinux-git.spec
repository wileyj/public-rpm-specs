%global provider        github
%global provider_tld    com
%global project        projectatomic 
%global repo       container-selinux
%global repo_url https://%{provider}.%{provider_tld}/%{project}/%{repo}
%global revision %(echo `git ls-remote %{repo_url}.git  | head -1 | cut -f 1 | cut -c1-7`)
%global git_version %(echo `curl -s %{repo_url}/releases | grep 'class="css-truncate-target"' | head -1 |  tr -d '\\-</span class="css-truncate-target">betarcv'`)
%define rel_version 1



%global debug_package   %{nil}
%global git0 %{repo_url}
%global commit0 %(echo `git ls-remote %{git0} | head -1 | awk {'print $1'}`)
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%global selinuxtype targeted
%global moduletype services
%global modulenames container
%global _format() export %1=""; for x in %{modulenames}; do %1+=%2; %1+=" "; done;

# Relabel files
%global relabel_files() %{_sbindir}/restorecon -R %{_bindir}/docker* %{_localstatedir}/run/containerd.sock %{_localstatedir}/run/docker.sock %{_localstatedir}/run/docker.pid %{_sysconfdir}/docker %{_localstatedir}/log/docker %{_localstatedir}/log/lxc %{_localstatedir}/lock/lxc %{_unitdir}/docker.service %{_unitdir}/docker-containerd.service %{_unitdir}/docker-latest.service %{_unitdir}/docker-latest-containerd.service %{_sysconfdir}/docker %{_libexecdir}/docker* &> /dev/null || :

# Version of SELinux we were using
%if 0%{?fedora} >= 22
%global selinux_policyver 3.13.1-220
%else
%global selinux_policyver 3.13.1-39
%endif

Name: container-selinux
%if 0%{?fedora} || 0%{?centos}
Epoch: 2
%endif
Version: 2.5
Release: %{rel_version}.%{?dist}
License: GPLv2
URL: %{git0}
Summary: SELinux policies for container runtimes
BuildArch: noarch
BuildRequires: git
BuildRequires: pkgconfig(systemd)
BuildRequires: selinux-policy >= %{selinux_policyver}
BuildRequires: selinux-policy-sandbox >= %{selinux_policyver}
BuildRequires: selinux-policy-devel >= %{selinux_policyver}
# RE: rhbz#1195804 - ensure min NVR for selinux-policy
Requires: selinux-policy >= %{selinux_policyver}
Requires(post): selinux-policy-base >= %{selinux_policyver}
Requires(post): selinux-policy-targeted >= %{selinux_policyver}
Requires(post): policycoreutils
%if 0%{?fedora}
Requires(post): policycoreutils-python-utils
%else
Requires(post): policycoreutils-python
%endif
Requires(post): libselinux-utils
Obsoletes: %{name} <= 2:1.12.5-13
Obsoletes: docker-selinux <= 2:1.12.4-28
Provides: docker-selinux = %{epoch}:%{version}-%{release}

%description
SELinux policy modules for use with container runtimes.

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
if [ -d %{buildroot} ]; then
    rm -rf %{buildroot}
fi
git clone %{repo_url} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update

%build
cd %{name}-%{version}
make

%install
cd %{name}-%{version}
# install policy modules
%_format MODULES $x.pp.bz2
install -d %{buildroot}%{_datadir}/selinux/packages
install -d -p %{buildroot}%{_datadir}/selinux/devel/include/services
install -p -m 644 container.if %{buildroot}%{_datadir}/selinux/devel/include/services
install -m 0644 $MODULES %{buildroot}%{_datadir}/selinux/packages

# remove spec file
rm -rf container-selinux.spec
%__mkdir_p  %{buildroot}%{_docdir}/%{name}-%{version}
%__cp -pr %{_builddir}/%{name}-%{version}/README %{buildroot}%{_docdir}/%{name}-%{version}/README

%check

%post
# Install all modules in a single transaction
if [ $1 -eq 1 ]; then
    %{_sbindir}/setsebool -P -N virt_use_nfs=1 virt_sandbox_use_all_caps=1
fi
%_format MODULES %{_datadir}/selinux/packages/$x.pp.bz2
%{_sbindir}/semodule -n -s %{selinuxtype} -r container 2> /dev/null
%{_sbindir}/semodule -n -s %{selinuxtype} -d docker 2> /dev/null
%{_sbindir}/semodule -n -s %{selinuxtype} -d gear 2> /dev/null
%{_sbindir}/semodule -n -X 200 -s %{selinuxtype} -i $MODULES > /dev/null
if %{_sbindir}/selinuxenabled ; then
    %{_sbindir}/load_policy
    %relabel_files
    if [ $1 -eq 1 ]; then
	restorecon -R %{_sharedstatedir}/docker &> /dev/null || :
    fi
fi

%postun
if [ $1 -eq 0 ]; then
%{_sbindir}/semodule -n -r %{modulenames} docker &> /dev/null || :
if %{_sbindir}/selinuxenabled ; then
%{_sbindir}/load_policy
%relabel_files
fi
fi

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%dir %{_docdir}/%{name}-%{version}
%{_docdir}/%{name}-%{version}/README
%{_datadir}/selinux/*

%changelog
