%define repo https://github.com/pierrec/xxHash
%global provider        github
%global provider_tld    com
%global repo_owner      pierrec
%global project         xxHash
%define secondary	xxhsum
%global import_path     %{provider}.%{provider_tld}/%{repo_owner}/%{project}
%define _summary        %(echo `curl -s %{repo} | grep "<title>" | cut -f2 -d ":" | sed 's|</title>||'`)
#%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">'`)
%define gitversion 1.0.0
%global _python_bytecompile_errors_terminate_build 0

Name:           golang-%{project}
Version:        %{gitversion}
Release:        1.%{dist}
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

%build
export GOPATH=%{buildroot}%{gopath}

go get %{import_path}/%{secondary}
%{__rm} -rf %{buildroot}%{gopath}/src/%{import_path}/.git
%{__rm} -f %{buildroot}%{gopath}/src/%{import_path}/.travis.yml
(
    echo '%defattr(-,root,root,-)'
    find %{buildroot}%{gopath}/src/%{import_path}%{secondary} -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/src/%{import_path}%{secondary} -type f -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/pkg/linux_amd64/%{provider}.%{provider_tld} -type f -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g'
) > %{name}-%{version}-filelist
echo '%dir "%{gopath}/src/%{import_path}/%{secondary}"' >> %{name}-%{version}-filelist
%{__sed} -i -e 's/%dir ""//g' %{name}-%{version}-filelist
%{__sed} -i -e '/^$/d' %{name}-%{version}-filelist

echo '%{gopath}/bin/xxhsum' >> %{name}-%{version}-filelist
echo '%{gopath}/src/%{import_path}/LICENSE' >> %{name}-%{version}-filelist
echo '%{gopath}/src/%{import_path}/README.md' >> %{name}-%{version}-filelist
echo '%{gopath}/src/%{import_path}/xxHash32/example_test.go' >> %{name}-%{version}-filelist
echo '%{gopath}/src/%{import_path}/xxHash32/xxHash32.go' >> %{name}-%{version}-filelist
echo '%{gopath}/src/%{import_path}/xxHash32/xxHash32_test.go' >> %{name}-%{version}-filelist
echo '%{gopath}/src/%{import_path}/xxHash64/example_test.go' >> %{name}-%{version}-filelist
echo '%{gopath}/src/%{import_path}/xxHash64/xxHash64.go' >> %{name}-%{version}-filelist
echo '%{gopath}/src/%{import_path}/xxHash64/xxHash64_test.go' >> %{name}-%{version}-filelist
echo '%{gopath}/src/%{import_path}/xxhsum/main.go' >> %{name}-%{version}-filelist



%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files -f %{name}-%{version}-filelist

%changelog
