%define repo https://github.com/prometheus/prometheus
%global provider        github
%global provider_tld    com
%global repo_owner      prometheus
%global project         prometheus
%global import_path     %{provider}.%{provider_tld}/%{repo_owner}/%{project}
%define _summary        %(echo `curl -s %{repo} | grep "<title>" | cut -f2 -d ":" | sed 's|</title>||'`)
%define gitversion %(echo `date +%Y%m`)
%define release_ver 1
%global revision %(echo `git ls-remote %{repo}  | head -1 | cut -f 1 | cut -c1-7`)
%global filelist        %{_builddir}/%{name}-%{version}-filelist

Name:           %{project}
Version:        %{gitversion}
Release:        %{release_ver}.%{revision}.%{dist}
Summary:        %{_summary}
License:        Go License
Vendor:         %{vendor}
Packager:       %{packager}

BuildRequires:  git golang >= 1.5.0
BuildRequires: 	golang-github-jteeuwen-go-bindata
Requires:       golang >= 1.5.0 golang-go-bindata
Provides:       golang-%{provider}
Provides:       golang(%{import_path}) = %{version}-%{release}
Requires: 	golang-github-prometheus-promu
Requires: 	golang-github-jteeuwen-go-bindata
Requires:   golang-github.com-prometheus-procfs
Requires:   golang-github.com-prometheus-common
Requires:   golang-github.com-prometheus-client_model
Requires:   golang-github.com-prometheus-client_golang

%include %{_rpmconfigdir}/macros.d/macros.golang
%description
%{summary}

%prep

%build
export GOPATH=%{buildroot}%{gopath}
go get %{import_path}/cmd/%{project}
%__rm -f %{buildroot}%{gopath}/src/%{import_path}/.travis.yml

cd %{buildroot}%{gopath}/src/%{import_path}
make build
make assets

cd %{_builddir}
%__rm -rf %{buildroot}%{gopath}/src/github.com/jteeuwen
%__rm -rf %{buildroot}%{gopath}/src/github.com/prometheus/promu
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/jteeuwen
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/prometheus/promu
%__rm -rf %{buildroot}%{gopath}/bin/go-bindata
%__rm -rf %{buildroot}%{gopath}/bin/promu
(
    echo '%defattr(-,root,root,-)'
    find %{buildroot}%{gopath}/src/%{import_path} -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/src/%{import_path} -type f -printf '%%%attr(664, root, root) "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/pkg/linux_amd64/%{provider}.%{provider_tld}/%{repo_owner} -type f -printf '%%%attr(664, root, root) "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/pkg/linux_amd64/%{provider}.%{provider_tld}/%{project}* -type f -printf '%%%attr(750, root, root) "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/bin/* -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/bin -type f -printf '%%%attr(750, root, root) "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
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

%changelog
