%include %{_rpmconfigdir}/macros.d/macros.python27
%define srcname thefuck

Name:           python27-%{srcname}
Version:        3.2
Release:        1.%{dist}
Summary:        Magnificent app which corrects your previous console command
Group:          Development/Languages
License:        MIT
Packager: %{packager}
Vendor: %{vendor}
URL:            https://github.com/nvbn/thefuck
Source0:        %{srcname}.tar.gz
BuildRoot:      %{_tmppath}/%{srcname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python27, python27-devel, python27-setuptools, git
Requires:       python27, python27-pip

%description
Magnificent app which corrects your previous console command

%prep
%setup -q -n %{srcname}

%build
git pull

%{__python27} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python27} setup.py install --skip-build --root $RPM_BUILD_ROOT

%{__mv} %{buildroot}%{python27_sitelib}/tests %{buildroot}%{python27_sitelib}/%{srcname}
pwd=`pwd`
cd %{buildroot}%{_bindir}
%__ln_s -f %{srcname} fuck
rm %{srcname}-alias
cd $pwd

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{srcname}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{srcname}-%{version}
[ "%{_builddir}/%{srcname}" != "/" ] && %__rm -rf %{_builddir}/%{srcname}

%files
%defattr(-,root,root,-)
%{_bindir}/thefuck
%{_bindir}/fuck
%{python27_sitelib}/%{srcname}/
%{python27_sitelib}/%{srcname}*.egg-info

%changelog

