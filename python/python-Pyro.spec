%global with_python3 0
%global _python_bytecompile_errors_terminate_build 0

%define pypi_name Pyro
%define pypi_alternate pyro
%define pypi_alternate1 pyro-es
%define pypi_alternate2 pyro-esd
%define pypi_alternate3 pyro-genguid
%define pypi_alternate4 pyro-ns
%define pypi_alternate5 pyro-nsc
%define pypi_alternate6 pyro-nsd
%define pypi_alternate7 pyro-wxnsc
%define pypi_alternate8 pyro-xnsc

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

Name:           python-%{pypi_alternate}
Version:        %{pypi_version}
Release:        1.%{?dist}
Summary:        "%{pypi_summary}"
Group:          Development/Languages
License:        MIT
URL:            %{pypi_url}
Provides:       python-%{pypi_name} = %{version}-%{release}
Provides:       python-%{pypi_alternate} = %{version}-%{release}
BuildArch:      noarch
Obsoletes:      python-%{pypi_name} < %{version}-%{release}
BuildRequires:  python-devel python2-rpm-macros python-srpm-macros 
Requires: python-six
Requires: python

%description
%{summary} for Python

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        "%{pypi_summary}"
Group:          Development/Languages
Provides:       python3-%{pypi_name} = %{version}-%{release}
Provides:       python3-%{pypi_alternate} = %{version}-%{release}
Obsoletes:      python3-%{pypi_name} < %{version}-%{release}
BuildRequires:  python3-devel python3-rpm-macros python-srpm-macros
Requires: python3
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
mv %{_builddir}/%{pypi_name}-%{version} %{_builddir}/%{name}-%{version}
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
%{__python2} setup.py build
popd


%install
cd $RPM_BUILD_DIR/%{name}-%{version}
pushd %{py2dir}
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
for file in %{pypi_alternate1} %{pypi_alternate2} %{pypi_alternate3} %{pypi_alternate4} %{pypi_alternate5} %{pypi_alternate6} %{pypi_alternate7} %{pypi_alternate8}; do
%__cp %{buildroot}%{_bindir}/${file} %{buildroot}%{_bindir}/${file}-%{python_version}
done
find %{buildroot}%{_prefix} -type d -depth -exec rmdir {} \; 2>/dev/null
popd

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
for file in %{pypi_alternate1} %{pypi_alternate2} %{pypi_alternate3} %{pypi_alternate4} %{pypi_alternate5} %{pypi_alternate6} %{pypi_alternate7} %{pypi_alternate8}; do
%__cp %{buildroot}%{_bindir}/${file} %{buildroot}%{_bindir}/${file}-%{python3_version}
done
find %{buildroot}%{_prefix} -type d -depth -exec rmdir {} \; 2>/dev/null
popd
%endif

for file in %{pypi_alternate1} %{pypi_alternate2} %{pypi_alternate3} %{pypi_alternate4} %{pypi_alternate5} %{pypi_alternate6} %{pypi_alternate7} %{pypi_alternate8}; do
%__rm -f %{buildroot}%{_bindir}/${file}
done


%post
for file in %{pypi_alternate1} %{pypi_alternate2} %{pypi_alternate3} %{pypi_alternate4} %{pypi_alternate5} %{pypi_alternate6} %{pypi_alternate7} %{pypi_alternate8}; do
if [ -f %{_bindir}/$file ];then
%__rm -f  %{_bindir}/$file
fi
%__ln_s %{_bindir}/${file}-%{python_version}  %{_bindir}/$file
done


%postun
for file in %{pypi_alternate1} %{pypi_alternate2} %{pypi_alternate3} %{pypi_alternate4} %{pypi_alternate5} %{pypi_alternate6} %{pypi_alternate7} %{pypi_alternate8}; do
if [ -f %{_bindir}/$file ];then
%__rm -f  %{_bindir}/$file
fi
%if 0%{?with_python3}
if [ -f %{_bindir}/${file}-%{python3_version} ]; then
%__ln_s %{_bindir}/${file}-%{python3_version}  %{_bindir}/$file
fi
%endif
done

%if 0%{?with_python3}
%post -n python3-%{pypi_name}
for file in %{pypi_alternate1} %{pypi_alternate2} %{pypi_alternate3} %{pypi_alternate4} %{pypi_alternate5} %{pypi_alternate6} %{pypi_alternate7} %{pypi_alternate8}; do
  if [ ! -f %{_bindir}/${file}-%{python_version} ];then
    if [ -f %{_bindir}/$file ];then
      %__rm -f  %{_bindir}/$file
    fi
    %__ln_s %{_bindir}/${file}-%{python3_version}  %{_bindir}/$file
  fi
done

%postun -n python3-%{pypi_name}
for file in %{pypi_alternate1} %{pypi_alternate2} %{pypi_alternate3} %{pypi_alternate4} %{pypi_alternate5} %{pypi_alternate6} %{pypi_alternate7} %{pypi_alternate8}; do
  if [ ! -f %{_bindir}/${file}-%{python_version} ];then
    if [ -f %{_bindir}/$file ];then
      %__rm -f  %{_bindir}/$file
    fi
    if [ -f %{_bindir}/${file}-%{python_version} ]; then
      %__ln_s %{_bindir}/${file}-%{python_version}  %{_bindir}/$file
    fi
  fi
done
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
%{_bindir}/*%{python3_version}
%endif

%files 
%{python2_sitelib}/*
%{_bindir}/*%{python_version}

