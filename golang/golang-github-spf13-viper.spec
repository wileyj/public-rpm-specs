%define repo https://github.com/spf13/viper
%global provider        github
%global provider_tld    com
%global repo_owner      spf13
%global project         viper
%global import_path     %{provider}.%{provider_tld}/%{repo_owner}/%{project}
%define _summary        %(echo `curl -s %{repo} | grep "<title>" | cut -f2 -d ":" | sed 's|</title>||'`)
%define gitversion %(echo `date +%Y%m`)
%define release_ver 1
%global revision %(echo `git ls-remote %{repo}  | head -1 | cut -f 1 | cut -c1-7`)
%global filelist        %{_builddir}/%{name}-%{version}-filelist

Name:           golang-%{project}
Version:        %{gitversion}
Release:        %{release_ver}.%{revision}.%{dist}
Summary:        %{_summary}
License:        Go License
Vendor:         %{vendor}
Packager:       %{packager}

BuildRequires:  git golang >= 1.5.0
BuildRequires:  gnulib-devel
Requires:       golang >= 1.5.0
Requires: 	golang-github-spf13-pflag 
Requires: 	golang-github-spf13-jwalterweatherman 
Requires: 	golang-github-spf13-cast 
Requires: 	golang-github-spf13-afero 
Requires: 	golang-github-pkg-sftp 
Requires: 	golang-github-pkg-errors 
Requires: 	golang-github-pelletier-go-toml 
Requires: 	golang-github-pelletier-go-buffruneio 
Requires:	golang-github-mitchellh-mapstructure 
Requires: 	golang-github-magiconair-properties 
Requires: 	golang-github-kr-fs 
Requires: 	golang-github-hashicorp-hcl 
Requires: 	golang-github-fsnotify-snotify 
Requires: 	golang-golang-x-text 
Requires: 	golang-gopkg-x-yaml.v2 
Requires: 	golang-golang-x-sys 
Requires: 	golang-golang-x-crypto
Provides:       golang-%{provider}
Provides:       golang(%{import_path}) = %{version}-%{release}
%include %{_rpmconfigdir}/macros.d/macros.golang
%description
%{summary}

%prep

%build
export GOPATH=%{buildroot}%{gopath}

go get -d -t -u %{import_path}/...
#%{__rm} -rf %{buildroot}%{gopath}/src/%{import_path}/.git
%{__rm} -f %{buildroot}%{gopath}/src/%{import_path}/.travis.yml
%__rm -rf %{buildroot}%{gopath}/src/github.com/spf13/pflag
%__rm -rf %{buildroot}%{gopath}/src/github.com/spf13/jwalterweatherman
%__rm -rf %{buildroot}%{gopath}/src/github.com/spf13/cast
%__rm -rf %{buildroot}%{gopath}/src/github.com/spf13/afero
%__rm -rf %{buildroot}%{gopath}/src/github.com/pkg/sftp
%__rm -rf %{buildroot}%{gopath}/src/github.com/pkg/errors
%__rm -rf %{buildroot}%{gopath}/src/github.com/pelletier/go-toml
%__rm -rf %{buildroot}%{gopath}/src/github.com/pelletier/go-buffruneio
%__rm -rf %{buildroot}%{gopath}/src/github.com/mitchellh/mapstructure
%__rm -rf %{buildroot}%{gopath}/src/github.com/magiconair/properties
%__rm -rf %{buildroot}%{gopath}/src/github.com/kr/fs
%__rm -rf %{buildroot}%{gopath}/src/github.com/hashicorp/hcl
%__rm -rf %{buildroot}%{gopath}/src/github.com/fsnotify/fsnotify
%__rm -rf %{buildroot}%{gopath}/src/golang.org
%__rm -rf %{buildroot}%{gopath}/src/gopkg.in
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/fsnotify
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/hashicorp
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/kr
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/magiconair
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/mitchellh
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/pelletier
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/pelletier
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/github.com/pkg
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/golang.org
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/gopkg.in
(
    echo '%defattr(-,root,root,-)'
    find %{buildroot}%{gopath}/src/%{import_path} -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/src/%{import_path} -type f -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/pkg/linux_amd64/%{provider}.%{provider_tld}/%{repo_owner} -type f -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g'
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

%files -f %{_builddir}/%{filelist}

%changelog

