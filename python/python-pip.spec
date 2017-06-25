%global with_python3 1
%define get_pip https://bootstrap.pypa.io/get-pip.py
%define pypi_name pip
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

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        1.%{?dist}
Summary:        "%{pypi_summary}"
Group:          Development/Languages
License:        MIT
URL:            %{pypi_url}
Provides:       python-%{pypi_name} = %{version}-%{release}
Obsoletes:      python-%{pypi_name} < %{version}-%{release}
BuildRequires:  python-devel python2-rpm-macros python-srpm-macros 
BuildArch:      noarch
Requires: python python-wheel python-setuptools

%description
%{summary} for Python

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        "%{pypi_summary}"
Group:          Development/Languages
Provides:       python3-%{pypi_name} = %{version}-%{release}
Obsoletes:      python3-%{pypi_name} < %{version}-%{release}
BuildRequires:  python3-devel python3-rpm-macros python-srpm-macros
Requires: python3 python3-wheel python3-setuptools
BuildArch:      noarch

%description -n python3-%{pypi_name}
%{summary} for Python 3
%endif


%prep
if [ -d %{_builddir}/%{name}-%{version} ];then
    rm -rf %{_builddir}/%{name}-%{version}
fi

curl -s %{get_pip} -o %{_builddir}/get_pip.py
chmod -R u+w %{_builddir}/get_pip.py
%if 0%{?with_python3}
rm -rf %{py3dir}
%endif

rm -rf %{py2dir}

%build
%install
%if 0%{?with_python3}
%{__python3} %{_builddir}/get_pip.py pip -I --force-reinstall --root %{buildroot} --only-binary --no-cache-dir --compile --no-deps --no-wheel
%endif

%{__python2} %{_builddir}/get_pip.py pip -I --force-reinstall --root %{buildroot} --only-binary --no-cache-dir --compile --no-deps --no-wheel

find %{buildroot}%{_prefix} -type d -depth -exec rmdir {} \; 2>/dev/null

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
%{_bindir}/*%{python3_version}
%{_bindir}/%{pypi_name}3
%endif

%files -n python-%{pypi_name}
%{python2_sitelib}/*
%{_bindir}/*%{python_version}
%{_bindir}/%{pypi_name}2
%{_bindir}/%{pypi_name}



