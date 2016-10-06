%define repo_url https://github.com/jteeuwen/go-bindata

%global with_devel 1 
%global with_bundled 0
%global with_debug 0
%global with_check 0
%global with_unit_test 0

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global provider        github
%global provider_tld    com
%global project         jteeuwen
%global repo            go-bindata
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          406e5b7bfd8201a36e2bb5f7bdae0b03380c2ce8
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           golang-%{provider}-%{project}-%{repo}
Version:        0
Release:        0.14.git%{shortcommit}%{?dist}
Summary:        Functions to retrieve system, kernel and process metrics from the /proc fs
License:        ASL 2.0
URL:            https://%{provider_prefix}
%include %{_rpmconfigdir}/macros.d/macros.golang

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
BuildRequires:  golang

%description
%{summary}

%package devel
Summary:       %{summary}
BuildArch:     noarch
Provides:      golang(%{import_path}) = %{version}-%{release}
%description devel
%{summary}

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.

%package unit-test
Summary:         Unit tests for %{name} package
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  golang
Requires:        %{name}-devel = %{version}-%{release}

%description unit-test
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo_url} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update
 
%build
cd %{name}-%{version}
export GOPATH=%{buildroot}%{gopath}

%install
cd %{name}-%{version}
# source codes for building projects
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> %{_builddir}/%{name}-devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> %{_builddir}/%{name}-devel.file-list
done

# testing files for this project
%if 0%{?with_unit_test}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go"); do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> %{_builddir}/%{name}-devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> %{_builddir}/%{name}-unit-test.file-list
done
for file in $(find ./fixtures/ -iname "*" -not -type d); do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> %{_builddir}/%{name}-devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> %{_builddir}/%{name}-unit-test.file-list
done
%endif

sort -u -o %{_builddir}/%{name}-devel.file-list %{_builddir}/%{name}-devel.file-list

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
export GOPATH=%{buildroot}/%{gopath}:$(pwd)/Godeps/_workspace:%{gopath}
%endif

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}
%endif

%{!?_licensedir:%global license %doc}

%files devel -f %{_builddir}/%{name}-devel.file-list
#%license LICENSE
#%doc README.md CONTRIBUTING.md AUTHORS.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}

%if 0%{?with_unit_test}
%files unit-test -f %{_builddir}/%{name}-unit-test.file-list
%license LICENSE
%doc README.md CONTRIBUTING.md AUTHORS.md
%endif

%changelog
