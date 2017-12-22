%global with_python3 0
%global with_git 0
%global include_tests 0
%define use_systemd 1
%define pypi_name ansible
%define repo https://github.com/ansible/ansible

%global pypi_version_test %(echo `curl -s https://pypi.python.org/pypi/%{pypi_name} | grep "<title>" | awk '{print $2}'`)
%if "%{?pypi_version_test:%{pypi_version_test}}%{!?pypi_version_test:0}" == "of"
%global pypi_version %(echo `curl -s https://pypi.python.org/pypi/%{pypi_name} | sed -n -e '/<table class="list">/{n;n;n;n;n;n;n;n;p;};h' | cut -d'"' -f2 | cut -d'/' -f4`)
%global pypi_url https://pypi.python.org/pypi/%{pypi_name}/%{pypi_version}
%global url https://pypi.python.org/pypi/%{pypi_name}/%{pypi_version}
%else
%global pypi_version %{pypi_version_test}
%global pypi_url https://pypi.python.org/pypi/%{pypi_name}
%global repo https://pypi.python.org/pypi/%{pypi_name}
%endif

%global pypi_summary %(echo `curl -s %{pypi_url} | grep '<meta name="description" content=' | cut -d'"' -f4`)

%if 0%{?with_git}
%define pypi_version %(echo `curl -s %{repo}/releases | grep 'class="css-truncate-target"' | head -1 |  tr -d '\\-</span class="css-truncate-target">'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1
%define build_time %(echo `date +%s`)
%define pypi_release git.%{build_time}.%{revision}.%{?dist}
%else
%global revision 1
%define pypi_release %{revision}.%{?dist}
%endif

Name:       %{pypi_name}
Version:    %{pypi_version}
Release:    %{pypi_release}
Summary:    %{pypi_summary}
Group:      System Environment/Daemons
License:    GPLv3
Vendor: %{vendor}
Packager: %{packager}

BuildArch: noarch
BuildRequires: git
BuildRequires: asciidoc
Requires: sshpass
%if 0%{?with_python3}
Requires: python3-PyYAML
Requires: python3-pycrypto
Requires: python3-paramiko
Requires: python3-keyczar
Requires: python3-Jinja2
Requires: python3-httplib2
%else
Requires: python-PyYAML
Requires: python-pycrypto
Requires: python-paramiko
Requires: python-keyczar
Requires: python-Jinja2
Requires: python-httplib2
%endif

%description
%{summary}


%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
if [ -d %{buildroot} ]; then
    rm -rf %{buildroot}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
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
%{__python27} setup.py build
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
%{__python27} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
find %{buildroot}%{_prefix} -type d -depth -exec rmdir {} \; 2>/dev/null
popd
%endif

mkdir -p %{buildroot}%{_sysconfdir}/ansible/
cp examples/hosts %{buildroot}%{_sysconfdir}/ansible/
cp examples/ansible.cfg %{buildroot}%{_sysconfdir}/ansible/
mkdir -p %{buildroot}/%{_mandir}
cp -R docs/man/* %{buildroot}/%{_mandir}/
mkdir -p %{buildroot}/%{_datadir}/ansible

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root)
%if 0%{?with_python3}
%{python3_sitelib}/*
%else
%{python_sitelib}/*
%endif

%{_bindir}/ansible*
%dir %{_datadir}/ansible
%config(noreplace) %{_sysconfdir}/ansible
%doc %{_mandir}/*

%changelog

