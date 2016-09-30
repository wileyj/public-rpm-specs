%define url https://github.com/google/cadvisor
%global provider        github
%global provider_tld    com
%global repo_owner      google
%global project         cadvisor
%global import_path     %{provider}.%{provider_tld}/%{repo_owner}/%{project}
%define _summary        %(echo `curl -s %{url} | grep "<title>" | cut -f2 -d ":" | sed 's|</title>||'`)
%define repo %{url}.git
%define gitversion %(echo `date +%s`)
%define release_ver 1
%global revision %(echo `git ls-remote %{repo}  | head -1 | cut -f 1 | cut -c1-7`)
%global _python_bytecompile_errors_terminate_build 0

Name:           %{project}
Version:        %{gitversion}
Release:        %{release_ver}.%{revision}.%{dist}
Summary:        %{_summary}
License:        Go License
Vendor:         %{vendor}
Packager:       %{packager}

BuildRequires:  git golang >= 1.5.0
Requires:       golang >= 1.5.0 golang-bindata
Provides:       golang-%{provider}
Provides:       golang(%{import_path}) = %{version}-%{release}


%include %{_rpmconfigdir}/macros.d/macros.golang
%description
%{summary}

%prep

%build
export GOPATH=%{buildroot}%{gopath}
go get -d %{import_path}
cd $GOPATH/src/%{import_path}
make build

%{__rm} -rf %{buildroot}%{gopath}/src/%{import_path}/.git
%{__rm} -f %{buildroot}%{gopath}/src/%{import_path}/.travis.yml
%{__rm} -rf  %{buildroot}%{gopath}/src/%{provider}.%{provider_tld}/jteeuwen
%{__rm} -rf  %{buildroot}%{gopath}/pkg/linux_amd64/%{provider}.%{provider_tld}/jteeuwen
%{__rm} -rf  %{buildroot}%{gopath}/bin/go-bindata
(
    echo '%defattr(-,root,root,-)'
    find %{buildroot}%{gopath}/src/%{import_path} -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/src/%{import_path} -type f -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/pkg/linux_amd64/%{provider}.%{provider_tld}/%{repo_owner} -type f -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g'
) > %{_builddir}/%{name}-%{version}-filelist
echo '%dir "%{gopath}/src/%{import_path}"' >> %{_builddir}/%{name}-%{version}-filelist
%{__sed} -i -e 's/%dir ""//g' %{_builddir}/%{name}-%{version}-filelist
%{__sed} -i -e '/^$/d' %{_builddir}/%{name}-%{version}-filelist


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
%__rm -f %{_builddir}/%{name}-%{version}-filelist

%files -f %{name}-%{version}-filelist

%changelog

