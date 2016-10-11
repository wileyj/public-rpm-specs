%define repo https://github.com/coreos/etcd
%global provider        github
%global provider_tld    com
%global repo_owner      coreos
%global project         etcd
%global import_path     %{provider}.%{provider_tld}/%{repo_owner}/%{project}
%define _summary        %(echo `curl -s %{repo} | grep "<title>" | cut -f2 -d ":" | sed 's|</title>||'`)
%define gitversion %(echo `date +%Y%m`)
%global filelist        %{_builddir}/%{name}-%{version}-filelist
%define release_ver 1
%global revision %(echo `git ls-remote %{repo}  | head -1 | cut -f 1 | cut -c1-7`)

%include                %{_rpmconfigdir}/macros.d/macros.golang
Name:                   golang-%{provider}-%{repo_owner}-%{project}
Version:                %{gitversion}
Release:                %{release_ver}.%{revision}.%{dist}
Summary:                %{_summary}
License:                Go License
Vendor:                 %{vendor}
Packager:               %{packager}
BuildRequires:          git golang >= 1.5.0
Requires:               golang >= 1.5.0
Provides:               %{name}
Provides:               %{name}-devel
Provides:               golang(%{import_path}) 
Provides:               golang(%{import_path})-devel
Requires: golang-gopkg-cheggaaa
Requires: golang-google-golang-grpc
Requires: golang-golang-x-time
Requires: golang-github-xiang90-probing
Requires: golang-github-urfave-cli
Requires: golang-github-stretchr-testify
Requires: golang-github-spacejam-loghisto
Requires: golang-github-olekukonko-tablewriter
Requires: golang-github-mattn-go-runewidth
Requires: golang-github-kr-pty
Requires: golang-github-jonboulle-clockwork
Requires: golang-github-grpc-ecosystem-grpc-gateway
Requires: golang-github-google-btree
Requires: golang-github-gogo-protobuf
Requires: golang-github-ghodss-yaml
Requires: golang-github-dustin-go-humanize
Requires: golang-github-coreos-go-semver
Requires: golang-github-cockroachdb-cmux
Requires: golang-github-cloudfoundry-incubator-candiedyaml
Requires: golang-github-boltdb-bolt
Requires: golang-github-akrennmair-gopcap
Requires: golang-github-ugorji-go
Requires: golang-github-spf13-pflag
Requires: golang-golang-x-net
Requires: golang-golang-x-crypto
Requires: golang-github-spf13-pflag
Requires: golang-github-spf13-cobra
Requires: golang-github-prometheus-procfs
Requires: golang-github-prometheus-common
Requires: golang-github-prometheus-client_model
Requires: golang-github-prometheus-client_golang
Requires: golang-github-matttproud-golang_protobuf
Requires: golang-github-golang-protobuf
Requires: golang-github-golang-glog
Requires: golang-github-coreos-pkg
Requires: golang-github-coreos-go-systemd
Requires: golang-github-bgentry-speakeasy
Requires: golang-github-beorn7-perks

%description
%{summary}

%prep

%build
export GOPATH=%{buildroot}%{gopath}

go get %{import_path}/...
%{__rm} -f %{buildroot}%{gopath}/src/%{import_path}/.travis.yml
%__rm -rf %{buildroot}%{gopath}/src/google.golang.org
%__rm -rf %{buildroot}%{gopath}/src/github.com/ugorji
%__rm -rf %{buildroot}%{gopath}/src/gopkg.in
%__rm -rf %{buildroot}%{gopath}/src/golang.org
%__rm -rf %{buildroot}%{gopath}/src/github.com/spf13
%__rm -rf %{buildroot}%{gopath}/src/github.com/xiang90
%__rm -rf %{buildroot}%{gopath}/src/github.com/urfave
%__rm -rf %{buildroot}%{gopath}/src/github.com/stretchr
%__rm -rf %{buildroot}%{gopath}/src/github.com/spacejam
%__rm -rf %{buildroot}%{gopath}/src/github.com/olekukonko
%__rm -rf %{buildroot}%{gopath}/src/github.com/mattn
%__rm -rf %{buildroot}%{gopath}/src/github.com/kr
%__rm -rf %{buildroot}%{gopath}/src/github.com/jonboulle
%__rm -rf %{buildroot}%{gopath}/src/github.com/grpc-ecosystem
%__rm -rf %{buildroot}%{gopath}/src/github.com/google
%__rm -rf %{buildroot}%{gopath}/src/github.com/gogo
%__rm -rf %{buildroot}%{gopath}/src/github.com/ghodss
%__rm -rf %{buildroot}%{gopath}/src/github.com/dustin
%__rm -rf %{buildroot}%{gopath}/src/github.com/coreos/go-semver
%__rm -rf %{buildroot}%{gopath}/src/github.com/cockroachdb
%__rm -rf %{buildroot}%{gopath}/src/github.com/cloudfoundry-incubator
%__rm -rf %{buildroot}%{gopath}/src/github.com/boltdb
%__rm -rf %{buildroot}%{gopath}/src/github.com/akrennmair
%__rm -rf %{buildroot}%{gopath}/src/github.com/prometheus
%__rm -rf %{buildroot}%{gopath}/src/github.com/coreos/pkg
%__rm -rf %{buildroot}%{gopath}/src/github.com/coreos/go-systemd
%__rm -rf %{buildroot}%{gopath}/src/github.com/golang
%__rm -rf %{buildroot}%{gopath}/src/github.com/matttproud
%__rm -rf %{buildroot}%{gopath}/src/github.com/bgentry
%__rm -rf %{buildroot}%{gopath}/src/github.com/beorn7

%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/google.golang.org
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/gopkg.in
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/golang.org
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/spf13
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/ugorji
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/xiang90
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/urfave
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/stretchr
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/spacejam
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/olekukonko
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/mattn
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/kr
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/jonboulle
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/grpc-ecosystem
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/google
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/gogo
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/ghodss
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/dustin
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/coreos/go-semver
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/cockroachdb
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/cloudfoundry-incubator
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/boltdb
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/akrennmair
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/prometheus
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/coreos/pkg
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/coreos/go-systemd
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/bgentry
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/matttproud
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/golang
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/beorn7
(
    echo '%defattr(-,root,root,-)'
    find %{buildroot}%{gopath}/src/%{import_path} -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/src/%{import_path} -type f -printf '%%%attr(664, root, root) "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    #find %{buildroot}%{gopath}/pkg/linux_amd64/%{provider}.%{provider_tld}/%{repo_owner} -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/pkg/linux_amd64/%{provider}.%{provider_tld}/%{repo_owner} -type f -printf '%%%attr(664, root, root) "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/bin/* -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/bin -type f -printf '%%%attr(750, root, root) "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/pkg/linux_amd64/%{provider}.%{provider_tld}/%{project}* -type f -printf '%%%attr(750, root, root) "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
) > %{filelist}
echo '%dir "%{gopath}/src/%{import_path}"' >> %{filelist}
%{__sed} -i -e 's/%dir ""//g' %{filelist}
%{__sed} -i -e '/^$/d' %{filelist}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
%__rm -f %{_builddir}/%{filelist}

%files -f %{filelist}
%{gopath}/src/%{import_path}/cmd/etcd
%{gopath}/src/%{import_path}/cmd/etcdctl
%{gopath}/src/%{import_path}/cmd/tools
%{gopath}/src/%{import_path}/cmd/vendor/github.com/coreos/etcd

%changelog

