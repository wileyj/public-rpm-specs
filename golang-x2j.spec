%global _python_bytecompile_errors_terminate_build 0
%global provider        github
%global provider_tld    com
%global repo_owner      clbanning
%global project         x2j
%global import_path     %{provider}.%{provider_tld}/%{repo_owner}/%{project}
%define _summary        Unmarshal an anonymous XML doc to map[string]interface{} and JSON, and extract values (using wildcards, if necessary) for the Go programming language.

Name:           golang-%{project}
Version:        1.0.0
Release:        1.%{dist}
Summary:        %{_summary}
License:        MIT
Vendor:         %{vendor}
Packager:       %{packager}
BuildArch:      noarch
BuildRequires:  git golang >= 1.5.0
Requires:       golang >= 1.5.0
Provides:       golang-%{project}
Provides:       golang(%{import_path}) = %{version}-%{release}

%description
%{summary}

%description
%{summary}

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone https://github.com/%{repo_owner}/%{project}.git %{name}-%{version}

%build
cd %{name}-%{version}

%install
cd %{name}-%{version}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
cp -pav *.go %{buildroot}/%{gopath}/src/%{import_path}/

(
    cd %{buildroot}
    echo '%defattr(-,root,root,-)'
    if [ -f %{buildroot}%{gopath}/src/%{provider}.%{provider_tld}/%{repo_owner}/%{project}/.gitignore ]
    then
        echo '%exclude "%{gopath}/src/%{provider}.%{provider_tld}/%{repo_owner}/%{project}/.gitignore"'
    fi
    if [ -f %{buildroot}%{gopath}/%{gopath}/src/%{import_path}/.gitignore ]
    then
        echo '%exclude "%{gopath}/%{gopath}/src/%{import_path}/.gitignore"'

    fi
    if [ -f %{buildroot}%{gopath}/%{gopath}/src/%{import_path}/.travis.yml ]
    then
        echo '%exclude "%{gem_dir}/gems/%{gemname}-*/.travis.yml"'
    fi
    if [ -f %{buildroot}%{gopath}/src/%{provider}.%{provider_tld}/%{repo_owner}/%{project}/.travis.yml ]
    then
        echo '%exclude "%{gopath}/src/%{provider}.%{provider_tld}/%{repo_owner}/%{project}/.travis.yml"'
    fi
    find %{buildroot} -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot} -type f -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g' 
) > filelist
%{__sed} -i -e 's/%dir ""//g' filelist
%{__sed} -i -e '/^$/d' filelist


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files -f %{name}-%{version}/filelist

%changelog
