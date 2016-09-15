%global with_check 0

%global revision %(echo `git ls-remote https://github.com/kubernetes/kubernetes.git  | head -1 | cut -f 1`)
%global debug_package   %{nil}
%global provider	github
%global provider_tld	com
%global project		GoogleCloudPlatform
%global repo		kubernetes
%global vendorname kubernetes
%global repo_url https://github.com/kubernetes/kubernetes
%global contrib_repo_url https://github.com/kubernetes/contrib
%global import_path	%{provider}.%{provider_tld}/%{project}/%{repo}
%global commit		fbc85e9838f25547be94fbffeeb92a756d908ca0
%global shortcommit	%(c=%{commit}; echo ${c:0:7})
%global gitversion %(echo `curl -s %{repo_url}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">betav'`)
%global _buildshell	/bin/bash
%global _checkshell	/bin/bash
%define rel_version 1

Name:          	%{repo}
Version:	%{gitversion}
Release:	%{rel_version}.%{revision}.%{?dist}
Summary:        Container cluster management
License:        ASL 2.0
URL:            %{import_path}
ExclusiveArch:  x86_64

Source0:      macros.golang
Source1:        genmanpages.sh
Patch0:         Update-github.com-elazarl-go-bindata-assetfs-to-at-l.patch
Patch1:         Fix-Persistent-Volumes-and-Persistent-Volume-Claims.patch
Patch2:         Change-etcd-server-port.patch
Patch4:         use-the-correct-delimiter-for-X-option-of-ldflags.patch
Obsoletes:      cadvisor
Requires: kubernetes-master = %{version}-%{release}
Requires: kubernetes-node = %{version}-%{release}
%include %{SOURCE0}

%description
%{summary}

%package devel
Summary:       %{summary}
BuildRequires: golang >= 1.7

Provides: golang(%{import_path}/cmd/genutils) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/kube-apiserver/app) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/kube-controller-manager/app) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/kube-proxy/app) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/kubelet/app) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/archive) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/assert) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/backoff) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/controllermanager) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/election) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/executor) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/executor/config) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/executor/messages) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/executor/service) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/hyperkube) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/offers) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/offers/metrics) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/proc) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/profile) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/queue) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/redirfd) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/runtime) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/scheduler) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/scheduler/config) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/scheduler/constraint) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/scheduler/ha) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/scheduler/meta) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/scheduler/metrics) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/scheduler/podtask) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/scheduler/service) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/scheduler/uid) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/mesos/pkg/service) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/admission) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/endpoints) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/errors) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/errors/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/latest) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/meta) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/registered) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/resource) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/rest) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/rest/resttest) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/testapi) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/testing) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/v1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/v1beta3) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/validation) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apiserver) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apiserver/metrics) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/auth/authenticator) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/auth/authenticator/bearertoken) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/auth/authorizer) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/auth/authorizer/abac) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/auth/handlers) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/auth/user) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/capabilities) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/cache) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/chaosclient) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientcmd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientcmd/api) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientcmd/api/latest) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientcmd/api/v1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/metrics) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/portforward) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/record) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/remotecommand) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/testclient) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/clientauth) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/cloudprovider) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/cloudprovider/mesos) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/cloudprovider/nodecontroller) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/cloudprovider/openstack) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/cloudprovider/rackspace) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/cloudprovider/routecontroller) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/cloudprovider/servicecontroller) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/framework) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/conversion) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/conversion/queryparams) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/credentialprovider) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/fieldpath) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/fields) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/healthz) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/httplog) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/hyperkube) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubectl) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubectl/cmd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubectl/cmd/config) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubectl/cmd/util) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubectl/resource) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/cadvisor) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/config) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/container) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/dockertools) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/envvars) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/leaky) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/lifecycle) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/metrics) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/network) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/network/exec) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/prober) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/rkt) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/types) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/util) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/labels) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/master) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/master/ports) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/namespace) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/probe) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/probe/exec) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/probe/http) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/probe/tcp) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/proxy) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/proxy/config) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/componentstatus) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/controller) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/controller/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/endpoint) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/endpoint/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/event) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/generic) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/generic/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/generic/rest) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/limitrange) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/minion) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/minion/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/namespace) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/namespace/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/persistentvolume) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/persistentvolume/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/persistentvolumeclaim) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/persistentvolumeclaim/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/pod) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/pod/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/podtemplate) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/podtemplate/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/registrytest) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/resourcequota) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/resourcequota/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/secret) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/secret/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/service) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/service/allocator) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/service/allocator/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/service/ipallocator) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/service/ipallocator/controller) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/service/ipallocator/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/service/portallocator) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/service/portallocator/controller) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/serviceaccount) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/serviceaccount/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/resourcequota) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/runtime) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/securitycontext) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/service) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/serviceaccount) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/tools) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/tools/etcdtest) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/types) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/ui) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/ui/data/dashboard) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/ui/data/swagger) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/config) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/errors) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/exec) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/fielderrors) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/flushwriter) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/httpstream) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/httpstream/spdy) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/iptables) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/mount) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/node) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/operationmanager) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/proxy) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/slice) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/strategicpatch) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/wait) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/workqueue) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/yaml) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/version) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/version/verflag) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/aws_ebs) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/empty_dir) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/gce_pd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/git_repo) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/glusterfs) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/host_path) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/iscsi) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/nfs) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/persistent_claim) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/rbd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/secret) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/util) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volumeclaimbinder) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/watch) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/watch/json) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/cmd/kube-scheduler/app) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/admit) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/deny) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/exec/denyprivileged) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/limitranger) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/namespace/autoprovision) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/namespace/exists) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/namespace/lifecycle) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/resourcequota) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/securitycontext/scdeny) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/serviceaccount) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authenticator) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authenticator/password) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authenticator/password/allow) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authenticator/password/passwordfile) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authenticator/request/basicauth) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authenticator/request/union) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authenticator/request/x509) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authenticator/token/tokenfile) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authenticator/token/tokentest) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/algorithm) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/algorithm/predicates) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/algorithm/priorities) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/algorithmprovider) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/algorithmprovider/defaults) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/api) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/api/latest) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/api/v1) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/api/validation) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/factory) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/metrics) = %{version}-%{release}
Provides: golang(%{import_path}/test/e2e) = %{version}-%{release}
Provides: golang(%{import_path}/test/integration) = %{version}-%{release}
Provides: golang(%{import_path}/test/integration/framework) = %{version}-%{release}

%description devel
%{summary}

This package contains library source intended for
building other packages which use %{project}/%{repo}.

%package unit-test
Summary: %{summary} - for running unit tests

Requires: golang >= 1.2-7
Requires: etcd >= 2.0.9
Requires: hostname
Requires: rsync
Requires: NetworkManager

%description unit-test
%{summary} - for running unit tests

%package master
Summary: Kubernetes services for master host

BuildRequires: golang >= 1.7
BuildRequires: systemd
BuildRequires: rsync
BuildRequires: go-md2man
BuildRequires: golang-go-bindata 

Requires(pre): shadow-utils
Requires: kubernetes-client = %{version}-%{release}
Conflicts: kubernetes-node < %{version}-%{release}
Conflicts: kubernetes-node > %{version}-%{release}

%description master
Kubernetes services for master host

%package node
Summary: Kubernetes services for node host

%if 0%{?fedora} >= 21 || 0%{?rhel} || 0%{?amzn} 
Requires: docker
%else
Requires: docker-io
%endif

BuildRequires: golang >= 1.7
BuildRequires: systemd
BuildRequires: rsync
BuildRequires: go-md2man
Requires(pre): shadow-utils
Requires: socat
Requires: kubernetes-client = %{version}-%{release}
Conflicts: kubernetes-master < %{version}-%{release}
Conflicts: kubernetes-master > %{version}-%{release}

%description node
Kubernetes services for node host

%package client
Summary: Kubernetes client tools

BuildRequires: golang >= 1.7

%description client
Kubernetes client tools like kubectl

%prep
if [ -d %{name}-%{version} ];then
    %{__rm} -rf %{name}-%{version}
fi
if [ -d %{name}-contrib-%{version} ]; then
  %{__rm} -rf %{name}-contrib-%{version}
fi
git clone %{repo_url} %{name}-%{version}
git clone %{contrib_repo_url} %{name}-contrib-%{version}
cd %{name}-%{version}
git submodule init
git submodule update

%build
cd %{name}-%{version}
source %{_sysconfdir}/profile.d/golang.sh
export KUBE_GIT_TREE_STATE="clean"
export KUBE_GIT_COMMIT=`git rev-parse HEAD`
export KUBE_GIT_VERSION=%{version}-%{revision}
make WHAT='--use_go_build'

# convert md to man
pushd docs
cp %{SOURCE1} genmanpages.sh
bash genmanpages.sh
popd

%install
cd %{name}-%{version}
. hack/lib/init.sh
kube::golang::setup_env
output_path="${KUBE_OUTPUT_BINPATH}/$(kube::golang::current_platform)"
#binaries=(kube-apiserver kube-controller-manager kube-scheduler kube-proxy kubelet kubectl kube-version-change)
binaries=(kube-apiserver kube-controller-manager kube-scheduler kube-proxy kubelet kubectl )
install -m 755 -d %{buildroot}%{_bindir}
for bin in "${binaries[@]}"; do
  echo "+++ INSTALLING ${bin}"
  install -p -m 755 -t %{buildroot}%{_bindir} ${output_path}/${bin}
done

# /etc/profile.d/%{name}.sh
%{__mkdir_p} %{buildroot}%{_sysconfdir}/profile.d
cat <<EOF> %{buildroot}%{_sysconfdir}/profile.d/%{name}.sh
%{_bindir}/kubectl completion <shell>
EOF

echo "Moving contrib folders to kubernetes source tree..."
for i in `ls ../%{name}-contrib-%{version}`; do
  if [ -d ../%{name}-contrib-%{version}/$i ]; then
    echo "Copying contrib dir: ../%{name}-contrib-%{version}/$i to contrib/$i"
    %{__cp} -R ../%{name}-contrib-%{version}/$i contrib/$i
  fi
done

# install config files
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
install -m 644 -t %{buildroot}%{_sysconfdir}/%{name} contrib/init/systemd/environ/*

# install service files
install -d -m 0755 %{buildroot}%{_unitdir}
install -m 0644 -t %{buildroot}%{_unitdir} contrib/init/systemd/*.service

# install manpages
install -d %{buildroot}%{_mandir}/man1
install -p -m 644 docs/man/man1/* %{buildroot}%{_mandir}/man1

# install the place the kubelet defaults to put volumes
install -d %{buildroot}%{_sharedstatedir}/kubelet

# place contrib/init/systemd/tmpfiles.d/kubernetes.conf to /usr/lib/tmpfiles.d/kubernetes.conf
install -d -m 0755 %{buildroot}%{_tmpfilesdir}
install -p -m 0644 -t %{buildroot}/%{_tmpfilesdir} contrib/init/systemd/tmpfiles.d/kubernetes.conf


# install devel source codes
install -d %{buildroot}/%{gopath}/src/%{import_path}
for d in build cluster cmd contrib examples hack pkg plugin test; do
    cp -rpav $d %{buildroot}/%{gopath}/src/%{import_path}/
done

# place files for unit-test rpm
install -d -m 0755 %{buildroot}%{_sharedstatedir}/kubernetes-unit-test/
#cp -pav README.md %{buildroot}%{_sharedstatedir}/kubernetes-unit-test/.
for d in _output Godeps api cmd docs examples hack pkg plugin third_party test; do
  cp -a $d %{buildroot}%{_sharedstatedir}/kubernetes-unit-test/
done

%if 0%{?with_check}
%check
cd %{name}-%{version}
# Fedora, RHEL7 and CentOS are tested via unit-test subpackage
if [ 1 != 1 ]; then
echo "******Testing the commands*****"
hack/test-cmd.sh
echo "******Benchmarking kube********"
hack/benchmark-go.sh

# In Fedora 20 and RHEL7 the go cover tools isn't available correctly
%if 0%{?fedora} >= 21
echo "******Testing the go code******"
hack/test-go.sh
echo "******Testing integration******"
hack/test-integration.sh --use_go_build
%endif
fi
%endif

%pre master
getent group kube >/dev/null || groupadd -r kube
getent passwd kube >/dev/null || useradd -r -g kube -d / -s /sbin/nologin -c "Kubernetes user" kube

%post master
%systemd_post kube-apiserver kube-scheduler kube-controller-manager

%preun master
%systemd_preun kube-apiserver kube-scheduler kube-controller-manager

%postun master
%systemd_postun


%pre node
getent group kube >/dev/null || groupadd -r kube
getent passwd kube >/dev/null || useradd -r -g kube -d / -s /sbin/nologin -c "Kubernetes user" kube

%post node
%systemd_post kubelet kube-proxy

%preun node
%systemd_preun kubelet kube-proxy

%postun node
%systemd_postun

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%%{name}-contrib-%{version}" != "/" ] && %__rm -rf %{_builddir}/%%{name}-contrib-%{version} 
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
[ "%{_builddir}/%{pkgname}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{pkgname}-%{version}
[ "%{_builddir}/%{name}-contrib-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-contrib-%{version}

%files
# empty as it depends on master and node

%files master
#%doc README.md LICENSE CONTRIB.md CONTRIBUTING.md DESIGN.md
%{_mandir}/man1/kube-apiserver.1*
%{_mandir}/man1/kube-controller-manager.1*
%{_mandir}/man1/kube-scheduler.1*
%attr(750, -, kube) %caps(cap_net_bind_service=ep) %{_bindir}/kube-apiserver
%{_bindir}/kube-controller-manager
%{_bindir}/kube-scheduler
#%{_bindir}/kube-version-change
%{_unitdir}/kube-apiserver.service
%{_unitdir}/kube-controller-manager.service
%{_unitdir}/kube-scheduler.service
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/apiserver
%config(noreplace) %{_sysconfdir}/%{name}/scheduler
%config(noreplace) %{_sysconfdir}/%{name}/config
%config(noreplace) %{_sysconfdir}/%{name}/controller-manager
%{_tmpfilesdir}/kubernetes.conf

%files node
#%doc README.md LICENSE CONTRIB.md CONTRIBUTING.md DESIGN.md
%{_mandir}/man1/kubelet.1*
%{_mandir}/man1/kube-proxy.1*
%{_bindir}/kubelet
%{_bindir}/kube-proxy
#%{_bindir}/kube-version-change
%{_unitdir}/kube-proxy.service
%{_unitdir}/kubelet.service
%dir %{_sharedstatedir}/kubelet
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/config
%config(noreplace) %{_sysconfdir}/%{name}/kubelet
%config(noreplace) %{_sysconfdir}/%{name}/proxy
%{_tmpfilesdir}/kubernetes.conf

%files client
#%doc README.md LICENSE CONTRIB.md CONTRIBUTING.md DESIGN.md
%{_mandir}/man1/kubectl.1*
%{_mandir}/man1/kubectl-*
%{_bindir}/kubectl
%attr(750, root, root) %{_sysconfdir}/profile.d/%{name}.sh
#%{_datadir}/bash-completion/completions/kubectl

%files unit-test
%{_sharedstatedir}/kubernetes-unit-test/

%files devel
#%doc README.md LICENSE CONTRIB.md CONTRIBUTING.md DESIGN.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%{gopath}/src/%{import_path}

%changelog
