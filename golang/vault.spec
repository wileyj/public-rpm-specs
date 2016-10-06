%define repo https://github.com/hashicorp/vault
%global provider        github
%global provider_tld    com
%global repo_owner      hashicorp
%global project         vault
%global import_path     %{provider}.%{provider_tld}/%{repo_owner}/%{project}
%define _summary        %(echo `curl -s %{repo} | grep "<title>" | cut -f2 -d ":" | sed 's|</title>||'`)
%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d 'v\\-</span class="tag-name">'`)
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
Requires:       golang >= 1.5.0
Provides:       golang-%{provider}
Provides:       golang(%{import_path}) = %{version}-%{release}


%include %{_rpmconfigdir}/macros.d/macros.golang
%description
%{summary}

%package -n %{project}-api
Summary: %{project} api
Requires: golang

%description -n %{project}-api
%{project} api

%package -n %{project}-web
Summary: %{project} web
Requires: golang %{name} nginx

%description -n %{project}-web
%{project} web


%prep
if [ -d %{buildroot} ]; then
  %{__rm} -rf %{buildroot}
fi

%build
export GOPATH=%{buildroot}%{gopath}

go get %{import_path}
%{__rm} -f %{buildroot}%{gopath}/src/%{import_path}/.travis.yml
(
    echo '%defattr(-,root,root,-)'
    echo '%exclude %{gopath}/src/%{import_path}/api'
    echo '%exclude %{gopath}/src/%{import_path}/website'
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

(
    echo '%defattr(-,root,root,-)'
    echo '%exclude %{gopath}/src/%{import_path}/api' 
    find %{buildroot}%{gopath}/src/%{import_path}/api -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/src/%{import_path}/api -type f -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g'
) > %{filelist}.api
echo '%dir "%{gopath}/src/%{import_path}"' >> %{filelist}.api
%{__sed} -i -e 's/%dir ""//g' %{filelist}.api
%{__sed} -i -e '/^$/d' %{filelist}.api

(
    echo '%defattr(-,root,root,-)'
    find %{buildroot}%{gopath}/src/%{import_path}/website -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/src/%{import_path}/website -type f -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g'
) > %{filelist}.web
echo '%dir "%{gopath}/src/%{import_path}"' >> %{filelist}.web
%{__sed} -i -e 's/%dir ""//g' %{filelist}.web
%{__sed} -i -e '/^$/d' %{filelist}.web

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
%__rm -f %{_builddir}/%{filelist}
%__rm -f %{_builddir}/%{filelist}.api
%__rm -f %{_builddir}/%{filelist}.web

%files -f %{filelist}

%files -n %{project}-api

%files -n %{project}-web

%changelog
