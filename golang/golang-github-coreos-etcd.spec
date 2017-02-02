#%define repo https://github.com/coreos/etcd
%define repo            https://%{provider}.%{provider_tld}/%{repo_owner}/%{project}
%global provider        github
%global provider_tld    com
%global repo_owner      coreos
%global project         etcd
%global import_path     %{provider}.%{provider_tld}/%{repo_owner}/%{project}
%define _summary        %(echo `curl -s %{repo} | grep "<title>" | cut -f2 -d ":" | sed 's|</title>||'`)
%define gitversion %(echo `date +%Y%m`)
%define release_ver 1
%global revision %(echo `git ls-remote %{repo}  | head -1 | cut -f 1 | cut -c1-7`)

Name:                   golang-%{provider}-%{repo_owner}-%{project}
Version:                %{gitversion}
Release:                %{release_ver}.%{revision}.%{dist}
Summary:                %{_summary}
License:                Go License
Vendor:                 %{vendor}
Packager:               %{packager}
BuildRequires:          git golang >= 1.8.0
BuildRequires:          golang-rpm-macros
Requires:               golang >= 1.8.0
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
Requires: golang-github-karlseguin-ccache

%description
%{summary}

%prep

%build
export GOPATH=%{buildroot}%{gopath}

go get %{import_path}/...
for pkg_dir in `find %{buildroot}%{gopath}/pkg/linux_amd64/ -maxdepth 2 \
! -path %{buildroot}%{gopath}/pkg/linux_amd64/ \
! -path %{buildroot}%{gopath}/pkg/linux_amd64/%{provider}.%{provider_tld} \
! -path %{buildroot}%{gopath}/pkg/linux_amd64/%{provider}.%{provider_tld}/%{repo_owner}`; do
    %__rm -rf ${pkg_dir}
done

for src_dir in `find %{buildroot}%{gopath}/src/ -maxdepth 2 \
! -path %{buildroot}%{gopath}/src/ \
! -path %{buildroot}%{gopath}/src/%{provider}.%{provider_tld} \
! -path %{buildroot}%{gopath}/src/%{provider}.%{provider_tld}/%{repo_owner}`; do
    %__rm -rf ${src_dir}
done

if [ -f  %{buildroot}%{gopath}/src/%{import_path}/.travis.yml ];then
    %__rm -f %{buildroot}%{gopath}/src/%{import_path}/.travis.yml
fi

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%{gopath}/src/*
%{gopath}/pkg/*
%{gopath}/bin/*

%changelog
