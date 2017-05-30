#%define repo https://github.com/sensu/uchiwa
%define repo            https://%{provider}.%{provider_tld}/%{repo_owner}/%{project}
%global provider        github
%global provider_tld    com
%global repo_owner      sensu
%global project         uchiwa
%global import_path     %{provider}.%{provider_tld}/%{repo_owner}/%{project}
%define _summary        %(echo `curl -s %{repo} | grep "<title>" | cut -f2 -d ":" | sed 's|</title>||'`)
%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">'`)
%define release_ver 1
%global revision %(echo `git ls-remote %{repo}  | head -1 | cut -f 1 | cut -c1-7`)

Name:           %{project}
Version:        %{gitversion}
Release:        %{release_ver}.%{revision}.%{dist}
Summary:        %{_summary}
License:        Go License
Vendor:         %{vendor}
Packager:       %{packager}
BuildRequires:          git golang >= 1.8
BuildRequires:          golang-rpm-macros
Provides:       golang-%{provider}
Provides:       golang(%{import_path}) = %{version}-%{release}
Requires:	golang-github-dgrijalva-jwt-go
Requires:	golang-github-jbenet-go-context
Requires:	golang-github-mitchellh-mapstructure 
Requires:	golang-github-palourde-mergo
Requires:	golang-github-bencaron-gosensu
Provides:       %{name} = %{version}

%description
%{summary}

%prep
if [ -d %{buildroot} ]; then
  %{__rm} -rf %{buildroot}
fi

%build
export GOPATH=%{buildroot}%{gopath}

go get %{import_path}
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
