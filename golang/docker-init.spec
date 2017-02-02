%define repo https://github.com/peterbourgon/runsvinit
%global provider        github
%global provider_tld    com
%global repo_owner      peterbourgon
%global project         runsvinit
%global import_path     %{provider}.%{provider_tld}/%{repo_owner}/%{project}
%define _summary        %(echo `curl -s %{repo} | grep "<title>" | cut -f2 -d ":" | sed 's|</title>||'`)
%define gitversion %(echo `date +%Y%m`)
%define release_ver 1

Name:                   docker-init
Version:                %{gitversion}
Release:                %{release_ver}.%{dist}
Summary:                Replacement init files for docker
License:                Go License
Vendor:                 %{vendor}
Packager:               %{packager}
BuildRequires:          git golang >= 1.8.0
BuildRequires:  golang-rpm-macros
Provides:               %{name}
Provides:               %{name}-devel
Provides:               golang(%{import_path}) 
Provides:               golang(%{import_path})-devel
Source1:		py_init.py


%description
%{summary}

%prep

%build
export GOPATH=%{buildroot}%{gopath}

go get %{import_path}

%__mkdir_p %{buildroot}/bin
%__install -m 0755 %{buildroot}%{gopath}/bin/%{project} %{buildroot}/bin/%{project}
%__install -m 0755 %{SOURCE1}  %{buildroot}/bin/py_init

%__rm -rf %{buildroot}%{gopath}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
/bin/%{project}
/bin/py_init

%changelog
