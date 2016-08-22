%global with_unit_test 1
# modifying the dockerinit binary breaks the SHA1 sum check by docker
%global __os_install_post %{_rpmconfigdir}/brp-compress

#debuginfo not supported with Go
%global debug_package %{nil}
%global provider_tld com
%global provider github
%global project docker
%global repo %{project}
%global common_path %{provider}.%{provider_tld}/%{project}
%global d_version 1.8.2

%global import_path %{common_path}/%{repo}
%global import_path_libcontainer %{common_path}/libcontainer

%global d_commit bb472f05c975b343fb13e55325a985f4ac1d0ca2
%global d_shortcommit %(c=%{d_commit}; echo ${c:0:7})

%global utils_commit dab51acd1b1a77f7cb01a1b7e2129ec85c846b71

# %%{name}-selinux stuff (prefix with ds_ for version/release etc.)
# Some bits borrowed from the openstack-selinux package
%global ds_commit 44abd21628c8f4c054343f12d609d03de4644234
%global ds_shortcommit %(c=%{ds_commit}; echo ${c:0:7})
%global selinuxtype targeted
%global moduletype services
%global modulenames %{name}

# %%{name}-storage-setup stuff (prefix with dss_ for version/release etc.)
%global dss_libdir %{_prefix}/lib/%{name}-storage-setup
%global dss_commit 6898d433f7c7666475656ab89565ec02d08c4c55
%global dss_shortcommit %(c=%{dss_commit}; echo ${c:0:7})

# Usage: _format var format
# Expand 'modulenames' into various formats as needed
# Format must contain '$x' somewhere to do anything useful
%global _format() export %1=""; for x in %{modulenames}; do %1+=%2; %1+=" "; done;

# Relabel files
%global relabel_files() %{_sbindir}/restorecon -R %{_bindir}/%{repo} %{_localstatedir}/run/%{repo}.sock %{_localstatedir}/run/%{repo}.pid %{_sysconfdir}/%{repo} %{_localstatedir}/log/%{repo} %{_localstatedir}/log/lxc %{_localstatedir}/lock/lxc %{_unitdir}/%{repo}.service %{_sysconfdir}/%{repo} &> /dev/null || :

# Version of SELinux we were using
%if 0%{?fedora} >= 22
%global selinux_policyver 3.13.1-119
%else
%global selinux_policyver 3.13.1-23
%endif

Name: %{repo}
Version: %{d_version}
Release: 7%{?dist}
Summary: Automates deployment of containerized applications
License: ASL 2.0
URL: https://%{import_path}
# only x86_64 for now: https://%%{provider}.%%{provider_tld}/%%{name}/%%{name}/issues/136
ExclusiveArch: x86_64
# Branch used available at
# https://%%{provider}.%%{provider_tld}/rhatdan/%%{name}/commits/rhel7-1.8
Source0: https://%{provider}.%{provider_tld}/rhatdan/%{name}/archive/%{d_commit}.tar.gz
Source1: %{name}.service
Source3: %{name}.sysconfig
Source4: %{name}-storage.sysconfig
Source5: %{name}-logrotate.sh
Source6: README.%{name}-logrotate
Source7: %{name}-network.sysconfig
# Source11 is the source tarball for %%{name}tarsum and %%{name}-fetch
Source11: https://%{provider}.%{provider_tld}/vbatts/%{name}-utils/archive/%{utils_commit}.tar.gz
# Source12 is the source tarball for %%{name}-selinux
Source12: https://%{provider}.%{provider_tld}/fedora-cloud/%{name}-selinux/archive/%{ds_commit}/%{name}-selinux-%{ds_shortcommit}.tar.gz
# Source13 is the source tarball for %%{name}-storage-setup
Source13: https://%{provider}.%{provider_tld}/projectatomic/%{name}-storage-setup/archive/%{dss_commit}/%{name}-storage-setup-%{dss_shortcommit}.tar.gz
Patch0: libcontainer.patch
Patch1: dev.patch
BuildRequires: glibc-static
BuildRequires: golang == 1.4.2
BuildRequires: device-mapper-devel
BuildRequires: btrfs-progs-devel
BuildRequires: sqlite-devel
BuildRequires: go-md2man
BuildRequires: pkgconfig(systemd)
# appropriate systemd version as per rhbz#1171054
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
# need xz to work with ubuntu images
Requires: xz
Requires: device-mapper-libs >= 7:1.02.90-1
#Requires: subscription-manager
Provides: lxc-%{name} = %{d_version}-%{release}
Provides: %{name}-io = %{d_version}-%{release}

# RE: rhbz#1195804 - ensure min NVR for selinux-policy
Requires: selinux-policy >= 3.13.1-23
Requires(pre): %{name}-selinux >= %{version}-%{release}

# rhbz#1214070 - update deps for d-s-s
Requires: lvm2 >= 2.02.112
Requires: xfsprogs

%description
Docker is an open-source engine that automates the deployment of any
application as a lightweight, portable, self-sufficient container that will
run virtually anywhere.

Docker containers can encapsulate any payload, and will run consistently on
and between virtually any server. The same container that a developer builds
and tests on a laptop will run at scale, in production*, on VMs, bare-metal
servers, OpenStack clusters, public instances, or combinations of the above.

%if 0%{?with_unit_test}
%package unit-test
Summary: %{summary} - for running unit tests

%description unit-test
%{summary} - for running unit tests
%endif

%package logrotate
Summary: cron job to run logrotate on Docker containers
Requires: %{name} = %{d_version}-%{release}
Provides: %{name}-io-logrotate = %{d_version}-%{release}

%description logrotate
This package installs %{summary}. logrotate is assumed to be installed on
containers for this to work, failures are silently ignored.

%package selinux
Summary: SELinux policies for Docker
BuildRequires: selinux-policy
BuildRequires: selinux-policy-devel
Requires(post): selinux-policy-base >= %{selinux_policyver}
Requires(post): selinux-policy-targeted >= %{selinux_policyver}
Requires(post): policycoreutils
Requires(post): policycoreutils-python
Requires(post): libselinux-utils
Provides: %{name}-io-selinux

%description selinux
SELinux policy modules for use with Docker.

%prep
%setup -qn %{name}-%{d_commit}
%patch0 -p1
%patch1 -p1
cp %{SOURCE6} .

# unpack %%{name}-selinux
tar zxf %{SOURCE12}

# untar %%{name}-utils tarball
tar zxf %{SOURCE11}

# untar d-s-s
tar zxf %{SOURCE13}

%build
mkdir _build

pushd _build
  mkdir -p src/%{provider}.%{provider_tld}/{%{name},vbatts}
  ln -s $(dirs +1 -l) src/%{import_path}
  ln -s $(dirs +1 -l)/%{name}-utils-%{utils_commit} src/%{provider}.%{provider_tld}/vbatts/%{name}-utils
popd

export DOCKER_GITCOMMIT="%{d_shortcommit}/%{d_version}"
export DOCKER_BUILDTAGS='selinux btrfs_noversion'
export GOPATH=$(pwd)/_build:$(pwd)/vendor:%{gopath}

# build %%{name} binary
sed -i '/rm -r autogen/d' hack/make.sh
DEBUG=1 hack/make.sh dynbinary
cp contrib/syntax/vim/LICENSE LICENSE-vim-syntax
cp contrib/syntax/vim/README.md README-vim-syntax.md

# build %%{name}-selinux
pushd %{name}-selinux-%{ds_commit}
make SHARE="%{_datadir}" TARGETS="%{modulenames}"
popd

pushd $(pwd)/_build/src
# build %{name}tarsum and %{name}-fetch
go build %{provider}.%{provider_tld}/vbatts/%{name}-utils/cmd/%{name}-fetch
go build %{provider}.%{provider_tld}/vbatts/%{name}-utils/cmd/%{name}tarsum
popd

# build %%{name} manpages
man/md2man-all.sh

%install
# install binary
install -d %{buildroot}%{_bindir}
install -p -m 755 bundles/%{d_version}/dynbinary/%{name}-%{d_version} %{buildroot}%{_bindir}/%{name}

# install %%{name}tarsum and %%{name}-fetch
install -p -m 755 _build/src/%{name}-fetch %{buildroot}%{_bindir}
install -p -m 755 _build/src/%{name}tarsum %{buildroot}%{_bindir}

# install %%{name}init
install -d %{buildroot}%{_libexecdir}/%{name}
install -p -m 755 bundles/%{d_version}/dynbinary/%{name}init-%{d_version} %{buildroot}%{_libexecdir}/%{name}/%{name}init

# install manpages
install -d %{buildroot}%{_mandir}/man1
install -p -m 644 man/man1/* %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man5
install -p -m 644 man/man5/* %{buildroot}%{_mandir}/man5

# install bash completion
install -d %{buildroot}%{_datadir}/bash-completion/completions/
install -p -m 644 contrib/completion/bash/%{name} %{buildroot}%{_datadir}/bash-completion/completions/

# install fish completion
# create, install and own /usr/share/fish/vendor_completions.d until
# upstream fish provides it
install -dp %{buildroot}%{_datadir}/fish/vendor_completions.d
install -p -m 644 contrib/completion/fish/%{name}.fish %{buildroot}%{_datadir}/fish/vendor_completions.d

# install container logrotate cron script
install -dp %{buildroot}%{_sysconfdir}/cron.daily/
install -p -m 755 %{SOURCE5} %{buildroot}%{_sysconfdir}/cron.daily/%{name}-logrotate

# install vim syntax highlighting
install -d %{buildroot}%{_datadir}/vim/vimfiles/{doc,ftdetect,syntax}
install -p -m 644 contrib/syntax/vim/doc/%{name}file.txt %{buildroot}%{_datadir}/vim/vimfiles/doc
install -p -m 644 contrib/syntax/vim/ftdetect/%{name}file.vim %{buildroot}%{_datadir}/vim/vimfiles/ftdetect
install -p -m 644 contrib/syntax/vim/syntax/%{name}file.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax

# install zsh completion
install -d %{buildroot}%{_datadir}/zsh/site-functions
install -p -m 644 contrib/completion/zsh/_%{name} %{buildroot}%{_datadir}/zsh/site-functions

# install udev rules
install -d %{buildroot}%{_udevrulesdir}
install -p -m 755 contrib/udev/80-%{name}.rules %{buildroot}%{_udevrulesdir}

# install storage dir
install -d -m 700 %{buildroot}%{_sharedstatedir}/%{name}

# install systemd/init scripts
install -d %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}

# for additional args
install -d %{buildroot}%{_sysconfdir}/sysconfig/
install -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -p -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/%{name}-storage
install -p -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/sysconfig/%{name}-network

# install SELinux interfaces
%_format INTERFACES $x.if
install -d %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}
install -p -m 644 %{name}-selinux-%{ds_commit}/$INTERFACES %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}

# install policy modules
%_format MODULES $x.pp.bz2
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 0644 %{name}-selinux-%{ds_commit}/$MODULES %{buildroot}%{_datadir}/selinux/packages

%if 0%{?with_unit_test}
install -d -m 0755 %{buildroot}%{_sharedstatedir}/%{name}-unit-test/
cp -pav VERSION Dockerfile %{buildroot}%{_sharedstatedir}/%{name}-unit-test/.
for d in */ ; do
  cp -a $d %{buildroot}%{_sharedstatedir}/%{name}-unit-test/
done
# remove %%{name}.initd as it requires /sbin/runtime no packages in Fedora
rm -rf %{buildroot}%{_sharedstatedir}/%{name}-unit-test/contrib/init/openrc/%{name}.initd
%endif

# remove %%{name}-selinux rpm spec file
rm -rf %{name}-selinux-%{ds_commit}/%{name}-selinux.spec

# don't install secrets dir
#install -d -p -m 750 %{buildroot}/%{_datadir}/rhel/secrets
# rhbz#1110876 - update symlinks for subscription management
#ln -s %{_sysconfdir}/pki/entitlement %{buildroot}%{_datadir}/rhel/secrets/etc-pki-entitlement
#ln -s %{_sysconfdir}/rhsm %{buildroot}%{_datadir}/rhel/secrets/rhsm
#ln -s %{_sysconfdir}/yum.repos.d/redhat.repo %{buildroot}%{_datadir}/rhel/secrets/rhel7.repo

#mkdir -p %{buildroot}/etc/%{name}/certs.d/redhat.{com,io}
#ln -s %{_sysconfdir}/rhsm/ca/redhat-uep.pem %{buildroot}/%{_sysconfdir}/%{name}/certs.d/redhat.com/redhat-ca.crt
#ln -s %{_sysconfdir}/rhsm/ca/redhat-uep.pem %{buildroot}/%{_sysconfdir}/%{name}/certs.d/redhat.io/redhat-ca.crt
mkdir -p %{buildroot}/etc/%{name}/certs.d

# install %%{name} config directory
install -dp %{buildroot}%{_sysconfdir}/%{name}/

# install %%{name}-storage-setup
pushd %{name}-storage-setup-%{dss_commit}
install -d %{buildroot}%{_bindir}
install -p -m 755 %{name}-storage-setup.sh %{buildroot}%{_bindir}/%{name}-storage-setup
install -d %{buildroot}%{_unitdir}
install -p -m 644 %{name}-storage-setup.service %{buildroot}%{_unitdir}
install -d %{buildroot}%{dss_libdir}
install -p -m 644 %{name}-storage-setup.conf %{buildroot}%{dss_libdir}/%{name}-storage-setup
install -p -m 755 libdss.sh %{buildroot}%{dss_libdir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 644 %{name}-storage-setup-override.conf %{buildroot}%{_sysconfdir}/sysconfig/%{name}-storage-setup
install -d %{buildroot}%{_mandir}/man1
install -p -m 644 %{name}-storage-setup.1 %{buildroot}%{_mandir}/man1
popd

%check
[ ! -w /run/%{name}.sock ] || {
    mkdir test_dir
    pushd test_dir
    git clone https://%{import_path}
    pushd %{name}
    make test
    popd
    popd
}

%pre
getent passwd %{name}root > /dev/null || %{_sbindir}/useradd -r -d %{_sharedstatedir}/%{name} -s /sbin/nologin -c "Docker User" %{name}root
exit 0

%post
%systemd_post %{name}.service

%post selinux
# Install all modules in a single transaction
%_format MODULES %{_datadir}/selinux/packages/$x.pp.bz2
%{_sbindir}/semodule -n -s %{selinuxtype} -i $MODULES
if %{_sbindir}/selinuxenabled ; then
    %{_sbindir}/load_policy
    %relabel_files
    if [ $1 -eq 1 ]; then
    restorecon -R %{_sharedstatedir}/%{repo}
    fi
fi

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%postun selinux
if [ $1 -eq 0 ]; then
%{_sbindir}/semodule -n -r %{modulenames} &> /dev/null || :
if %{_sbindir}/selinuxenabled ; then
%{_sbindir}/load_policy
%relabel_files
fi
fi

%files
%doc AUTHORS CHANGELOG.md CONTRIBUTING.md MAINTAINERS NOTICE
%doc LICENSE* README*.md
%{_mandir}/man1/%{name}*
%{_mandir}/man5/*
%{_bindir}/%{name}
#%dir %{_datadir}/rhel
#%dir %{_datadir}/rhel/secrets
#%{_datadir}/rhel/secrets/etc-pki-entitlement
#%{_datadir}/rhel/secrets/rhel7.repo
#%{_datadir}/rhel/secrets/rhsm
%{_libexecdir}/%{name}
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}-storage
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}-network
%{_datadir}/bash-completion/completions/%{name}
%dir %{_sharedstatedir}/%{name}
%{_udevrulesdir}/80-%{name}.rules
%dir %{_datadir}/fish/vendor_completions.d/
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%dir %{_datadir}/vim/vimfiles/doc
%{_datadir}/vim/vimfiles/doc/%{name}file.txt
%dir %{_datadir}/vim/vimfiles/ftdetect
%{_datadir}/vim/vimfiles/ftdetect/%{name}file.vim
%dir %{_datadir}/vim/vimfiles/syntax
%{_datadir}/vim/vimfiles/syntax/%{name}file.vim
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_%{name}
%{_sysconfdir}/%{name}
%{_bindir}/%{name}-fetch
%{_bindir}/%{name}tarsum
# %%{name}-storage-setup specific
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}-storage-setup
%{_unitdir}/%{name}-storage-setup.service
%{_bindir}/%{name}-storage-setup
%{dss_libdir}/%{name}-storage-setup
%{dss_libdir}/libdss.sh

%if 0%{?with_unit_test}
%files unit-test
%{_sharedstatedir}/%{name}-unit-test/
%endif

%files logrotate
%doc README.%{name}-logrotate
%{_sysconfdir}/cron.daily/%{name}-logrotate

%files selinux
%doc %{name}-selinux-%{ds_commit}/README.md
%{_datadir}/selinux/*

%changelog
