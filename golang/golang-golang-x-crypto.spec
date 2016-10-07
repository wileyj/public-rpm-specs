%define repo https://github.com/golang/crypto
%global provider        golang
%global provider_tld    org
%global repo_owner      x 
%global project         crypto
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
Requires:		golang-golang-x-net
%description
%{summary}

%prep
if [ -d %{buildroot} ]; then
  %{__rm} -rf %{buildroot}
fi

%build
export GOPATH=%{buildroot}%{gopath}

go get -d -t -u %{import_path}/...
%{__rm} -f %{buildroot}%{gopath}/src/%{import_path}/.travis.yml
%__rm -rf %{buildroot}%{gopath}/src/golang.org/x/net
%__rm -rf %{buildroot}%{gopath}/pkg/linux_amd64/golang.org/x/net
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