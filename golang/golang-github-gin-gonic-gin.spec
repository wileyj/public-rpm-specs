%define repo https://github.com/gin-gonic/gin
%global provider        github
%global provider_tld    com
%global repo_owner      gin-gonic
%global project         gin
%global import_path     %{provider}.%{provider_tld}/%{repo_owner}/%{project}
%define _summary        %(echo `curl -s %{repo} | grep "<title>" | cut -f2 -d ":" | sed 's|</title>||'`)
%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">v'`)
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

Requires:   	golang-sse golang-net golang-validator.v8 golang-yaml.v2 golang-protobuf
Requires: golang-github-golang-protobuf
Requires: golang-github-manucorporat
Requires: golang-golang-x-net
Requires: golang-gopkg-go-playground
Requires: golang-gopkg-yaml.v2

%description
%{summary}

%prep
if [ -d %{buildroot} ]; then
  %{__rm} -rf %{buildroot}
fi

%build
export GOPATH=%{buildroot}%{gopath}

go get %{import_path}
%{__rm} -f %{buildroot}%{gopath}/src/%{import_path}/.travis.yml
%__rm -rf %{buildroot}%{gopath}/src/github.com/golang/protobuf
%__rm -rf %{buildroot}%{gopath}/src/github.com/manucorporat
%__rm -rf %{buildroot}%{gopath}/src/golang.org/x/net
%__rm -rf %{buildroot}%{gopath}/src/gopkg.in/go-playground
%__rm -rf %{buildroot}%{gopath}/src/gopkg.in/yaml.v2
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/golang
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/manucorporat
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/golang.org
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/gopkg.in
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
