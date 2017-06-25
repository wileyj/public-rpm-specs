%global _python_bytecompile_errors_terminate_build 0
%global with_python3 0
%define pypi_name gyp
%define repo https://chromium.googlesource.com/experimental/external/gyp

%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1
%define build_time %(echo `date +%s`)
%define pypi_release %{revision}.%{?dist}
%define pypi_summary "GYP is intended to support large projects that need to be built on multiple platforms"

Name:           %{pypi_name}
Version:        %{build_time}
Release:        %{pypi_release}
Summary:        "%{pypi_summary}"
Group:          Development/Languages
License:        MIT
URL:            %{pypi_url}
Provides:       python-%{pypi_name} = %{version}-%{release}
%if 0%{?with_python3}
BuildRequires:  python3-devel python3-rpm-macros python-srpm-macros
Requires:       python3-six
%else
BuildRequires:  python-devel python-rpm-macros python-srpm-macros
Requires:       python-six
%endif

%description
%{summary} for Python


%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
if [ -d %{buildroot} ]; then
    rm -rf %{buildroot}
fi
git clone %{repo} %{name}-%{version}
cd $RPM_BUILD_DIR/%{name}-%{version}
git submodule init
git submodule update

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%else
rm -rf %{py2dir}
cp -a . %{py2dir}
%endif

%build
cd $RPM_BUILD_DIR/%{name}-%{version}
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%else
pushd %{py2dir}
%{__python2} setup.py build
popd
%endif

%install
cd $RPM_BUILD_DIR/%{name}-%{version}
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
find %{buildroot}%{_prefix} -type d -depth -exec rmdir {} \; 2>/dev/null
popd
%else
pushd %{py2dir}
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
find %{buildroot}%{_prefix} -type d -depth -exec rmdir {} \; 2>/dev/null
popd
%endif

%__mkdir_p %{buildroot}/%{_bindir}
%__install -m0755 gyp %{buildroot}%{_bindir}/%{pypi_name}
%if 0%{?with_python3}
%__install -m0755 gyp %{buildroot}%{_bindir}/%{pypi_name}3
%endif

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
[ "%{_builddir}/python-%{pypi_name}-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python-python-%{pypi_name}-%{version}-%{release}
[ "%{_builddir}/python2-%{pypi_name}-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python2-python-%{pypi_name}-%{version}-%{release}
[ "%{_builddir}/python3-%{pypi_name}-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python3-python-%{pypi_name}-%{version}-%{release}


%files
%{_bindir}/%{pypi_name}*
%if 0%{?with_python3}
%{python3_sitelib}/*
%{_bindir}/%{pypi_name}3
%else
%{python2_sitelib}/*
%endif
