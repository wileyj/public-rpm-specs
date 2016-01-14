%define name ansible
%define ansible_version $VERSION
%if 0%{?el6}
    %define macro %{_rpmconfigdir}/macros.d/macros.python27
    %global __python /usr/bin/python27
%else
    %define macro %{_rpmconfigdir}/macros.d/macros.python
    %global __python /usr/bin/python
%endif

%include %{macro}

Name:      %{name}
Version:   2.0.0.5
Release:   1.%{dist}
Url:       http://www.ansible.com
Summary:   SSH-based application deployment, configuration management, and IT orchestration platform
License:   GPLv3
Vendor: %{vendor}
Packager: %{packager}
Group:     Development/Libraries
Source:    %{name}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildArch: noarch
%if 0%{?el6}  == 6
BuildRequires: python27-devel
BuildRequires: python27-setuptools
Requires: python27-devel
Requires: python27-setuptools
%else
BuildRequires: python-devel
BuildRequires: python-setuptools
Requires: python-devel
Requires: python-setuptools
%endif

BuildRequires: git
Requires: PyYAML
Requires: gcc
Requires: gcc-c++
Requires: sshpass


%description

Ansible is a radically simple model-driven configuration management,
multi-node deployment, and orchestration engine. Ansible works
over SSH and does not require any software or daemons to be installed
on remote nodes. Extension modules can be written in any language and
are transferred to managed machines automatically.

%prep
%setup -q -n %{name}

%build
git pull

%{__python27} setup.py build
make docs
%install

%{__python27} setup.py install -O1 --prefix=%{_prefix} --root=%{buildroot}
mkdir -p %{buildroot}/etc/ansible/
cp examples/hosts %{buildroot}/etc/ansible/
cp examples/ansible.cfg %{buildroot}/etc/ansible/
mkdir -p %{buildroot}/%{_mandir}/man1/
cp -v docs/man/man1/*.1 %{buildroot}/%{_mandir}/man1/
mkdir -p %{buildroot}/%{_datadir}/ansible

%pre
/usr/bin/pip2.7 install pycrypto paramiko python-keyczar Jinja2 httplib2

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root)
%if 0%{?el6}  == 6
%{python27_sitelib}/ansible*
%else
%{python_sitelib}/ansible*
%endif

%{_bindir}/ansible*
%dir %{_datadir}/ansible
%config(noreplace) %{_sysconfdir}/ansible
%doc README.md COPYING
%doc %{_mandir}/man1/ansible*

%changelog
