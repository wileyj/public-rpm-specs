#%define repo https://github.com/mitchellh/gox
%define repo            https://%{provider}.%{provider_tld}/%{repo_owner}/%{project}
%global provider        github
%global provider_tld    com
%global repo_owner      mitchellh
%global project         gox
%global import_path     %{provider}.%{provider_tld}/%{repo_owner}/%{project}
%define _summary        %(echo `curl -s %{repo} | grep "<title>" | cut -f2 -d ":" | sed 's|</title>||'`)
%define gitversion %(echo `date +%Y%m`)
%define release_ver 1
%global revision %(echo `git ls-remote %{repo}  | head -1 | cut -f 1 | cut -c1-7`)


Name:                   %{project}
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
Requires:		golang-github-mitchellh-iochan

%description
%{summary}

%package -n %{project}-devel
Summary: %{project} devel
Requires: golang

%description -n %{project}-devel
%{project} devel

%prep
if [ -d %{buildroot} ]; then
  %{__rm} -rf %{buildroot}
fi

%build
export GOPATH=%{buildroot}%{gopath}

go get %{import_path}

for src_dir in `find %{buildroot}%{gopath}/src/ -maxdepth 2 \
! -path %{buildroot}%{gopath}/src/ \
! -path %{buildroot}%{gopath}/src/%{provider}.%{provider_tld} \
! -path %{buildroot}%{gopath}/src/%{provider}.%{provider_tld}/%{repo_owner}`; do
    %__rm -rf ${src_dir}
done
%__rm -rf %{buildroot}%{gopath}/src/%{provider}.%{provider_tld}/%{repo_owner}/iochan
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/

if [ -f  %{buildroot}%{gopath}/src/%{import_path}/.travis.yml ];then
    %__rm -f %{buildroot}%{gopath}/src/%{import_path}/.travis.yml
fi
%__mkdir_p %{buildroot}%{_bindir}
%__mv %{buildroot}%{gopath}/bin/%{name} %{buildroot}%{_bindir}/%{name}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files -n %{project}-devel
%{gopath}/src/*

%files
%{_bindir}/%{name}

%changelog
