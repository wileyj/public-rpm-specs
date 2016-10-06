%define repo https://github.com/jteeuwen/go-bindata
%global provider        github
%global provider_tld    com
%global repo_owner      jteeuwen
%global project         go-bindata
%global import_path     %{provider}.%{provider_tld}/%{repo_owner}/%{project}
%define _summary        %(echo `curl -s %{repo} | grep "<title>" | cut -f2 -d ":" | sed 's|</title>||'`)
%define gitversion %(echo `date +%Y%m`)
%define release_ver 1
%global revision %(echo `git ls-remote %{repo}  | head -1 | cut -f 1 | cut -c1-7`)
%global filelist %{_builddir}/%{name}-%{version}-filelist

Name:           golang-%{provider}-%{repo_owner}-%{project}
Version:        %{gitversion}
Release:        %{release_ver}.%{revision}.%{dist}
Summary:        %{_summary}
License:        Go License
Vendor:         %{vendor}
Packager:       %{packager}

BuildRequires:  git golang >= 1.5.0
Requires:       golang >= 1.5.0
Provides:       %{name}
Provides:       %{name}-devel
Provides:       golang(%{import_path}) 
Provides:	golang(%{import_path})-devel
%include %{_rpmconfigdir}/macros.d/macros.golang

%description
%{summary}

%prep
if [ -d %{buildroot} ]; then
  %{__rm} -rf %{buildroot}
fi

%build
export GOPATH=%{buildroot}%{gopath}

go get %{import_path}/%{project}
%{__rm} -f %{buildroot}%{gopath}/src/%{import_path}/.travis.yml
(
    echo '%defattr(-,root,root,-)'
    find %{buildroot}%{gopath}/src/%{import_path} -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/src/%{import_path} -type f -printf '%%%attr(664, root, root) "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    #find %{buildroot}%{gopath}/pkg/linux_amd64/%{provider}.%{provider_tld}/%{repo_owner} -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/pkg/linux_amd64/%{provider}.%{provider_tld}/%{repo_owner} -type f -printf '%%%attr(664, root, root) "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/bin/* -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/bin -type f -printf '%%%attr(750, root, root) "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
) > %{name}-%{version}-filelist
echo '%dir "%{gopath}/src/%{import_path}"' >> %{name}-%{version}-filelist
#echo '"%{gopath}/bin/go-bindata"' >> %{name}-%{version}-filelist
#%{__rm} -rf %{buildroot}%{gopath}/src/%{import_path}/testdata/symlinkFile/file1
#%{__rm} -rf %{buildroot}%{gopath}/src/%{import_path}/testdata/symlinkParent/symlinkTarget
#%{__rm} -rf %{buildroot}%{gopath}/src/%{import_path}/testdata/symlinkRecursiveParent/symlinkTarget
%{__sed} -i -e 's/%dir ""//g' %{name}-%{version}-filelist
%{__sed} -i -e '/^$/d' %{name}-%{version}-filelist


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
%__rm -f %{_builddir}/%{name}-%{version}-filelist

%files -f %{name}-%{version}-filelist
%{gopath}/src/%{import_path}/testdata/symlinkFile/file1
%{gopath}/src/%{import_path}/testdata/symlinkParent/symlinkTarget
%{gopath}/src/%{import_path}/testdata/symlinkRecursiveParent/symlinkTarget

%changelog
