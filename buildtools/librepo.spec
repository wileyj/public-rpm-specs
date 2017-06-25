%define repo https://github.com/rpm-software-management/librepo
%define gitversion %(echo `curl -s  %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">bro'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1

%global with_python3 1
%global with_tests 1

Name:           librepo
Version:        %{gitversion}
Release:        1.%{?dist}
Summary:        A library providing C and Python (libcURL like) API for downloading packages and linux repository metadata in rpm-md format
License:        LGPLv2+
URL:            %{repo}

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  check-devel
BuildRequires:  doxygen
BuildRequires:  expat-devel
BuildRequires:  glib2-devel >= 2.26.0
BuildRequires:  gpgme-devel
BuildRequires:  libattr-devel
BuildRequires:  libcurl-devel >= 7.19.0
BuildRequires:  openssl-devel

%description
%{summary}

%package -n %{name}-devel
Summary:        Repodata downloading library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n %{name}-devel
Development files for librepo.

%package -n python-%{name}
Summary:        Python bindings for the librepo library
Provides:	python-%{name} = %{version}
BuildRequires:  pygpgme
BuildRequires:  python-devel
%if 0%{with_tests}
BuildRequires:  python-flask
BuildRequires:  python-nose
%endif
BuildRequires:  python-sphinx
BuildRequires:  pyxattr
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python-%{name}
Python 2 bindings for the librepo library.

%if 0%{with_python3}
%package -n python3-%{name}
Summary:        Python 3 bindings for the librepo library
Provides:	python3-%{name} = %{version}
BuildRequires:  python3-pygpgme
BuildRequires:  python3-devel
%if %{with tests}
BuildRequires:  python3-flask
BuildRequires:  python3-nose
%endif
BuildRequires:  python3-sphinx
BuildRequires:  python3-pyxattr
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python3-%{name}
Python 3 bindings for the librepo library.
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
popd

%if 0%{with_python3}
pushd build-py3
  %cmake -DPYTHON_DESIRED:str=3 ..
  %make_build
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
%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
#%license COPYING
#%doc README.md
%{_libdir}/%{name}.so.*

%files devel
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/

%files -n python-%{name}
%{python2_sitearch}/%{name}/

%if 0%{with_python3}
%files -n python3-%{name}
%{python3_sitearch}/%{name}/
%endif

%changelog

