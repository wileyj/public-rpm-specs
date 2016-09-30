%define repo https://github.com/gin-gonic/gin
%global provider        github
%global provider_tld    com
%global repo_owner      gin-gonic
%global project         gin
%global import_path     %{provider}.%{provider_tld}/%{repo_owner}/%{project}
%define _summary        %(echo `curl -s %{repo} | grep "<title>" | cut -f2 -d ":" | sed 's|</title>||'`)
%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">v'`)
%define release_ver 1
%global revision %(echo `git ls-remote %{repo}  | head -1 | cut -f 1 | cut -c1-7`)
%global _python_bytecompile_errors_terminate_build 0

Name:           golang-%{project}
Version:        %{gitversion}
Release:        %{release_ver}.%{revision}.%{dist}

Summary:        %{_summary}
License:        Go License
Vendor:         %{vendor}
Packager:       %{packager}

BuildRequires:  git golang >= 1.5.0 
Requires:       golang >= 1.5.0
Provides:       golang-%{provider}
Provides:       golang(%{import_path}) = %{version}-%{release}
Requires:   	golang-sse golang-net golang-validator.v8 golang-yaml.v2 golang-protobuf
%include %{_rpmconfigdir}/macros.d/macros.golang
%description
%{summary}

%prep
if [ -d %{buildroot} ]; then
  %{__rm} -rf %{buildroot}
fi

%build
export GOPATH=%{buildroot}%{gopath}

go get %{import_path}
%{__rm} -rf %{buildroot}%{gopath}/src/%{import_path}/.git
%{__rm} -rf %{buildroot}%{gopath}/src/github.com/manucorporat
%{__rm} -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/manucorporat
%{__rm} -rf %{buildroot}%{gopath}/src/github.com/golang
%{__rm} -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/golang
%{__rm} -rf %{buildroot}%{gopath}/src/gopkg.in
%{__rm} -rf %{buildroot}%{gopath}/pkg/linux_amd64/gopkg.in
%{__rm} -rf %{buildroot}%{gopath}/src/golang.org
%{__rm} -rf %{buildroot}%{gopath}/pkg/linux_amd64/golang.org
%{__rm} -f %{buildroot}%{gopath}/src/%{import_path}/.travis.yml
(
    echo '%defattr(-,root,root,-)'
    find %{buildroot}%{gopath}/src/%{import_path} -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/src/%{import_path} -type f -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/pkg/linux_amd64/%{provider}.%{provider_tld}/%{repo_owner} -type f -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g'
) > %{name}-%{version}-filelist
echo '%dir "%{gopath}/src/%{import_path}"' >> %{name}-%{version}-filelist
%{__sed} -i -e 's/%dir ""//g' %{name}-%{version}-filelist
%{__sed} -i -e '/^$/d' %{name}-%{version}-filelist


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
%__rm -f %{_builddir}/%{name}-%{version}-filelist

%files -f %{name}-%{version}-filelist

%changelog
