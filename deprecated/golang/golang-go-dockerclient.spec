%define repo https://github.com/fsouza/go-dockerclient
%global provider        github
%global provider_tld    com
%global repo_owner      fsouza
%global project         go-dockerclient
%global import_path     %{provider}.%{provider_tld}/%{repo_owner}/%{project}
%define _summary        %(echo `curl -s %{repo} | grep "<title>" | cut -f2 -d ":" | sed 's|</title>||'`)
#%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d 'v\\-</span class="tag-name">'`)
%define gitversion 1.0.0
%define release_ver 1
%global _python_bytecompile_errors_terminate_build 0

Name:           golang-%{project}
Version:        %{gitversion}
Release:        %{release_ver}.%{dist}
Summary:        %{_summary}
License:        Go License
Vendor:         %{vendor}
Packager:       %{packager}
BuildRequires:  git golang >= 1.5.0 
Requires:       golang >= 1.5.0
Provides:       golang-%{provider}
Provides:       golang(%{import_path}) = %{version}-%{release}

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
for i in `find %{buildroot} -type d -name ".git" `; do
    %{__rm} -rf $i
done
for i in `find %{buildroot} -type f -name ".gitignore"`;do
    %{__rm} -f $i
done
for i in `find %{buildroot} -type f -name ".travis.yml"` ;do
    %{__rm} -f $i
done
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
[ "%{_builddir}/%{name}-%{version}-filelist" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}-filelist

%files -f %{name}-%{version}-filelist
%changelog

