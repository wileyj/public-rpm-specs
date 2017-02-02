%define repo https://github.com/rpm-software-management/hawkey
%define gitversion %(echo `curl -s  %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">bro'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1

%global with_python3 1

Name:           hawkey
Version:        %{gitversion}
Release:        1.%{?dist}
Summary:        Library providing simplified C and Python API to libsolv
License:        LGPLv2+
URL:            %{repo}
BuildRequires:  libsolv-devel >= %{libsolv_version}
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  expat-devel
BuildRequires:  rpm-devel
BuildRequires:  zlib-devel
BuildRequires:  check-devel

%description
%{summary}

%package -n %{name}-devel
Summary:        A Library providing simplified C and Python API to libsolv
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libsolv-devel

%description -n %{name}-devel
Development files for hawkey.


%package -n python-%{name}
Summary:        Python bindings for the hawkey library
Provides:	python-%{name} = %{version}
BuildRequires:  pygpgme
BuildRequires:  python-devel
BuildRequires:  python-flask
BuildRequires:  python-nose
BuildRequires:  python-sphinx
BuildRequires:  pyxattr
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python-%{name}
Python 2 bindings for the hawkey library.

%if 0%{with_python3}
%package -n python3-%{name}
Summary:        Python 3 bindings for the hawkey library
%{?system_python_abi}
Provides:	python3-%{name} = %{version}
BuildRequires:  python3-pygpgme
BuildRequires:  python3-devel
BuildRequires:  python3-flask
BuildRequires:  python3-nose
BuildRequires:  python3-sphinx
BuildRequires:  python3-pyxattr
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python3-%{name}
Python 3 bindings for the hawkey library.
%endif

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
mkdir build build-py3

%build
cd %{name}-%{version}
pushd build
  %cmake ..
  %make_build
  make doc-man
popd

%if 0%{with_python3}
pushd build-py3
  %cmake -DPYTHON_DESIRED:str=3 ..
  %make_build
  make doc-man
popd
%endif

%install
cd %{name}-%{version}
pushd build
  %make_install
popd
%if 0%{with_python3}
pushd build-py3
  %make_install
popd
%endif 

%check
if [ "$(id -u)" == "0" ] ; then
        cat <<ERROR 1>&2
Package tests cannot be run under superuser account.
Please build the package as non-root user.
ERROR
        exit 1
fi
pushd build
  ctest -VV
popd
%if 0%{with_python3}
# Run just the Python tests, not all of them, since
# we have coverage of the core from the first build
pushd build-py3/tests/python
  ctest -VV
popd
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%doc README.rst
%{_libdir}/lib%{name}.so.*

%files -n %{name}-devel
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/
%{_mandir}/man3/%{name}.3*

%files -n python-%{name}
%{python2_sitearch}/%{name}/

%if 0%{with_python3}
%files -n python3-%{name}
%{python3_sitearch}/%{name}/
%endif
