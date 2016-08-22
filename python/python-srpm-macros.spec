Name:           python-srpm-macros
Version:        1
Release:        1.%{?dist}
Summary:        RPM macros for building packages for various architectures utilizing python
Group:          Development/Libraries
License:        GPLv3+
Source0:        macros.python
Source1:        macros.python_build
BuildArch:      noarch
BuildRequires:  coreutils
Provides: %{name}

%include /usr/lib/rpm/macros.d/macros.python
%description
The package provides macros for building projects on various architectures utilizing python.

%prep
# nothing to prep, just for hooks

%build
# nothing to build, just for hooks

%install
mkdir -p %{buildroot}/%{_sysconfdir}/rpm
mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -m 644 %{SOURCE0} %{buildroot}/%{_sysconfdir}/rpm/macros.python
install -m 644 %{SOURCE1} %{buildroot}%{_rpmconfigdir}/macros.d/macros.python


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%config(noreplace) %{_rpmconfigdir}/macros.d/macros.python
%config(noreplace) %{_sysconfdir}/rpm/macros.python
%changelog
