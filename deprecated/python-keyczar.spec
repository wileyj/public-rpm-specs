%global with_python3 0
%global with_alinux 1

%define pypi_name python-keyczar
%define pypi_alternate keyczar

%global pypi_version_test %(echo `curl -s https://pypi.python.org/pypi/%{pypi_name} | grep "<title>" | awk '{print $2}'`)
%if "%{?pypi_version_test:%{pypi_version_test}}%{!?pypi_version_test:0}" == "of"
%global pypi_version %(echo `curl -s https://pypi.python.org/pypi/%{pypi_name} | sed -n -e '/<table class="list">/{n;n;n;n;n;n;n;n;p;};h' | cut -d'"' -f2 | cut -d'/' -f4`)
%global pypi_url https://pypi.python.org/pypi/%{pypi_name}/%{pypi_version}
%define multi true
%else
%global pypi_version %{pypi_version_test}
%global pypi_url https://pypi.python.org/pypi/%{pypi_name}
%define multi false
%endif
%global pypi_summary %(echo `curl -s %{pypi_url} | grep '<meta name="description" content=' | cut -d'"' -f4`)

Name:           %{pypi_name}
Version:        %{pypi_version}
Release:        1.%{?dist}
Summary:        "%{pypi_summary}"
Group:          Development/Languages
License:        MIT
URL:            %{pypi_url}
Provides:       python-%{pypi_name} = %{version}-%{release}
Provides:       python-%{pypi_alternate} = %{version}-%{release}
Obsoletes:      python-%{pypi_name} < %{version}-%{release}
BuildRequires:  python-devel python2-rpm-macros python-srpm-macros
Requires: python
BuildArch:      noarch
Requires: python-pycrypto
Requires: python-pyasn1

%description
%{summary} for Python

%if 0%{?with_alinux}
%package -n python27-%{pypi_name}
Summary:        "%{pypi_summary}"
Group:          Development/Languages
Provides:       python27-%{pypi_name} = %{version}-%{release}
Obsoletes:      python27-%{pypi_name} < %{version}-%{release}
BuildRequires:  python-devel python-rpm-macros python-srpm-macros
Requires: python27-pycrypto
Requires: python27-pyasn1
Requires: python27
BuildArch:      noarch

%description -n python27-%{pypi_name}
%{summary} for Amazon Linux Python
%endif

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        "%{pypi_summary}"
Group:          Development/Languages
Provides:       python3-%{pypi_name} = %{version}-%{release}
Provides:       python3-%{pypi_alternate} = %{version}-%{release}
Obsoletes:      python3-%{pypi_name} < %{version}-%{release}
BuildRequires:  python3-devel python3-rpm-macros python-srpm-macros
Requires: python3
Requires: python3-pycrypto
Requires: python3-pyasn1
BuildArch:      noarch

%description -n python3-%{pypi_name}
%{summary} for Python 3
%endif


%prep
if [ -d %{_builddir}/%{name}-%{version} ];then
    rm -rf %{_builddir}/%{name}-%{version}
fi
curl -o $RPM_SOURCE_DIR/%{name}.tar.gz `curl -s %{pypi_url} | grep tar.gz | cut -d '"' -f2 | cut -f1 -d "#" | tail -2 | grep 1`
tar -xzvf $RPM_SOURCE_DIR/%{name}.tar.gz
#mv %{_builddir}/%{pypi_name}-%{version} %{_builddir}/%{name}-%{version}
chmod -R u+w %{_builddir}/%{name}-%{version}
cd $RPM_BUILD_DIR/%{name}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

rm -rf %{py2dir}
cp -a . %{py2dir}


%build
cd $RPM_BUILD_DIR/%{name}-%{version}
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

pushd %{py2dir}
%{__python27} setup.py build
popd


%install
cd $RPM_BUILD_DIR/%{name}-%{version}
pushd %{py2dir}
%{__python27} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
find %{buildroot}%{_prefix} -type d -depth -exec rmdir {} \; 2>/dev/null
popd

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
find %{buildroot}%{_prefix} -type d -depth -exec rmdir {} \; 2>/dev/null
popd
%endif

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
[ "%{_builddir}/python-%{pypi_name}-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python-python-%{pypi_name}-%{version}-%{release}
[ "%{_builddir}/python2-%{pypi_name}-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python2-python-%{pypi_name}-%{version}-%{release}
[ "%{_builddir}/python3-%{pypi_name}-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python3-python-%{pypi_name}-%{version}-%{release}


%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%{python3_sitelib}/*
%endif

%files
%{python2_sitelib}/*
%{_bindir}/keyczart

%if 0%{?with_alinux}
%files -n python27-%{pypi_name}
%{python2_sitelib}/*
%{_bindir}/keyczart
%endif
