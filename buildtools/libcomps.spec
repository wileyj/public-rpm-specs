%define repo https://github.com/rpm-software-management/libcomps
%define gitversion %(echo `curl -s  %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">bro'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1

%global with_python3 1
%global with_tests 0

Name:           libcomps
Version:        %{gitversion}
Release:        1.%{?dist}
Summary:        A library providing C and Python (libcURL like) API for downloading packages and linux repository metadata in rpm-md format
License:        LGPLv2+
URL:            %{repo}

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  libxml2-devel
BuildRequires:  check-devel
BuildRequires:  expat-devel

%description
%{summary}

%package -n %{name}-devel
Summary:        Repodata downloading library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n %{name}-devel
Development files for libcomps.

%package -n python-%{name}
Summary:        Python bindings for the libcomps library
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
Python 2 bindings for the libcomps library.

%if 0%{with_python3}
%package -n python3-%{name}
Summary:        Python 3 bindings for the libcomps library
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
Python 3 bindings for the libcomps library.
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
pushd libcomps
%if 0%{with_python3}
  %cmake -DPYTHON_DESIRED:str=3 .
  %make_build
%else
  %cmake .
  %make_build
%endif
popd

%install
cd %{name}-%{version}
pushd libcomps
  %make_install
popd
%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/%{name}.so.*

%files devel
%{_libdir}/%{name}.so
#%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/

%if 0%{with_python3}
%files -n python3-%{name}
%{python3_sitearch}/%{name}/
%else
%files -n python-%{name}
%{python2_sitearch}/%{name}/
%endif

%changelog

