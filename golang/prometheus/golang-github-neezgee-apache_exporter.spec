%define repo https://github.com/neezgee/apache_exporter
%global provider        github
%global provider_tld    com
%global repo_owner      neezgee
%global project         apache_exporter
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
Provides:               prometheus-apache_exporter
Requires:   golang-github-prometheus-procfs
Requires:   golang-github-prometheus-log
Requires:   golang-github-prometheus-common
Requires:   golang-github-prometheus-client_model
Requires:   golang-github-prometheus-client_golang
Requires:   golang-github-matttproud-golang_protobuf_extensions
Requires:   golang-github-golang-protobuf
Requires:   golang-github-beorn7-perks
Requires:   golang-github-sirupsen-logrus

%description
%{summary}

%prep

%build
export GOPATH=%{buildroot}%{gopath}

go get %{import_path}/...
%{__rm} -f %{buildroot}%{gopath}/src/%{import_path}/.travis.yml
%__rm -rf %{buildroot}%{gopath}/src/github.com/prometheus
%__rm -rf %{buildroot}%{gopath}/src/github.com/matttproud
%__rm -rf %{buildroot}%{gopath}/src/github.com/golang
%__rm -rf %{buildroot}%{gopath}/src/github.com/beorn7
%__rm -rf %{buildroot}%{gopath}/src/github.com/Sirupsen

%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/prometheus
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/golang
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/beorn7
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/Sirupsen
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/matttproud
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

%changelog
