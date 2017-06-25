%global provider        github
%global provider_tld    com
%global project         moby
%global git_repo        moby
%global vendorname kubernetes
%global repo_url https://%{provider}.%{provider_tld}/%{project}/%{git_repo}
%global revision %(echo `git ls-remote %{repo_url}.git  | head -1 | cut -f 1 | cut -c1-7`)
%global git_version %(echo `curl -s %{repo_url}/releases | grep 'class="css-truncate-target"' | head -1 |  tr -d '\\-</span class="css-truncate-target">betarcv'`)
%define rel_version 1
%define docker_release %{rel_version}.%{revision}.%{dist}

%if 0%{?fedora}
%global with_devel 1
%global with_debug 1
%global with_unit_test 1
%else
%global with_devel 0
%global with_debug 0
%global with_unit_test 0
%endif

# modifying the dockerinit binary breaks the SHA1 sum check by docker
%global __os_install_post %{_rpmconfigdir}/brp-compress

# docker builds in a checksum of dockerinit into docker,
# so stripping the binaries breaks docker
%if 0%{?with_debug}
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif
%global provider github
%global provider_tld com
%global project docker
%global repo %{project}

%global import_path %{provider}.%{provider_tld}/%{project}/%{repo}

# docker
%global git0 https://github.com/projectatomic/%{repo}
%global commit0  %(echo `git ls-remote %{git0} | head -1 | awk {'print $1'}`)
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
# docker_branch used in %%check
%global docker_branch docker-%{git_version}

# d-s-s
%global git1 https://github.com/projectatomic/%{repo}-storage-setup/
%global git1_dir %{repo}-storage-setup
%global commit1  %(echo `git ls-remote %{git1} | head -1 | awk {'print $1'}`)
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global dss_libdir %{_exec_prefix}/lib/%{repo}-storage-setup

# docker-novolume-plugin
%global git4 https://github.com/projectatomic/%{repo}-novolume-plugin
%global git4_dir %{repo}-novolume-plugin
%global commit4  %(echo `git ls-remote %{git4} | head -1 | awk {'print $1'}`)
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})

# docker-runc
%global git6 https://github.com/projectatomic/runc/
%global git6_dir runc
%global commit6  %(echo `git ls-remote %{git6} | head -1 | awk {'print $1'}`)
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})

# docker-containerd
%global git7 https://github.com/projectatomic/containerd
%global git7_dir containerd
%global commit7  %(echo `git ls-remote %{git7} | head -1 | awk {'print $1'}`)
%global shortcommit7 %(c=%{commit7}; echo ${c:0:7})

# rhel-push-plugin
%global git8 https://github.com/projectatomic/rhel-push-plugin
%global git8_dir rhel-push-plugin
%global commit8  %(echo `git ls-remote %{git8} | head -1 | awk {'print $1'}`)
%global shortcommit8 %(c=%{commit8}; echo ${c:0:7})

# docker-lvm-plugin
%global git9 https://github.com/projectatomic/%{repo}-lvm-plugin
%global git9_dir %{repo}-lvm-plugin
%global commit9  %(echo `git ls-remote %{git9} | head -1 | awk {'print $1'}`)
%global shortcommit9 %(c=%{commit9}; echo ${c:0:7})

Name: %{repo}
%if 0%{?fedora} || 0%{?centos}
Epoch: 2
%endif
Version: %{git_version}
Release: %{docker_release}
#Release: 17.git%{shortcommit0}.%{?dist}
Summary: Automates deployment of containerized applications
License: ASL 2.0
URL: https://%{provider}.%{provider_tld}/projectatomic/%{repo}
# Temp fix for rhbz#1315903
#ExclusiveArch: %%{go_arches}
ExclusiveArch: %{ix86} x86_64 %{arm} aarch64 ppc64le s390x %{mips}
#Source1: %{git1}/archive/%{commit1}/%{repo}-storage-setup-%{shortcommit1}.tar.gz
#Source4: %{git4}/archive/%{commit4}/%{repo}-novolume-plugin-%{shortcommit4}.tar.gz
Source5: %{repo}.service
Source6: %{repo}.sysconfig
Source7: %{repo}-storage.sysconfig
Source8: %{repo}-logrotate.sh
Source9: README.%{repo}-logrotate
Source10: %{repo}-network.sysconfig
#Source12: %{git6}/archive/%{commit6}/runc-%{shortcommit6}.tar.gz
#Source13: %{git7}/archive/%{commit7}/containerd-%{shortcommit7}.tar.gz
Source14: %{repo}-containerd.service
Source16: %{repo}-common.sh
Source17: README-%{repo}-common
#Source18: %{git8}/archive/%{commit8}/rhel-push-plugin-%{shortcommit8}.tar.gz
#Source19: %{git9}/archive/%{commit9}/%{repo}-lvm-plugin-%{shortcommit9}.tar.gz
Source20: %{repo}.service.centos
Source21: %{repo}-containerd.service.centos

%if 0%{?with_debug}
# Build with debug
#Patch0:      build-with-debug-info.patch
%endif

BuildRequires: git
BuildRequires: glibc-static
BuildRequires: gpgme-devel
BuildRequires: libassuan-devel
BuildRequires: golang >= 1.6.2
BuildRequires: go-md2man
BuildRequires: device-mapper-devel
%if 0%{?fedora}
BuildRequires: godep
BuildRequires: libseccomp-static >= 2.3.0
%else %if 0%{?centos}
BuildRequires: libseccomp-devel
%endif
BuildRequires: pkgconfig
BuildRequires: btrfs-progs-devel
BuildRequires: sqlite-devel
BuildRequires: pkgconfig(systemd)
%if 0%{?fedora} >= 21
# Resolves: rhbz#1165615
Requires: device-mapper-libs >= 1.02.90-1
%endif

Requires: skopeo-containers
Requires: gnupg

# BZ#1399098
Requires: python-rhsm-certificates

# Resolves: #1379184 - include epoch
Requires: %{repo}-common = %{epoch}:%{version}-%{release}

#Requires(pre): container-selinux >= 2:2.2-2

# BZ#1398860
Requires: %{name}-rhel-push-plugin = %{epoch}:%{version}-%{release}

# Resolves: rhbz#1045220
Requires: xz
Provides: lxc-%{repo} = %{epoch}:%{version}-%{release}

# Match with upstream name - include epoch as well
Provides: %{repo}-engine = %{epoch}:%{version}-%{release}

# needs tar to be able to run containers
Requires: tar

# BZ1327809
Requires: iptables

# #1416929
Requires: parted

# permitted by https://fedorahosted.org/fpc/ticket/341#comment:7
# In F22, the whole package should be renamed to be just "docker" and
# this changed to "Provides: docker-io".
%if 0%{?fedora} >= 22
Provides: %{repo}-io = %{epoch}:%{version}-%{release}
Obsoletes: %{repo}-io <= 1.5.0-19
%endif

# include d-s-s into main docker package and obsolete existing d-s-s rpm
# also update BRs and Rs
Requires: lvm2
Requires: xfsprogs
Obsoletes: %{repo}-storage-setup <= 0.5-3

Requires: libseccomp >= 2.3.0

%if 0%{?fedora}
Recommends: oci-register-machine
Recommends: oci-systemd-hook
%else
Requires: oci-register-machine
Requires: oci-systemd-hook
%endif

%description
Docker is an open-source engine that automates the deployment of any
application as a lightweight, portable, self-sufficient container that will
run virtually anywhere.

Docker containers can encapsulate any payload, and will run consistently on
and between virtually any server. The same container that a developer builds
and tests on a laptop will run at scale, in production*, on VMs, bare-metal
servers, OpenStack clusters, public instances, or combinations of the above.

%if 0%{?with_devel}
%package devel
BuildArch: noarch
Provides: %{repo}-io-devel = %{epoch}:%{version}-%{release}
Provides: %{repo}-pkg-devel = %{epoch}:%{version}-%{release}
Provides: %{repo}-io-pkg-devel = %{epoch}:%{version}-%{release}
Summary:  A golang registry for global request variables (source libraries)

Provides: golang(%{import_path}/api) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/api/client) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/api/client/formatter) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/api/client/inspect) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/api/server) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/api/server/httputils) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/api/server/middleware) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/api/server/router) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/api/server/router/build) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/api/server/router/container) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/api/server/router/image) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/api/server/router/network) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/api/server/router/system) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/api/server/router/volume) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/api/types/backend) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/builder) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/builder/dockerfile) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/builder/dockerfile/command) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/builder/dockerfile/parser) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/builder/dockerignore) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/cli) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/cliconfig) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/cliconfig/credentials) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/container) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/caps) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/dockerhooks) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/events) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/events/testutils) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/exec) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/graphdriver) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/graphdriver/aufs) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/graphdriver/btrfs) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/graphdriver/devmapper) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/graphdriver/graphtest) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/graphdriver/overlay) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/graphdriver/register) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/graphdriver/vfs) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/graphdriver/windows) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/graphdriver/zfs) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/links) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/logger) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/logger/awslogs) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/logger/etwlogs) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/logger/fluentd) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/logger/gcplogs) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/logger/gelf) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/logger/journald) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/logger/jsonfilelog) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/logger/loggerutils) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/logger/splunk) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/logger/syslog) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/daemon/network) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/distribution) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/distribution/metadata) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/distribution/xfer) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/docker/hack) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/docker/listeners) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/dockerversion) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/errors) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/image) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/image/tarexport) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/image/v1) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/layer) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/libcontainerd) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/libcontainerd/windowsoci) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/migrate/v1) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/oci) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/opts) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/aaparser) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/archive) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/audit) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/authorization) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/broadcaster) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/chrootarchive) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/devicemapper) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/directory) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/discovery) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/discovery/file) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/discovery/kv) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/discovery/memory) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/discovery/nodes) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/filenotify) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/fileutils) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/gitutils) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/graphdb) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/homedir) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/httputils) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/idtools) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/integration) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/integration/checker) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/ioutils) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/jsonlog) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/jsonmessage) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/locker) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/longpath) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/loopback) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/mflag) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/mount) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/namesgenerator) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/parsers) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/parsers/kernel) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/parsers/operatingsystem) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/pidfile) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/platform) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/plugins) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/plugins/pluginrpc-gen/fixtures) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/plugins/transport) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/pools) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/progress) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/promise) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/proxy) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/pubsub) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/random) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/reexec) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/registrar) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/rpm) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/signal) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/stdcopy) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/streamformatter) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/stringid) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/stringutils) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/symlink) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/sysinfo) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/system) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/tailfile) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/tarsum) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/term) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/term/windows) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/tlsconfig) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/truncindex) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/urlutil) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/useragent) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/version) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/profiles/apparmor) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/profiles/seccomp) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/reference) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/registry) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/restartmanager) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/runconfig) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/runconfig/opts) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/utils) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/utils/templates) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/volume) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/volume/drivers) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/volume/local) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/volume/store) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/volume/testutils) = %{epoch}:%{version}-%{release}

%description devel
%{summary}

This package provides the source libraries for Docker.
%endif

%if 0%{?with_unit_test}
%package unit-test
Summary: %{summary} - for running unit tests

%description unit-test
%{summary} - for running unit tests
%endif

%package fish-completion
Summary: fish completion files for Docker
Requires: %{repo} = %{epoch}:%{version}-%{release}
Requires: fish
Provides: %{repo}-io-fish-completion = %{epoch}:%{version}-%{release}

%description fish-completion
This package installs %{summary}.

%package logrotate
Summary: cron job to run logrotate on Docker containers
Requires: %{repo} = %{epoch}:%{version}-%{release}
Provides: %{repo}-io-logrotate = %{epoch}:%{version}-%{release}

%description logrotate
This package installs %{summary}. logrotate is assumed to be installed on
containers for this to work, failures are silently ignored.

%package novolume-plugin
URL: %{git4}
License: MIT
Summary: Block container starts with local volumes defined
Requires: %{repo} = %{epoch}:%{version}-%{release}

%description novolume-plugin
When a volume in provisioned via the `VOLUME` instruction in a Dockerfile or
via `docker run -v volumename`, host's storage space is used. This could lead to
an unexpected out of space issue which could bring down everything.
There are situations where this is not an accepted behavior. PAAS, for
instance, can't allow their users to run their own images without the risk of
filling the entire storage space on a server. One solution to this is to deny users
from running images with volumes. This way the only storage a user gets can be limited
and PAAS can assign quota to it.

This plugin solves this issue by disallowing starting a container with
local volumes defined. In particular, the plugin will block `docker run` with:

- `--volumes-from`
- images that have `VOLUME`(s) defined
- volumes early provisioned with `docker volume` command

The only thing allowed will be just bind mounts.

%package common
Summary: Common files for docker and docker-latest

%description common
This package contains the common files %{_bindir}/%{repo} which will point to
%{_bindir}/%{repo}-current or %{_bindir}/%{repo}-latest configurable via
%{_sysconfdir}/sysconfig/%{repo}

%package vim
Summary: vim syntax highlighting files for Docker
Requires: %{repo} = %{epoch}:%{version}-%{release}
Requires: vim
Provides: %{repo}-io-vim = %{epoch}:%{version}-%{release}

%description vim
This package installs %{summary}.

%package zsh-completion
Summary: zsh completion files for Docker
Requires: %{repo} = %{epoch}:%{version}-%{release}
Requires: zsh
Provides: %{repo}-io-zsh-completion = %{epoch}:%{version}-%{release}

%description zsh-completion
This package installs %{summary}.

%package rhel-push-plugin
License: GPLv2
Summary: Avoids pushing a RHEL-based image to docker.io registry

%description rhel-push-plugin
In order to use this plugin you must be running at least Docker 1.10 which
has support for authorization plugins.

This plugin avoids any RHEL based image to be pushed to the default docker.io
registry preventing users to violate the RH subscription agreement.

%package lvm-plugin
License: LGPLv3
Summary: Docker volume driver for lvm volumes
Requires: %{name} = %{epoch}:%{version}-%{release}

%description lvm-plugin
Docker Volume Driver for lvm volumes.

This plugin can be used to create lvm volumes of specified size, which can
then be bind mounted into the container using `docker run` command.

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
# here keep the new line above otherwise autosetup fails when applying patch
cp %{SOURCE9} .

# untar d-s-s
git clone %{git1} %{repo}-storage-setup-%{commit1}

# untar docker-novolume-plugin
git clone %{git4} %{repo}-novolume-plugin-%{commit4}


# untar docker-runc
git clone %{git6} runc-%{commit6}

# untar docker-containerd
git clone %{git7} containerd-%{commit7}

# common exec script
cp %{SOURCE16} .

# common exec README
cp %{SOURCE17} .

# untar rhel-push-plugin
git clone %{git8} rhel-push-plugin-%{commit8}

# untar lvm-plugin
git clone %{git9} %{repo}-lvm-plugin-%{commit9}
pushd %{repo}-lvm-plugin-%{commit9}/vendor
mkdir src
mv g* src/
popd

%build
cd %{name}-%{version}
# set up temporary build gopath, and put our directory there
mkdir _build
pushd _build
mkdir -p src/%{provider}.%{provider_tld}/{%{repo},projectatomic}
ln -s $(dirs +1 -l) src/%{import_path}
ln -s $(dirs +1 -l)/%{repo}-novolume-plugin-%{commit4} src/%{provider}.%{provider_tld}/projectatomic/%{repo}-novolume-plugin
ln -s $(dirs +1 -l)/containerd-%{commit7} src/%{provider}.%{provider_tld}/docker/containerd
ln -s $(dirs +1 -l)/rhel-push-plugin-%{commit8} src/%{provider}.%{provider_tld}/projectatomic/rhel-push-plugin
ln -s $(dirs +1 -l)/%{repo}-lvm-plugin-%{commit9} src/%{provider}.%{provider_tld}/projectatomic/%{repo}-lvm-plugin
popd

# compile novolume first - otherwise deps in gopath conflict with the others below and this fails
export GOPATH=$(pwd)/%{repo}-novolume-plugin-%{commit4}/Godeps/_workspace:$(pwd)/_build
pushd $(pwd)/_build/src
go build -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" github.com/projectatomic/%{repo}-novolume-plugin
popd

export GOPATH=$(pwd)/rhel-push-plugin-%{commit8}/Godeps/_workspace:$(pwd)/_build
pushd $(pwd)/_build/src
go build -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" %{provider}.%{provider_tld}/projectatomic/rhel-push-plugin
popd

export GOPATH=$(pwd)/%{name}-lvm-plugin-%{commit9}/vendor:$(pwd)/_build
pushd $(pwd)/_build/src
go build -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" %{provider}.%{provider_tld}/projectatomic/%{repo}-lvm-plugin
popd

export DOCKER_GITCOMMIT="%{shortcommit0}/%{version}"
export DOCKER_BUILDTAGS="selinux seccomp"
export GOPATH=$(pwd)/_build:$(pwd)/vendor:%{gopath}:$(pwd)/containerd-%{commit7}/vendor

DOCKER_DEBUG=1 bash -x hack/make.sh dynbinary
man/md2man-all.sh
cp contrib/syntax/vim/LICENSE LICENSE-vim-syntax
cp contrib/syntax/vim/README.md README-vim-syntax.md
cp %{repo}-novolume-plugin-%{commit4}/LICENSE LICENSE-novolume-plugin
cp %{repo}-novolume-plugin-%{commit4}/README.md README-novolume-plugin.md
go-md2man -in %{repo}-novolume-plugin-%{commit4}/man/docker-novolume-plugin.8.md -out docker-novolume-plugin.8
go-md2man -in rhel-push-plugin-%{commit8}/man/rhel-push-plugin.8.md -out rhel-push-plugin.8
go-md2man -in %{repo}-lvm-plugin-%{commit9}/man/%{repo}-lvm-plugin.8.md -out %{repo}-lvm-plugin.8

# build docker-runc
pushd runc-%{commit6}
make BUILDTAGS="seccomp selinux"
popd

# build docker-containerd
pushd containerd-%{commit7}
make
popd

%install
cd %{name}-%{version}

# install binary
install -d %{buildroot}%{_bindir}
rm bundles/latest/dynbinary-client/*.md5 bundles/latest/dynbinary-client/*.sha256
rm bundles/latest/dynbinary-daemon/*.md5 bundles/latest/dynbinary-daemon/*.sha256
install -p -m 755 bundles/latest/dynbinary-client/%{repo}-* %{buildroot}%{_bindir}/%{repo}-current
install -p -m 755 bundles/latest/dynbinary-daemon/%{repo}d-* %{buildroot}%{_bindir}/%{repo}d-current
install -d %{buildroot}%{_libexecdir}/%{repo}
#install -p -m 755 bundles/latest/dynbinary-daemon/%{repo}-proxy-* %{buildroot}%{_libexecdir}/%{repo}/%{repo}-proxy-current

# install manpages
install -d %{buildroot}%{_mandir}/man1
install -p -m 644 man/man1/%{repo}*.1 %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man5
install -p -m 644 man/man5/*.5 %{buildroot}%{_mandir}/man5
install -d %{buildroot}%{_mandir}/man8
install -p -m 644 man/man8/%{repo}*.8 %{buildroot}%{_mandir}/man8

# install bash completion
install -dp %{buildroot}%{_datadir}/bash-completion/completions
install -p -m 644 contrib/completion/bash/%{repo} %{buildroot}%{_datadir}/bash-completion/completions

# install fish completion
# create, install and own /usr/share/fish/vendor_completions.d until
# upstream fish provides it
install -dp %{buildroot}%{_datadir}/fish/vendor_completions.d
install -p -m 644 contrib/completion/fish/%{repo}.fish %{buildroot}%{_datadir}/fish/vendor_completions.d

# install container logrotate cron script
install -dp %{buildroot}%{_sysconfdir}/cron.daily/
install -p -m 755 %{SOURCE8} %{buildroot}%{_sysconfdir}/cron.daily/%{repo}-logrotate

# install vim syntax highlighting
install -d %{buildroot}%{_datadir}/vim/vimfiles/{doc,ftdetect,syntax}
install -p -m 644 contrib/syntax/vim/doc/%{repo}file.txt %{buildroot}%{_datadir}/vim/vimfiles/doc
install -p -m 644 contrib/syntax/vim/ftdetect/%{repo}file.vim %{buildroot}%{_datadir}/vim/vimfiles/ftdetect
install -p -m 644 contrib/syntax/vim/syntax/%{repo}file.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax

# install zsh completion
install -d %{buildroot}%{_datadir}/zsh/site-functions
install -p -m 644 contrib/completion/zsh/_%{repo} %{buildroot}%{_datadir}/zsh/site-functions

# install udev rules
install -d %{buildroot}%{_udevrulesdir}
install -p contrib/udev/80-%{repo}.rules %{buildroot}%{_udevrulesdir}

# install storage dir
install -d %{buildroot}%{_sharedstatedir}/%{repo}

# install secret patch directory
install -d %{buildroot}%{_datadir}/rhel/secrets

# install systemd/init scripts
install -d %{buildroot}%{_unitdir}
%if 0%{?fedora}
install -p -m 644 %{SOURCE5} %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE14} %{buildroot}%{_unitdir}
%else
install -p -m 644 %{SOURCE20} %{buildroot}%{_unitdir}/%{repo}.service
install -p -m 644 %{SOURCE21} %{buildroot}%{_unitdir}/%{repo}-containerd.service
%endif

# install novolume-plugin executable, unitfile, socket and man
install -d %{buildroot}%{_libexecdir}/%{repo}
install -p -m 755 _build/src/%{repo}-novolume-plugin %{buildroot}%{_libexecdir}/%{repo}
install -p -m 644 %{repo}-novolume-plugin-%{commit4}/systemd/%{repo}-novolume-plugin.service %{buildroot}%{_unitdir}
install -p -m 644 %{repo}-novolume-plugin-%{commit4}/systemd/%{repo}-novolume-plugin.socket %{buildroot}%{_unitdir}
install -d %{buildroot}%{_mandir}/man8
install -p -m 644 %{repo}-novolume-plugin.8 %{buildroot}%{_mandir}/man8

# install docker-runc
install -d %{buildroot}%{_libexecdir}/%{repo}
install -p -m 755 runc-%{commit6}/runc %{buildroot}%{_libexecdir}/%{repo}/%{repo}-runc-current

#install docker-containerd-current
install -d %{buildroot}%{_libexecdir}/%{repo}
install -p -m 755 containerd-%{commit7}/bin/containerd %{buildroot}%{_libexecdir}/%{repo}/%{repo}-containerd-current
install -p -m 755 containerd-%{commit7}/bin/containerd-shim %{buildroot}%{_libexecdir}/%{repo}/%{repo}-containerd-shim-current
install -p -m 755 containerd-%{commit7}/bin/ctr %{buildroot}%{_libexecdir}/%{repo}/%{repo}-ctr-current

# for additional args
install -d %{buildroot}%{_sysconfdir}/sysconfig/
install -p -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/sysconfig/%{repo}
install -p -m 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/sysconfig/%{repo}-network
install -p -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/sysconfig/%{repo}-storage

%if 0%{?with_unit_test}
install -d -m 0755 %{buildroot}%{_sharedstatedir}/%{repo}-unit-test/
cp -pav VERSION Dockerfile %{buildroot}%{_sharedstatedir}/%{repo}-unit-test/.
for d in */ ; do
  cp -rpav $d %{buildroot}%{_sharedstatedir}/%{repo}-unit-test/
done
# remove docker.initd as it requires /sbin/runtime no packages in Fedora
rm -rf %{buildroot}%{_sharedstatedir}/%{repo}-unit-test/contrib/init/openrc/docker.initd
%endif

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
%endif

# install %%{repo} config directory
install -dp %{buildroot}%{_sysconfdir}/%{repo}

# install d-s-s
pushd %{repo}-storage-setup-%{commit1}
make install DESTDIR=%{buildroot}
popd

# install %%{_bindir}/%{name}
install -d %{buildroot}%{_bindir}
install -p -m 755 %{SOURCE16} %{buildroot}%{_bindir}/%{repo}

# install rhel-push-plugin executable, unitfile, socket and man
install -d %{buildroot}%{_libexecdir}/%{repo}
install -p -m 755 _build/src/rhel-push-plugin %{buildroot}%{_libexecdir}/%{repo}/rhel-push-plugin
install -p -m 644 rhel-push-plugin-%{commit8}/systemd/rhel-push-plugin.service %{buildroot}%{_unitdir}/rhel-push-plugin.service
install -p -m 644 rhel-push-plugin-%{commit8}/systemd/rhel-push-plugin.socket %{buildroot}%{_unitdir}/rhel-push-plugin.socket
install -d %{buildroot}%{_mandir}/man8
install -p -m 644 rhel-push-plugin.8 %{buildroot}%{_mandir}/man8

# install %%{repo}-lvm-plugin executable, unitfile, socket and man
install -d %{buildroot}/%{_libexecdir}/%{repo}
install -p -m 755 _build/src/%{repo}-lvm-plugin %{buildroot}/%{_libexecdir}/%{repo}/%{repo}-lvm-plugin
install -p -m 644 %{repo}-lvm-plugin-%{commit9}/systemd/%{repo}-lvm-plugin.s* %{buildroot}%{_unitdir}
install -d %{buildroot}%{_mandir}/man8
install -p -m 644 %{repo}-lvm-plugin.8 %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}%{_sysconfdir}/%{repo}
install -p -m 644 %{repo}-lvm-plugin-%{commit9}%{_sysconfdir}/%{repo}/%{repo}-lvm-plugin %{buildroot}%{_sysconfdir}/%{repo}/%{repo}-lvm-plugin

%__mkdir_p %{buildroot}%{_docdir}/%{name}-%{version}
%__mkdir_p %{buildroot}%{_datarootdir}/licenses/%{name}-%{version}

%__cp -pr %{_builddir}/%{name}-%{version}/AUTHORS %{buildroot}%{_docdir}/%{name}-%{version}/AUTHORS
%__cp -pr %{_builddir}/%{name}-%{version}/CHANGELOG.md %{buildroot}%{_docdir}/%{name}-%{version}/CHANGELOG.md 
%__cp -pr %{_builddir}/%{name}-%{version}/CONTRIBUTING.md %{buildroot}%{_docdir}/%{name}-%{version}/CONTRIBUTING.md
%__cp -pr %{_builddir}/%{name}-%{version}/MAINTAINERS %{buildroot}%{_docdir}/%{name}-%{version}/MAINTAINERS
%__cp -pr %{_builddir}/%{name}-%{version}/NOTICE %{buildroot}%{_docdir}/%{name}-%{version}/NOTICE
%__cp -pr %{_builddir}/%{name}-%{version}/README-novolume-plugin.md %{buildroot}%{_docdir}/%{name}-%{version}/README-novolume-plugin.md
%__cp -pr %{_builddir}/%{name}-%{version}/README-vim-syntax.md %{buildroot}%{_docdir}/%{name}-%{version}/README-vim-syntax.md
%__cp -pr %{_builddir}/%{name}-%{version}/README.md %{buildroot}%{_docdir}/%{name}-%{version}/README.md
%__cp -pr %{_builddir}/%{name}-%{version}/README.docker-logrotate %{buildroot}%{_docdir}/%{name}-%{version}/README.docker-logrotate
%__cp -pr %{_builddir}/%{name}-%{version}/README-docker-common %{buildroot}%{_docdir}/%{name}-%{version}/README-docker-common
%__cp -pr %{_builddir}/%{name}-%{version}/rhel-push-plugin-%{commit8}/README.md %{buildroot}%{_docdir}/%{name}-%{version}/README-rhel-push-plugin
%__cp -pr %{_builddir}/%{name}-%{version}/%{repo}-lvm-plugin-%{commit9}/README.md %{buildroot}%{_docdir}/%{name}-%{version}/README.lvm-plugin

%__cp -pr %{_builddir}/%{name}-%{version}/LICENSE %{buildroot}%{_datarootdir}/licenses/%{name}-%{version}/LICENSE
%__cp -pr %{_builddir}/%{name}-%{version}/LICENSE-novolume-plugin %{buildroot}%{_datarootdir}/licenses/%{name}-%{version}/LICENSE-novolume-plugin
%__cp -pr %{_builddir}/%{name}-%{version}/LICENSE-vim-syntax %{buildroot}%{_datarootdir}/licenses/%{name}-%{version}/LICENSE-vim-syntax
%__cp -pr %{_builddir}/%{name}-%{version}/rhel-push-plugin-%{commit8}/LICENSE  %{buildroot}%{_datarootdir}/licenses/%{name}-%{version}/LICENSE-rhel-push-plugin
%__cp -pr %{_builddir}/%{name}-%{version}/%{repo}-lvm-plugin-%{commit9}/LICENSE %{buildroot}%{_datarootdir}/licenses/%{name}-%{version}/LICENSE-lvm-plugin

%check
[ ! -w /run/%{repo}.sock ] || {
    mkdir test_dir
    pushd test_dir
    git clone https://github.com/projectatomic/%{name}.git -b %{docker_branch}
    pushd %{repo}
    make test
    popd
    popd
}

%post
%systemd_post %{repo}

%preun
%systemd_preun %{repo}

%postun
%systemd_postun_with_restart %{repo}

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%config(noreplace) %{_sysconfdir}/sysconfig/%{repo}-*
%{_mandir}/man1/%{repo}*.1.gz
%{_mandir}/man5/*.5.gz
%{_mandir}/man8/%{repo}*.8.gz
%{_bindir}/%{repo}-current
%{_bindir}/%{repo}d-current
%{_unitdir}/%{repo}.service
%{_unitdir}/%{repo}-containerd.service
%{_datadir}/bash-completion/completions/%{repo}
%dir %{_datadir}/rhel/secrets
%dir %{_sharedstatedir}/%{repo}
%{_udevrulesdir}/80-%{repo}.rules
%{_sysconfdir}/%{repo}
# d-s-s specific
%config(noreplace) %{_sysconfdir}/sysconfig/%{repo}-storage-setup
%{_unitdir}/%{repo}-storage-setup.service
%{_bindir}/%{repo}-storage-setup
%dir %{dss_libdir}
%{dss_libdir}/*
# >= 1.11 specific
%{_libexecdir}/%{repo}/%{repo}-runc-current
%{_libexecdir}/%{repo}/%{repo}-containerd-current
%{_libexecdir}/%{repo}/%{repo}-containerd-shim-current
%{_libexecdir}/%{repo}/%{repo}-ctr-current
#%{_libexecdir}/%{repo}/%{repo}-proxy-current
%dir %{_docdir}/%{name}-%{version}
%dir %{_datarootdir}/licenses/%{name}-%{version}
%{_docdir}/%{name}-%{version}/AUTHORS
%{_docdir}/%{name}-%{version}/CHANGELOG.md 
%{_docdir}/%{name}-%{version}/CONTRIBUTING.md
%{_docdir}/%{name}-%{version}/MAINTAINERS
%{_docdir}/%{name}-%{version}/NOTICE
%{_docdir}/%{name}-%{version}/README.md
%{_datarootdir}/licenses/%{name}-%{version}/LICENSE

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE
%endif

%if 0%{?with_unit_test}
%files unit-test
%{_sharedstatedir}/docker-unit-test/
%endif

%files fish-completion
%dir %{_datadir}/fish/vendor_completions.d/
%{_datadir}/fish/vendor_completions.d/%{repo}.fish

%files logrotate
%{_docdir}/%{name}-%{version}/README.docker-logrotate
%{_sysconfdir}/cron.daily/%{repo}-logrotate

%files novolume-plugin
%{_docdir}/%{name}-%{version}/README-novolume-plugin.md
%{_datarootdir}/licenses/%{name}-%{version}/LICENSE-novolume-plugin
%{_libexecdir}/%{repo}/%{repo}-novolume-plugin
%{_unitdir}/%{repo}-novolume-plugin.service
%{_unitdir}/%{repo}-novolume-plugin.socket

%post novolume-plugin
%systemd_post docker-novolume-plugin.service

%preun novolume-plugin
%systemd_preun docker-novolume-plugin.service

%postun novolume-plugin
%systemd_postun_with_restart docker-novolume-plugin.service

%files common
%{_docdir}/%{name}-%{version}/README-docker-common
%{_bindir}/%{repo}
%config(noreplace) %{_sysconfdir}/sysconfig/%{repo}

%files vim
%{_datarootdir}/licenses/%{name}-%{version}/LICENSE-vim-syntax
%{_docdir}/%{name}-%{version}/README-vim-syntax.md
%{_datadir}/vim/vimfiles/doc/%{repo}file.txt
%{_datadir}/vim/vimfiles/ftdetect/%{repo}file.vim
%{_datadir}/vim/vimfiles/syntax/%{repo}file.vim

%files zsh-completion
%{_datadir}/zsh/site-functions/_%{repo}

%files rhel-push-plugin
%{_docdir}/%{name}-%{version}/README-rhel-push-plugin
%{_datarootdir}/licenses/%{name}-%{version}/LICENSE-rhel-push-plugin
%{_mandir}/man8/rhel-push-plugin.8.gz
%{_libexecdir}/%{repo}/rhel-push-plugin
%{_unitdir}/rhel-push-plugin.*

%post rhel-push-plugin
%systemd_post docker-rhel-push-plugin.service

%preun rhel-push-plugin
%systemd_preun docker-rhel-push-plugin.service

%postun rhel-push-plugin
%systemd_postun_with_restart docker-rhel-push-plugin.service

%files lvm-plugin
%{_datarootdir}/licenses/%{name}-%{version}/LICENSE-lvm-plugin
%{_docdir}/%{name}-%{version}/README.lvm-plugin
%config(noreplace) %{_sysconfdir}/%{repo}/%{repo}-lvm-plugin
%{_mandir}/man8/%{repo}-lvm-plugin.8.gz
%{_libexecdir}/%{repo}/%{repo}-lvm-plugin
%{_unitdir}/%{repo}-lvm-plugin.*

%post lvm-plugin
%systemd_post docker-lvm-plugin.service

%preun lvm-plugin
%systemd_preun docker-lvm-plugin.service

%postun lvm-plugin
%systemd_postun_with_restart docker-lvm-plugin.service

%changelog
