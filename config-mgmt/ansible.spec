%define repo https://github.com/ansible/ansible.git
%define gitversion %(echo `curl -s https://github.com/ansible/ansible/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">'`)
%define name ansible
%define macro %{_rpmconfigdir}/macros.d/macros.python
BuildRequires: git python-srpm-macros
%include %{macro}

Name:      %{name}
Version:   %{gitversion}
Release:   1.%{dist}
Url:       http://www.ansible.com
Summary:   SSH-based application deployment, configuration management, and IT orchestration platform
License:   GPLv3
Vendor: %{vendor}
Packager: %{packager}
Group:     Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildArch: noarch
BuildRequires: python27-devel
BuildRequires: python27-setuptools
Requires: python27-devel
Requires: python27-setuptools
BuildRequires: git 
Requires: PyYAML
Requires: gcc
Requires: gcc-c++
Requires: sshpass
#Requires: python27-pycrypto python27-paramiko python27-keyczar python27-jinja2 python27-httplib2
Requires: python27-crypto python27-paramiko python27-keyczar python27-jinja2 python27-httplib2


%description

Ansible is a radically simple model-driven configuration management,
multi-node deployment, and orchestration engine. Ansible works
over SSH and does not require any software or daemons to be installed
on remote nodes. Extension modules can be written in any language and
are transferred to managed machines automatically.


%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update

%build
cd %{name}-%{version}
%{__python} setup.py build
make docs

%install
cd %{name}-%{version}
%{__python} setup.py install -O1 --prefix=%{_prefix} --root=%{buildroot}
mkdir -p %{buildroot}/etc/ansible/
cp examples/hosts %{buildroot}/etc/ansible/
cp examples/ansible.cfg %{buildroot}/etc/ansible/
mkdir -p %{buildroot}/%{_mandir}/man1/
cp -v docs/man/man1/*.1 %{buildroot}/%{_mandir}/man1/
mkdir -p %{buildroot}/%{_datadir}/ansible


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}


%files
%defattr(-,root,root)
%{python_sitelib}/ansible*

%{_bindir}/ansible*
%dir %{_datadir}/ansible
%config(noreplace) %{_sysconfdir}/ansible
%doc %{_mandir}/man1/ansible*

%changelog
